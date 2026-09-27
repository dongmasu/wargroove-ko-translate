# HALLEYPK Tool

`halleypk.py` is a parser, extractor, and repacker for Wargroove's
`HALLEYPK`/`HALLEYP2` asset containers, including ModPacker-compatible
AES/CBC payload handling. `halleyconfig.py` converts Halley
`ConfigFile` string payloads between the runtime LZ4/binary form and JSON.
`config_workspace.py` provides the normal translation workflow: unpack a
`config.dat` into readable files, edit the workspace, then pack it back.
Neither tool modifies files under `references/`.

To create a fully unpacked source snapshot, including removal of the
container AES layer and per-asset LZ4/zlib wrappers:

```sh
python3 tools/unpack_source_snapshot.py \
  "references/Wargroove 2/assets/config.dat" \
  /tmp/wargroove2-config-unpacked
```

The output contains raw asset payloads and a manifest that records which
compression wrapper was removed. JSON conversion is a separate analysis step
and does not belong in `src/`.

## Translation workspace workflow

To create the dated DAT files and GitHub-ready ZIP in one step:

```sh
python3 tools/build_dist_package.py
```

The script reads the versioned `work/Wargroove 2/1.2.x/` workspace, uses the
latest modification date of that workspace, and writes:

```text
dist/Wargroove 2/1.2.x/YYYYMMDD/assets/config.dat
dist/Wargroove 2/1.2.x/YYYYMMDD/assets/ui.dat
dist/Wargroove 2/1.2.x/YYYYMMDD/Wargroove2-ko-translate-1.2.x-YYYYMMDD.zip
```

The ZIP contains `INSTALL.md`, `assets/config.dat`, and `assets/ui.dat`.
Existing release files are never overwritten.

For a complete editable workspace, use `config_workspace.py` rather than
calling the lower-level extraction commands separately:

```sh
python3 tools/config_workspace.py unpack \
  "references/Wargroove 2/assets/config.dat" \
  "work/Wargroove 2/1.2.x/config"
```

The workspace contains:

- `configFile/**/*.json`: decoded, readable ConfigFile resources
- other asset types as `/**/*.json`: decoded binary resources with the
  original payload preserved in `_payloadHex`
- `workspace.json`: asset names, metadata, AES IV, container layout, wrapper
  type, and ConfigFile version

For translation work, edit or add Korean files under:

```text
work/Wargroove 2/1.2.x/config/configFile/strings/ko-KR*.json
```

Keep the string keys unchanged and edit the string values. Use the matching
`en-GB`, `ja-JP`, and `zh-Hans` files as references. This workflow does not
require an AI tool or a third-party Python package.

Binary JSON is currently a readable analysis format. Repacking restores the
preserved payload exactly; edits to `_decoded` are not serialized back into
binary until a type-specific encoder is added.

After editing JSON files, create the distributable pack without touching the
source pack:

```sh
python3 tools/config_workspace.py pack \
  "work/Wargroove 2/1.2.x/config" \
  "dist/Wargroove 2/1.2.x/20260926/config.dat"
```

The pack command restores the original container version, AES IV, index
layout, metadata, and per-asset LZ4/zlib/raw wrapper. It refuses to overwrite
an existing output. LZ4 compression may produce different bytes while
preserving the same decoded payload; validation therefore compares decoded
ConfigFile values and decompressed opaque payloads.

The same workflow applies to Wargroove 1:

```sh
python3 tools/config_workspace.py unpack \
  "references/Wargroove/assets/config.dat" \
  "work/Wargroove 1/2.1.x/config"
```

The same workspace format is used for `ui.dat`:

```sh
python3 tools/config_workspace.py unpack \
  "references/Wargroove 2/assets/ui.dat" \
  "src/Wargroove 2/1.2.x/ui"
```

This produces one JSON file per UI asset. `uiDefinition` resources are
decoded as Halley ConfigNode JSON. Fonts, textures, sprites, sprite sheets,
animations, and other binary UI resources retain a readable JSON envelope
with their type information and exact decompressed payload in `_payloadHex`.

Pack a modified UI workspace with the same command:

```sh
python3 tools/config_workspace.py pack \
  "work/Wargroove 2/1.2.x/ui" \
  "dist/Wargroove 2/1.2.x/YYYYMMDD/ui.dat"
```

When replacing a texture payload, update `workspace.json` as well as the
asset JSON. Its `metadata.width`, `metadata.height`, `metadata.format`, and
matching `metadata_raw` must agree with the HLIF header. The packer checks this
automatically and refuses to create a pack with mismatched texture metadata;
otherwise the game may crash during startup.

Regression tests live under `tests/` rather than alongside the implementation:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Requirements

- Python 3.10 or newer
- No third-party packages
- AES acceleration is optional. On macOS Homebrew,
  `/opt/homebrew/lib/libcrypto.dylib` is detected automatically.
- If no supported system crypto library is available, the tool falls back to
  its bundled pure-Python AES-128-CBC implementation.

Run it from the project root:

```sh
python3 tools/halleypk.py --help
```

## Commands

### Decode and encode ConfigFile payloads

NSW Wargroove 2 string resources use Halley's `LZ4` file wrapper around a
`ConfigFile` binary resource:

```sh
python3 tools/halleyconfig.py decode \
  "work/docs/analysis/ko-KR.bin" \
  "work/docs/analysis/decoded-ko-KR.json"

python3 tools/halleyconfig.py encode \
  "work/docs/analysis/decoded-ko-KR.json" \
  "work/docs/analysis/roundtrip-ko-KR.bin"
```

The encoder preserves the ConfigFile v3 structure and writes a valid LZ4
payload. LZ4 compression is not byte deterministic, so verification compares
decoded structure and values rather than raw compressed bytes.

### List an index

Print the parsed AssetDatabase as JSON:

```sh
python3 tools/halleypk.py list \
  "references/Wargroove 2/assets/config.dat"
```

Save the result:

```sh
python3 tools/halleypk.py list \
  "references/Wargroove 2/assets/config.dat" \
  --output work/docs/analysis/wargroove2-config-index.json
```

Filter by asset type or path. The option can be repeated:

```sh
python3 tools/halleypk.py list \
  "references/Wargroove 2/assets/config.dat" \
  --match "strings/"
```

### Extract payloads

Extract matching assets and create an accompanying `manifest.json`:

```sh
python3 tools/halleypk.py extract \
  "references/Wargroove 2/assets/config.dat" \
  work/docs/analysis/extracted/wargroove2-config-strings \
  --match "strings/"
```

Extract UI fonts:

```sh
python3 tools/halleypk.py extract \
  "references/Wargroove 2/assets/ui.dat" \
  work/docs/analysis/extracted/wargroove2-ui-fonts \
  --match "fontTex/"
```

Extract everything by omitting `--match`:

```sh
python3 tools/halleypk.py extract \
  "references/Wargroove 2/assets/config.dat" \
  work/docs/analysis/extracted/wargroove2-config-all
```

Extracted payloads currently use `.bin` because the runtime asset format is
not inferred from the index name. The manifest records the original asset
type, name, offset, size, and metadata.

### Convert JSON payloads

Binary-resource JSON keeps the original decoded payload in `_payloadHex`.
Export it as a raw file without changing the JSON:

```sh
python3 tools/halleypk.py payload export \
  "src/Wargroove 2/1.2.x/ui/font/Wargroove Medium.json" \
  /tmp/wargroove-medium-font.bin
```

After editing or replacing the raw payload, import it into a new JSON file.
The template metadata and `_decoded` section are preserved, while only
`_payloadHex` is replaced:

```sh
python3 tools/halleypk.py payload import \
  "src/Wargroove 2/1.2.x/ui/font/Wargroove Medium.json" \
  /tmp/wargroove-medium-font.bin \
  work/docs/analysis/Wargroove-Medium-replaced.json
```

These commands convert the hexadecimal representation to bytes and back.
They do not convert a Halley font into TTF/OTF or a Halley texture into PNG.

### Convert TTF/OTF to Halley font assets

The complete replacement workflow, including texture metadata synchronization,
the current Noto Serif settings, and release verification, is documented in
[`docs/font-editing-guide.md`](../docs/font-editing-guide.md).

Halley source confirms that fonts are generated from FreeType glyphs and
stored as a serialized `font` asset plus a matching `fontTex` image. The
project converter follows the legacy Wargroove layout:

```sh
python3 -m pip install Pillow
python3 tools/ttf_to_halley.py \
  "/path/to/font.ttf" \
  --reference-font "src/Wargroove 2/1.2.x/ui/font/Wargroove Medium.json" \
  --reference-texture "src/Wargroove 2/1.2.x/ui/texture/fontTex/Wargroove Medium.json" \
  --characters "work/docs/analysis/font-characters.txt" \
  --output "work/docs/analysis/generated-font"
```

The output contains:

```text
font/Wargroove Medium.json
texture/fontTex/Wargroove Medium.json
manifest.json
```

The character file is UTF-8 text. Each distinct non-newline character becomes
a requested glyph. The converter reads the source font's Unicode cmap and
omits unsupported codepoints so Halley can use the font's fallback list instead
of displaying a `.notdef` glyph. Without `--bitmap`, the output is a
single-channel SDF atlas. With
`--bitmap`, the output is an RGBA HLIF bitmap atlas whose RGB channels are
premultiplied by alpha for Halley's default premultiplied-alpha sprite
material. Use `filtering=false` in the matching texture metadata for pixel
fonts.

The current build does not use Galmuri. The final direction replaces only
`Noto Serif` with a Google Noto Serif Korean Regular-derived single-channel
SDF asset; `Sitka Text Bold Italic` and every other UI font remain unchanged.
The historical Galmuri experiments used Galmuri11 at 12px, Galmuri9 at 10px,
and Galmuri7 at 8px as nominal rasterization sizes. Those bitmap packages were
temporary comparisons and are not part of the release.

The default atlas width, padding, and SDF radius are 256 px, 2 px, and 1.5 px;
use the corresponding options to change them. `fontTools` is required in
addition to Pillow for cmap filtering. The command refuses to overwrite
existing output files.

The converter's important rendering options are:

```text
--pixel-size N       TTF rasterization size
--render-scale N     rasterize at N times the target size, then reduce
--atlas-width N      generated atlas width
--padding N          glyph padding in atlas pixels
--sdf-radius N       SDF smoothing radius; default 1.5
--sdf-threshold N    grayscale cutoff for SDF inside/outside; default 1
--antialias off      binary glyph mask; default
--antialias on       preserve grayscale glyph edges
--bitmap-gamma N     sharpen bitmap antialias edges; default 1.0
--bitmap             disable SDF and write an RGBA bitmap atlas
```

`--antialias off` controls antialiasing during TTF-to-pixel conversion. It
does not disable smoothing performed by Halley's SDF material at runtime. For
a genuinely pixel-crisp result, use `--bitmap` and keep the matching texture
metadata's `filtering=false`. With `--antialias on`, values above
`--bitmap-gamma 1.0` darken semi-transparent edge pixels while preserving
connected glyph strokes.

### Decode ConfigFile assets

The `src/` tree remains an immutable source snapshot. Decode all Wargroove 2
`configFile` assets directly from the original pack into a separate readable
analysis tree with:

```sh
python3 tools/decode_config_resources.py
```

The default input is `references/Wargroove 2/assets/config.dat` and the
default output is `work/docs/analysis/wargroove2-config-readable/`. It
contains one JSON file for every `configFile` asset and a `manifest.json`.
The source pack and `src/` files are never modified.

### Decode binary resources

Some non-`configFile` resources also use Halley's binary serializer. Decode
the supported `audioEvent`, `audioObject`, and `gameProperties` assets into a
readable analysis tree with:

```sh
python3 tools/decode_binary_resources.py \
  "references/Wargroove 2/assets/config.dat" \
  work/docs/analysis/wargroove2-binary-readable
```

The tool removes the container encryption and compression through
`halleypk.py`, then writes JSON plus `manifest.json`. It recognizes both the
current Halley serializer and the legacy serializers used by Wargroove 1 and
Wargroove 2 `v1.2.12` build `#45031`. The output is an analysis artifact;
binary source files under `src/` and the round-trip workspace remain
unchanged.

The schemas are based on the open-source Halley engine at
`https://github.com/amzeratul/halley`. The current serializer is not always
byte-compatible with Wargroove's historical build, so the decoder keeps
explicit legacy branches rather than guessing fields.

For a directly unpacked legacy source snapshot, use `--source-dir`:

```sh
python3 tools/decode_config_resources.py \
  --source-dir "src/Wargroove 1/2.1.x/config" \
  --output work/docs/analysis/wargroove1-config-readable
```

### Verify a copy

Create a new byte-identical copy and verify its SHA-256:

```sh
python3 tools/halleypk.py roundtrip \
  "references/Wargroove 2/assets/ui.dat" \
  work/docs/analysis/roundtrip-wargroove2-ui.dat
```

The command refuses to overwrite an existing output. `roundtrip` is not a
real serializer or packer; it only confirms that the source can be parsed and
copied safely.

### Add one asset

Add an asset to a new output file. The source pack and output file are kept
separate:

```sh
python3 tools/halleypk.py add \
  "references/Wargroove 2/assets/config.dat" \
  configFile \
  "strings/ko-KR" \
  work/docs/analysis/wg2-ko-strings.bin \
  work/docs/analysis/wargroove2-config-ko-test.dat
```

By default, metadata is copied from the first asset of the same type. Choose a
specific metadata source when needed:

```sh
python3 tools/halleypk.py add \
  "references/Wargroove 2/assets/config.dat" \
  configFile \
  "strings/ko-KR" \
  work/docs/analysis/wg2-ko-strings.bin \
  work/docs/analysis/wargroove2-config-ko-test.dat \
  --metadata-from "strings/en-GB"
```

The command rejects duplicate asset names, existing output files, and attempts
to overwrite the input. It preserves the source index layout and writes a
`HALLEYPK` v1 output. It reopens the generated pack and verifies the added
payload before returning success.

### Replace one asset

Replace an existing asset in a new output pack:

```sh
python3 tools/halleypk.py replace \
  "references/posts/WG2_KR/romfs/config.dat" \
  configFile \
  "strings/ko-KR" \
  "work/Wargroove 2/1.2.x/config/strings/ko-KR.bin" \
  "work/Wargroove 2/1.2.x/config/tests/nsw-config-batch-001.dat"
```

The command refuses to overwrite the source or an existing output and verifies
the replacement after reopening the generated pack. If the source has a
non-zero IV, the output preserves that IV and encrypts the rebuilt payload
region using the embedded ModPacker-compatible AES key.

### Repack all assets

Create a newly packed copy without adding or removing assets:

```sh
python3 tools/halleypk.py pack \
  "references/Wargroove 2/assets/config.dat" \
  work/docs/analysis/packed-wargroove2-config.dat
```

`pack` preserves the source's legacy/new index and metadata variants, then
reopens the output and compares every asset payload against the source.

### Build the Windows Korean pack

After regenerating the 24 Korean resources, build a new Windows WG2
`config.dat` in one pass:

```sh
python3 tools/build_windows_korean_pack.py
```

The default output is
`dist/Wargroove 2/1.2.x/20260926/config.dat`. The command refuses to overwrite
an existing output, preserves the
Windows source IV, adds `strings/ko-KR*`, and reopens the result to verify all
added payloads.

The Windows smoke-test helper is:

```powershell
.\tools\windows\Test-Wargroove2-KoreanPack.ps1 `
  -GameRoot "C:\Program Files (x86)\Steam\steamapps\common\Wargroove 2"
```

It verifies the final pack hash, creates a backup before copying, and supports
`-Action Restore` afterward. The helper does not launch the game or claim that
the runtime test passed.

Audit all generated resources:

```sh
python3 tools/audit_translation_coverage.py
```

The report is written to
`work/docs/review/translation-coverage-2026-09-26.md`.

## Current Limitations

- Deletion of indexed assets is not implemented.
- `add`, `replace`, and `pack` preserve the source's legacy/new index and
  metadata variants and write `HALLEYPK` v1 output. Encrypted sources retain
  their IV and use AES/CBC/NoPadding for the payload region.
- `halleyconfig.py` currently supports ConfigFile v3 resources with position
  fields and requires host `liblz4`.
- Wargroove 1 Windows ConfigFile resources use an older format that is not yet
  supported by `halleyconfig.py`; the HALLEYPK AES layer is supported.
- The AES fallback is pure Python and can be slow for multi-megabyte packs.
  `libcrypto` is used automatically when available, so no external Python
  encryption package is required.

## Next Packing Work

The next implementation should be staged and validated on copies:

1. Add deletion support and explicit index-diff reporting.
2. Convert confirmed string/font payloads to editable formats.
3. Validate the resulting package before any game installation or overwrite.
