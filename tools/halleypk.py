#!/usr/bin/env python3
"""Inspect, extract, and repack Halley asset packs without changing inputs."""

from __future__ import annotations

import argparse
import ctypes
from ctypes.util import find_library
from functools import lru_cache
import hashlib
import json
import shutil
import struct
import sys
import zlib
from dataclasses import dataclass, asdict
from pathlib import Path, PurePosixPath
from typing import Any


ASSET_TYPES = (
    "binaryFile",
    "textFile",
    "configFile",
    "gameProperties",
    "texture",
    "shader",
    "materialDefinition",
    "image",
    "spriteSheet",
    "sprite",
    "animation",
    "font",
    "audioClip",
    "audioObject",
    "audioEvent",
    "mesh",
    "meshAnimation",
    "variableTable",
    "renderGraphDefinition",
    "scriptGraph",
    "navmeshSet",
    "prefab",
    "scene",
    "uiDefinition",
)

MAGIC_V1 = b"HALLEYPK"
MAGIC_V2 = b"HALLEYP2"
AES_KEY = b"+Ohzep4z06NuKguN"
ZERO_IV = b"\0" * 16

_SBOX = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)
_INV_SBOX = tuple(_SBOX.index(value) for value in range(256))
_RCON = (0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36)


def _xtime(value: int) -> int:
    return ((value << 1) ^ (0x11B if value & 0x80 else 0)) & 0xFF


def _multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left = _xtime(left)
        right >>= 1
    return result


@lru_cache(maxsize=4)
def _round_keys(key: bytes) -> tuple[bytes, ...]:
    if len(key) != 16:
        raise ValueError("AES-128 requires a 16-byte key")
    expanded = bytearray(key)
    for index in range(4, 44):
        word = list(expanded[(index - 1) * 4 : index * 4])
        if index % 4 == 0:
            word = [_SBOX[word[1]], _SBOX[word[2]], _SBOX[word[3]], _SBOX[word[0]]]
            word[0] ^= _RCON[index // 4]
        previous = expanded[(index - 4) * 4 : (index - 3) * 4]
        expanded.extend(left ^ right for left, right in zip(previous, word))
    return tuple(bytes(expanded[index : index + 16]) for index in range(0, 176, 16))


def _add_round_key(state: list[int], key: bytes) -> None:
    for index, value in enumerate(key):
        state[index] ^= value


def _sub_bytes(state: list[int], inverse: bool = False) -> None:
    box = _INV_SBOX if inverse else _SBOX
    for index, value in enumerate(state):
        state[index] = box[value]


def _shift_rows(state: list[int], inverse: bool = False) -> None:
    original = state[:]
    for row in range(4):
        for column in range(4):
            source = (column - row if inverse else column + row) % 4
            state[4 * column + row] = original[4 * source + row]


def _mix_columns(state: list[int], inverse: bool = False) -> None:
    for column in range(4):
        offset = 4 * column
        a, b, c, d = state[offset : offset + 4]
        if inverse:
            state[offset : offset + 4] = (
                _multiply(a, 0x0E) ^ _multiply(b, 0x0B) ^ _multiply(c, 0x0D) ^ _multiply(d, 0x09),
                _multiply(a, 0x09) ^ _multiply(b, 0x0E) ^ _multiply(c, 0x0B) ^ _multiply(d, 0x0D),
                _multiply(a, 0x0D) ^ _multiply(b, 0x09) ^ _multiply(c, 0x0E) ^ _multiply(d, 0x0B),
                _multiply(a, 0x0B) ^ _multiply(b, 0x0D) ^ _multiply(c, 0x09) ^ _multiply(d, 0x0E),
            )
        else:
            state[offset : offset + 4] = (
                _multiply(a, 2) ^ _multiply(b, 3) ^ c ^ d,
                a ^ _multiply(b, 2) ^ _multiply(c, 3) ^ d,
                a ^ b ^ _multiply(c, 2) ^ _multiply(d, 3),
                _multiply(a, 3) ^ b ^ c ^ _multiply(d, 2),
            )


def _aes_block(block: bytes, key: bytes, decrypt: bool = False) -> bytes:
    state = list(block)
    keys = _round_keys(key)
    if decrypt:
        _add_round_key(state, keys[10])
        for round_key in reversed(keys[1:10]):
            _shift_rows(state, inverse=True)
            _sub_bytes(state, inverse=True)
            _add_round_key(state, round_key)
            _mix_columns(state, inverse=True)
        _shift_rows(state, inverse=True)
        _sub_bytes(state, inverse=True)
        _add_round_key(state, keys[0])
    else:
        _add_round_key(state, keys[0])
        for round_key in keys[1:10]:
            _sub_bytes(state)
            _shift_rows(state)
            _mix_columns(state)
            _add_round_key(state, round_key)
        _sub_bytes(state)
        _shift_rows(state)
        _add_round_key(state, keys[10])
    return bytes(state)


@lru_cache(maxsize=1)
def _libcrypto() -> Any:
    candidates = (
        find_library("crypto"),
        "libcrypto.dylib",
        "libcrypto.so",
        "libcrypto-3-x64.dll",
        "libcrypto-1_1-x64.dll",
    )
    for candidate in candidates:
        if not candidate:
            continue
        try:
            library = ctypes.CDLL(candidate)
            library.AES_set_encrypt_key.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
            library.AES_set_encrypt_key.restype = ctypes.c_int
            library.AES_set_decrypt_key.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
            library.AES_set_decrypt_key.restype = ctypes.c_int
            library.AES_cbc_encrypt.argtypes = [
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_size_t,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_int,
            ]
            library.AES_cbc_encrypt.restype = None
            return library
        except (AttributeError, OSError):
            continue
    return None


def _libcrypto_aes_cbc(data: bytes, iv: bytes, decrypt: bool) -> bytes | None:
    library = _libcrypto()
    if library is None:
        return None
    key = ctypes.create_string_buffer(512)
    key_bytes = ctypes.create_string_buffer(AES_KEY)
    set_key = library.AES_set_decrypt_key if decrypt else library.AES_set_encrypt_key
    if set_key(key_bytes, 128, key) != 0:
        raise FormatError("libcrypto rejected the Halley AES key")
    source = ctypes.create_string_buffer(data)
    output = ctypes.create_string_buffer(len(data))
    chain = ctypes.create_string_buffer(iv)
    library.AES_cbc_encrypt(source, output, len(data), key, chain, 0 if decrypt else 1)
    return output.raw


def aes_cbc(data: bytes, iv: bytes, decrypt: bool = False) -> bytes:
    """Apply AES-128-CBC with no padding, matching ModPacker."""
    if len(iv) != 16 or len(data) % 16:
        raise FormatError("AES-CBC data and IV must be 16-byte aligned")
    accelerated = _libcrypto_aes_cbc(data, iv, decrypt)
    if accelerated is not None:
        return accelerated
    result = bytearray()
    previous = iv
    for offset in range(0, len(data), 16):
        block = data[offset : offset + 16]
        if decrypt:
            plain = bytes(left ^ right for left, right in zip(_aes_block(block, AES_KEY, True), previous))
            result.extend(plain)
            previous = block
        else:
            encrypted = _aes_block(
                bytes(left ^ right for left, right in zip(block, previous)),
                AES_KEY,
            )
            result.extend(encrypted)
            previous = encrypted
    return bytes(result)


class FormatError(ValueError):
    """Raised when a pack is malformed or uses an unsupported encoding."""


@dataclass(frozen=True)
class Entry:
    asset_type: int
    asset_type_name: str
    name: str
    offset: int
    size: int
    metadata: Any
    metadata_raw: bytes


class Reader:
    """Reader for Halley's serializer version 0, used by these v1 packs."""

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def remaining(self) -> int:
        return len(self.data) - self.pos

    def read(self, size: int) -> bytes:
        if size < 0 or size > self.remaining():
            raise FormatError(
                f"index ends at byte {self.pos}; requested {size} bytes "
                f"with {self.remaining()} remaining"
            )
        result = self.data[self.pos : self.pos + size]
        self.pos += size
        return result

    def unpack(self, fmt: str) -> Any:
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.read(size))[0]

    def uint32(self) -> int:
        return self.unpack("<I")

    def int32(self) -> int:
        return self.unpack("<i")

    def int64(self) -> int:
        return self.unpack("<q")

    def float32(self) -> float:
        return self.unpack("<f")

    def boolean(self) -> bool:
        return bool(self.unpack("<?"))

    def string(self) -> str:
        size = self.uint32()
        raw = self.read(size)
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise FormatError(f"invalid UTF-8 string at index byte {self.pos - size}") from error

    def node(self, depth: int = 0) -> Any:
        if depth > 128:
            raise FormatError("metadata nesting exceeds 128 levels")

        node_type = self.int32()
        if node_type == 0:  # Undefined
            return None
        if node_type == 1:  # String
            return self.string()
        if node_type == 2:  # Sequence
            return [self.node(depth + 1) for _ in range(self.uint32())]
        if node_type == 3:  # Map
            return {self.string(): self.node(depth + 1) for _ in range(self.uint32())}
        if node_type == 4:  # Int
            return self.int32()
        if node_type == 5:  # Float
            return self.float32()
        if node_type == 6:  # Int2
            return [self.int32(), self.int32()]
        if node_type == 7:  # Float2
            return [self.float32(), self.float32()]
        if node_type == 8:  # Bytes
            return {"bytes": self.read(self.uint32()).hex()}
        if node_type in (9, 10):  # DeltaSequence, DeltaMap
            value = (
                [self.node(depth + 1) for _ in range(self.uint32())]
                if node_type == 9
                else {self.string(): self.node(depth + 1) for _ in range(self.uint32())}
            )
            return {"delta": value, "aux": self.int32()}
        if node_type in (11, 13):  # Noop, Del
            return {"node_type": node_type}
        if node_type == 12:  # Idx
            return {"idx": [self.int32(), self.int32()]}
        if node_type in (14, 15):  # Int64, EntityId
            return self.int64()
        if node_type == 16:  # Bool
            return self.boolean()
        raise FormatError(f"unsupported serialized ConfigNode type {node_type}")


class HalleyPack:
    """A Halley asset pack with a readable AssetDatabase."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = path.read_bytes()
        self.magic, self.asset_db_start, self.data_start, self.iv = self._read_header()
        if not (0 <= self.asset_db_start <= self.data_start <= len(self.data)):
            raise FormatError("header contains invalid AssetDatabase or payload offsets")
        encrypted_payload = self.data[self.data_start :]
        self.payload_data = (
            aes_cbc(encrypted_payload, self.iv, decrypt=True)
            if self.iv != ZERO_IV
            else encrypted_payload
        )
        packed_index = self.data[self.asset_db_start : self.data_start]
        if len(packed_index) < 8:
            raise FormatError("AssetDatabase block is smaller than its size prefix")
        expected_size = struct.unpack_from("<Q", packed_index, 0)[0]
        self.compressed_index = packed_index[8:]
        try:
            self.index = zlib.decompress(self.compressed_index)
        except zlib.error as error:
            raise FormatError("unable to decompress the AssetDatabase") from error
        if len(self.index) != expected_size:
            raise FormatError(
                f"AssetDatabase size mismatch: expected {expected_size}, got {len(self.index)}"
            )
        self.entries = self._read_entries()

    def _read_header(self) -> tuple[str, int, int, bytes]:
        if len(self.data) < 40:
            raise FormatError("file is smaller than the minimum Halley pack header")
        magic = self.data[:8]
        if magic == MAGIC_V1:
            # AssetPackHeaderV1: 16-byte IV, then two uint64 offsets.
            iv, asset_db_start, data_start = struct.unpack_from("<16sQQ", self.data, 8)
            return "v1", asset_db_start, data_start, iv
        if magic == MAGIC_V2:
            # AssetPackHeaderV2: version, padding, six reserved bytes, offsets, IV.
            version, _padding, _reserved, asset_db_start, data_start, iv = struct.unpack_from(
                "<BB6sQQ16s", self.data, 8
            )
            if version != 2:
                raise FormatError(f"unsupported HALLEYP2 version {version}")
            return "v2", asset_db_start, data_start, iv
        raise FormatError("not a HALLEYPK or HALLEYP2 asset pack")

    def _read_entries(self) -> list[Entry]:
        errors: list[FormatError] = []
        for legacy_layout in (False, True):
            for legacy_metadata in (False, True):
                try:
                    return self._read_entries_layout(legacy_layout, legacy_metadata)
                except FormatError as error:
                    errors.append(error)
        raise errors[0]

    def _read_entries_layout(self, legacy: bool, legacy_metadata: bool) -> list[Entry]:
        reader = Reader(self.index)
        databases = reader.uint32()
        entries: list[Entry] = []
        for _ in range(databases):
            if legacy:
                # Older Wargroove 1 config packs omitted the TreeMap key and
                # serialized TypedDB.type directly before the entry count.
                asset_type = reader.int32()
                count = reader.uint32()
            else:
                _database_key = reader.int32()
                asset_type = reader.int32()
                count = reader.uint32()
            if asset_type < 0 or asset_type >= len(ASSET_TYPES):
                raise FormatError(f"unknown AssetType value {asset_type}")
            for _ in range(count):
                name = reader.string()
                location = reader.string()
                metadata_start = reader.pos
                if legacy_metadata:
                    metadata = {
                        reader.string(): reader.string()
                        for _ in range(reader.uint32())
                    }
                else:
                    metadata = reader.node()
                try:
                    offset_text, size_text = location.split(":", 1)
                    offset, size = int(offset_text), int(size_text)
                except ValueError as error:
                    raise FormatError(f"invalid payload location {location!r} for {name!r}") from error
                if offset < 0 or size < 0 or offset + size > len(self.payload_data):
                    raise FormatError(f"payload outside container for {name!r}")
                entries.append(
                    Entry(
                        asset_type,
                        ASSET_TYPES[asset_type],
                        name,
                        offset,
                        size,
                        metadata,
                        self.index[metadata_start : reader.pos],
                    )
                )
        if reader.remaining():
            raise FormatError(f"AssetDatabase has {reader.remaining()} unread trailing bytes")
        self.legacy_layout = legacy
        self.legacy_metadata = legacy_metadata
        return entries

    def payload(self, entry: Entry) -> bytes:
        return self.payload_data[entry.offset : entry.offset + entry.size]

    def manifest(self) -> dict[str, Any]:
        def serializable_entry(entry: Entry) -> dict[str, Any]:
            result = asdict(entry)
            del result["metadata_raw"]
            return result

        return {
            "source": str(self.path),
            "container": self.magic,
            "file_bytes": len(self.data),
            "asset_database_start": self.asset_db_start,
            "data_start": self.data_start,
            "encrypted_payload": self.iv != ZERO_IV,
            "compressed_index_bytes": len(self.compressed_index),
            "decompressed_index_bytes": len(self.index),
            "entry_count": len(self.entries),
            "entries": [serializable_entry(entry) for entry in self.entries],
        }


def matches(entry: Entry, patterns: list[str]) -> bool:
    if not patterns:
        return True
    candidate = f"{entry.asset_type_name}:{entry.name}"
    return any(pattern in candidate for pattern in patterns)


def output_path(root: Path, entry: Entry) -> Path:
    relative = PurePosixPath(entry.asset_type_name) / PurePosixPath(entry.name)
    if relative.is_absolute() or ".." in relative.parts:
        raise FormatError(f"unsafe asset path {entry.name!r}")
    return root.joinpath(*relative.parts).with_suffix(".bin")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_manifest(entry: Entry) -> dict[str, Any]:
    result = asdict(entry)
    del result["metadata_raw"]
    return result


def pack_container(
    entries: list[tuple[Entry, bytes]],
    legacy_layout: bool,
    legacy_metadata: bool,
    version: int = 1,
    iv: bytes = ZERO_IV,
) -> bytes:
    """Build a pack while preserving the source index's serialization variants."""
    if len(iv) != 16:
        raise FormatError("pack IV must be exactly 16 bytes")
    payload = bytearray()
    indexed: list[tuple[Entry, int, int]] = []
    for entry, content in entries:
        aligned = (len(payload) + 15) & ~15
        payload.extend(b"\0" * (aligned - len(payload)))
        offset = len(payload)
        payload.extend(content)
        indexed.append((entry, offset, len(content)))

    databases: dict[int, list[tuple[Entry, int, int]]] = {}
    for item in indexed:
        databases.setdefault(item[0].asset_type, []).append(item)

    index = bytearray()
    index.extend(struct.pack("<I", len(databases)))
    for asset_type in sorted(databases):
        group = sorted(databases[asset_type], key=lambda item: item[0].name)
        if legacy_layout:
            index.extend(struct.pack("<i", asset_type))
        else:
            index.extend(struct.pack("<i", asset_type))
            index.extend(struct.pack("<i", asset_type))
        index.extend(struct.pack("<I", len(group)))
        for entry, offset, size in group:
            name = entry.name.encode("utf-8")
            location = f"{offset}:{size}".encode("ascii")
            index.extend(struct.pack("<I", len(name)))
            index.extend(name)
            index.extend(struct.pack("<I", len(location)))
            index.extend(location)
            index.extend(entry.metadata_raw or b"\0\0\0\0")

    compressed = zlib.compress(bytes(index))
    packed_index = struct.pack("<Q", len(index)) + compressed
    payload_bytes = bytes(payload)
    if iv != ZERO_IV:
        payload_bytes += b"\0" * ((-len(payload_bytes)) % 16)
    packed_payload = aes_cbc(payload_bytes, iv) if iv != ZERO_IV else payload_bytes
    if version == 1:
        asset_db_start = 40
        data_start = asset_db_start + len(packed_index)
        header = MAGIC_V1 + struct.pack("<16sQQ", iv, asset_db_start, data_start)
        return header + packed_index + packed_payload
    asset_db_start = 48
    padded_index_size = (len(packed_index) + 15) & ~15
    data_start = asset_db_start + padded_index_size
    header = MAGIC_V2 + struct.pack(
        "<BB6sQQ16s",
        2,
        padded_index_size - len(packed_index),
        b"\0" * 6,
        asset_db_start,
        data_start,
        iv,
    )
    return header + packed_index + b"\0" * (padded_index_size - len(packed_index)) + packed_payload


def cmd_list(args: argparse.Namespace) -> int:
    pack = HalleyPack(args.pack)
    manifest = pack.manifest()
    if args.match:
        selected = [entry for entry in pack.entries if matches(entry, args.match)]
        manifest["entry_count"] = len(selected)
        manifest["entries"] = [entry_manifest(entry) for entry in selected]
    output = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    pack = HalleyPack(args.pack)
    selected = [entry for entry in pack.entries if matches(entry, args.match)]
    if not selected:
        raise FormatError("no entries matched")
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = pack.manifest()
    manifest["entry_count"] = len(selected)
    manifest["entries"] = [entry_manifest(entry) for entry in selected]
    for entry in selected:
        destination = output_path(args.output, entry)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(pack.payload(entry))
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Extracted {len(selected)} entries to {args.output}")
    return 0


def _read_payload_json(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FormatError(f"invalid payload JSON: {path}") from error
    if not isinstance(document, dict) or "_payloadHex" not in document:
        raise FormatError(f"JSON has no _payloadHex field: {path}")
    if not isinstance(document["_payloadHex"], str):
        raise FormatError(f"_payloadHex must be a string: {path}")
    try:
        bytes.fromhex(document["_payloadHex"])
    except ValueError as error:
        raise FormatError(f"_payloadHex is not valid hexadecimal: {path}") from error
    return document


def cmd_payload_export(args: argparse.Namespace) -> int:
    document = _read_payload_json(args.source)
    payload = bytes.fromhex(document["_payloadHex"])
    if args.output.exists():
        raise FormatError(f"refusing to overwrite existing output: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(f"Exported {len(payload)} payload bytes to {args.output}")
    return 0


def cmd_payload_import(args: argparse.Namespace) -> int:
    document = _read_payload_json(args.template)
    payload = args.payload.read_bytes()
    document["_payloadHex"] = payload.hex()
    if args.output.exists():
        raise FormatError(f"refusing to overwrite existing output: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Imported {len(payload)} payload bytes into {args.output}")
    return 0


def cmd_roundtrip(args: argparse.Namespace) -> int:
    # A byte-for-byte copy validates source accessibility without serializing a new pack.
    HalleyPack(args.pack)
    if args.output.exists():
        raise FormatError(f"refusing to overwrite existing output: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.pack, args.output)
    source_hash = sha256(args.pack)
    output_hash = sha256(args.output)
    if source_hash != output_hash:
        raise FormatError("round-trip copy hash mismatch")
    print(f"Verified byte-identical copy: {output_hash}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    pack = HalleyPack(args.pack)
    if args.output.resolve() == args.pack.resolve():
        raise FormatError("refusing to overwrite the input pack")
    if args.asset_type not in ASSET_TYPES:
        raise FormatError(f"unknown asset type {args.asset_type!r}")
    if any(entry.asset_type_name == args.asset_type and entry.name == args.asset_name for entry in pack.entries):
        raise FormatError(f"asset already exists: {args.asset_type}:{args.asset_name}")
    if "/" not in args.asset_name and args.asset_name.startswith(".."):
        raise FormatError("unsafe asset name")

    metadata_source = None
    if args.metadata_from:
        metadata_source = next(
            (entry for entry in pack.entries if entry.name == args.metadata_from),
            None,
        )
        if metadata_source is None:
            raise FormatError(f"metadata source was not found: {args.metadata_from}")
    else:
        metadata_source = next(
            (entry for entry in pack.entries if entry.asset_type_name == args.asset_type),
            None,
        )
    metadata_raw = metadata_source.metadata_raw if metadata_source else b"\0\0\0\0"
    new_type = ASSET_TYPES.index(args.asset_type)
    new_entry = Entry(
        new_type,
        args.asset_type,
        args.asset_name,
        0,
        0,
        {},
        metadata_raw,
    )
    all_entries = [(entry, pack.payload(entry)) for entry in pack.entries]
    all_entries.append((new_entry, args.payload.read_bytes()))
    output_data = pack_container(
        all_entries,
        pack.legacy_layout,
        pack.legacy_metadata,
        version=1,
        iv=pack.iv,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FormatError(f"refusing to overwrite existing output: {args.output}")
    args.output.write_bytes(output_data)

    verified = HalleyPack(args.output)
    added = next(
        (entry for entry in verified.entries
         if entry.asset_type_name == args.asset_type and entry.name == args.asset_name),
        None,
    )
    if added is None or verified.payload(added) != args.payload.read_bytes():
        raise FormatError("output verification failed for the added asset")
    print(f"Added {args.asset_type}:{args.asset_name} to {args.output}")
    print(f"Output SHA-256: {hashlib.sha256(output_data).hexdigest()}")
    return 0


def cmd_pack(args: argparse.Namespace) -> int:
    pack = HalleyPack(args.pack)
    if args.output.resolve() == args.pack.resolve():
        raise FormatError("refusing to overwrite the input pack")
    if args.output.exists():
        raise FormatError(f"refusing to overwrite existing output: {args.output}")
    entries = [(entry, pack.payload(entry)) for entry in pack.entries]
    output_data = pack_container(
        entries,
        pack.legacy_layout,
        pack.legacy_metadata,
        version=1,
        iv=pack.iv,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output_data)
    verified = HalleyPack(args.output)
    if len(verified.entries) != len(pack.entries):
        raise FormatError("packed output entry count does not match the source")
    for original, rebuilt in zip(
        sorted(pack.entries, key=lambda entry: (entry.asset_type, entry.name)),
        sorted(verified.entries, key=lambda entry: (entry.asset_type, entry.name)),
    ):
        if (
            original.asset_type != rebuilt.asset_type
            or original.name != rebuilt.name
            or pack.payload(original) != verified.payload(rebuilt)
        ):
            raise FormatError(f"packed output differs for {original.asset_type_name}:{original.name}")
    print(f"Packed and verified {len(verified.entries)} entries to {args.output}")
    print(f"Output SHA-256: {hashlib.sha256(output_data).hexdigest()}")
    return 0


def cmd_replace(args: argparse.Namespace) -> int:
    pack = HalleyPack(args.pack)
    if args.output.resolve() == args.pack.resolve():
        raise FormatError("refusing to overwrite the input pack")
    target = next(
        (
            entry
            for entry in pack.entries
            if entry.asset_type_name == args.asset_type and entry.name == args.asset_name
        ),
        None,
    )
    if target is None:
        raise FormatError(f"asset was not found: {args.asset_type}:{args.asset_name}")
    replacement = args.payload.read_bytes()
    entries = [
        (entry, replacement if entry is target else pack.payload(entry))
        for entry in pack.entries
    ]
    output_data = pack_container(
        entries,
        pack.legacy_layout,
        pack.legacy_metadata,
        version=1,
        iv=pack.iv,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FormatError(f"refusing to overwrite existing output: {args.output}")
    args.output.write_bytes(output_data)
    verified = HalleyPack(args.output)
    rebuilt = next(
        (
            entry
            for entry in verified.entries
            if entry.asset_type_name == args.asset_type and entry.name == args.asset_name
        ),
        None,
    )
    if rebuilt is None or verified.payload(rebuilt) != replacement:
        raise FormatError("output verification failed for the replaced asset")
    print(f"Replaced {args.asset_type}:{args.asset_name} in {args.output}")
    print(f"Output SHA-256: {hashlib.sha256(output_data).hexdigest()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read, extract, add to, and repack unencrypted Halley asset packs."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    list_parser = commands.add_parser("list", help="write a parsed AssetDatabase manifest")
    list_parser.add_argument("pack", type=Path)
    list_parser.add_argument("--match", action="append", default=[], help="substring filter; repeatable")
    list_parser.add_argument("--output", type=Path, help="JSON destination; stdout by default")
    list_parser.set_defaults(func=cmd_list)

    extract_parser = commands.add_parser("extract", help="extract matching payloads and manifest")
    extract_parser.add_argument("pack", type=Path)
    extract_parser.add_argument("output", type=Path)
    extract_parser.add_argument("--match", action="append", default=[], help="substring filter; repeatable")
    extract_parser.set_defaults(func=cmd_extract)

    payload_parser = commands.add_parser("payload", help="convert JSON _payloadHex and raw payload files")
    payload_commands = payload_parser.add_subparsers(dest="payload_command", required=True)

    payload_export_parser = payload_commands.add_parser(
        "export", help="write a JSON _payloadHex value as raw bytes"
    )
    payload_export_parser.add_argument("source", type=Path, help="binary-resource JSON")
    payload_export_parser.add_argument("output", type=Path, help="raw payload output")
    payload_export_parser.set_defaults(func=cmd_payload_export)

    payload_import_parser = payload_commands.add_parser(
        "import", help="replace a JSON _payloadHex value with raw bytes"
    )
    payload_import_parser.add_argument("template", type=Path, help="binary-resource JSON template")
    payload_import_parser.add_argument("payload", type=Path, help="raw payload input")
    payload_import_parser.add_argument("output", type=Path, help="new JSON output")
    payload_import_parser.set_defaults(func=cmd_payload_import)

    roundtrip_parser = commands.add_parser(
        "roundtrip", help="make a verified byte-identical copy; never alters the input"
    )
    roundtrip_parser.add_argument("pack", type=Path)
    roundtrip_parser.add_argument("output", type=Path)
    roundtrip_parser.set_defaults(func=cmd_roundtrip)

    add_parser = commands.add_parser("add", help="add one asset to a new pack copy")
    add_parser.add_argument("pack", type=Path, help="existing HALLEYPK source")
    add_parser.add_argument("asset_type", choices=ASSET_TYPES)
    add_parser.add_argument("asset_name")
    add_parser.add_argument("payload", type=Path)
    add_parser.add_argument("output", type=Path)
    add_parser.add_argument(
        "--metadata-from",
        help="existing asset name whose metadata should be copied",
    )
    add_parser.set_defaults(func=cmd_add)

    pack_parser = commands.add_parser(
        "pack", help="repack all assets into a verified copy"
    )
    pack_parser.add_argument("pack", type=Path, help="existing HALLEYPK source")
    pack_parser.add_argument("output", type=Path)
    pack_parser.set_defaults(func=cmd_pack)

    replace_parser = commands.add_parser(
        "replace", help="replace one existing asset in a new pack copy"
    )
    replace_parser.add_argument("pack", type=Path, help="existing HALLEYPK source")
    replace_parser.add_argument("asset_type", choices=ASSET_TYPES)
    replace_parser.add_argument("asset_name")
    replace_parser.add_argument("payload", type=Path)
    replace_parser.add_argument("output", type=Path)
    replace_parser.set_defaults(func=cmd_replace)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except (FormatError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
