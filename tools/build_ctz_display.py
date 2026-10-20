from __future__ import annotations

import copy
import io
import math
import subprocess
from pathlib import Path

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.varLib.featureVars import addFeatureVariations


ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
BUILD = ROOT / "build"
OUTPUTS = ROOT / "outputs"
MYANMAR = BUILD / "Pyidaungsu-Myanmar-subset.ttf"
MYANMAR_BOLD = BUILD / "Pyidaungsu-Bold-Myanmar-subset.ttf"

FAMILY_WIN_ASCENT = 2306
FAMILY_WIN_DESCENT = 1300


def prepare_myanmar_subset(source_name: str, destination: Path) -> None:
    subprocess.run(
        [
            "fonttools",
            "subset",
            str(SOURCES / source_name),
            "--unicodes=U+1000-109F,U+A9E0-A9FF,U+AA60-AA7F",
            "--layout-features=*",
            "--glyph-names",
            "--name-IDs=*",
            "--name-legacy",
            "--name-languages=*",
            "--notdef-glyph",
            "--notdef-outline",
            "--recommended-glyphs",
            f"--output-file={destination}",
        ],
        check=True,
    )


def set_name(font: TTFont, name_id: int, value: str) -> None:
    name_table = font["name"]
    name_table.removeNames(nameID=name_id)
    name_table.setName(value, name_id, 3, 1, 0x409)
    name_table.setName(value, name_id, 1, 0, 0)


def normalize_vertical_metrics(font: TTFont, inter_source: TTFont) -> None:
    font["hhea"].ascent = inter_source["hhea"].ascent
    font["hhea"].descent = inter_source["hhea"].descent
    font["hhea"].lineGap = inter_source["hhea"].lineGap

    font["OS/2"].sTypoAscender = inter_source["OS/2"].sTypoAscender
    font["OS/2"].sTypoDescender = inter_source["OS/2"].sTypoDescender
    font["OS/2"].sTypoLineGap = inter_source["OS/2"].sTypoLineGap
    font["OS/2"].usWinAscent = max(font["OS/2"].usWinAscent, inter_source["OS/2"].usWinAscent, FAMILY_WIN_ASCENT)
    font["OS/2"].usWinDescent = max(font["OS/2"].usWinDescent, inter_source["OS/2"].usWinDescent, FAMILY_WIN_DESCENT)
    font["OS/2"].fsSelection |= 1 << 7


def slant_anchor(anchor, shear: float) -> None:
    if anchor is not None:
        anchor.XCoordinate = round(anchor.XCoordinate + shear * anchor.YCoordinate)


def slant_myanmar_gpos(font: TTFont, myanmar_names: set[str], shear: float) -> None:
    if "GPOS" not in font:
        return
    for lookup in font["GPOS"].table.LookupList.Lookup:
        for subtable in lookup.SubTable:
            if lookup.LookupType == 9:
                lookup_type = subtable.ExtensionLookupType
                subtable = subtable.ExtSubTable
            else:
                lookup_type = lookup.LookupType
            if lookup_type == 4:
                for glyph_name, record in zip(subtable.MarkCoverage.glyphs, subtable.MarkArray.MarkRecord):
                    if glyph_name in myanmar_names:
                        slant_anchor(record.MarkAnchor, shear)
                for glyph_name, record in zip(subtable.BaseCoverage.glyphs, subtable.BaseArray.BaseRecord):
                    if glyph_name in myanmar_names:
                        for anchor in record.BaseAnchor:
                            slant_anchor(anchor, shear)
            elif lookup_type == 5:
                for glyph_name, record in zip(subtable.MarkCoverage.glyphs, subtable.MarkArray.MarkRecord):
                    if glyph_name in myanmar_names:
                        slant_anchor(record.MarkAnchor, shear)
                for glyph_name, attach in zip(subtable.LigatureCoverage.glyphs, subtable.LigatureArray.LigatureAttach):
                    if glyph_name in myanmar_names:
                        for component in attach.ComponentRecord:
                            for anchor in component.LigatureAnchor:
                                slant_anchor(anchor, shear)
            elif lookup_type == 6:
                for glyph_name, record in zip(subtable.Mark1Coverage.glyphs, subtable.Mark1Array.MarkRecord):
                    if glyph_name in myanmar_names:
                        slant_anchor(record.MarkAnchor, shear)
                for glyph_name, record in zip(subtable.Mark2Coverage.glyphs, subtable.Mark2Array.Mark2Record):
                    if glyph_name in myanmar_names:
                        for anchor in record.Mark2Anchor:
                            slant_anchor(anchor, shear)


def slant_myanmar_outlines(font: TTFont, myanmar_names: set[str], angle: float = 9.4) -> None:
    shear = math.tan(math.radians(angle))
    buffer = io.BytesIO()
    font.save(buffer)
    source = TTFont(io.BytesIO(buffer.getvalue()))
    source_glyph_set = source.getGlyphSet()
    transform = (1, 0, shear, 1, 0, 0)

    for glyph_name in myanmar_names:
        recording = DecomposingRecordingPen(source_glyph_set)
        source_glyph_set[glyph_name].draw(recording)
        glyph_pen = TTGlyphPen(None)
        recording.replay(TransformPen(glyph_pen, transform))
        glyph = glyph_pen.glyph()
        glyph.recalcBounds(font["glyf"])
        font["glyf"][glyph_name] = glyph
        advance_width, _ = font["hmtx"][glyph_name]
        font["hmtx"][glyph_name] = (advance_width, glyph.xMin if glyph.numberOfContours else 0)

    slant_myanmar_gpos(font, myanmar_names, shear)


def build(source_name: str, output_name: str, italic: bool) -> None:
    source_path = SOURCES / source_name
    merge_ready_path = BUILD / f"merge-ready-{source_path.name}"
    merged_path = BUILD / f"merged-{output_name}"

    source = TTFont(source_path)
    merge_ready = TTFont(source_path)
    gdef = merge_ready["GDEF"].table
    if hasattr(gdef, "VarStore"):
        gdef.VarStore = None
    gdef.Version = 0x00010002 if getattr(gdef, "MarkGlyphSetsDef", None) is not None else 0x00010000
    merge_ready.save(merge_ready_path)

    subprocess.run(
        [
            "fonttools",
            "merge",
            str(merge_ready_path),
            str(MYANMAR),
            str(MYANMAR_BOLD),
            f"--output-file={merged_path}",
        ],
        check=True,
    )

    merged = TTFont(merged_path)
    source_order = source.getGlyphOrder()
    merged_order = merged.getGlyphOrder()
    if merged_order[: len(source_order)] != source_order:
        raise RuntimeError("The merge changed Inter glyph order; variation tables cannot be restored safely.")

    regular_myanmar = TTFont(MYANMAR)
    bold_myanmar = TTFont(MYANMAR_BOLD)
    regular_order = regular_myanmar.getGlyphOrder()
    bold_order = bold_myanmar.getGlyphOrder()
    expected_count = len(source_order) + len(regular_order) + len(bold_order)
    if len(merged_order) != expected_count:
        raise RuntimeError("Unexpected merged glyph count; Myanmar master mapping is unsafe.")

    for tag in ("fvar", "avar", "STAT", "MVAR", "HVAR", "gvar"):
        merged[tag] = copy.deepcopy(source[tag])

    source_gdef = source["GDEF"].table
    if getattr(source_gdef, "VarStore", None) is not None:
        merged["GDEF"].table.VarStore = copy.deepcopy(source_gdef.VarStore)
        merged["GDEF"].table.Version = max(merged["GDEF"].table.Version, 0x00010003)

    for glyph_name in merged_order[len(source_order) :]:
        merged["HVAR"].table.AdvWidthMap.mapping[glyph_name] = 0
        merged["gvar"].variations[glyph_name] = []

    regular_index = {glyph_name: index for index, glyph_name in enumerate(regular_order)}
    bold_index = {glyph_name: index for index, glyph_name in enumerate(bold_order)}
    regular_cmap = regular_myanmar.getBestCmap()
    bold_cmap = bold_myanmar.getBestCmap()
    substitutions = {}
    regular_offset = len(source_order)
    bold_offset = regular_offset + len(regular_order)
    for codepoint in sorted(set(regular_cmap) & set(bold_cmap)):
        regular_name = merged_order[regular_offset + regular_index[regular_cmap[codepoint]]]
        bold_name = merged_order[bold_offset + bold_index[bold_cmap[codepoint]]]
        substitutions[regular_name] = bold_name

    # The generic merger adds a synthetic `locl` lookup for cmap conflicts and
    # attaches it to mym2, which would otherwise force the last (Bold) source at
    # every weight. Remove only that synthetic Myanmar feature; both originals
    # have no mym2 `locl` feature in their active default language system.
    gsub = merged["GSUB"].table
    for script_record in gsub.ScriptList.ScriptRecord:
        if script_record.ScriptTag != "mym2":
            continue
        language_systems = [script_record.Script.DefaultLangSys]
        language_systems.extend(record.LangSys for record in script_record.Script.LangSysRecord)
        for language_system in language_systems:
            if language_system is None:
                continue
            language_system.FeatureIndex = [
                feature_index
                for feature_index in language_system.FeatureIndex
                if gsub.FeatureList.FeatureRecord[feature_index].FeatureTag != "locl"
            ]
            language_system.FeatureCount = len(language_system.FeatureIndex)

    # Inter's avar maps user weight 650 to about 0.45 normalized. The Myanmar
    # outlines therefore switch discretely to the supplied Bold drawings from
    # 650 through 900 while retaining each master's native shaping lookups.
    addFeatureVariations(
        merged,
        [([{"wght": (0.45, 1.0)}], substitutions)],
        featureTag="rvrn",
    )

    if italic:
        slant_myanmar_outlines(merged, set(merged_order[len(source_order) :]))

    normalize_vertical_metrics(merged, source)

    style = "Italic" if italic else "Regular"
    postscript = "CTZDisplay01-Italic" if italic else "CTZDisplay01-Regular"
    set_name(merged, 0, "Copyright 2016 The Inter Project Authors; Copyright 2014-2016 Myanmar Computer Federation. Modified and combined as CTZ Display 01 in 2026.")
    set_name(merged, 1, "CTZ Display 01")
    set_name(merged, 2, style)
    set_name(merged, 3, f"2026;CTZDisplay01-{style};0.4.1")
    set_name(merged, 4, f"CTZ Display 01 {style}")
    set_name(merged, 5, "Version 0.4.1")
    set_name(merged, 6, postscript)
    set_name(merged, 13, "This Font Software is licensed under the SIL Open Font License, Version 1.1. CTZ Display 01 is a derivative of Inter and Pyidaungsu.")
    set_name(merged, 14, "https://openfontlicense.org")
    set_name(merged, 16, "CTZ Display 01")
    set_name(merged, 17, style)
    set_name(merged, 25, "CTZDisplay01Italic" if italic else "CTZDisplay01")

    merged["OS/2"].achVendID = "CTZ "
    merged["head"].fontRevision = 0.401
    merged["post"].italicAngle = -9.4 if italic else 0
    merged.save(OUTPUTS / output_name, reorderTables=False)


BUILD.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)
prepare_myanmar_subset("Pyidaungsu-2.5.3_Regular.ttf", MYANMAR)
prepare_myanmar_subset("Pyidaungsu-2.5.3_Bold.ttf", MYANMAR_BOLD)
build("Inter-VariableFont_opsz,wght.ttf", "CTZDisplay01-Variable.ttf", italic=False)
build("Inter-Italic-VariableFont_opsz,wght.ttf", "CTZDisplay01-Italic-Variable.ttf", italic=True)
