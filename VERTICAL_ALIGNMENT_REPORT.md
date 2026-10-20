# CTZ Display 01 v0.4.1 vertical-alignment resolution

## Executive conclusion

The Latin outlines and base advance widths in CTZ Display 01 v0.4.0 are identical to the exact Inter 4.001 source at Regular, Medium, SemiBold, and Bold. Current v0.4.0 `hhea` and OS/2 typographic metrics also match Inter exactly.

Two build defects were confirmed:

1. The variable fonts retained Inter's variation PostScript prefix in name ID 25 (`Inter` and `InterItalic`). This can collide with Inter's generated variable-instance identities and can confuse application font caches.
2. The merge workaround removed Inter's GDEF Item Variation Store. Inter's variable GPOS kerning references this store. As a result, CTZ had a 3-unit kerning difference in “View” at weight 500 even though its Latin outlines and `hmtx` values were identical.

The reported 24px automatic line box is not produced by the current v0.4.0 typographic metrics. At 14px, the current `hhea` span predicts 16.94px, which rounds to 17px. The old pre-v0.4 `hhea` span predicts 24.13px, matching the reported 24px. The current safe Windows span also rounds to about 24px, so a Figma-only test is required to distinguish stale cached metrics from Figma using Windows clipping metrics.

The separately named **CTZ Display QA** family confirmed both fixes in Figma. Those validated changes are now promoted to CTZ Display 01 v0.4.1; the experimental QA fonts and WinProbe are no longer distributed.

## Confirmed findings

- All inspected fonts use 2048 units per em.
- CTZ v0.4.0 and Inter share `hhea` `1984/-494/0` and OS/2 typo `1984/-494/0`.
- `USE_TYPO_METRICS` is enabled in CTZ v0.4.0 and Inter.
- Inter and CTZ have no `BASE` table.
- CTZ retains Inter's `MVAR` table; it varies x-height, strikeout, and underline values, not vertical ascender/descender metrics.
- All 95 ASCII glyph outlines and base `hmtx` values match Inter after instancing at weights 400, 500, 600, and 700 with `opsz=14`.
- Restoring the GDEF variation store makes tested Latin HarfBuzz output exactly match Inter at all four weights.
- Myanmar-only shaping output remains exactly identical to production CTZ for the tested words, marks, stacks, digits, and weights.
- Chrome on macOS renders Inter and the validated build with identical 22px explicit line boxes, identical 17px automatic line boxes, and identical actual “View” bounds at weights 400 and 500.
- A browser WinProbe with `usWinAscent=3000` still renders a 17px automatic line box in Chrome, confirming Chrome does not use Windows clipping bounds for this line box.

## Figma result

The user confirmed that the uniquely named QA family works in Figma. This validates the corrected font data and separates the result from the cached v0.4.0 production identity. Version 0.4.1 carries the validated fixes under the production family name and uses a new version and unique ID; v0.4.0 must be removed before installation so Figma cannot continue using its cached copy.

## Before/after table

| Item | CTZ Display 01 v0.4.0 | CTZ Display 01 v0.4.1 | Reason |
|---|---:|---:|---|
| Family name | CTZ Display 01 | CTZ Display 01 | Production replacement |
| Version name | 0.4.0 | 0.4.1 | Identify the corrected release |
| Variable PostScript prefix, upright | `Inter` | `CTZDisplay01` | Remove Inter collision |
| Variable PostScript prefix, italic | `InterItalic` | `CTZDisplay01Italic` | Remove Inter collision |
| GDEF version | 1.2 | 1.3 | Required for variation store |
| GDEF Item Variation Store | Missing | Restored from exact Inter source | Preserve variable GPOS kerning |
| `hhea` ascent/descent/gap | `1984/-494/0` | `1984/-494/0` | No change |
| OS/2 typo ascent/descent/gap | `1984/-494/0` | `1984/-494/0` | No change |
| Windows ascent/descent | `2269/1300` | `2306/1300` | Cover measured family extrema |
| Cap height / x-height | `1490/1118` | `1490/1118` | No change |
| Global default bounds | about `-1298/2269` | about `-1298/2269` | No glyph translation |
| `BASE` | Absent | Absent | No evidence it is required |
| `MVAR` | Present | Present, unchanged | Preserve Inter variation behavior |

## Trade-off if Figma uses Windows clipping metrics

Safe Myanmar clipping bounds and an Inter-sized Windows line box cannot both be guaranteed in one font: Myanmar outlines extend substantially below Inter's Windows descent. No clipping bounds were reduced. If Figma proves that it uses Windows bounds for line placement, choose among these alternatives before changing production:

1. Keep the full bilingual family and accept a taller automatic line box while using explicit design-system line heights.
2. Publish a separate UI subset with explicitly documented Myanmar coverage and clipping risk after corpus testing.
3. Use Inter and Pyidaungsu as separate script-specific families instead of one combined font.

No such compromise was necessary or applied. The QA family passed the user's Figma test with safe Myanmar clipping bounds intact.

## Reproduction

```sh
python3 tools/audit_vertical_alignment.py > vertical-audit.json
python3 tools/build_ctz_display.py
python3 tools/build_static_instances.py
```

The production build pipeline is in `tools/build_ctz_display.py`; static instances are built by `tools/build_static_instances.py`. Exact OFL source binaries are retained in `sources/`.

## Rollback

To roll back, uninstall CTZ Display 01 v0.4.1, reinstall the v0.4.0 files from Git commit `4add142`, and restart Figma. Do not keep both releases installed simultaneously.

