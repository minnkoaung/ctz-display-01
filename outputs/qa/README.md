# CTZ Display QA 0.4.1 QA1

Experimental, separately named family for diagnosing CTZ Display 01 vertical alignment in Figma and browsers. It does not replace the production family.

## Primary QA fonts

- `variable/CTZDisplayQA-Variable.ttf`
- `variable/CTZDisplayQA-Italic-Variable.ttf`
- `static/` — Regular, Medium, SemiBold, and Bold, upright and italic
- `web/` — WOFF2 variable fonts used by the browser specimen

## Diagnostic probe

`probe/CTZDisplayQA-WinProbe-Variable.ttf` intentionally increases Windows ascent to 3000 while leaving outlines and typographic metrics unchanged. Use it only to determine whether Figma bases line boxes on Windows clipping metrics.

## Fixes included

- Unique family, full, PostScript, and variation-prefix names
- Restored Inter GDEF Item Variation Store for exact variable Latin kerning
- Inter-identical `hhea` and OS/2 typographic metrics
- Safe Windows bounds `2306/1300`, derived from measured family extremes
- Unchanged Latin outlines, Myanmar outlines, GSUB/GPOS shaping, advances, and weight behavior

See `../../VERTICAL_ALIGNMENT_REPORT.md` and `specimens/FIGMA_TEST_PLAN.md`.
