# Wargroove 2 Font Editing Guide

This guide describes how to replace a Wargroove 2 Windows font safely, from
a TTF/OTF source to a modified `ui.dat`.

## Core Rules

Wargroove does not store fonts as standalone TTF, OTF, or WOFF files. Each
font is represented by two Halley assets:

```text
ui/font/<name>.json
ui/texture/fontTex/<name>.json
```

The first asset stores the font name, metrics, glyph records, UV coordinates,
fallback names, and the `fontTex/<name>` reference. The second stores the
glyph atlas as an `HLIFv01` texture payload. Both assets must be replaced
together. A raw TTF cannot be copied into `ui.dat`.

The texture has three synchronized representations:

1. `ui/font/<name>.json` stores the atlas `image_size`.
2. `ui/texture/fontTex/<name>.json` stores the actual HLIF width and height.
3. `ui/workspace.json` stores indexed texture metadata and `metadata_raw`.

If the atlas dimensions or format change, update all three. The workspace
packer rejects mismatches because an inconsistent texture can make the game
crash during startup.

## Recommended Workflow

1. Keep the original Windows WG2 `ui.dat` as the base.
2. Choose the target font and matching `fontTex` asset.
3. Prepare an explicit character list.
4. Convert the TTF/OTF with `tools/ttf_to_halley.py`.
5. Generate into a disposable analysis directory first.
6. Inspect metrics, glyph count, and atlas dimensions.
7. Copy the two generated JSON assets into the UI workspace.
8. Update `ui/workspace.json` for the new texture dimensions and format.
9. Pack a new `ui.dat`; never modify the original in place.
10. Reopen the generated pack and verify the target assets.
11. Test the exact `ui.dat` in Windows before release.

## Conversion Command

```sh
python3 tools/ttf_to_halley.py \
  "path/to/font.ttf" \
  --reference-font "src/Wargroove 2/1.2.x/ui/font/Wargroove Medium.json" \
  --reference-texture "src/Wargroove 2/1.2.x/ui/texture/fontTex/Wargroove Medium.json" \
  --characters "work/docs/analysis/font-characters.txt" \
  --output "work/docs/analysis/generated-font"
```

The output contains:

```text
font/<name>.json
texture/fontTex/<name>.json
manifest.json
```

The converter reads the source font's Unicode cmap and omits unsupported
codepoints. This preserves the fallback chain instead of inserting a `.notdef`
glyph for unsupported characters.

## Important Options

```text
--pixel-size N       TTF rasterization size
--render-scale N     supersampling scale before reduction
--atlas-width N      atlas width in pixels
--padding N          gap between glyphs in the atlas
--sdf-radius N       SDF smoothing radius
--sdf-threshold N    mask threshold used for SDF generation
--antialias on|off   grayscale antialiasing during rasterization
--bitmap             write an RGBA bitmap atlas instead of an SDF atlas
```

The original Wargroove font assets are single-channel SDF assets. Unless
there is a specific reason to use bitmap output, preserve that format and do
not pass `--bitmap`.

## Current Noto Serif Configuration

The current Windows release keeps the original UI and replaces only:

```text
font/Noto Serif
texture/fontTex/Noto Serif
```

`Sitka Text Bold Italic` and every other UI font remain unchanged. The
original Noto Serif contains only 51 Hangul syllables, so the direct
`Sitka Text Bold Italic -> Noto Serif` fallback can show missing glyphs in
skill and groove-effect text.

The approved source is Google Noto Serif Korean Regular:

```text
Google Fonts:
https://fonts.google.com/noto/specimen/Noto+Serif+KR?preview.script=Kore&preview.lang=ko_Kore
```

```sh
.venv-font/bin/python tools/ttf_to_halley.py \
  "references/fonts/Noto_Serif_KR/static/NotoSerifKR-Regular.ttf" \
  --reference-font "src/Wargroove 2/1.2.x/ui/font/Noto Serif.json" \
  --reference-texture "src/Wargroove 2/1.2.x/ui/texture/fontTex/Noto Serif.json" \
  --characters "work/docs/analysis/font-sets/20260927/sitka-characters.txt" \
  --output "/private/tmp/noto-serif-kr-generated" \
  --pixel-size 42 \
  --render-scale 1 \
  --atlas-width 4096 \
  --padding 2 \
  --sdf-radius 4 \
  --sdf-threshold 1 \
  --antialias on
```

Effective output:

```text
glyphs:          4,804
font size_pt:    42.0
atlas:           4096 x 2387
texture format:  single_channel
distance_field:  true
```

The NSW `Noto Serif` asset is reference material only. Its texture uses the
Switch-specific BNTX format and is not directly usable in Windows `ui.dat`.
A converter could make it usable, but conversion is deferred while Google
Noto Serif Korean provides broader coverage without a known problem.

## License and Attribution

The source font is Noto Serif Korean by Google. The downloaded source files
include:

```text
references/fonts/Noto_Serif_KR/OFL.txt
references/fonts/Noto_Serif_KR/README.txt
```

The font is Copyright 2012 Google Inc. and is licensed under the SIL Open Font
License, Version 1.1:

```text
https://openfontlicense.org
```

The OFL permits the font to be used, studied, modified, embedded, bundled,
and redistributed, including as part of software that is sold. The font
software itself must not be sold by itself, and the original or modified font
software must remain under the OFL. Any reserved font names must not be used
for a modified version. The full license text in `OFL.txt` is authoritative.

This project converts the Regular source into a Halley font asset and embeds
the resulting glyph data in `ui.dat`; it does not distribute the original
TTF as a standalone product. The source attribution and license are retained
in the project documentation and must remain available with future
redistribution materials.

## Applying Generated Assets

After reviewing the generated JSON, copy the matching files into:

```text
work/Wargroove 2/1.2.x/ui/font/<name>.json
work/Wargroove 2/1.2.x/ui/texture/fontTex/<name>.json
```

Then update the corresponding `ui/workspace.json` entry. Do not change only
`_payloadHex`.

Pack the workspace into a new file:

```sh
python3 tools/config_workspace.py pack \
  "work/Wargroove 2/1.2.x/ui" \
  "work/docs/analysis/modified-ui.dat"
```

For a release package, use:

```sh
python3 tools/build_dist_package.py
```

This packages `config.dat` and `ui.dat` together.

## Verification Checklist

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Also verify that:

- the asset count is unchanged unless an addition was intentional;
- both target `font` and `fontTex` entries exist;
- texture dimensions match the font `image_size`;
- `workspace.json` metadata matches the HLIF header;
- unsupported characters are absent rather than encoded as `.notdef`;
- fallback font names remain unchanged unless deliberately edited.

Finally, test the exact generated `ui.dat` on Windows for missing glyphs,
clipping, outlines, shadows, language selection, launch stability, and
save/load behavior.

## Related Documents

- [`docs/ui-dat-analysis.md`](ui-dat-analysis.md): format investigation and
  historical experiments.
- [`docs/specs/2026-09-26-ttf-to-halley-font-design.md`](specs/2026-09-26-ttf-to-halley-font-design.md):
  converter design.
- [`docs/plans/2026-09-26-ttf-to-halley-font-plan.md`](plans/2026-09-26-ttf-to-halley-font-plan.md):
  implementation plan.
- [`tools/README.md`](../tools/README.md): command reference.
