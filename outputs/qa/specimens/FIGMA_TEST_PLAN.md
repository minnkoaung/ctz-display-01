# Figma Desktop validation plan

## Install

Install only these experimental files for the primary Figma test:

- `../variable/CTZDisplayQA-Variable.ttf`
- `../variable/CTZDisplayQA-Italic-Variable.ttf`

They use unique family, full, PostScript, and variable-prefix names and can coexist with CTZ Display 01 and Inter.

Install `../probe/CTZDisplayQA-WinProbe-Variable.ttf` only for the metric-source test. It intentionally has an exaggerated Windows ascent and must not be used for design work.

Fully quit and reopen Figma after installation.

## Controlled alignment matrix

Create paired text layers using exact Inter 4.001 and CTZ Display QA. Keep width, alignment, letter spacing, paragraph spacing, and OpenType settings identical.

Test Regular, Medium, SemiBold, and Bold at:

| Font size | Explicit line height |
|---:|---:|
| 12 | 16 |
| 14 | 22 |
| 16 | 24 |
| 18 | 26 |
| 24 | 32 |
| 30 | 38 |

Repeat every row with automatic line height.

Latin strings:

```text
View
Search
Submit
Placeholder
Ag
gjpqy
0123456789 !?.,:;()[]{}+-/%@#&
```

Myanmar and mixed strings:

```text
မြန်မာစာ ကြိုဆိုပါတယ်။ မြို့ နိုင်ငံတော်
က္က န္တ မ္ဘာ ကျွမ်းကျင်မှု
ပေးပို့ရန် ၁၂၃၄၅
Submit ပေးပို့ရန် · ၁၂၃၄၅ · MMK 50,000
```

Test single-line controls, wrapped paragraphs, and at least three lines of mixed text. Check upper marks, lower marks, stacks, line overlap, clipping, and horizontal wrapping.

## Metric-source test

At 14px Regular with automatic line height, compare:

1. Inter
2. CTZ Display QA
3. CTZ Display QA WinProbe

Interpretation:

- QA = 17px and WinProbe = 17px: Figma uses typographic/`hhea` metrics; the production problem was most likely stale identity/cache data.
- QA ≈ 25px and WinProbe becomes substantially taller: Figma uses Windows clipping metrics.
- QA = 17px but production CTZ remains 24px: production CTZ is cached or colliding; QA naming fixes the test path.

## Pass criteria

- Inter and QA Latin glyphs occupy the same visual vertical position at explicit line heights.
- Automatic line boxes match closely when the renderer uses typographic metrics.
- No horizontal differences appear in the tested Latin strings.
- Myanmar marks and stacks remain correctly shaped without clipping or line collisions.
- Wrapping and control widths do not change unexpectedly.

Record screenshots with text-layer bounds visible. The browser reference is `browser-comparison-chromium.png`.

## Rollback

Remove CTZ Display QA and CTZ Display QA WinProbe from Font Book and restart Figma. Production CTZ Display 01 is untouched.

