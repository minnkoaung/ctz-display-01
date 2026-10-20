from __future__ import annotations

import copy
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
QA = OUTPUTS / "qa"
QA_VARIABLE = QA / "variable"
QA_STATIC = QA / "static"
QA_WEB = QA / "web"
QA_PROBE = QA / "probe"

QA_VERSION_NAME = "Version 0.4.1 QA1"
QA_REVISION = 0.401
STATIC_WEIGHTS = {
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
}


def set_name(font: TTFont, name_id: int, value: str) -> None:
    table = font["name"]
    table.removeNames(nameID=name_id)
    table.setName(value, name_id, 3, 1, 0x409)
    table.setName(value, name_id, 1, 0, 0)


def safe_windows_metrics() -> tuple[int, int]:
    fonts = [TTFont(path) for path in sorted((OUTPUTS / "static").glob("*.ttf"))]
    ascent = max(font["OS/2"].usWinAscent for font in fonts)
    descent = max(font["OS/2"].usWinDescent for font in fonts)
    ascent = max(ascent, max(font["head"].yMax for font in fonts))
    descent = max(descent, max(-font["head"].yMin for font in fonts))
    return ascent, descent


def rename_variable(font: TTFont, italic: bool, win_ascent: int, win_descent: int) -> None:
    style = "Italic" if italic else "Regular"
    postscript_style = style.replace(" ", "")
    set_name(font, 1, "CTZ Display QA")
    set_name(font, 2, style)
    set_name(font, 3, f"2026;CTZDisplayQA-{postscript_style};0.4.1-QA1")
    set_name(font, 4, f"CTZ Display QA {style}")
    set_name(font, 5, QA_VERSION_NAME)
    set_name(font, 6, f"CTZDisplayQA-{postscript_style}")
    set_name(font, 16, "CTZ Display QA")
    set_name(font, 17, style)
    set_name(font, 25, "CTZDisplayQAItalic" if italic else "CTZDisplayQA")
    font["head"].fontRevision = QA_REVISION
    font["OS/2"].usWinAscent = win_ascent
    font["OS/2"].usWinDescent = win_descent


def restore_inter_gdef_varstore(font: TTFont, italic: bool) -> None:
    source_name = "Inter-Italic-VariableFont_opsz,wght.ttf" if italic else "Inter-VariableFont_opsz,wght.ttf"
    source = TTFont(ROOT / "sources" / source_name)
    source_gdef = source["GDEF"].table
    if getattr(source_gdef, "VarStore", None) is not None:
        font["GDEF"].table.VarStore = copy.deepcopy(source_gdef.VarStore)
        font["GDEF"].table.Version = max(font["GDEF"].table.Version, 0x00010003)


def legacy_names(weight_name: str, italic: bool) -> tuple[str, str]:
    if weight_name == "Regular":
        return "CTZ Display QA", "Italic" if italic else "Regular"
    if weight_name == "Bold":
        return "CTZ Display QA", "Bold Italic" if italic else "Bold"
    return f"CTZ Display QA {weight_name}", "Italic" if italic else "Regular"


def build_static(variable_path: Path, italic: bool) -> None:
    for weight, weight_name in STATIC_WEIGHTS.items():
        font = instantiateVariableFont(
            TTFont(variable_path),
            {"opsz": 14, "wght": weight},
            inplace=False,
        )
        style = f"{weight_name} Italic" if italic else weight_name
        legacy_family, legacy_subfamily = legacy_names(weight_name, italic)
        postscript_style = style.replace(" ", "")
        set_name(font, 1, legacy_family)
        set_name(font, 2, legacy_subfamily)
        set_name(font, 3, f"2026;CTZDisplayQA-{postscript_style};0.4.1-QA1")
        set_name(font, 4, f"CTZ Display QA {style}")
        set_name(font, 5, QA_VERSION_NAME)
        set_name(font, 6, f"CTZDisplayQA-{postscript_style}")
        set_name(font, 16, "CTZ Display QA")
        set_name(font, 17, style)
        font["name"].removeNames(nameID=25)
        font["OS/2"].usWeightClass = weight
        selection = font["OS/2"].fsSelection
        selection &= ~((1 << 0) | (1 << 5) | (1 << 6))
        if italic:
            selection |= 1 << 0
        if weight >= 700:
            selection |= 1 << 5
        if weight == 400 and not italic:
            selection |= 1 << 6
        font["OS/2"].fsSelection = selection
        font["head"].macStyle = (1 if weight >= 700 else 0) | (2 if italic else 0)
        font.save(QA_STATIC / f"CTZDisplayQA-{postscript_style}.ttf", reorderTables=False)


def build_variable(source_name: str, output_name: str, italic: bool, win_ascent: int, win_descent: int) -> Path:
    font = TTFont(OUTPUTS / source_name)
    restore_inter_gdef_varstore(font, italic)
    rename_variable(font, italic, win_ascent, win_descent)
    output_path = QA_VARIABLE / output_name
    font.save(output_path, reorderTables=False)

    web_font = TTFont(output_path)
    web_font.flavor = "woff2"
    web_font.save(QA_WEB / output_name.replace(".ttf", ".woff2"))
    return output_path


def build_windows_metric_probe(source_path: Path) -> None:
    font = TTFont(source_path)
    set_name(font, 1, "CTZ Display QA WinProbe")
    set_name(font, 2, "Regular")
    set_name(font, 3, "2026;CTZDisplayQAWinProbe-Regular;0.4.1-QA1")
    set_name(font, 4, "CTZ Display QA WinProbe Regular")
    set_name(font, 5, QA_VERSION_NAME)
    set_name(font, 6, "CTZDisplayQAWinProbe-Regular")
    set_name(font, 16, "CTZ Display QA WinProbe")
    set_name(font, 17, "Regular")
    set_name(font, 25, "CTZDisplayQAWinProbe")
    font["OS/2"].usWinAscent = 3000
    font["OS/2"].usWinDescent = 1300
    output_path = QA_PROBE / "CTZDisplayQA-WinProbe-Variable.ttf"
    font.save(output_path, reorderTables=False)
    font.flavor = "woff2"
    font.save(QA_PROBE / "CTZDisplayQA-WinProbe-Variable.woff2")


for directory in (QA_VARIABLE, QA_STATIC, QA_WEB, QA_PROBE):
    directory.mkdir(parents=True, exist_ok=True)

safe_ascent, safe_descent = safe_windows_metrics()
upright = build_variable("CTZDisplay01-Variable.ttf", "CTZDisplayQA-Variable.ttf", False, safe_ascent, safe_descent)
italic = build_variable("CTZDisplay01-Italic-Variable.ttf", "CTZDisplayQA-Italic-Variable.ttf", True, safe_ascent, safe_descent)
build_static(upright, False)
build_static(italic, True)
build_windows_metric_probe(upright)
