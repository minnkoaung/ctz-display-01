# CTZ Display 01

CTZ Display 01 is a bilingual Latin–Myanmar variable font combining Inter 4.001 with Pyidaungsu 2.5.3 Regular and Bold.

## Download

- [Upright variable TTF](outputs/CTZDisplay01-Variable.ttf)
- [Italic variable TTF](outputs/CTZDisplay01-Italic-Variable.ttf)
- [Upright WOFF2](outputs/CTZDisplay01-Variable.woff2)
- [Italic WOFF2](outputs/CTZDisplay01-Italic-Variable.woff2)
- [Technical notes](outputs/README.md)

## Variable behavior

- Inter varies continuously over `wght` 100–900 and `opsz` 14–32.
- Myanmar uses Pyidaungsu Regular at weights 100–600.
- Myanmar switches to the authentic Pyidaungsu Bold glyph set at weights 650–900.
- Myanmar shaping uses the original `mym2` GSUB/GPOS behavior from each Pyidaungsu master.

The Myanmar transition is discrete because the supplied Regular and Bold outlines are not interpolation-compatible. The italic font keeps Myanmar upright because no Pyidaungsu italic source was available.

## Specimens

### Regular

![CTZ Display 01 Regular](outputs/CTZDisplay01-Specimen-Regular.png)

### Bold

![CTZ Display 01 Bold](outputs/CTZDisplay01-Specimen-Bold.png)

## Installation

Remove older CTZ Display builds before installing the CTZ Display 01 TTF files. Restart or reload Figma after installation to clear cached font data.

## License

CTZ Display 01, Inter, and Pyidaungsu are distributed under the SIL Open Font License 1.1. See [LICENSE.txt](LICENSE.txt).

