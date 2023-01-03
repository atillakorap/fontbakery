"""
Checks for Monotype Fonts.
"""
import unicodedata

from fontbakery.callable import check
from fontbakery.constants import (
  ALL_HANGUL_SYLLABLES_CODEPOINTS,
  MODERN_HANGUL_SYLLABLES_CODEPOINTS,
)
from fontbakery.fonts_profile import profile_factory
from fontbakery.message import Message, KEEP_ORIGINAL_MESSAGE
from fontbakery.profiles.fontwerk import FONTWERK_PROFILE_CHECKS
from fontbakery.profiles.googlefonts import GOOGLEFONTS_PROFILE_CHECKS
from fontbakery.profiles.notofonts import NOTOFONTS_PROFILE_CHECKS
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS
from fontbakery.section import Section
from fontbakery.status import PASS, FAIL, WARN, SKIP, INFO
from fontbakery.utils import add_check_overrides

profile_imports = (
  (".", ("shared_conditions", "universal", "fontwerk", "googlefonts", "notofonts")),
)
profile = profile_factory(default_section=Section("Monotype"))

SET_EXPLICIT_CHECKS = {
  # This is the set of explict checks that will be invoked
  # when fontbakery is run with the 'check-adobefonts' subcommand.
  # The contents of this set were last updated on September 14, 2022.
  #
  # =======================================
  # From adobefonts.py (this file)
  "com.adobe.fonts/check/family/consistent_upm",
  "com.adobe.fonts/check/find_empty_letters",
  "com.adobe.fonts/check/nameid_1_win_english",
  "com.adobe.fonts/check/unsupported_tables",
  #
  # =======================================
  # From cff.py
  "com.adobe.fonts/check/cff2_call_depth",
  "com.adobe.fonts/check/cff_call_depth",
  "com.adobe.fonts/check/cff_deprecated_operators",
  #
  # =======================================
  # From cmap.py
  "com.google.fonts/check/all_glyphs_have_codepoints",
  "com.google.fonts/check/family/equal_unicode_encodings",
  #
  # =======================================
  # From dsig.py
  # "com.google.fonts/check/dsig",  # PERMANENTLY_EXCLUDED
  #
  # =======================================
  # From fontwerk.py
  # "com.fontwerk/check/style_linking",  # PERMANENTLY_EXCLUDED
  # "com.fontwerk/check/vendor_id",      # PERMANENTLY_EXCLUDED
  # "com.fontwerk/check/no_mac_entries",
  "com.fontwerk/check/inconsistencies_between_fvar_stat",
  "com.fontwerk/check/weight_class_fvar",
  #
  # =======================================
  # From fvar.py
  "com.adobe.fonts/check/varfont/distinct_instance_records",
  "com.adobe.fonts/check/varfont/same_size_instance_records",
  "com.adobe.fonts/check/varfont/valid_axis_nameid",
  "com.adobe.fonts/check/varfont/valid_default_instance_nameids",
  "com.adobe.fonts/check/varfont/valid_postscript_nameid",
  "com.adobe.fonts/check/varfont/valid_subfamily_nameid",
  "com.google.fonts/check/varfont/bold_wght_coord",  # IS_OVERRIDDEN
  "com.google.fonts/check/varfont/regular_ital_coord",
  "com.google.fonts/check/varfont/regular_opsz_coord",
  "com.google.fonts/check/varfont/regular_slnt_coord",
  "com.google.fonts/check/varfont/regular_wdth_coord",
  "com.google.fonts/check/varfont/regular_wght_coord",
  "com.google.fonts/check/varfont/slnt_range",
  "com.google.fonts/check/varfont/wdth_valid_range",
  "com.google.fonts/check/varfont/wght_valid_range",
  #
  # =======================================
  # From gdef.py
  # "com.google.fonts/check/gdef_mark_chars",
  # "com.google.fonts/check/gdef_non_mark_chars",
  # "com.google.fonts/check/gdef_spacing_marks",
  #
  # =======================================
  # From glyf.py
  "com.google.fonts/check/glyf_non_transformed_duplicate_components",
  "com.google.fonts/check/glyf_unused_data",
  "com.google.fonts/check/points_out_of_bounds",
  #
  # =======================================
  # From googlefonts.py
  # "com.google.fonts/check/varfont_weight_instances",  # weak rationale
  "com.google.fonts/check/aat",
  "com.google.fonts/check/fvar_name_entries",
  "com.google.fonts/check/varfont_duplicate_instance_names",
  #
  # =======================================
  # From gpos.py
  "com.google.fonts/check/gpos_kerning_info",
  #
  # =======================================
  # From head.py
  "com.google.fonts/check/family/equal_font_versions",
  "com.google.fonts/check/font_version",
  "com.google.fonts/check/unitsperem",
  #
  # =======================================
  # From hhea.py
  "com.google.fonts/check/linegaps",
  "com.google.fonts/check/maxadvancewidth",
  #
  # =======================================
  # From kern.py
  "com.google.fonts/check/kern_table",
  #
  # =======================================
  # From layout.py
  "com.google.fonts/check/layout_valid_feature_tags",
  "com.google.fonts/check/layout_valid_language_tags",
  "com.google.fonts/check/layout_valid_script_tags",
  #
  # =======================================
  # From loca.py
  "com.google.fonts/check/loca/maxp_num_glyphs",
  #
  # =======================================
  # From name.py
  # "com.google.fonts/check/name/no_copyright_on_description",  # PERMANENTLY_EXCLUDED # noqa
  "com.google.fonts/check/name/match_familyname_fullfont",  # IS_OVERRIDDEN
  "com.adobe.fonts/check/family/max_4_fonts_per_family_name",
  "com.adobe.fonts/check/name/empty_records",
  "com.adobe.fonts/check/name/postscript_name_consistency",
  "com.adobe.fonts/check/name/postscript_vs_cff",
  "com.google.fonts/check/family_naming_recommendations",
  "com.google.fonts/check/monospace",
  #
  # =======================================
  # From notofonts.py
  # "com.google.fonts/check/cmap/unexpected_subtables",  # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/hmtx/comma_period",          # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/hmtx/encoded_latin_digits",  # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/hmtx/whitespace_advances",   # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/name/noto_designer",         # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/name/noto_manufacturer",     # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/name/noto_trademark",        # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/os2/noto_vendor",            # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/cmap/alien_codepoints",
  # "com.google.fonts/check/unicode_range_bits",
  "com.google.fonts/check/cmap/format_12",
  #
  # =======================================
  # From os2.py
  # "com.google.fonts/check/xavgcharwidth",  # PERMANENTLY_EXCLUDED
  "com.adobe.fonts/check/family/bold_italic_unique_for_nameid1",
  "com.adobe.fonts/check/fsselection_matches_macstyle",
  "com.google.fonts/check/code_pages",
  "com.google.fonts/check/family/panose_familytype",
  "com.google.fonts/check/family/panose_proportion",
  #
  # =======================================
  # From post.py
  "com.google.fonts/check/family/underline_thickness",
  "com.google.fonts/check/post_table_version",
  #
  # =======================================
  # From stat.py
  "com.adobe.fonts/check/stat_has_axis_value_tables",
  "com.google.fonts/check/varfont/stat_axis_record_for_each_axis",
  #
  # =======================================
  # From universal.py
  # "com.google.fonts/check/whitespace_glyphnames",  # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/whitespace_ink",         # PERMANENTLY_EXCLUDED
  # "com.google.fonts/check/cjk_chws_feature",
  # "com.google.fonts/check/contour_count",
  # "com.google.fonts/check/dotted_circle",
  # "com.google.fonts/check/unreachable_glyphs",
  # ---
  "com.adobe.fonts/check/freetype_rasterizer",  # IS_OVERRIDDEN
  "com.google.fonts/check/family/win_ascent_and_descent",  # IS_OVERRIDDEN
  "com.google.fonts/check/fontbakery_version",  # IS_OVERRIDDEN
  "com.google.fonts/check/name/trailing_spaces",  # IS_OVERRIDDEN
  "com.google.fonts/check/os2_metrics_match_hhea",  # IS_OVERRIDDEN
  "com.google.fonts/check/valid_glyphnames",  # IS_OVERRIDDEN
  "com.google.fonts/check/whitespace_glyphs",  # IS_OVERRIDDEN
  # ---
  "com.adobe.fonts/check/sfnt_version",
  "com.google.fonts/check/family/single_directory",
  "com.google.fonts/check/family/vertical_metrics",
  "com.google.fonts/check/gpos7",
  "com.google.fonts/check/mandatory_glyphs",
  "com.google.fonts/check/ots",
  "com.google.fonts/check/required_tables",
  "com.google.fonts/check/rupee",
  "com.google.fonts/check/STAT_strings",
  "com.google.fonts/check/transformed_components",
  "com.google.fonts/check/ttx_roundtrip",
  "com.google.fonts/check/unique_glyphnames",
  "com.google.fonts/check/whitespace_widths",
}

CHECKS_IN_THIS_FILE = [
  "com.adobe.fonts/check/family/consistent_upm",
  "com.monotype.fonttools/check/empty_hdmx",
]

SET_IMPORTED_CHECKS = set(
  UNIVERSAL_PROFILE_CHECKS
  + FONTWERK_PROFILE_CHECKS
  + GOOGLEFONTS_PROFILE_CHECKS
  + NOTOFONTS_PROFILE_CHECKS
)

ADOBEFONTS_PROFILE_CHECKS = [ c for c in CHECKS_IN_THIS_FILE if c in SET_EXPLICIT_CHECKS ] + [c for c in SET_IMPORTED_CHECKS if c in SET_EXPLICIT_CHECKS]

OVERRIDDEN_CHECKS = [
  "com.adobe.fonts/check/freetype_rasterizer",
  "com.google.fonts/check/family/win_ascent_and_descent",
  "com.google.fonts/check/fontbakery_version",
  "com.google.fonts/check/name/match_familyname_fullfont",
  "com.google.fonts/check/name/trailing_spaces",
  "com.google.fonts/check/os2_metrics_match_hhea",
  "com.google.fonts/check/valid_glyphnames",
  "com.google.fonts/check/varfont/bold_wght_coord",
  "com.google.fonts/check/whitespace_glyphs",
]


@check(
  id="com.adobe.fonts/check/family/consistent_upm",
  rationale="""
        While not required by the OpenType spec, we (Adobe) expect that a group
        of fonts designed & produced as a family have consistent units per em.
    """,
  proposal="https://github.com/googlefonts/fontbakery/pull/2372",
)
def com_adobe_fonts_check_family_consistent_upm(ttFonts):
  """Fonts have consistent Units Per Em?"""
  upm_set = set()
  for ttFont in ttFonts:
    upm_set.add(ttFont["head"].unitsPerEm)
  if len(upm_set) > 1:
    yield FAIL, Message(
      "inconsistent-upem",
      f"Fonts have different units per em: {sorted(upm_set)}.",
    )
  else:
    yield PASS, "Fonts have consistent units per em."


@check(
  id="com.monotype.fonttools/check/empty_hdmx",
  rationale="""
        Test whether the hdmx table has entries or not.
    """
)
def check_empty_hdmx(ttFont):
  """
  hdmx exists and has entries?
  """

  if ttFont.has_key('hdmx'):
    if len(ttFont.hdmx) > 0:
      yield PASS, "hdmx table present and not empty"
    else:
      yield FAIL, Message(
        "hmtx table is empty",
        "When present, the hdmx table needs to have at least one entry.",
      )
  else:
    yield INFO, "Font does not have an hdmx."


profile.auto_register(
  globals(),
  filter_func=lambda _, checkid, __: checkid
                                     not in SET_IMPORTED_CHECKS - SET_EXPLICIT_CHECKS,
)


ADOBEFONTS_PROFILE_CHECKS = add_check_overrides(
  ADOBEFONTS_PROFILE_CHECKS, profile.profile_tag, OVERRIDDEN_CHECKS
)

profile.test_expected_checks(ADOBEFONTS_PROFILE_CHECKS, exclusive=True)
