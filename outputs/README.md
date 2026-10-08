# CTZ Display 01 — version 0.2.0

CTZ Display 01 combines Inter 4.001 with Pyidaungsu 2.5.3 Regular and Bold in one bilingual variable-font family.

## Current files

- `CTZDisplay01-Variable.ttf` — upright variable TTF for desktop apps and Figma.
- `CTZDisplay01-Italic-Variable.ttf` — italic variable TTF; Latin is italic and Myanmar remains upright.
- `CTZDisplay01-Variable.woff2` — upright webfont.
- `CTZDisplay01-Italic-Variable.woff2` — italic webfont.
- `CTZDisplay01-Specimen-Regular.png` and `CTZDisplay01-Specimen-Bold.png` — rendering comparison.
- `OFL.txt` — SIL Open Font License 1.1 and attribution notices.

Files beginning with `CTZDisplay-` are the superseded 0.1 build and should not be installed alongside CTZ Display 01.

## Variable behavior

- `wght`: 100–900, default 400.
- `opsz`: 14–32, default 14.
- Inter varies continuously across both axes.
- Myanmar uses Pyidaungsu Regular from weight 100 through 600.
- Myanmar switches to the authentic Pyidaungsu Bold drawings from weight 650 through 900.

The Myanmar change is intentionally discrete rather than smoothly interpolated. The supplied Pyidaungsu Regular and Bold binaries are not interpolation-compatible: their glyph order differs and most shared glyphs have different contour/component structures. The variable font therefore uses OpenType Feature Variations to activate the complete Bold Myanmar glyph set at bold weights.

## Myanmar shaping

Both Pyidaungsu masters' `mym2` shaping lookups are retained. Regular-weight shaping matches Pyidaungsu 2.5.3 Regular; Bold-weight shaping matches Pyidaungsu 2.5.3 Bold. Complex substitutions, medials, vowels, punctuation, and Myanmar digits were tested with HarfBuzz.

`Pyidaungsu-2.5.3_Numbers.ttf` was not merged. CTZ Display 01 keeps Inter for ASCII `0`–`9` and Pyidaungsu for Myanmar digits U+1040–U+1049.

## Validation

- Verified family naming as `CTZ Display 01`.
- Instantiated and reloaded upright and italic files at weights 100, 400, 600, 650, 700, and 900.
- Confirmed the Myanmar Regular→Bold switch occurs at weight 650.
- Compared Regular and Bold shaping with their original Pyidaungsu source fonts.
- Rendered mixed Latin/Myanmar specimens at weights 400 and 700.
- Compressed to WOFF2, decompressed, and reloaded successfully.

The fonts were not installed into the user's operating system or opened directly in Figma. They are structurally suitable for Figma's local-font path. Remove the old CTZ Display installation, install the new CTZ Display 01 TTFs, and restart or reload Figma to avoid cached font data.

## Licensing

The supplied Inter and Pyidaungsu binaries identify themselves as SIL Open Font License 1.1. The derivative is renamed CTZ Display 01 and remains under OFL 1.1. This is an engineering assessment, not legal advice.

## SHA-256

```text
1f2b6d650389a44a0b24f18d1463b142cf5422c3b19f378437542dad65fe0c9a  CTZDisplay01-Variable.ttf
2a212b646bd19d12596f43e2570050e80a89cf456ab3b518a2a79034557325fc  CTZDisplay01-Italic-Variable.ttf
4e849de10ed4ad1a8b434321abcd7c6c5b825f064f08cff104664d993ffa5440  CTZDisplay01-Variable.woff2
9389f31bf08fd3a89da9d315a93c77148346f7bf88a4e14f293e4dead7e33c19  CTZDisplay01-Italic-Variable.woff2
```
