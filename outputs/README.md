# CTZ Display 01 — version 0.4.1

CTZ Display 01 combines Inter 4.001 with Pyidaungsu 2.5.3 Regular and Bold in one bilingual variable-font family.

## Current files

- `CTZDisplay01-Variable.ttf` — upright variable TTF for desktop apps and Figma.
- `CTZDisplay01-Italic-Variable.ttf` — italic variable TTF with embedded slanted Myanmar outlines.
- `CTZDisplay01-Static-TTF.zip` — 18 static TTFs for LibreOffice and software without variable-font support.
- `static/` — unpacked Thin through Black, upright and italic static fonts.
- `CTZDisplay01-Variable.woff2` — upright webfont.
- `CTZDisplay01-Italic-Variable.woff2` — italic webfont.
- `CTZDisplay01-Specimen-*.png` — Regular, Bold, Italic, and Bold Italic rendering specimens.
- `OFL.txt` — SIL Open Font License 1.1 and attribution notices.

Files beginning with `CTZDisplay-` are the superseded 0.1 build and should not be installed alongside CTZ Display 01.

## Variable behavior

- `wght`: 100–900, default 400.
- `opsz`: 14–32, default 14.
- Inter varies continuously across both axes.
- Myanmar uses Pyidaungsu Regular from weight 100 through 600.
- Myanmar switches to the authentic Pyidaungsu Bold drawings from weight 650 through 900.
- The italic font contains slanted Myanmar outlines for both weight states.

The Myanmar change is intentionally discrete rather than smoothly interpolated. The supplied Pyidaungsu Regular and Bold binaries are not interpolation-compatible: their glyph order differs and most shared glyphs have different contour/component structures. The variable font therefore uses OpenType Feature Variations to activate the complete Bold Myanmar glyph set at bold weights.

The Myanmar italic is embedded in the font by transforming the actual outlines and their GPOS positioning anchors to match Inter's italic angle. It is therefore not synthetic styling applied by Figma. Since no separately designed Pyidaungsu italic master was supplied, the result is technically an oblique rather than a hand-drawn cursive italic.

## Vertical metrics

Version 0.4.1 normalizes `hhea` and OS/2 typographic metrics to Inter: ascender `1984`, descender `-494`, and line gap `0`. It also restores Inter's GDEF Item Variation Store for exact variable kerning and uses a CTZ-specific variation PostScript prefix. Windows clipping metrics are `2306/1300`, covering measured family extremes without changing line-placement metrics, and `USE_TYPO_METRICS` remains enabled.

## Static family

The static package provides Thin, ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold, and Black in upright and italic styles. All variation tables are removed, and each file has explicit legacy and typographic family/style metadata for traditional application font menus.

Install either the variable fonts or the static family, not both simultaneously. Use the static package for LibreOffice and other applications that do not support OpenType variable fonts.

## Myanmar shaping

Both Pyidaungsu masters' `mym2` shaping lookups are retained. Regular-weight shaping matches Pyidaungsu 2.5.3 Regular; Bold-weight shaping matches Pyidaungsu 2.5.3 Bold. Complex substitutions, medials, vowels, punctuation, and Myanmar digits were tested with HarfBuzz.

`Pyidaungsu-2.5.3_Numbers.ttf` was not merged. CTZ Display 01 keeps Inter for ASCII `0`–`9` and Pyidaungsu for Myanmar digits U+1040–U+1049.

## Validation

- Verified family naming as `CTZ Display 01`.
- Instantiated and reloaded upright and italic files at weights 100, 400, 600, 650, 700, and 900.
- Confirmed the Myanmar Regular→Bold switch occurs at weight 650.
- Compared Regular and Bold shaping with their original Pyidaungsu source fonts.
- Rendered mixed Latin/Myanmar specimens at weights 400 and 700.
- Rendered and visually checked Myanmar Italic and Bold Italic specimens.
- Compressed to WOFF2, decompressed, and reloaded successfully.
- Validated all 18 static fonts for naming, weight classes, style flags, absence of variable tables, reload, and Myanmar shaping.
- Confirmed variable instances and all static fonts match Inter's vertical metrics while retaining Myanmar safety bounds.

The fixes were confirmed in Figma with a separately named QA build before promotion to production. Remove CTZ Display 01 v0.4.0, install the v0.4.1 TTFs, and fully restart Figma to avoid cached font data.

## Licensing

The supplied Inter and Pyidaungsu binaries identify themselves as SIL Open Font License 1.1. The derivative is renamed CTZ Display 01 and remains under OFL 1.1. This is an engineering assessment, not legal advice.

## SHA-256

```text
3ac6f3f8bbc411db66ca10e83165d5472c5253b7dbc59d67b9db3296e3deb380  CTZDisplay01-Variable.ttf
244b0a6fa73701ce902203602dfaac1e69cfad0f4ca3aaef3161296470bf2383  CTZDisplay01-Italic-Variable.ttf
34533d6591087e59ef545e0c5703af7ccc36ded1f69cf6195076cf4aa261a583  CTZDisplay01-Variable.woff2
e55b922612ea0bb043f6e43f2fb867e152cbfa08a2c00793f9a9a43fd4bf9c00  CTZDisplay01-Italic-Variable.woff2
30f0a5c8a5c5343c03a546ba1b439fb8456766c44ce5707288c528c4550df6dc  CTZDisplay01-Static-TTF.zip
```
