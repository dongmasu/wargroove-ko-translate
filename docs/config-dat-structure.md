# Wargroove `config.dat` Structure

Date: 2026-09-26

This document records the structure observed in Windows Wargroove 2
`v1.2.12`, build `#45031`, and the project workflow for converting
`config.dat` into an editable translation workspace and rebuilding it.

## Source Snapshots

Both source snapshots are generated directly from their corresponding
`references/*/assets/config.dat` files with `config_workspace.py`.

| Target | Pack entries | `configFile` | Other extracted assets |
| --- | ---: | ---: | ---: |
| Wargroove 1 | 2,228 | 371 | 1,857 `audioClip` |
| Wargroove 2 | 3,514 | 375 | 3,139 other assets |

The translation workspace contains readable JSON for every asset. Container
AES and per-asset LZ4/zlib wrappers are removed before editing and restored
during packing. Wargroove 2 uses ConfigFile v3/LZ4, while Wargroove 1 uses an
older version 2/zlib format. Binary asset JSON also preserves the exact
decrypted payload in `_payloadHex` so the packer can rebuild it safely.

The intended workflow is:

```text
references/*/assets/config.dat
        | config_workspace.py unpack
        v
work/*/config/             <- edit only this tree
        | config_workspace.py pack
        v
dist/*/yyyymmdd/config.dat
```

`src/` is the immutable readable baseline generated from the original pack;
`work/` is the editable copy used for translation.

All source assets now use `.json`. ConfigFile JSON is editable and packable;
binary-resource JSON is readable and preserves `_payloadHex` for exact
round-trip packing.

## Container Layout

```text
HALLEYPK
  Header
  zlib-compressed AssetDatabase index
  AES-CBC encrypted payload region
```

### Header

The Windows Wargroove 2 file uses `HALLEYPK` v1:

| Field | Size | Description |
| --- | ---: | --- |
| Magic | 8 bytes | `HALLEYPK` |
| IV | 16 bytes | Non-zero AES IV |
| AssetDatabase start | 8 bytes | Usually `40` |
| Payload start | 8 bytes | End of the compressed index |

For the current Windows WG2 source:

```text
IV: 6b224f8788bf85934e50c9a7fffd6614
AssetDatabase start: 40
Payload start: 45334
Indexed assets: 3514
```

### AssetDatabase Index

The index is zlib-compressed. Its entries contain:

```text
asset type
logical asset name
offset:size
metadata
```

The `offset:size` values point into the decrypted logical payload region.
Offsets are aligned to 16 bytes. The complete payload region is also padded to
a 16-byte boundary for AES-CBC with no padding.

Example metadata for a string resource:

```json
{
  "asset_type": 2,
  "asset_type_name": "configFile",
  "name": "strings/en-GB",
  "metadata": {
    "asset_compression": "lz4"
  }
}
```

### Payload Region

The payload region is encrypted with the ModPacker-compatible algorithm:

```text
AES-128-CBC
NoPadding
IV = header IV
```

After decryption, each string resource is an LZ4-wrapped Halley `ConfigFile`
resource. The decoded root contains a language map such as:

```json
{
  "ko-KR": {
    "some_string_key": "한국어 문자열"
  }
}
```

The project tool uses `libcrypto` when available and has a pure-Python fallback.

## Binary Resource Decoding

`configFile` resources use the generic Halley `ConfigNode` serializer. Other
resource types use class-specific serializers and must not be decoded with
the ConfigFile reader.

The project currently decodes all binary resources in the Windows Wargroove 2
`v1.2.12` build `#45031` pack:

| Asset type | Count | Result |
| --- | ---: | --- |
| `audioEvent` | 3,135 | JSON, including legacy `play` actions |
| `audioObject` | 1 | JSON, legacy object header recognized |
| `gameProperties` | 2 | JSON, including legacy audio properties |
| Other binary types | 1 | Preserved as decompressed `.bin` |

Run:

```sh
python3 tools/decode_binary_resources.py \
  "references/Wargroove 2/assets/config.dat" \
  work/docs/analysis/wargroove2-binary-readable
```

The implementation was cross-checked against the open-source Halley
serializer sources at `https://github.com/amzeratul/halley`. Wargroove's
historical serializer differs from the current engine in several places:
legacy audio events store the object action before play parameters, and
legacy game properties omit the newer material-tag section. These are handled
as explicit version branches. The decoder is for readable analysis; the
workspace packer continues to preserve opaque binary payloads.

Wargroove 1 contains 1,857 `audioClip` resources. These are not encoded
Vorbis samples in this pack; they are legacy playback metadata. The decoder
extracts the clip path, group, gain/pitch ranges, and preserves remaining
version-specific fields as hexadecimal bytes and 32-bit float candidates.

## Windows WG2 String Resources

The Windows pack contains 375 `configFile` payloads. Of these, 214 are
`strings/*.bin` resources and the remainder cover game configuration groups
such as stages, messages, achievements, art, and UI styles.

The current `src/Wargroove 2/1.2.x/config/` snapshot contains only 214
encrypted string payloads from an earlier extraction. They do not begin with
the Halley `LZ4` header and are not readable ConfigFile data. This snapshot is
kept unchanged until it can be replaced with a verified full extraction.

For a translation workspace, unpack the original pack into:

```text
work/Wargroove 2/1.2.x/config/
```

using:

```sh
python3 tools/config_workspace.py unpack \
  "references/Wargroove 2/assets/config.dat" \
  "work/Wargroove 2/1.2.x/config"
```

The generated directory contains 375 JSON files plus a manifest. Koreanization
adds the
corresponding 24 resources with the same suffixes:

```text
strings/ko-KR
strings/ko-KR_NPCs
strings/ko-KR_birds
strings/ko-KR_campaign_air
strings/ko-KR_campaign_earth
strings/ko-KR_campaign_final
strings/ko-KR_campaign_sea
strings/ko-KR_campaign_tutorial
strings/ko-KR_codex
strings/ko-KR_codex_commanders
strings/ko-KR_codex_lore_wg2
strings/ko-KR_codex_units
strings/ko-KR_conquest
strings/ko-KR_dev
strings/ko-KR_gallery
strings/ko-KR_grooves
strings/ko-KR_new_VO_lines
strings/ko-KR_secret
strings/ko-KR_structures
strings/ko-KR_ui
strings/ko-KR_ui_cutscene
strings/ko-KR_wargroove2
strings/ko-KR_wargroove2_dev
strings/ko-KR_zz_append
```

The Korean resource payloads are generated from the NSW `ko-KR` resources,
with Wargroove 1 terminology and the approved terminology review decisions
applied.

## Files To Add or Modify

### Rebuilding `config.dat`

Do not modify the installed source file in place. Pack a new copy from the
workspace:

```sh
python3 tools/config_workspace.py pack \
  "work/Wargroove 2/1.2.x/config" \
  "dist/Wargroove 2/1.2.x/20260926/config.dat"
```

The packer keeps all assets in the workspace, preserves their asset names and
metadata, restores the original container/AES settings, and verifies the
rebuilt pack can be reopened. ConfigFile JSON changes are encoded back to the
original ConfigFile version and compression wrapper.

```text
dist/Wargroove 2/1.2.x/20260926/config.dat
```

It contains 3,538 assets. The final output SHA-256 is:

```text
746b17b14cb52dcbd3d9e94ca33d8400e2bae6555d564b66a40a6661a456bbc6
```

The pack was reopened on macOS, all 24 added payloads were verified, and
sample campaign-air strings were decoded from the encrypted output. The
earlier experimental pack was tested in Windows with Korean text rendering
successfully; the final pack still requires a separate Windows smoke test.

### `ui.dat`

`ui.dat` is analyzed separately in
`docs/ui-dat-analysis.md`. It is not required for the current Korean
text test because the existing Windows font rendered the Korean strings
successfully. Only investigate and add a font asset from `ui.dat` if later
testing finds missing glyphs, boxes, fallback fonts, clipping, or unreadable
characters.

## Current Validation

Completed for the generated final pack on macOS:

- AES decrypt/repack of the original `config.dat`;
- addition of 24 Korean string resources;
- reopening and decoding `strings/ko-KR`;
- verification of all 3,538 indexed assets;
- decoding of sample campaign-air strings from the encrypted output.

The earlier experimental pack rendered Korean text successfully on Windows
WG2 `v1.2.12`, build `#45031`. The generated final pack has completed
structural and payload verification, but the final release gate is testing
this exact hash in Windows, including menu, campaign dialogue, codex, UI
clipping, language selection, and font rendering.
