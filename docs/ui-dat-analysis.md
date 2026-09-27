# Wargroove 2 `ui.dat` Analysis

Date: 2026-09-26

## Decoded Source Snapshots

Both Windows UI packs are now unpacked into readable JSON source trees:

```text
src/Wargroove 1/2.1.x/ui/
src/Wargroove 2/1.2.x/ui/
```

The trees contain one `.json` file per indexed asset:

| Target | Entries | JSON files | Binary files |
| --- | ---: | ---: | ---: |
| Wargroove 1 | 675 | 675 | 0 |
| Wargroove 2 | 2,662 | 2,662 | 0 |

`uiDefinition` assets are decoded into their Halley ConfigNode structure.
Font, texture, sprite, sprite-sheet, animation, and binary-file assets use a
JSON envelope containing `_assetType`, `_decoded`, and `_payloadHex`.
`_payloadHex` preserves the decrypted and decompressed payload so the source
tree can be repacked without losing data. Asset names retain their original
extensions in the JSON filename, preventing collisions such as
`CF_Logo` and `CF_Logo.png`.

## What `ui.dat` Is Used For

`ui.dat` contains the assets used to render and lay out the game's
presentation layer:

- font definitions and font textures;
- menus, dialogs, panels, buttons, and editor windows;
- UI sprites and sprite sheets;
- UI animations;
- splash and background textures;
- localized binary text such as EULA files.

It does not contain the main campaign, unit, faction, or dialogue string
resources. Those are in `config.dat`.

The actual font selection is not controlled solely by `ui.dat`. `ui.dat`
provides font definitions and `fontTex/*` textures, while `config.dat`
contains `ui_style/*` resources that select a named font for each UI style.

For example, `configFile:ui_style/label` contains:

```json
{
  "label": {
    "font": "Wargroove Medium",
    "size": 16,
    "smoothness": 0
  }
}
```

UI definition resources generally select widgets, images, text keys, and
styles. They do not repeat the font name for every widget.

## Windows and NSW Comparison

Windows Wargroove 2 and NSW Wargroove 2 use the same UI asset index:

| Metric | Windows WG2 | NSW WG2 |
| --- | ---: | ---: |
| Asset entries | 2,662 | 2,662 |
| Font definitions | 17 | 17 |
| Font textures | 17 | 17 |
| UI definitions | 218 | 218 |
| Sprites | 1,177 | 1,177 |
| Animations | 1,176 | 1,176 |

The logical asset names and types are identical. However, many payloads differ
in size and hash. All 17 `fontTex/*` payloads differ, and 121 of the 218
`uiDefinition` payloads differ. This is consistent with platform-specific
asset serialization, texture data, or layout details; it is not evidence that
NSW has additional UI asset names required by Korean.

The Windows WG2 `config.dat` `ui_style/*` resources reference nine font names:

| Font | Approximate style references |
| --- | ---: |
| `Wargroove Medium` | 94 |
| `MatchFont` | 24 |
| `Nope` | 12 |
| `Ubuntu Bold` | 18 |
| `Ubuntu Light` | 16 |
| `Ubuntu Regular` | 21 |
| `Sitka Text Bold Italic` | 1 |
| `Wargroove Small` | 2 |
| `SitkaText Card` | 2 |

The game therefore does not force every UI element to one font. It selects
fonts centrally by style, with `Wargroove Medium` as the dominant normal game
UI font.

The NSW file is also much larger:

```text
Windows WG2 ui.dat: approximately 8.5 MB
NSW WG2 ui.dat:     approximately 14 MB
```

## Why the NSW Patch Includes `ui.dat`

The NSW patch was distributed as a filesystem/ROM replacement and includes
the paired `config.dat` and `ui.dat` resources. There are two likely reasons:

1. The patch package preserves the complete UI resource set for the target
   platform, including its font textures and UI definitions.
2. The translator or patch author wanted to ensure Korean glyph rendering and
   localized UI resources were present without relying on the original NSW
   files.

The presence of `ui.dat` in the patch does not mean it can be copied directly
to Windows. The asset index is compatible at the logical-name level, but the
payloads are platform-specific and the Windows game must use Windows-built
assets.

## Koreanization Decision

For Windows Wargroove 2 `v1.2.12`, build `#45031`, the final package keeps the
Windows UI unchanged except for the two `Noto Serif` assets in `ui.dat`.
`config.dat` supplies the Korean resources and `ui.dat` supplies the expanded
fallback glyph set, so both files must be installed together.

- `config.dat`: required for the Korean string resources;
- `ui.dat`: required for the final `Noto Serif` glyph replacement;
- `font/Noto Serif`: generated from Google Noto Serif Korean Regular;
- `texture/fontTex/Noto Serif`: matching single-channel SDF atlas;
- every other `ui.dat` asset, including `Sitka Text Bold Italic`: unchanged;
- NSW `ui.dat`: reference material for font and UI comparison, not a direct
  replacement source.

The first font investigation targets are the 17 `fontTex/*` assets, especially
the large text fonts such as `fontTex/Noto Serif`, `fontTex/Zpix`, and
`fontTex/Sitka Text Bold Italic`.

The NSW `Noto Serif` comparison is recorded in
`work/docs/analysis/nsw-noto-serif.md`. It contains `송 사이클론`, but its
texture is a Switch-specific `BNTX` payload rather than the Windows `HLIF`
format. A converter could make it usable on Windows, but Google Noto Serif
Korean has broader coverage, so NSW conversion is deferred unless the current
replacement shows a runtime or visual problem.

## Font File Format

`Wargroove Medium` and `Wargroove Small` are not embedded as standalone
`.ttf`, `.otf`, or `.woff` files.

Each one is split into two Halley assets:

```text
font:    Wargroove Medium
texture: fontTex/Wargroove Medium

font:    Wargroove Small
texture: fontTex/Wargroove Small
```

The `font` payload begins with the font name, its `fontTex/...` reference,
metrics, and glyph records. The `fontTex/...` payload begins with a Halley
image/texture header and contains the rasterized glyph atlas. Standard font
signatures such as `OTTO`, `true`, `ttcf`, and `wOFF` are absent.

Replacing a font therefore requires replacing both the font definition and
its texture atlas, or reusing an existing font name and texture pair. A raw
TTF file cannot be dropped into `ui.dat` without converting it to Halley's
font and texture formats.

**Important:** the three representations of a font texture must stay
synchronized:

1. `ui/font/<name>.json` stores glyph UVs and the font's `image_size`.
2. `ui/texture/fontTex/<name>.json` stores the HLIF payload and its actual
   width/height.
3. `ui/workspace.json` stores the indexed texture metadata and
   `metadata_raw`, including the same width/height and pixel format.

Updating only `_payloadHex` is invalid. It can produce a structurally
packable `ui.dat` that crashes the game during startup because Halley reads
texture dimensions from the index metadata while decoding the payload. The
workspace packer now rejects this mismatch before writing `ui.dat`.

This failure occurred during the 12/10/8px Galmuri conversion: the payloads
were regenerated with new atlas heights, but the old `workspace.json`
metadata remained. The fix updated both the readable metadata and its raw
serialized form before repacking.

### Font payload structure

The payload exported from `ui/font/Wargroove Medium.json` is 27,894 bytes.
Its currently verified layout is:

```text
offset  size       meaning
0x0000  u32 + text font name, "Wargroove Medium"
0x0014  u32 + text texture reference, "fontTex/Wargroove Medium"
0x0030  f32        11.0
0x0034  f32        14.0
0x0038  f32        16.0
0x003c  0x11 bytes serializer flags/metrics, not fully assigned
0x004d  u32        glyph count: 534 (0x216)
0x0051  52 * 534   glyph records
0x6cc9  u32        fallback font count: 3
0x6ccd  strings    PixelMPlus, Zpix, AaCassiopeiaL1
...     u8         trailing flag: 1
```

Each glyph record is 52 bytes: a little-endian `u32` Unicode code point
followed by twelve little-endian `f32` values. The exact semantic names of
those twelve values still need comparison with Halley's font loader, but they
are the glyph's layout/atlas metrics rather than outline data. The raster
glyphs themselves are stored separately in the matching
`texture/fontTex/Wargroove Medium` payload.

This confirms that exporting `_payloadHex` produces a proprietary Halley font
asset, not a standard font file. A TTF-to-Halley converter would need to
generate both these glyph metrics and the matching raster atlas.

The project converter can generate either a single-channel SDF atlas or a
bitmap atlas. The original Wargroove font remains an SDF asset, and the final
Noto Serif replacement also remains a single-channel SDF asset.

### Galmuri replacement

The following local font files were used during the Windows Wargroove 2
`v1.2.12`, build `#45031` test:

```text
Wargroove Medium -> Galmuri11.ttf      (12px)
Wargroove Small  -> Galmuri9.ttf       (10px)
SitkaText Card   -> Galmuri11.ttf      (12px)
Nope             -> original Wargroove font
```

The numbers in the Galmuri family names are not the converter's nominal
point-size values. The matching nominal sizes are 12px for Galmuri11, 10px
for Galmuri9, and 8px for Galmuri7. The converter uses those values directly
with the regular or bold outline TTF, then stores the rendered glyphs in a
Halley RGBA bitmap atlas.

The historical Galmuri comparison used Galmuri11 at 12px for `SitkaText Card`
and `Wargroove Medium`, Galmuri9 at 10px for `Wargroove Small`, and left `Nope`
unchanged. The converter filters the requested character set through the
source TTF's Unicode cmap. This is important because Pillow otherwise renders an
unsupported character as the font's `.notdef` glyph; once that codepoint is
present in the Halley font table, Halley does not consult the configured
fallback fonts. The current `Galmuri11-Bold.ttf` does not contain several
CJK characters and symbols, so those codepoints must be omitted and allowed
to fall back to `Zpix` or `AaCassiopeiaL1`.
The generated atlas sizes are:

```text
Wargroove Medium -> 1024 x 1113
Wargroove Small  -> 1024 x 810
```

The replacement font definitions use `distance_field=false`. The matching
texture metadata uses `compression=hlif`, `format=rgba`, and
`filtering=false`.

### Alternative Galmuri font sets

`Wargroove Small` is referenced by these Windows WG2 styles:

```text
ui_style/mainMenu.card.progress -> Wargroove Small
ui_style/labelSmall.label       -> Wargroove Small
```

It is used for compact progress and secondary-label text, while the
top-level main-menu labels use `Nope`.

Two alternative Galmuri `ui.dat` packages were generated on September 27,
2026 for comparison. They retained the same Korean `config.dat` and differed
only in the selected font assets. The packages are no longer retained because
the project direction changed to the narrower Noto Serif replacement.

```text
Wargroove2-ko-translate-1.2.x-20260927-galmuri11-9-14.zip
  Wargroove Medium       -> Galmuri11 (12px)
  Wargroove Small        -> Galmuri9  (10px)
  Sitka Text Bold Italic -> Galmuri14 (15px)

Wargroove2-ko-translate-1.2.x-20260927-galmuri9-7-14.zip
  Wargroove Medium       -> Galmuri9  (10px)
  Wargroove Small        -> Galmuri7  (8px)
  Sitka Text Bold Italic -> Galmuri14 (15px)
```

Both generated `ui.dat` files contain 2,662 UI entries. The replacement
`Sitka Text Bold Italic` assets include the Korean syllables in `송 사이클론`
so the large groove-name effect can be tested without relying on its partial
`Noto Serif` fallback.

### Font texture metadata synchronization (historical)

The earlier successful Galmuri build already contained the same
`Wargroove Medium` payload used by the 2026-09-27 comparison builds. A
regression in the new comparison packages came from the newly replaced
`Sitka Text Bold Italic` texture: its payload was an RGBA HLIF bitmap, but the
packed `metadata_raw` still described it as `single_channel`. The readable
`metadata` field had been updated while the serialized metadata used for
packing had not.

This mismatch can make the game interpret the RGBA font atlas incorrectly,
causing large styled text to render black or disappear. Corrected comparison
packages synchronize both fields to:

```text
format: rgba
filtering: false
width: 1024
height: 1666
```

The corrected packages were repacked and validated with all 2,662 UI entries.

### Why Korean renders although the main font has no Hangul

The original `Wargroove Medium` asset does not contain Hangul glyph records.
Halley font assets can define a fallback chain, and the game searches that
chain when a glyph is missing from the selected font.

The original Windows WG2 font records contain these relevant fallback chains:

```text
Wargroove Medium -> PixelMPlus -> Zpix -> AaCassiopeiaL1
Wargroove Small  -> Zpix -> AaCassiopeiaL1
SitkaText Card   -> Zpix -> AaCassiopeiaL1
Nope             -> Zpix -> AaCassiopeiaL1
```

The parsed glyph counts confirm the role of the last fallback:

```text
Wargroove Medium:  534 glyphs, 0 Hangul syllables
Wargroove Small:   191 glyphs, 0 Hangul syllables
PixelMPlus:       7,252 glyphs, 0 Hangul syllables
Zpix:            22,235 glyphs, 0 Hangul syllables
AaCassiopeiaL1:  12,425 glyphs, 11,172 Hangul syllables and 127 Jamo
```

Therefore, Korean text appearing in ordinary UI is evidence that the fallback
chain is working, not that `Wargroove Medium` itself contains Korean. The
fallback font definitions and their matching `fontTex/*` atlases must remain
in `ui.dat`; replacing or removing them can make Korean disappear even when
the selected primary font still works for Latin text.

This also separates missing-glyph problems from layout problems. If a Korean
phrase is partially clipped in a special effect while the same characters
render elsewhere, the first suspects are that effect's layout, text box,
scaling, or clipping rules rather than the absence of Korean glyphs from
`Wargroove Medium`.

### `Song Cyclone` partial-square symptom

The observed rendering of `송 사이클론` as approximately `ㅁ 사이ㅁㅁ`
is not consistent with clipping. It matches a partial fallback-font failure.
The relevant assets contain this chain:

```text
Sitka Text Bold Italic -> Noto Serif
```

The original `Sitka Text Bold Italic` asset does not contain the Korean
syllables in this phrase and falls back to `Noto Serif`. The parsed `Noto Serif`
asset contains `사` and `이`, but not `송`, `클`, or `론`. This exactly explains
why the middle characters can render while the first and last characters are
shown as missing-glyph squares.

This large groove-name effect therefore uses a different font path from the
ordinary UI path:

```text
ordinary UI:       Wargroove Medium -> ... -> AaCassiopeiaL1
groove-name style: Sitka Text Bold Italic -> Noto Serif
```

The fix target is the `Sitka Text Bold Italic`/`Noto Serif` chain, not the
text-box width. The current `SitkaText Card` replacement does not affect this
effect because `SitkaText Card` and `Sitka Text Bold Italic` are separate
font assets.

### Windows WG2 original-font limitation

Windows Wargroove 2 does not officially support Korean. As a result, Korean
text can be missing even when using the untouched, original Windows WG2
`ui.dat`. In particular, skill/groove effects that use the
`Sitka Text Bold Italic -> Noto Serif` path can show missing-glyph squares for
some Korean syllables. This was observed with the original font resources as
well as with the Galmuri replacement, because the earlier Galmuri change did
not replace `Sitka Text Bold Italic`.

This is a known limitation of the original Windows WG2 font/fallback setup,
not evidence that the Korean translation string is corrupt. Replacing only
`Noto Serif` fixes the observed direct fallback path without changing the
primary `Sitka Text Bold Italic` asset.

### Font conversion experiments

The following issues were observed and recorded rather than treated as
successful conversions:

1. Pretendard SDF rendered at the intended size but had visibly broken
   strokes in the game.
2. Regular Galmuri TTF files were rendered with grayscale anti-aliasing and
   did not preserve the intended pixel-font appearance.
3. A single-channel bitmap atlas was interpreted by the default sprite
   material as a red channel, producing red glyphs and a black background.
4. An RGBA atlas with white RGB and a separate alpha channel leaked white
   RGB through Halley's premultiplied-alpha blend, producing a white
   background.

The final bitmap encoder stores each pixel as `(alpha, alpha, alpha, alpha)`.
This is white premultiplied by the glyph alpha, so transparent pixels remain
transparent and opaque glyph pixels remain white. Rendering the nominal-size
outline TTF preserves the requested family size; unlike the fixed-strike
bitmap TTF files, it also permits the 12/10/8px conversion sizes.

The final `ui.dat` was repacked successfully and reopened with the project
Halley reader. Both replacement textures were verified as RGBA, with matching
metadata/payload dimensions. The converter and packer tests passed, but the
release must still be checked in the Windows game after installation.

### Galmuri source and license

Galmuri is the bitmap font project by Minseo Lee (`quiple`), inspired by
Nintendo DS font design. The project source and releases are:

- Repository: <https://github.com/quiple/galmuri>
- Release used locally: `v2.40.4`
- Project page: <https://quiple.dev/font/galmuri>
- License: SIL Open Font License 1.1

The font files under `references/` are local development inputs and are not
part of the Git-tracked release assets. Anyone reproducing the conversion
should obtain Galmuri from the official project and follow its license and
attribution terms.

### Storage format vs. visual style

The Wargroove fonts are not fixed-pixel bitmap fonts. Their glyphs are stored
as single-channel SDF data, which allows the renderer to scale the glyphs and
apply smoothing, outlines, and shadows. However, SDF describes how the glyph
is stored and rendered; it does not determine the glyph's artistic style.

The original Wargroove font has a deliberately pixel-like retro design. Its
low-resolution atlas, sharp shapes, and pixel-oriented letterforms can make
the text look rough or difficult to read even though the underlying asset is
SDF. A more readable Korean font can therefore be converted to the same Halley
SDF format without changing the game's font rendering pipeline.

### Earlier font experiments (historical)

Pretendard, Nanum Gothic, Galmuri, and Neo둥근모 were tested as SDF or bitmap
replacements. The experiments established that bitmap channel metadata must
match the payload, premultiplied RGBA is required for Halley's default sprite
material, and several candidates produced broken strokes, excessive weight,
blur, or unsuitable pixel-grid rendering. Their generated packages were
temporary comparison artifacts and were removed after the final direction was
chosen.

The detailed findings remain summarized here and in the converter tests; none
of these fonts is part of the current release direction.

### Pixel Font Maker reference

`exqt/pixel-font-maker` is a browser-based pixel-font editor that exports
TTF, WOFF2, and BDF files. It is not an automatic Nanum Gothic-to-pixel
converter, but it provides Korean syllable templates for either the common
2,350-character set or all 11,172 syllables, using reusable consonant/vowel/
final-consonant components. citeturn0view0

This makes it a possible future route for a genuinely pixel-designed Korean
font: design a compact glyph set in the editor, export a TTF, then pass that
TTF through `ttf_to_halley.py --bitmap --antialias off`.

### Neo둥근모 Sitka-only comparison

To isolate the large groove/skill-effect text, a comparison package was
generated from the untouched Windows Wargroove 2 `v1.2.12` source:

```text
config.dat                         original, unchanged
all ui.dat assets                  original, unchanged
Sitka Text Bold Italic             Neo둥근모 v1.601, 30px bitmap
                                   antialias=off
                                   RGBA, filtering=false
                                   atlas=1024 x 1421
```

Only these two UI assets differ semantically from the original `ui.dat`:

```text
font/Sitka Text Bold Italic
texture/fontTex/Sitka Text Bold Italic
```

The generated font contains the five glyphs in `송 사이클론`. Unsupported
Japanese, Cyrillic, and other characters remain handled by the original
fallback chain.

This was a runtime comparison package only. It was not a replacement for the
translation release and was removed during analysis cleanup.

### Final Noto Serif Korean replacement decision

The final font direction is intentionally narrower than the earlier font
experiments:

```text
base:                 untouched Windows Wargroove 2 ui.dat workspace
changed font asset:   font/Noto Serif
changed texture:      texture/fontTex/Noto Serif
unchanged:            every other ui.dat asset, including Sitka Text Bold Italic
source font:          references/fonts/Noto_Serif_KR/static/NotoSerifKR-Regular.ttf
source family:        Google Noto Serif Korean
```

Source and license:

- Google Fonts specimen:
  `https://fonts.google.com/noto/specimen/Noto+Serif+KR?preview.script=Kore&preview.lang=ko_Kore`
- License: SIL Open Font License 1.1
- Local license copy:
  `references/fonts/Noto_Serif_KR/OFL.txt`
- Copyright: 2012 Google Inc.

The operational replacement procedure and license summary are consolidated in
`docs/font-editing-guide.md`.

The reason for replacing the asset is that the untouched WG2 `Noto Serif`
contains only 51 Hangul syllable glyphs. The skill and groove-effect path
uses `Sitka Text Bold Italic -> Noto Serif`; because that fallback does not
reach `AaCassiopeiaL1`, phrases such as `송 사이클론` can contain missing
glyphs even though ordinary UI text renders Korean correctly. Replacing only
`Noto Serif` fixes that direct fallback path while leaving the primary Sitka
font and the rest of the UI unchanged.

The replacement was generated on 2026-09-27 with the existing converter:

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

All converter options are recorded here, including their effective defaults:

```text
--pixel-size 42       rasterization size; matches Noto Serif size_pt 42
--render-scale 1      no supersampling reduction
--atlas-width 4096    atlas width; matches the original Noto Serif width
--padding 2           glyph packing gap in atlas pixels
--sdf-radius 4        SDF smoothing radius; matches the original
--sdf-threshold 1     mask threshold used before SDF generation
--antialias on        preserve grayscale glyph edges
--bitmap              not used; output remains single-channel SDF
--bitmap-gamma 1.0    default; irrelevant because --bitmap was not used
```

The character input contains 5,049 distinct requested characters. The source
font supplied 4,804 of them; unsupported characters were omitted so the
original fallback behavior remains available for those codepoints. The
generated asset contains `송 사이클론` and the other Korean characters needed
by the current Sitka-effect test.

The generated result is:

```text
font payload:         249,882 bytes
font glyphs:          4,804
font size_pt:         42.0
font ascender:        23.0
font height:          60.0
distance_field:       true
smooth_radius:        4.0
font image_size:      4096 x 2387
texture format:       single_channel
texture filtering:    true
texture mipmap:       false
texture payload:      3,675,427 bytes
```

The retained runtime verification package is:

```text
work/docs/analysis/noto-serif-kr-test/ui.dat
```

It contains all 2,662 original UI entries, with no added assets. The package
was reopened successfully and verified to contain the `Noto Serif` font,
`fontTex/Noto Serif` atlas at `4096 x 2387`, and the `송 사이클론` glyphs.
Its SHA-256 is:

```text
06224bc3d513136f3111c1f59823f1294793867dcbb1e8cf87a1601290939331
```
