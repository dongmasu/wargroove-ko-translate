#!/usr/bin/env python3
"""Decode and encode Halley ConfigFile resources stored in LZ4 files."""

from __future__ import annotations

import argparse
import ctypes
import json
import struct
import zlib
from pathlib import Path
from typing import Any


class ConfigFormatError(ValueError):
    pass


class Reader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def take(self, size: int) -> bytes:
        if size < 0 or self.pos + size > len(self.data):
            raise ConfigFormatError(f"read outside payload at {self.pos}, size {size}")
        result = self.data[self.pos : self.pos + size]
        self.pos += size
        return result

    def u32(self) -> int:
        return struct.unpack("<I", self.take(4))[0]

    def i32(self) -> int:
        return struct.unpack("<i", self.take(4))[0]

    def i64(self) -> int:
        return struct.unpack("<q", self.take(8))[0]

    def f32(self) -> float:
        return struct.unpack("<f", self.take(4))[0]

    def boolean(self) -> bool:
        return bool(self.take(1)[0])

    def string(self) -> str:
        return self.take(self.u32()).decode("utf-8")

    def node(self, with_position: bool = True) -> Any:
        node_type = self.i32()
        if node_type == 0:
            value = None
        elif node_type == 1:
            value = self.string()
        elif node_type == 2:
            value = [self.node(with_position) for _ in range(self.u32())]
        elif node_type == 3:
            value = {self.string(): self.node(with_position) for _ in range(self.u32())}
        elif node_type == 4:
            value = self.i32()
        elif node_type == 5:
            value = self.f32()
        elif node_type == 6:
            value = [self.i32(), self.i32()]
        elif node_type == 7:
            value = [self.f32(), self.f32()]
        elif node_type == 8:
            value = {"bytes": self.take(self.u32()).hex()}
        elif node_type == 9:
            value = {"delta": [self.node(with_position) for _ in range(self.u32())], "aux": 0}
            value["aux"] = self.i32()
        elif node_type == 10:
            value = {"delta": {self.string(): self.node(with_position) for _ in range(self.u32())}, "aux": 0}
            value["aux"] = self.i32()
        elif node_type in (11, 13):
            value = {"node_type": node_type}
        elif node_type == 12:
            value = {"idx": [self.i32(), self.i32()]}
        elif node_type in (14, 15):
            value = self.i64()
        elif node_type == 16:
            value = self.boolean()
        else:
            raise ConfigFormatError(f"unsupported ConfigNode type {node_type} at {self.pos - 4}")

        # ConfigFile version 3 stores source line and column after each node.
        if with_position:
            self.take(8)
        return value


class Writer:
    def __init__(self) -> None:
        self.data = bytearray()

    def u32(self, value: int) -> None:
        self.data.extend(struct.pack("<I", value))

    def i32(self, value: int) -> None:
        self.data.extend(struct.pack("<i", value))

    def i64(self, value: int) -> None:
        self.data.extend(struct.pack("<q", value))

    def f32(self, value: float) -> None:
        self.data.extend(struct.pack("<f", value))

    def boolean(self, value: bool) -> None:
        self.data.extend(struct.pack("<?", value))

    def string(self, value: str) -> None:
        encoded = value.encode("utf-8")
        self.u32(len(encoded))
        self.data.extend(encoded)

    def node(self, value: Any) -> None:
        if value is None:
            self.i32(0)
        elif isinstance(value, bool):
            self.i32(16)
            self.boolean(value)
        elif isinstance(value, str):
            self.i32(1)
            self.string(value)
        elif isinstance(value, list):
            if len(value) == 2 and all(isinstance(item, int) for item in value):
                self.i32(6)
                self.i32(value[0])
                self.i32(value[1])
            else:
                self.i32(2)
                self.u32(len(value))
                for item in value:
                    self.node(item)
        elif isinstance(value, int):
            self.i32(4)
            self.i32(value)
        elif isinstance(value, float):
            self.i32(5)
            self.f32(value)
        elif isinstance(value, dict):
            if set(value) == {"bytes"}:
                self.i32(8)
                raw = bytes.fromhex(value["bytes"])
                self.u32(len(raw))
                self.data.extend(raw)
            elif set(value) == {"idx"}:
                self.i32(12)
                self.i32(value["idx"][0])
                self.i32(value["idx"][1])
            elif set(value) == {"node_type"}:
                self.i32(int(value["node_type"]))
            elif set(value) == {"delta", "aux"}:
                delta = value["delta"]
                self.i32(9 if isinstance(delta, list) else 10)
                if isinstance(delta, list):
                    self.u32(len(delta))
                    for item in delta:
                        self.node(item)
                else:
                    self.u32(len(delta))
                    for key, item in delta.items():
                        self.string(key)
                        self.node(item)
                self.i32(int(value["aux"]))
            else:
                self.i32(3)
                self.u32(len(value))
                for key, item in value.items():
                    self.string(key)
                    self.node(item)
        else:
            raise ConfigFormatError(f"cannot encode value of type {type(value).__name__}")

        # Keep the same ConfigFile v3 position fields as the game serializer.
        self.i32(0)
        self.i32(0)


def _lz4() -> ctypes.CDLL:
    candidates = ("liblz4.dylib", "liblz4.so", "liblz4.so.1")
    for name in candidates:
        try:
            library = ctypes.CDLL(name)
            break
        except OSError:
            continue
    else:
        raise ConfigFormatError("liblz4 was not found; install lz4 on the host")
    library.LZ4_decompress_safe.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    library.LZ4_decompress_safe.restype = ctypes.c_int
    library.LZ4_compress_default.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
    ]
    library.LZ4_compress_default.restype = ctypes.c_int
    library.LZ4_compressBound.argtypes = [ctypes.c_int]
    library.LZ4_compressBound.restype = ctypes.c_int
    return library


def decode_lz4(data: bytes) -> bytes:
    if len(data) < 8 or data[:4] != b"LZ4\0":
        raise ConfigFormatError("payload does not have a Halley LZ4 header")
    size = struct.unpack_from("<I", data, 4)[0]
    output = ctypes.create_string_buffer(size)
    result = _lz4().LZ4_decompress_safe(data[8:], output, len(data) - 8, size)
    if result != size:
        raise ConfigFormatError(f"LZ4 decompression produced {result}, expected {size}")
    return output.raw


def encode_lz4(data: bytes) -> bytes:
    library = _lz4()
    bound = library.LZ4_compressBound(len(data))
    output = ctypes.create_string_buffer(bound)
    result = library.LZ4_compress_default(data, output, len(data), bound)
    if result <= 0:
        raise ConfigFormatError("LZ4 compression failed")
    return b"LZ4\0" + struct.pack("<I", len(data)) + output.raw[:result]


def _unwrap_payload(data: bytes) -> bytes:
    if data[:4] == b"LZ4\0":
        return decode_lz4(data)
    if len(data) >= 10 and data[8:10] in {b"x\x01", b"x\x5e", b"x\x9c", b"x\xda"}:
        return zlib.decompress(data[8:])
    return data


def decode_payload(data: bytes) -> dict[str, Any]:
    reader = Reader(_unwrap_payload(data))
    version = reader.i32()
    if version == 2:
        root = reader.node(with_position=True)
    elif version == 3:
        store_file_position = reader.boolean()
        if not store_file_position:
            raise ConfigFormatError("only ConfigFile resources with position fields are supported")
        root = reader.node(with_position=True)
    else:
        raise ConfigFormatError(f"unsupported ConfigFile version {version}")
    if reader.pos != len(reader.data):
        raise ConfigFormatError(f"{len(reader.data) - reader.pos} trailing bytes remain")
    return root


def encode_payload(root: dict[str, Any]) -> bytes:
    writer = Writer()
    writer.i32(3)
    writer.boolean(True)
    writer.node(root)
    return encode_lz4(bytes(writer.data))


def cmd_decode(args: argparse.Namespace) -> int:
    root = decode_payload(args.payload.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(root, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


def cmd_encode(args: argparse.Namespace) -> int:
    root = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encode_payload(root))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    decode = commands.add_parser("decode")
    decode.add_argument("payload", type=Path)
    decode.add_argument("output", type=Path)
    decode.set_defaults(func=cmd_decode)
    encode = commands.add_parser("encode")
    encode.add_argument("input", type=Path)
    encode.add_argument("output", type=Path)
    encode.set_defaults(func=cmd_encode)
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ConfigFormatError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
