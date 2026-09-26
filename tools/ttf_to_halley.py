#!/usr/bin/env python3
"""Convert a TTF/OTF font into legacy Halley font JSON assets."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

try:
    from tools.halley_font import (
        GlyphRecord,
        HalleyFontError,
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
    pixels: bytes


def _load_pillow() -> Any:
    try:
        from PIL import ImageFont
    except ImportError as error:
        raise HalleyFontError(
            "Pillow is required for TTF conversion; install it with "
            "'python3 -m pip install Pillow'"
        ) from error
    return ImageFont


def load_characters(path: Path) -> list[int]:
    text = path.read_text(encoding="utf-8")
    result = sorted({ord(char) for char in text if char not in "\r\n"})
    if not result:
        raise HalleyFontError("character set is empty")
    return result


def _render_glyph(font: Any, codepoint: int, padding: int) -> tuple[int, int, float, float, float, bytes]:
    char = chr(codepoint)
    bbox = font.getbbox(char)
    if bbox is None:
        raise HalleyFontError(f"font has no glyph for U+{codepoint:04X}")
    left, top, right, bottom = bbox
    advance = float(font.getlength(char))
    width = max(1, right - left, round(advance) if right == left else 0)
    height = max(1, bottom - top)
    canvas_width = width + padding * 2
    canvas_height = height + padding * 2
    image = font.getmask(char, mode="L")
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
    return (
        canvas_width,
        canvas_height,
        float(left - padding),
        float(-top + padding),
        advance,
        bytes(pixels),
    )


def _pack_glyphs(font: Any, characters: list[int], atlas_width: int, padding: int) -> tuple[list[PlacedGlyph], bytes, int]:
    pending = []
    for codepoint in characters:
        width, height, bearing_x, bearing_y, advance, pixels = _render_glyph(
            font, codepoint, padding
        )
        pending.append((codepoint, width, height, bearing_x, bearing_y, advance, pixels))

    x = 0
    y = 0
    row_height = 0
    placements: list[PlacedGlyph] = []
    for codepoint, width, height, bearing_x, bearing_y, advance, pixels in pending:
        if width > atlas_width:
            raise HalleyFontError(f"glyph U+{codepoint:04X} exceeds atlas width")
        if x and x + width > atlas_width:
            x = 0
            y += row_height
            row_height = 0
        placements.append(
            PlacedGlyph(codepoint, x, y, width, height, bearing_x, bearing_y, advance, pixels)
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
    image_font = _load_pillow()
    reference = parse_font_payload(load_payload_json(args.reference_font))
    reference_texture = load_payload_json(args.reference_texture)
    characters = load_characters(args.characters)
    font = image_font.truetype(str(args.font), args.pixel_size)
    placements, pixels, atlas_height = _pack_glyphs(
        font, characters, args.atlas_width, args.padding
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
            (glyph.advance, 0.0),
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
    texture_pixels = (
        generate_sdf(bytes(pixels), args.atlas_width, atlas_height, args.sdf_radius)
        if not args.bitmap
        else bytes(pixels)
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
        "character_count": len(characters),
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
    parser.add_argument("--atlas-width", type=int, default=256)
    parser.add_argument("--padding", type=int, default=2)
    parser.add_argument("--sdf-radius", type=float, default=1.5)
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
