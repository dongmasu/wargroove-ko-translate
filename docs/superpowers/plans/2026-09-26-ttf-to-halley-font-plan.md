# TTF to Halley Font Converter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic converter that turns a user-provided TTF/OTF and an explicit character set into Halley `font` and `fontTex` JSON assets that can be packed into Wargroove 2 `ui.dat`.

**Architecture:** Keep the converter separate from `halleypk.py` and `config_workspace.py`. A FreeType adapter produces glyph metrics and grayscale bitmaps, an atlas builder places them deterministically, and versioned serializers produce Halley payloads using reference assets for unknown fields. JSON envelopes are written only to a new output directory.

**Tech Stack:** Python 3.11+, `ctypes` FreeType adapter, standard-library JSON/struct/zlib/hashlib, existing Halley pack/workspace modules, unittest.

**Spec:** `docs/superpowers/specs/2026-09-26-ttf-to-halley-font-design.md`

## Global Constraints

- Do not modify files under `references/`.
- Do not overwrite existing output files.
- Do not commit font binaries supplied by users.
- Preserve the existing JSON `_payloadHex` workspace format.
- Keep the first implementation limited to one grayscale atlas and explicit glyph selection.
- Generated output must be deterministic for identical inputs and options.

---

### Task 1: Establish Halley reference fixtures and format probes

**Files:**
- Create: `tests/fixtures/font_format.py`
- Modify: `tests/test_halley_pk.py`
- Modify: `docs/ui-dat-analysis.md`

**Interfaces:**
- Produces `load_payload_json(path: Path) -> bytes` for fixture tests.
- Produces `parse_reference_font_payload(payload: bytes) -> dict[str, Any]` with the verified header, glyph count, record size, and fallback names.

- [ ] **Step 1: Write the failing parser test**

```python
def test_parses_wargroove_medium_reference_layout():
    payload = load_payload_json(
        Path("src/Wargroove 2/1.2.x/ui/font/Wargroove Medium.json")
    )
    parsed = parse_reference_font_payload(payload)
    assert parsed["name"] == "Wargroove Medium"
    assert parsed["texture"] == "fontTex/Wargroove Medium"
    assert parsed["glyph_count"] == 534
    assert parsed["record_size"] == 52
    assert parsed["fallbacks"] == ["PixelMPlus", "Zpix", "AaCassiopeiaL1"]
```

- [ ] **Step 2: Run the focused test and confirm it fails**

Run: `python3 -m unittest tests.test_halley_pk -v`

Expected: FAIL because the parser fixture helper does not exist.

- [ ] **Step 3: Implement the minimal reference parser**

Read little-endian length-prefixed UTF-8 strings, retain the unknown header
bytes, read the glyph count at offset `0x4d`, skip `glyph_count * 52` bytes,
then read the fallback string list and trailing flag. Reject truncated input
with `FormatError`.

- [ ] **Step 4: Run focused and full tests**

Run: `python3 -m unittest tests.test_halley_pk -v`

Expected: PASS.

Run: `python3 -m unittest discover -s tests -v`

Expected: all existing tests and the new parser test PASS.

- [ ] **Step 5: Document the verified parser boundary**

Update `docs/ui-dat-analysis.md` to distinguish confirmed offsets from fields
that remain copied from a reference asset.

- [ ] **Step 6: Commit**

```bash
git add tests/fixtures/font_format.py tests/test_halley_pk.py docs/ui-dat-analysis.md
git commit -m "Add Halley font format reference parser"
```

### Task 2: Add FreeType glyph loading

**Files:**
- Create: `tools/freetype_adapter.py`
- Create: `tests/test_freetype_adapter.py`
- Modify: `tools/README.md`

**Interfaces:**
- `GlyphBitmap`: dataclass with `codepoint`, `width`, `height`, `bearing_x`, `bearing_y`, `advance_x`, and grayscale `pixels`.
- `FreeTypeFace(font_path: Path, pixel_size: int)`: context-managed loader.
- `FreeTypeFace.load_glyph(codepoint: int) -> GlyphBitmap`.
- `FreeTypeUnavailableError`: actionable error with installation guidance.

- [ ] **Step 1: Write tests for missing library and glyph properties**

Use a test font path supplied by `HALLEY_TEST_FONT`, skip the rasterization
test when it is unset, and always test that an invalid library/path produces a
clear project exception rather than a raw `ctypes` traceback.

- [ ] **Step 2: Run the focused tests**

Run: `python3 -m unittest tests.test_freetype_adapter -v`

Expected: missing-dependency test PASS; rasterization test skipped unless a
system test font is configured.

- [ ] **Step 3: Implement the ctypes adapter**

Load `libfreetype` candidates by platform, bind only the required FreeType
functions, select the Unicode charmap, set pixel size, load/render a glyph,
copy the bitmap buffer immediately, and close the face/library resources.
Support negative pitch by copying rows in display order.

- [ ] **Step 4: Run tests with a local system font**

Find a readable system TTF without copying it into the repository, then run:

```sh
HALLEY_TEST_FONT="/path/to/system-font.ttf" \
python3 -m unittest tests.test_freetype_adapter -v
```

Expected: glyph `A` has non-empty pixels and a positive advance.

- [ ] **Step 5: Document runtime dependency**

Document how to locate FreeType on macOS and Windows, and state that user
fonts are input-only and are not distributed by this project.

- [ ] **Step 6: Commit**

```bash
git add tools/freetype_adapter.py tests/test_freetype_adapter.py tools/README.md
git commit -m "Add FreeType glyph loading adapter"
```

### Task 3: Implement deterministic atlas packing

**Files:**
- Create: `tools/halley_atlas.py`
- Create: `tests/test_halley_atlas.py`

**Interfaces:**
- `AtlasOptions`: dataclass with `width`, `height`, `padding`, and `background`.
- `AtlasGlyph`: dataclass with `codepoint`, `x`, `y`, `width`, `height`.
- `pack_glyphs(glyphs: Sequence[GlyphBitmap], options: AtlasOptions) -> AtlasResult`.
- `AtlasResult`: texture dimensions, grayscale pixels, and ordered placements.

- [ ] **Step 1: Write failing deterministic packing tests**

Test that glyphs are ordered by codepoint, repeated inputs produce identical
pixels and placements, padding is respected, and an atlas overflow raises a
specific `AtlasOverflowError`.

- [ ] **Step 2: Run the focused tests**

Run: `python3 -m unittest tests.test_halley_atlas -v`

Expected: FAIL before implementation.

- [ ] **Step 3: Implement row-based packing**

Sort by codepoint, place glyphs left-to-right with padding, wrap rows at the
configured width, reject height overflow, and copy grayscale pixels into a
zero-filled atlas buffer.

- [ ] **Step 4: Run focused tests**

Expected: all atlas tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/halley_atlas.py tests/test_halley_atlas.py
git commit -m "Add deterministic glyph atlas packing"
```

### Task 4: Serialize Halley font metrics and HLIF texture payloads

**Files:**
- Create: `tools/halley_font.py`
- Create: `tests/test_halley_font.py`
- Modify: `docs/ui-dat-analysis.md`

**Interfaces:**
- `ReferenceFont`: parsed reference payload and reference texture metadata.
- `build_font_payload(reference: ReferenceFont, glyphs: Sequence[PlacedGlyph], options: FontBuildOptions) -> bytes`.
- `build_texture_payload(atlas: AtlasResult, reference_texture: bytes) -> bytes`.
- `write_font_json(output: Path, asset_name: str, payload: bytes, decoded: dict) -> None`.

- [ ] **Step 1: Write failing serializer tests**

Use a small synthetic glyph set and assert:

```python
font_payload = build_font_payload(reference, glyphs, options)
parsed = parse_reference_font_payload(font_payload)
assert parsed["glyph_count"] == len(glyphs)
assert parsed["codepoints"] == sorted(codepoints)
```

Also assert that the texture serializer emits the expected `HLIFv01` header
and rejects unsupported channel/pixel modes.

- [ ] **Step 2: Run focused tests**

Run: `python3 -m unittest tests.test_halley_font -v`

Expected: FAIL before implementation.

- [ ] **Step 3: Implement font serialization**

Copy reference header values and fallback names, replace the font and texture
names, write one 52-byte glyph record per selected codepoint, and encode
metrics using the reference coordinate conventions. Keep the serializer
versioned and reject glyph metrics that cannot fit the observed record.

- [ ] **Step 4: Implement HLIF texture serialization**

First decode the reference texture header and pixel encoding from
`fontTex/Wargroove Medium.json`. Encode the atlas using the same dimensions,
channel order, compression marker, and terminator conventions. If the
reference format cannot represent the requested atlas, fail with a diagnostic
instead of producing a guessed payload.

- [ ] **Step 5: Run payload round-trip tests**

Export the generated payloads with `halleypk.py payload export`, import them
again, and assert byte equality. Run the full test suite.

- [ ] **Step 6: Document confirmed HLIF fields**

Record only fields verified by round-trip or reference comparison. Mark
unconfirmed fields as unsupported rather than describing guesses as facts.

- [ ] **Step 7: Commit**

```bash
git add tools/halley_font.py tests/test_halley_font.py docs/ui-dat-analysis.md
git commit -m "Serialize Halley font and texture payloads"
```

### Task 5: Add the user-facing TTF conversion command

**Files:**
- Create: `tools/ttf_to_halley.py`
- Create: `tests/test_ttf_to_halley.py`
- Modify: `tools/README.md`

**Interfaces:**
- `load_character_set(path: Path | None, inline: str | None) -> list[int]`.
- `convert_font(args: argparse.Namespace) -> dict[str, Any]`.
- CLI command:

```sh
python3 tools/ttf_to_halley.py FONT.ttf \
  --reference-font REFERENCE_FONT.json \
  --reference-texture REFERENCE_TEXTURE.json \
  --characters CHARACTERS.txt \
  --output OUTPUT_DIR
```

- [ ] **Step 1: Write command validation tests**

Test missing character source, duplicate codepoints, unsupported glyphs,
existing output directory, and successful manifest generation with a configured
system font.

- [ ] **Step 2: Run focused tests**

Run: `python3 -m unittest tests.test_ttf_to_halley -v`

Expected: validation tests fail until the command exists.

- [ ] **Step 3: Implement character-set loading**

Read UTF-8 text, deduplicate by codepoint, sort deterministically, and include
newline-free characters only. Report missing glyphs by codepoint and name.

- [ ] **Step 4: Implement conversion pipeline**

Load reference assets, rasterize requested glyphs, pack the atlas, serialize
both Halley payloads, write JSON envelopes and a manifest, and refuse to
overwrite any existing output file.

- [ ] **Step 5: Add optional atlas preview**

Write a PNG only when Pillow is available; otherwise write a clear note in the
manifest and continue because the preview is diagnostic, not runtime data.

- [ ] **Step 6: Run command tests and full tests**

Expected: all converter tests and the existing test suite PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/ttf_to_halley.py tests/test_ttf_to_halley.py tools/README.md
git commit -m "Add TTF to Halley conversion command"
```

### Task 6: Build and validate a Wargroove 2 test asset

**Files:**
- Create: `work/docs/analysis/font-conversion-test/characters.txt`
- Create: `work/docs/analysis/font-conversion-test/README.md`
- Modify: `docs/translation-process.md`
- Modify: `docs/ui-dat-analysis.md`

**Interfaces:**
- Uses the CLI from Task 5 and the existing `config_workspace.py pack`.
- Produces a disposable test `ui.dat` under `work/docs/analysis/`, never under
  `dist/` until runtime validation succeeds.

- [ ] **Step 1: Generate a minimal Latin/Korean test set**

Include ASCII, punctuation, and the Korean characters from the current
translation resources, deduplicated and sorted.

- [ ] **Step 2: Run conversion with a user-provided font**

Run the documented command with the user’s TTF/OTF and the reference
`Wargroove Medium` assets.

- [ ] **Step 3: Pack a temporary ui.dat**

Use `config_workspace.py pack` with a copied temporary workspace containing
the generated font and texture JSON. Do not overwrite `src`, `work` source
translation files, or any existing distribution artifact.

- [ ] **Step 4: Verify static invariants**

Check asset names, payload sizes, JSON import/export round-trip, and
`HalleyPack` readability before asking for game runtime testing.

- [ ] **Step 5: Document the result**

Record the tested font, character-set size, atlas dimensions, platform, and
whether the game rendered Korean without missing-glyph boxes.

- [ ] **Step 6: Commit documentation and fixtures**

```bash
git add docs/translation-process.md docs/ui-dat-analysis.md \
  work/docs/analysis/font-conversion-test
git commit -m "Document Halley font conversion validation"
```
