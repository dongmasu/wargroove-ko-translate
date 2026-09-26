# TTF to Halley Font Converter

## Goal

Create a reproducible tool that converts a user-provided TTF or OTF font into
the two Halley UI assets required by Wargroove:

- a `font` payload containing glyph metrics;
- a matching `texture/fontTex` payload containing the rasterized glyph atlas.

The generated assets must be usable through the existing JSON workspace and
`ui.dat` packing workflow. The original source font is never modified.

## Scope

The first version targets Windows Wargroove 2 `ui.dat` and the existing
`Wargroove Medium` asset shape. It will support:

- TrueType and OpenType fonts readable by FreeType;
- an explicit Unicode character set supplied as UTF-8 text or a text file;
- ASCII, common punctuation, and Korean characters selected by the project;
- one grayscale glyph atlas;
- one generated Halley font asset and one generated Halley texture asset;
- JSON output with `_payloadHex` and enough metadata to add or replace assets;
- deterministic output for the same font, size, character set, and options.

The initial version will not attempt to support kerning pairs, complex script
shaping, color fonts, variable-font axes, signed-distance-field rendering, or
automatic replacement of every font in `ui.dat`.

## Architecture

### Font reader and rasterizer

Use FreeType through a small adapter. The adapter loads a face, selects a
Unicode charmap, sets the requested pixel size, loads each requested glyph,
and returns:

- Unicode code point;
- bitmap dimensions and bearing;
- advance values;
- grayscale coverage bitmap.

The tool should prefer a system FreeType installation and report a clear
installation error when it is unavailable. No font binaries are committed to
the repository.

### Atlas builder

Pack glyph bitmaps into a deterministic rectangle atlas. The first version
will use a simple row/skyline strategy with configurable padding and fixed
maximum dimensions. The builder returns each glyph's atlas rectangle and the
final texture dimensions.

The atlas format must be checked against the existing `HLIFv01` payloads in
`ui.dat`. If the format contains compression or palette metadata, the
implementation must preserve the exact header conventions observed in the
reference assets.

### Halley font serializer

Generate the currently observed font payload layout:

- length-prefixed UTF-8 font name;
- length-prefixed `fontTex/<name>` reference;
- font-level metrics and flags;
- glyph count;
- one fixed-size glyph record per Unicode code point;
- fallback font names and trailing flags.

The serializer must be isolated behind a versioned format class. Unknown
header fields remain configurable and are copied from a reference font until
their semantics are confirmed against Halley source or runtime tests.

### Workspace integration

Add a command such as:

```sh
python3 tools/ttf_to_halley.py \
  input.ttf \
  --reference "src/Wargroove 2/1.2.x/ui/font/Wargroove Medium.json" \
  --reference-texture "src/Wargroove 2/1.2.x/ui/texture/fontTex/Wargroove Medium.json" \
  --characters work/Wargroove\ 2/1.2.x/font-characters.txt \
  --output work/docs/analysis/generated-font
```

The output will contain:

```text
font/Wargroove Medium.json
texture/fontTex/Wargroove Medium.json
manifest.json
atlas-preview.png
```

The generated JSON can then be copied into a workspace or passed to a
dedicated replace step. The converter must not silently overwrite existing
files.

## Data Flow

```text
TTF/OTF + character set
  -> FreeType glyph metrics and bitmaps
  -> deterministic atlas packing
  -> Halley font/fontTex payloads
  -> JSON envelopes with _payloadHex
  -> config_workspace.py pack
  -> ui.dat
```

## Validation

Automated tests will cover:

- deterministic glyph ordering and atlas placement;
- empty and unsupported glyph handling;
- font payload serialization and parsing;
- atlas payload round-trip;
- JSON payload export/import;
- generated `ui.dat` entry names and payload sizes;
- refusal to overwrite existing output.

Runtime validation will use a small test character set first, then the Korean
translation character set. The game must start, retain Korean in the language
selection, display Latin and Korean text, and avoid missing-glyph boxes in
menus and dialogue.

## Licensing and Distribution

The converter only reads a user-supplied font. The project will not distribute
commercial fonts or generated font assets without checking their license.
FreeType licensing and any source-font license notices must be documented
when the tool is distributed.

## Risks

- The exact `HLIFv01` pixel encoding may require more reverse engineering than
  the font metric payload.
- The runtime may expect a specific alpha convention, channel order, or texture
  padding.
- Font fallback and UI styles may reference multiple font assets.
- A complete Korean glyph set can exceed the atlas dimensions used by the
  original font and require multiple atlases or font splitting.

The first implementation should therefore use a small, explicit character set
and preserve the existing `Wargroove Medium` dimensions wherever possible.
