
"""
Checks for Monotype.
"""

from fontbakery.section import Section
from fontbakery.fonts_profile import profile_factory
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS
from fontbakery.profiles.googlefonts import GOOGLEFONTS_PROFILE_CHECKS

from fontbakery.profiles.monotype.metrics_checks import *



profile_imports = ('fontbakery.profiles.googlefonts', 'fontbakery.profiles.universal')
profile = profile_factory(default_section=Section("Monotype"))


CHECKS_IN_THIS_FILE = [
  'com.monotype.fonttools/check/empty_hdmx',
  'com.monotype.fonttools/check/bounds'
]

MONOTYPE_PROFILE_CHECKS = CHECKS_IN_THIS_FILE + UNIVERSAL_PROFILE_CHECKS + GOOGLEFONTS_PROFILE_CHECKS





profile.auto_register(
    globals(),
#    filter_func=lambda _, checkid, __: checkid
#    not in SET_IMPORTED_CHECKS - SET_EXPLICIT_CHECKS,
)

profile.test_expected_checks(set(MONOTYPE_PROFILE_CHECKS), exclusive=True)
