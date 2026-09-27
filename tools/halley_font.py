#!/usr/bin/env python3
"""Read and write the legacy Halley font and HLIF texture payloads."""

from __future__ import annotations

import ctypes
from ctypes.util import find_library
from dataclasses import dataclass
import json
from pathlib import Path
import struct
from typing import Any, Sequence


class HalleyFontError(ValueError):
    """Invalid or unsupported Halley font data."""


@dataclass(frozen=True)
class GlyphRecord:
    codepoint: int
    area: tuple[float, float, float, float]
    size: tuple[float, float]
    horizontal_bearing: tuple[float, float]
    vertical_bearing: tuple[float, float]
    advance: tuple[float, float]


@dataclass(frozen=True)
class HalleyFont:
    name: str
    image_name: str
    ascender: float
    height: float
    size_pt: float
    distance_field: bool
    smooth_radius: float
    image_size: tuple[int, int]
    replacement_scale: float
    glyphs: tuple[GlyphRecord, ...]
    fallback: tuple[str, ...]
    floor_glyph_position: bool
    trailing: bytes = b""


@dataclass(frozen=True)
class HLIFImage:
    width: int
    height: int
    pixels: bytes


def generate_sdf(
    pixels: bytes,
    width: int,
    height: int,
    radius: float,
    threshold: int = 127,
) -> bytes:
    """Generate Halley's single-channel signed-distance representation."""
    if len(pixels) != width * height:
        raise HalleyFontError("SDF input has the wrong size")
    if radius < 0:
        raise HalleyFontError("SDF radius must be non-negative")
    if not 0 <= threshold <= 255:
        raise HalleyFontError("SDF threshold must be between 0 and 255")
    result = bytearray(width * height)
    iradius = int(radius + 0.999999)
    for cy in range(height):
        for cx in range(width):
            inside = pixels[cx + cy * width] > threshold
            best = None
            for y in range(max(0, cy - iradius), min(height, cy + iradius + 1)):
                for x in range(max(0, cx - iradius), min(width, cx + iradius + 1)):
                    if (pixels[x + y * width] > threshold) != inside:
                        distance = (x - cx) ** 2 + (y - cy) ** 2
                        best = distance if best is None else min(best, distance)
            distance = (best ** 0.5) if best is not None else float(iradius)
            normal = (2.0 * distance - 1.0) / (2.0 * radius) if radius else 0.0
            value = 0.5 * (1.0 + normal if inside else 1.0 - normal)
            result[cx + cy * width] = max(0, min(255, int(value * 255)))
    return bytes(result)


def _read_string(data: bytes, offset: int) -> tuple[str, int]:
    if offset + 4 > len(data):
        raise HalleyFontError("truncated string length")
    size = struct.unpack_from("<I", data, offset)[0]
    offset += 4
    end = offset + size
    if end > len(data):
        raise HalleyFontError("truncated string")
    try:
        return data[offset:end].decode("utf-8"), end
    except UnicodeDecodeError as error:
        raise HalleyFontError("invalid UTF-8 string") from error


def _write_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack("<I", len(encoded)) + encoded


def parse_font_payload(data: bytes) -> HalleyFont:
    name, offset = _read_string(data, 0)
    image_name, offset = _read_string(data, offset)
    if offset + 17 > len(data):
        raise HalleyFontError("truncated font header")
    ascender, height, size_pt = struct.unpack_from("<3f", data, offset)
    offset += 12
    distance_field = bool(data[offset])
    offset += 1
    smooth_radius = struct.unpack_from("<f", data, offset)[0]
    offset += 4
    image_size = struct.unpack_from("<2i", data, offset)
    offset += 8
    replacement_scale = struct.unpack_from("<f", data, offset)[0]
    offset += 4
    if offset + 4 > len(data):
        raise HalleyFontError("missing glyph count")
    glyph_count = struct.unpack_from("<I", data, offset)[0]
    offset += 4

    glyphs: list[GlyphRecord] = []
    for _ in range(glyph_count):
        if offset + 52 > len(data):
            raise HalleyFontError("truncated legacy glyph record")
        codepoint = struct.unpack_from("<i", data, offset)[0]
        offset += 4
        values = struct.unpack_from("<12f", data, offset)
        offset += 48
        glyphs.append(
            GlyphRecord(
                codepoint,
                tuple(values[0:4]),
                tuple(values[4:6]),
                tuple(values[6:8]),
                tuple(values[8:10]),
                tuple(values[10:12]),
            )
        )

    if offset + 4 > len(data):
        raise HalleyFontError("missing fallback count")
    fallback_count = struct.unpack_from("<I", data, offset)[0]
    offset += 4
    fallback: list[str] = []
    for _ in range(fallback_count):
        value, offset = _read_string(data, offset)
        fallback.append(value)
    if offset >= len(data):
        raise HalleyFontError("missing floorGlyphPosition flag")
    floor_glyph_position = bool(data[offset])
    offset += 1
    return HalleyFont(
        name,
        image_name,
        ascender,
        height,
        size_pt,
        distance_field,
        smooth_radius,
        image_size,
        replacement_scale,
        tuple(glyphs),
        tuple(fallback),
        floor_glyph_position,
        data[offset:],
    )


def serialize_font_payload(font: HalleyFont) -> bytes:
    result = bytearray()
    result.extend(_write_string(font.name))
    result.extend(_write_string(font.image_name))
    result.extend(struct.pack("<3f", font.ascender, font.height, font.size_pt))
    result.extend(bytes([int(font.distance_field)]))
    result.extend(struct.pack("<f", font.smooth_radius))
    result.extend(struct.pack("<2i", *font.image_size))
    result.extend(struct.pack("<f", font.replacement_scale))
    result.extend(struct.pack("<I", len(font.glyphs)))
    for glyph in font.glyphs:
        result.extend(struct.pack("<i", glyph.codepoint))
        result.extend(struct.pack("<12f", *(
            *glyph.area,
            *glyph.size,
            *glyph.horizontal_bearing,
            *glyph.vertical_bearing,
            *glyph.advance,
        )))
    result.extend(struct.pack("<I", len(font.fallback)))
    for value in font.fallback:
        result.extend(_write_string(value))
    result.extend(bytes([int(font.floor_glyph_position)]))
    result.extend(font.trailing)
    return bytes(result)


def load_payload_json(path: Path) -> bytes:
    document = json.loads(path.read_text(encoding="utf-8"))
    try:
        return bytes.fromhex(document["_payloadHex"])
    except (KeyError, TypeError, ValueError) as error:
        raise HalleyFontError(f"invalid _payloadHex in {path}") from error


def _lz4() -> Any:
    candidates = (
        find_library("lz4"),
        "liblz4.dylib",
        "liblz4.so",
        "liblz4.so.1",
        "lz4.dll",
    )
    for candidate in candidates:
        if not candidate:
            continue
        try:
            library = ctypes.CDLL(candidate)
            library.LZ4_compress_default.argtypes = [
                ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int
            ]
            library.LZ4_compress_default.restype = ctypes.c_int
            library.LZ4_decompress_safe.argtypes = [
                ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int
            ]
            library.LZ4_decompress_safe.restype = ctypes.c_int
            library.LZ4_compressBound.argtypes = [ctypes.c_int]
            library.LZ4_compressBound.restype = ctypes.c_int
            return library
        except (AttributeError, OSError):
            continue
    raise HalleyFontError("liblz4 was not found")


def _encode_lines(pixels: bytes, width: int, height: int, bytes_per_pixel: int) -> bytes:
    # HLIF accepts unfiltered rows; all-zero line encodings preserve the
    # pixel bytes unchanged for both single-channel and RGBA textures.
    if len(pixels) != width * height * bytes_per_pixel:
        raise HalleyFontError("HLIF pixel data has the wrong size")
    return bytes(height) + pixels


def _encode_hlif(pixels: bytes, width: int, height: int, fmt: int, bytes_per_pixel: int) -> bytes:
    if not 0 < width <= 65535 or not 0 < height <= 65535:
        raise HalleyFontError("HLIF dimensions must fit uint16")
    raw = _encode_lines(pixels, width, height, bytes_per_pixel)
    library = _lz4()
    bound = library.LZ4_compressBound(len(raw))
    output = ctypes.create_string_buffer(bound)
    result = library.LZ4_compress_default(raw, output, len(raw), bound)
    if result <= 0:
        raise HalleyFontError("HLIF LZ4 compression failed")
    header = struct.pack(
        "<8sHHIIBBBB",
        b"HLIFv01\0",
        width,
        height,
        result,
        len(raw),
        fmt,
        0,
        0,
        0,
    )
    return header + output.raw[:result]


def encode_hlif_single_channel(pixels: bytes, width: int, height: int) -> bytes:
    return _encode_hlif(pixels, width, height, 1, 1)


def encode_hlif_rgba(pixels: bytes, width: int, height: int) -> bytes:
    """Encode an RGBA HLIF image without palette optimization."""
    return _encode_hlif(pixels, width, height, 0, 4)


def _decode_hlif(data: bytes, expected_format: int, bytes_per_pixel: int) -> HLIFImage:
    if len(data) < 24 or data[:8] != b"HLIFv01\0":
        raise HalleyFontError("not an HLIF payload")
    magic, width, height, compressed_size, raw_size, fmt, flags, palettes, reserved = struct.unpack_from(
        "<8sHHIIBBBB", data, 0
    )
    if fmt != expected_format or flags != 0 or palettes != 0 or reserved != 0:
        raise HalleyFontError("unexpected HLIF format")
    compressed = data[24:24 + compressed_size]
    if len(compressed) != compressed_size:
        raise HalleyFontError("truncated HLIF payload")
    output = ctypes.create_string_buffer(raw_size)
    result = _lz4().LZ4_decompress_safe(compressed, output, len(compressed), raw_size)
    if result != raw_size:
        raise HalleyFontError("HLIF LZ4 decompression failed")
    raw = output.raw[:raw_size]
    if len(raw) != height + width * height * bytes_per_pixel:
        raise HalleyFontError("invalid HLIF raw size")
    return HLIFImage(width, height, raw[height:])


def decode_hlif_single_channel(data: bytes) -> HLIFImage:
    return _decode_hlif(data, 1, 1)


def decode_hlif_rgba(data: bytes) -> HLIFImage:
    return _decode_hlif(data, 0, 4)
