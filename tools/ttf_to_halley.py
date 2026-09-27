#!/usr/bin/env python3
"""Convert a TTF/OTF font into legacy Halley font JSON assets."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any

try:
    from tools.halley_font import (
        GlyphRecord,
        HalleyFontError,
        encode_hlif_rgba,
        encode_hlif_single_channel,
        generate_sdf,
        load_payload_json,
        parse_font_payload,
        serialize_font_payload,
    )
except ModuleNotFoundError:
    from halley_font import (
        GlyphRecord,
        HalleyFontError,
        encode_hlif_rgba,
        encode_hlif_single_channel,
        generate_sdf,
        load_payload_json,
        parse_font_payload,
        serialize_font_payload,
    )


@dataclass(frozen=True)
class PlacedGlyph:
    codepoint: int
    x: int
    y: int
    width: int
    height: int
    bearing_x: float
    bearing_y: float
    advance: float
    advance_y: float
    pixels: bytes


def _load_pillow() -> tuple[Any, Any]:
    try:
        from PIL import Image, ImageFont
    except ImportError as error:
        raise HalleyFontError(
            "Pillow is required for TTF conversion; install it with "
            "'python3 -m pip install Pillow'"
        ) from error
    return ImageFont, Image


def load_characters(path: Path) -> list[int]:
    text = path.read_text(encoding="utf-8")
    result = sorted({ord(char) for char in text if char not in "\r\n"})
    if not result:
        raise HalleyFontError("character set is empty")
    return result


def load_supported_codepoints(path: Path) -> set[int]:
    try:
        from fontTools.ttLib import TTFont
    except ImportError as error:
        raise HalleyFontError(
            "fontTools is required to filter unsupported glyphs; install it with "
            "'python3 -m pip install Pillow fonttools'"
        ) from error
    try:
        font = TTFont(path)
        return set().union(*(set(table.cmap) for table in font["cmap"].tables))
    except (OSError, KeyError, ValueError) as error:
        raise HalleyFontError(f"cannot read font cmap from {path}") from error


def _apply_antialiasing(raw: bytes, enabled: bool, gamma: float = 1.0) -> bytes:
    if enabled:
        if gamma == 1.0:
            return raw
        return bytes(
            round(((value / 255.0) ** gamma) * 255.0)
            for value in raw
        )
    return bytes(255 if value >= 128 else 0 for value in raw)


def _render_glyph(
    font: Any,
    codepoint: int,
    padding: int,
    antialias: bool,
    bitmap_gamma: float,
    render_scale: int,
    image_module: Any,
) -> tuple[int, int, float, float, float, float, bytes]:
    char = chr(codepoint)
    # Halley metrics use the baseline as the origin. Pillow's default
    # anchor uses a top/ascender origin, which puts glyphs off-screen.
    bbox = font.getbbox(char, anchor="ls")
    if bbox is None:
        raise HalleyFontError(f"font has no glyph for U+{codepoint:04X}")
    left, top, right, bottom = bbox
    advance = float(font.getlength(char))
    width = max(1, right - left, round(advance) if right == left else 0)
    height = max(1, bottom - top)
    canvas_width = width + padding * 2
    canvas_height = height + padding * 2
    image = font.getmask(char, mode="L", anchor="ls")
    raw = bytes(image)
    if not raw:
        raw = bytes(max(0, right - left) * max(0, bottom - top))
    if len(raw) not in {width * height, max(0, right - left) * max(0, bottom - top)}:
        raise HalleyFontError(f"unexpected bitmap size for U+{codepoint:04X}")
    pixels = bytearray(canvas_width * canvas_height)
    bitmap_width = max(0, right - left)
    bitmap_height = max(0, bottom - top)
    for y in range(bitmap_height):
        start = y * bitmap_width
        dst = (y + padding) * canvas_width + padding
        pixels[dst:dst + bitmap_width] = raw[start:start + bitmap_width]
    if render_scale > 1:
        target_width = max(1, round(canvas_width / render_scale))
        target_height = max(1, round(canvas_height / render_scale))
        resized = image_module.frombytes(
            "L", (canvas_width, canvas_height), bytes(pixels)
        ).resize(
            (target_width, target_height),
            image_module.Resampling.LANCZOS,
        )
        pixels = bytearray(resized.tobytes())
        canvas_width = target_width
        canvas_height = target_height

    pixels = bytearray(_apply_antialiasing(bytes(pixels), antialias, bitmap_gamma))
    return (
        canvas_width,
        canvas_height,
        float((left - padding) / render_scale),
        float((-top + padding) / render_scale),
        advance / render_scale,
        float(getattr(font, "size", 16)) / render_scale,
        bytes(pixels),
    )


def _pack_glyphs(
    font: Any,
    characters: list[int],
    atlas_width: int,
    padding: int,
    antialias: bool,
    bitmap_gamma: float,
    render_scale: int,
    image_module: Any,
) -> tuple[list[PlacedGlyph], bytes, int]:
    pending = []
    for codepoint in characters:
        width, height, bearing_x, bearing_y, advance, advance_y, pixels = _render_glyph(
            font,
            codepoint,
            padding * render_scale,
            antialias,
            bitmap_gamma,
            render_scale,
            image_module,
        )
        pending.append(
            (codepoint, width, height, bearing_x, bearing_y, advance, advance_y, pixels)
        )

    x = 0
    y = 0
    row_height = 0
    placements: list[PlacedGlyph] = []
    for (
        codepoint,
        width,
        height,
        bearing_x,
        bearing_y,
        advance,
        advance_y,
        pixels,
    ) in pending:
        if width > atlas_width:
            raise HalleyFontError(f"glyph U+{codepoint:04X} exceeds atlas width")
        if x and x + width > atlas_width:
            x = 0
            y += row_height
            row_height = 0
        placements.append(
            PlacedGlyph(
                codepoint,
                x,
                y,
                width,
                height,
                bearing_x,
                bearing_y,
                advance,
                advance_y,
                pixels,
            )
        )
        x += width
        row_height = max(row_height, height)

    atlas_height = max(1, y + row_height)
    pixels = bytearray(atlas_width * atlas_height)
    for glyph in placements:
        for row in range(glyph.height):
            src = row * glyph.width
            dst = (glyph.y + row) * atlas_width + glyph.x
            pixels[dst:dst + glyph.width] = glyph.pixels[src:src + glyph.width]
    return placements, bytes(pixels), atlas_height


def convert_font(args: argparse.Namespace) -> dict[str, Any]:
    if args.bitmap_gamma <= 0:
        raise HalleyFontError("bitmap gamma must be greater than zero")
    if args.render_scale < 1:
        raise HalleyFontError("render scale must be at least 1")
    image_font, image_module = _load_pillow()
    reference = parse_font_payload(load_payload_json(args.reference_font))
    reference_texture = load_payload_json(args.reference_texture)
    requested_characters = load_characters(args.characters)
    supported_codepoints = load_supported_codepoints(args.font)
    characters = [
        codepoint
        for codepoint in requested_characters
        if codepoint in supported_codepoints
    ]
    unsupported_codepoints = sorted(set(requested_characters) - set(characters))
    if not characters:
        raise HalleyFontError("font has no glyphs from the requested character set")
    render_size = args.pixel_size * args.render_scale
    font = image_font.truetype(str(args.font), render_size)
    placements, pixels, atlas_height = _pack_glyphs(
        font,
        characters,
        args.atlas_width,
        args.padding,
        args.antialias == "on",
        args.bitmap_gamma if args.bitmap else 1.0,
        args.render_scale,
        image_module,
    )
    glyphs = tuple(
        GlyphRecord(
            glyph.codepoint,
            (
                glyph.x / args.atlas_width,
                glyph.y / atlas_height,
                (glyph.x + glyph.width) / args.atlas_width,
                (glyph.y + glyph.height) / atlas_height,
            ),
            (float(glyph.width), float(glyph.height)),
            (glyph.bearing_x, glyph.bearing_y),
            (0.0, 0.0),
            (glyph.advance, glyph.advance_y),
        )
        for glyph in placements
    )
    output_font = reference.__class__(
        reference.name,
        reference.image_name,
        reference.ascender,
        reference.height,
        reference.size_pt,
        not args.bitmap,
        args.sdf_radius if not args.bitmap else 0.0,
        (args.atlas_width, atlas_height),
        reference.replacement_scale,
        glyphs,
        reference.fallback,
        reference.floor_glyph_position,
        reference.trailing,
    )
    font_payload = serialize_font_payload(output_font)
    if args.bitmap:
        # Halley's default font material uses premultiplied alpha. Keep the
        # glyph white, but premultiply RGB so transparent texels stay clear.
        texture_pixels = bytearray(args.atlas_width * atlas_height * 4)
        for index, alpha in enumerate(pixels):
            offset = index * 4
            texture_pixels[offset:offset + 4] = bytes((alpha, alpha, alpha, alpha))
        texture_payload = encode_hlif_rgba(
            bytes(texture_pixels), args.atlas_width, atlas_height
        )
    else:
        texture_pixels = generate_sdf(
            bytes(pixels),
            args.atlas_width,
            atlas_height,
            args.sdf_radius,
            args.sdf_threshold,
        )
        texture_payload = encode_hlif_single_channel(
            texture_pixels, args.atlas_width, atlas_height
        )
    output_font_path = args.output / "font" / f"{reference.name}.json"
    output_texture_path = args.output / "texture" / "fontTex" / f"{reference.name}.json"
    for path in (output_font_path, output_texture_path, args.output / "manifest.json"):
        if path.exists():
            raise HalleyFontError(f"refusing to overwrite existing output: {path}")
    output_font_path.parent.mkdir(parents=True, exist_ok=True)
    output_texture_path.parent.mkdir(parents=True, exist_ok=True)
    output_font_path.write_text(
        json.dumps({
            "_assetType": "font",
            "_decoded": {"decoded": False, "generatedBy": "ttf_to_halley.py"},
            "_payloadHex": font_payload.hex(),
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    output_texture_path.write_text(
        json.dumps({
            "_assetType": "texture",
            "_decoded": {"decoded": False, "generatedBy": "ttf_to_halley.py"},
            "_payloadHex": texture_payload.hex(),
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "font": str(args.font),
        "reference_font": str(args.reference_font),
        "reference_texture": str(args.reference_texture),
        "requested_character_count": len(requested_characters),
        "character_count": len(characters),
        "unsupported_codepoints": unsupported_codepoints,
        "atlas": {"width": args.atlas_width, "height": atlas_height},
        "font_payload_bytes": len(font_payload),
        "texture_payload_bytes": len(texture_payload),
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font", type=Path)
    parser.add_argument("--reference-font", type=Path, required=True)
    parser.add_argument("--reference-texture", type=Path, required=True)
    parser.add_argument("--characters", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pixel-size", type=int, default=16)
    parser.add_argument(
        "--render-scale",
        type=int,
        default=1,
        help="rasterize at an integer multiple before reducing the atlas",
    )
    parser.add_argument("--atlas-width", type=int, default=256)
    parser.add_argument("--padding", type=int, default=2)
    parser.add_argument("--sdf-radius", type=float, default=1.5)
    parser.add_argument(
        "--antialias",
        choices=("off", "on"),
        default="off",
        help="keep grayscale glyph edges; default off creates a binary mask",
    )
    parser.add_argument(
        "--bitmap-gamma",
        type=float,
        default=1.0,
        help="darken bitmap antialias edges; values above 1 sharpen them",
    )
    parser.add_argument(
        "--sdf-threshold",
        type=int,
        default=1,
        help="minimum grayscale value treated as inside the glyph",
    )
    parser.add_argument("--bitmap", action="store_true", help="disable SDF generation")
    args = parser.parse_args()
    try:
        print(json.dumps(convert_font(args), ensure_ascii=False, indent=2))
        return 0
    except (HalleyFontError, OSError, ValueError) as error:
        print(f"error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
