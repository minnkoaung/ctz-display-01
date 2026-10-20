from __future__ import annotations

from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
STATIC_OUTPUTS = OUTPUTS / "static"

WEIGHTS = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}


def set_name(font: TTFont, name_id: int, value: str) -> None:
    name_table = font["name"]
    name_table.removeNames(nameID=name_id)
    name_table.setName(value, name_id, 3, 1, 0x409)
    name_table.setName(value, name_id, 1, 0, 0)


def legacy_names(weight_name: str, italic: bool) -> tuple[str, str]:
    if weight_name == "Regular":
        return "CTZ Display 01", "Italic" if italic else "Regular"
    if weight_name == "Bold":
        return "CTZ Display 01", "Bold Italic" if italic else "Bold"
    return f"CTZ Display 01 {weight_name}", "Italic" if italic else "Regular"


def build_instances(source_name: str, italic: bool) -> None:
    source_path = OUTPUTS / source_name
    for weight, weight_name in WEIGHTS.items():
        font = instantiateVariableFont(
            TTFont(source_path),
            {"opsz": 14, "wght": weight},
            inplace=False,
        )
        style_name = f"{weight_name} Italic" if italic else weight_name
        legacy_family, legacy_subfamily = legacy_names(weight_name, italic)
        postscript_style = style_name.replace(" ", "")

        set_name(font, 1, legacy_family)
        set_name(font, 2, legacy_subfamily)
        set_name(font, 3, f"2026;CTZDisplay01-{postscript_style};0.4.1")
        set_name(font, 4, f"CTZ Display 01 {style_name}")
        set_name(font, 5, "Version 0.4.1")
        set_name(font, 6, f"CTZDisplay01-{postscript_style}")
        set_name(font, 16, "CTZ Display 01")
        set_name(font, 17, style_name)
        font["name"].removeNames(nameID=25)

        font["OS/2"].usWeightClass = weight
        selection = font["OS/2"].fsSelection
        selection &= ~((1 << 0) | (1 << 5) | (1 << 6))
        if italic:
            selection |= 1 << 0
        if weight >= 700:
            selection |= 1 << 5
        if not italic and weight == 400:
            selection |= 1 << 6
        font["OS/2"].fsSelection = selection

        font["head"].macStyle = (1 if weight >= 700 else 0) | (2 if italic else 0)
        output_name = f"CTZDisplay01-{postscript_style}.ttf"
        font.save(STATIC_OUTPUTS / output_name, reorderTables=False)


STATIC_OUTPUTS.mkdir(parents=True, exist_ok=True)
build_instances("CTZDisplay01-Variable.ttf", italic=False)
build_instances("CTZDisplay01-Italic-Variable.ttf", italic=True)
