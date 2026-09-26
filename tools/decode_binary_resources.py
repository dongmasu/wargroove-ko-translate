#!/usr/bin/env python3
"""Decode selected Halley binary resources into readable JSON."""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path
from typing import Any

try:
    from tools.halleyconfig import decode_lz4, decode_payload
    from tools.halleypk import HalleyPack
except ModuleNotFoundError:
    from halleyconfig import decode_lz4, decode_payload
    from halleypk import HalleyPack


class DecodeError(ValueError):
    pass


class Reader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def take(self, size: int) -> bytes:
        if size < 0 or self.pos + size > len(self.data):
            raise DecodeError(f"read outside payload at {self.pos}, size {size}")
        result = self.data[self.pos : self.pos + size]
        self.pos += size
        return result

    def u32(self) -> int:
        return struct.unpack("<I", self.take(4))[0]

    def u16(self) -> int:
        return struct.unpack("<H", self.take(2))[0]

    def i32(self) -> int:
        return struct.unpack("<i", self.take(4))[0]

    def f32(self) -> float:
        return struct.unpack("<f", self.take(4))[0]

    def boolean(self) -> bool:
        return bool(self.take(1)[0])

    def string(self) -> str:
        try:
            return self.take(self.u32()).decode("utf-8")
        except UnicodeDecodeError as error:
            raise DecodeError("invalid UTF-8 string") from error

    def fixed_string(self) -> str:
        """Read Halley's version-0 string length used by legacy audio data."""
        return self.string()

    def optional(self, reader: str) -> Any:
        if not self.boolean():
            return None
        return getattr(self, reader)()

    def remaining(self) -> int:
        return len(self.data) - self.pos


def range_float(reader: Reader) -> list[float]:
    return [reader.f32(), reader.f32()]


def fade(reader: Reader) -> dict[str, Any]:
    return {
        "length": reader.f32(),
        "delay": reader.f32(),
        "curve": reader.i32(),
    }


def object_action(reader: Reader) -> dict[str, Any]:
    result = {
        "scope": reader.i32(),
        "object": reader.string(),
        "fade": fade(reader),
    }
    return result


def legacy_object_action(reader: Reader) -> dict[str, Any]:
    """Read the packed-string form used by the old Wargroove audio schema."""
    scope = reader.i32()
    reader.take(2)
    name = reader.take(reader.u16()).decode("utf-8")
    return {
        "scope": scope,
        "object": name,
        "fade": fade(reader),
    }


def decode_audio_event(data: bytes) -> dict[str, Any]:
    reader = Reader(data)
    actions: list[dict[str, Any]] = []
    action_count = reader.u32()
    action_names = {
        "play",
        "playLegacy",
        "stop",
        "pause",
        "resume",
        "stopBus",
        "pauseBus",
        "resumeBus",
        "setBusVolume",
        "setVolume",
        "setSwitch",
        "copySwitch",
        "setVariable",
    }

    def next_action_offset(start: int) -> int:
        candidates: list[int] = []
        for offset in range(start, len(data) - 4):
            length = struct.unpack_from("<I", data, offset)[0]
            if 0 < length < 32 and offset + 4 + length <= len(data):
                try:
                    name = data[offset + 4 : offset + 4 + length].decode("ascii")
                except UnicodeDecodeError:
                    continue
                if name in action_names:
                    candidates.append(offset)
        return min(candidates, default=len(data))

    for _ in range(action_count):
        action_type = reader.string()
        action: dict[str, Any] = {"type": action_type}
        if action_type == "playLegacy":
            # Wargroove 2 retains the pre-AudioObject event serializer. The
            # tail is the embedded legacy object; its clip table is decoded
            # separately once its historical sub-object schema is identified.
            end = next_action_offset(reader.pos)
            legacy = Reader(data[reader.pos:end])
            action["scope"] = legacy.take(1)[0]
            action["legacyFlag"] = legacy.boolean()
            action["group"] = legacy.fixed_string()
            action["gain"] = range_float(legacy)
            action["pitch"] = range_float(legacy)
            action["dopplerScale"] = legacy.f32()
            action["legacyPayloadHex"] = legacy.take(legacy.remaining()).hex()
            reader.pos = end
        elif action_type == "play":
            # Older Wargroove 2 builds serialized the common object action
            # first, then the play parameters. Newer Halley writes the play
            # parameters first. The scope/string pair is unambiguous here.
            legacy_scope = struct.unpack_from("<i", data, reader.pos)[0]
            legacy_name_size = (
                struct.unpack_from("<H", data, reader.pos + 6)[0]
                if reader.remaining() >= 8
                else 0
            )
            is_legacy = (
                legacy_scope in {0, 1, 2}
                and 0 < legacy_name_size < 4096
                and reader.pos + 8 + legacy_name_size <= len(data)
            )
            if is_legacy:
                action.update(legacy_object_action(reader))
                action["gain"] = range_float(reader)
                action["pitch"] = range_float(reader)
                action["delay"] = reader.f32()
                action["legacy"] = True
            else:
                action["singleton"] = reader.boolean()
                action["gain"] = range_float(reader)
                action["pitch"] = range_float(reader)
                action["delay"] = reader.f32()
                action.update(object_action(reader))
        elif action_type in {"stop", "pause"}:
            action.update(object_action(reader))
        elif action_type == "resume":
            action.update(object_action(reader))
            action["force"] = reader.boolean()
        elif action_type in {"stopBus", "pauseBus"}:
            action["scope"] = reader.i32()
            action["bus"] = reader.string()
            action["fade"] = fade(reader)
        elif action_type == "resumeBus":
            action["scope"] = reader.i32()
            action["bus"] = reader.string()
            action["fade"] = fade(reader)
            action["force"] = reader.boolean()
        elif action_type == "setBusVolume":
            action["scope"] = reader.i32()
            action["bus"] = reader.string()
            action["fade"] = fade(reader)
            action["gain"] = reader.f32()
            action["volume"] = reader.string()
        elif action_type == "setVolume":
            action.update(object_action(reader))
            action["gain"] = reader.f32()
        elif action_type == "setSwitch":
            action["scope"] = reader.i32()
            action["switch"] = reader.string()
            action["value"] = reader.string()
        elif action_type == "copySwitch":
            action["scope"] = reader.i32()
            action["destination"] = reader.string()
            action["source"] = reader.string()
        elif action_type == "setVariable":
            action["scope"] = reader.i32()
            action["variable"] = reader.string()
            action["value"] = reader.f32()
        else:
            raise DecodeError(f"unsupported AudioEvent action {action_type!r}")
        actions.append(action)
    if reader.remaining() and data[reader.pos:] not in {b"\0", b"\0\0", b"\0\0\0"}:
        raise DecodeError(f"{reader.remaining()} trailing AudioEvent bytes")
    return {"actions": actions}


def decode_audio_clip(data: bytes) -> dict[str, Any]:
    """Decode Wargroove 1's legacy audioClip metadata resource."""
    reader = Reader(data)
    action_count = reader.u32()
    actions = []
    for _ in range(action_count):
        if reader.string() != "play":
            raise DecodeError("unsupported legacy audioClip action")
        scope = reader.i32()
        clip = reader.string()
        group = reader.string()
        gain = range_float(reader)
        pitch = range_float(reader)

        next_action = len(data)
        for offset in range(reader.pos, len(data) - 8):
            if data[offset : offset + 4] == b"\x04\0\0\0" and data[
                offset + 4 : offset + 8
            ] == b"play":
                next_action = offset
                break
        tail = data[reader.pos : next_action]
        reader.pos = next_action
        actions.append(
            {
                "type": "play",
                "scope": scope,
                "clip": clip,
                "group": group,
                "gain": gain,
                "pitch": pitch,
                "legacyTailHex": tail.hex(),
                "legacyTailFloats": [
                    struct.unpack("<f", tail[index : index + 4])[0]
                    for index in range(0, len(tail) - 3, 4)
                ],
            }
        )
    if reader.remaining():
        raise DecodeError(f"{reader.remaining()} trailing audioClip bytes")
    return {"legacy": True, "actions": actions}


SUB_OBJECT_TYPES = ("none", "clips", "layers", "switch", "sequence")


def decode_sub_object(reader: Reader) -> dict[str, Any] | None:
    type_id = reader.i32()
    if not 0 <= type_id < len(SUB_OBJECT_TYPES):
        raise DecodeError(f"unknown AudioSubObject type {type_id}")
    if type_id == 0:
        return None
    result: dict[str, Any] = {"type": SUB_OBJECT_TYPES[type_id], "id": reader.string()}
    if type_id == 1:
        result.update(
            {
                "clips": [reader.string() for _ in range(reader.u32())],
                "loop": reader.boolean(),
                "randomiseStart": reader.boolean(),
                "gain": range_float(reader),
                "loopStart": reader.i32(),
                "loopEnd": reader.i32(),
            }
        )
    else:
        # These types are uncommon in the Wargroove 2 object table. Keep the
        # common identity and stop with an explicit unsupported marker.
        result["decode_note"] = "nested Halley audio sub-object not implemented"
        raise DecodeError(f"AudioSubObject type {SUB_OBJECT_TYPES[type_id]} needs nested decoding")
    return result


def decode_audio_object(data: bytes) -> dict[str, Any]:
    reader = Reader(data)
    # Wargroove 2.1-era AudioObject omitted Halley's serialization version
    # and stored the legacy object table directly after dopplerScale.
    first = struct.unpack_from("<i", data, 0)[0] if len(data) >= 4 else -1
    if first != 1 and data[:4] != b"\x01\x00\x00\x00":
        return decode_legacy_audio_object(data)
    result: dict[str, Any] = {
        "serializationVersion": reader.i32(),
        "bus": reader.string(),
        "pitch": range_float(reader),
        "gain": range_float(reader),
        "dopplerScale": reader.f32(),
        "objects": [],
    }
    result["objects"] = [
        decode_sub_object(reader) for _ in range(reader.u32())
    ]
    result["attenuationOverride"] = (
        {
            "referenceDistance": reader.f32(),
            "maximumDistance": reader.f32(),
            "rollOffFactor": reader.f32(),
            "curve": reader.i32(),
        }
        if reader.boolean()
        else None
    )
    result["pruneDistant"] = reader.boolean()
    result["cooldown"] = reader.optional("f32")
    result["maxInstances"] = reader.optional("i32")
    result["limitType"] = reader.i32()
    result["priority"] = reader.i32()
    result["minStereoWidth"] = reader.optional("f32")
    result["maxStereoWidth"] = reader.optional("f32")
    if reader.remaining():
        raise DecodeError(f"{reader.remaining()} trailing AudioObject bytes")
    return result


def decode_legacy_audio_object(data: bytes) -> dict[str, Any]:
    reader = Reader(data)
    result: dict[str, Any] = {
        "legacy": True,
        "bus": reader.string(),
        "pitch": range_float(reader),
        "gain": range_float(reader),
        "dopplerScale": reader.f32(),
        "objects": [],
    }
    object_count = reader.u32()
    result["objectCount"] = object_count
    # The legacy object graph is still useful for inspection even when a
    # nested historical sub-object cannot be fully decoded.
    for _ in range(object_count):
        start = reader.pos
        try:
            result["objects"].append(decode_sub_object(reader))
        except DecodeError:
            reader.pos = start
            result["objects"].append(
                {
                    "decoded": False,
                    "payloadHex": reader.take(reader.remaining()).hex(),
                }
            )
            break
    if reader.remaining():
        result["trailingBytes"] = reader.take(reader.remaining()).hex()
    return result


def decode_audio_properties(reader: Reader) -> dict[str, Any]:
    switches = []
    for _ in range(reader.u32()):
        switches.append(
            {
                "id": reader.string(),
                "defaultValue": reader.string(),
                "values": [reader.string() for _ in range(reader.u32())],
            }
        )
    variables = []
    for _ in range(reader.u32()):
        variables.append(
            {
                "id": reader.string(),
                "defaultValue": reader.f32(),
                "range": range_float(reader),
                "nHorizontalDividers": reader.i32(),
            }
        )

    def bus() -> dict[str, Any]:
        return {
            "id": reader.string(),
            "children": [bus() for _ in range(reader.u32())],
        }

    return {
        "switches": switches,
        "variables": variables,
        "buses": [bus() for _ in range(reader.u32())],
    }


def decode_game_properties(data: bytes) -> dict[str, Any]:
    raw = decode_lz4(data) if data[:4] == b"LZ4\0" else data
    if not raw:
        return {}
    if len(raw) == 12 and raw == b"\0" * 12:
        return {
            "audioProperties": {"switches": [], "variables": [], "buses": []},
            "materialTags": [],
        }
    reader = Reader(raw)
    try:
        result = {
            "audioProperties": decode_audio_properties(reader),
            "materialTags": [reader.string() for _ in range(reader.u32())],
        }
    except DecodeError:
        # Wargroove 2.1 uses the pre-material-tag serializer:
        # switches, variables, then buses. Switches omit defaultValue and
        # variables are absent in the shipped game properties resource.
        reader = Reader(raw)
        switches = []
        for _ in range(reader.u32()):
            switch_id = reader.string()
            switches.append(
                {
                    "id": switch_id,
                    "defaultValue": "",
                    "values": [reader.string() for _ in range(reader.u32())],
                }
            )
        variables = []
        for _ in range(reader.u32()):
            variables.append(
                {
                    "id": reader.string(),
                    "defaultValue": reader.f32(),
                    "range": range_float(reader),
                    "nHorizontalDividers": reader.i32(),
                }
            )

        def legacy_bus() -> dict[str, Any]:
            return {
                "id": reader.string(),
                "children": [legacy_bus() for _ in range(reader.u32())],
            }

        result = {
            "legacy": True,
            "audioProperties": {
                "switches": switches,
                "variables": variables,
                "buses": [legacy_bus() for _ in range(reader.u32())],
            },
        }
    if reader.remaining():
        raise DecodeError(f"{reader.remaining()} trailing GameProperties bytes")
    return result


def decode_ui_definition(data: bytes) -> dict[str, Any]:
    """Decode Halley's LZ4-wrapped UI ConfigNode resource."""
    return decode_payload(data)


DECODERS = {
    "audioClip": decode_audio_clip,
    "audioEvent": decode_audio_event,
    "audioObject": decode_audio_object,
    "gameProperties": decode_game_properties,
    "uiDefinition": decode_ui_definition,
}


def decode_opaque_structured(asset_type: str, data: bytes) -> dict[str, Any]:
    """Return a readable fallback when a historical schema is unavailable."""
    strings: list[str] = []
    reader = Reader(data)
    while reader.remaining() >= 4:
        start = reader.pos
        try:
            value = reader.string()
        except DecodeError:
            reader.pos = start + 1
            continue
        if value and all(ord(char) >= 32 for char in value):
            strings.append(value)
    return {
        "assetType": asset_type,
        "decoded": False,
        "decodeNote": "Historical serializer schema is not implemented.",
        "size": len(data),
        "strings": strings,
        "payloadHex": data.hex(),
    }


def decode_pack(pack_path: Path, output: Path, asset_types: set[str]) -> dict[str, Any]:
    pack = HalleyPack(pack_path)
    files = []
    for entry in pack.entries:
        if entry.asset_type_name not in asset_types:
            continue
        decoder = DECODERS.get(entry.asset_type_name)
        if decoder is None:
            continue
        try:
            decoded = decoder(pack.payload(entry))
        except DecodeError as error:
            decoded = decode_opaque_structured(entry.asset_type_name, pack.payload(entry))
            decoded["decodeError"] = str(error)
            status = "fallback"
        else:
            status = "decoded"
        destination = output / entry.asset_type_name / Path(entry.name).with_suffix(".json")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(decoded, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        files.append(
            {
                "asset": entry.name,
                "asset_type": entry.asset_type_name,
                "output": str(destination.relative_to(output)),
                "status": status,
            }
        )
    manifest = {"source": str(pack_path), "output": str(output), "files": files}
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--type",
        dest="asset_types",
        action="append",
        choices=sorted(DECODERS),
        default=sorted(DECODERS),
    )
    args = parser.parse_args()
    try:
        manifest = decode_pack(args.pack, args.output, set(args.asset_types))
    except (OSError, DecodeError) as error:
        print(f"error: {error}")
        return 2
    print(
        f"Decoded {sum(item['status'] in {'decoded', 'fallback'} for item in manifest['files'])} "
        f"binary resources to {manifest['output']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
