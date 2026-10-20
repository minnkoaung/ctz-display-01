from __future__ import annotations

import json
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parent.parent
INTER = ROOT / "sources/Inter-VariableFont_opsz,wght.ttf"
CTZ = ROOT / "outputs/CTZDisplay01-Variable.ttf"


def metrics(path: Path) -> dict[str, object]:
    font = TTFont(path)
    os2 = font["OS/2"]
    hhea = font["hhea"]
    head = font["head"]
    return {
        "file": str(path.relative_to(ROOT)),
        "family": font["name"].getDebugName(16) or font["name"].getDebugName(1),
        "style": font["name"].getDebugName(17) or font["name"].getDebugName(2),
        "version": font["name"].getDebugName(5),
        "upm": head.unitsPerEm,
        "head_y_min": head.yMin,
        "head_y_max": head.yMax,
        "hhea_ascent": hhea.ascent,
        "hhea_descent": hhea.descent,
        "hhea_line_gap": hhea.lineGap,
        "typo_ascent": os2.sTypoAscender,
        "typo_descent": os2.sTypoDescender,
        "typo_line_gap": os2.sTypoLineGap,
        "win_ascent": os2.usWinAscent,
        "win_descent": os2.usWinDescent,
        "cap_height": getattr(os2, "sCapHeight", None),
        "x_height": getattr(os2, "sxHeight", None),
        "weight_class": os2.usWeightClass,
        "use_typo_metrics": bool(os2.fsSelection & (1 << 7)),
        "has_BASE": "BASE" in font,
        "has_MVAR": "MVAR" in font,
        "has_fvar": "fvar" in font,
    }


def glyph_signature(font: TTFont, glyph_name: str) -> tuple[object, ...]:
    glyph = font["glyf"][glyph_name]
    if glyph.isComposite():
        return (
            "composite",
            tuple(
                (
                    component.glyphName,
                    tuple(component.getComponentInfo()[1]),
                )
                for component in glyph.components
            ),
        )
    coordinates, endpoints, flags = glyph.getCoordinates(font["glyf"])
    return (
        "simple",
        tuple(coordinates),
        tuple(endpoints),
        tuple(flags),
    )


def compare_latin(weight: int) -> dict[str, object]:
    inter = instantiateVariableFont(TTFont(INTER), {"wght": weight, "opsz": 14}, inplace=False)
    ctz = instantiateVariableFont(TTFont(CTZ), {"wght": weight, "opsz": 14}, inplace=False)
    inter_cmap = inter.getBestCmap()
    ctz_cmap = ctz.getBestCmap()
    differences = []
    for codepoint in range(0x20, 0x7F):
        inter_name = inter_cmap.get(codepoint)
        ctz_name = ctz_cmap.get(codepoint)
        if inter_name != ctz_name:
            differences.append({"codepoint": codepoint, "reason": "cmap", "inter": inter_name, "ctz": ctz_name})
            continue
        if inter_name is None:
            continue
        if glyph_signature(inter, inter_name) != glyph_signature(ctz, ctz_name):
            differences.append({"codepoint": codepoint, "glyph": inter_name, "reason": "outline"})
            continue
        if inter["hmtx"][inter_name] != ctz["hmtx"][ctz_name]:
            differences.append(
                {
                    "codepoint": codepoint,
                    "glyph": inter_name,
                    "reason": "hmtx",
                    "inter": inter["hmtx"][inter_name],
                    "ctz": ctz["hmtx"][ctz_name],
                }
            )
    return {"weight": weight, "ascii_glyphs_compared": 95, "differences": differences}


font_paths = [
    INTER,
    ROOT / "sources/Inter-Italic-VariableFont_opsz,wght.ttf",
    ROOT / "sources/Pyidaungsu-2.5.3_Regular.ttf",
    ROOT / "sources/Pyidaungsu-2.5.3_Bold.ttf",
    CTZ,
    ROOT / "outputs/CTZDisplay01-Italic-Variable.ttf",
]
font_paths.extend(sorted((ROOT / "outputs/static").glob("*.ttf")))

report = {
    "fonts": [metrics(path) for path in font_paths],
    "latin_comparisons": [compare_latin(weight) for weight in (400, 500, 600, 700)],
    "predicted_auto_line_height_px_at_14": {
        "inter_current_hhea": (1984 - (-494)) / 2048 * 14,
        "ctz_pre_0_4_hhea": (2230 - (-1300)) / 2048 * 14,
        "ctz_0_4_hhea": (1984 - (-494)) / 2048 * 14,
    },
}
print(json.dumps(report, indent=2))
