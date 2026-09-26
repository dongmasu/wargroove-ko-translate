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

For Windows Wargroove 2 `v1.2.12`, build `#45031`, the original Windows
`ui.dat` was left unchanged and Korean text rendered successfully after
adding the Korean `config.dat` resources. Therefore:

- `config.dat`: required for the Korean string resources;
- `ui.dat`: not required for the current Korean text test;
- font assets in `ui.dat`: investigate only if missing glyphs, square boxes,
  fallback fonts, clipping, or unreadable text appear;
- font selection: edit the relevant `config.dat` `ui_style/*` resource if a
  specific style must be redirected to another existing font;
- NSW `ui.dat`: reference material for font and UI comparison, not a direct
  replacement source.

The first font investigation targets are the 17 `fontTex/*` assets, especially
the large text fonts such as `fontTex/Noto Serif`, `fontTex/Zpix`, and
`fontTex/Sitka Text Bold Italic`.

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

The project converter now generates Halley's single-channel SDF atlas by
default, using the same radius-based signed-distance mapping as the engine.
`--bitmap` remains available for diagnostic output only. MSDF/MTSDF generation
is separate and is not required for the original single-channel
`Wargroove Medium` asset.

For the current translation build, this conversion is deferred: the original
Windows WG2 fonts rendered the Korean test strings successfully. Revisit font
conversion only if runtime review finds poor readability, missing glyphs,
fallback fonts, clipping, or other rendering problems.
