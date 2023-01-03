"""
Checks for Monotype.
"""

from fontbakery.callable import check
from fontbakery.status import PASS, FAIL, INFO, ERROR
from fontbakery.message import Message





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


@check(
  id="com.monotype.fonttools/check/bounds",
  rationale="Check font bounding box."
)
def check_bounds(ttFont):
  """
  Check bounds
  """

  if b'CFF ' in ttFont.keys():
    yield INFO, "Font is a CFF font. Cannot check bounds for now."
    return
  glyphs = ttFont[b'glyf']

  fontBoundsXMax = -ttFont[b'head'].unitsPerEm
  fontBoundsXMin = ttFont[b'head'].unitsPerEm
  fontBoundsYMax = -ttFont[b'head'].unitsPerEm
  fontBoundsYMin = ttFont[b'head'].unitsPerEm

  for glyphIndex in range(len(glyphs.glyphOrder)):
    glyph_to_check = glyphs.get(glyphs.glyphOrder[glyphIndex])
    if glyph_to_check.numberOfContours > 0:

      if glyph_to_check.xMax >= fontBoundsXMax:
        fontBoundsXMax = glyph_to_check.xMax

      if glyph_to_check.xMin <= fontBoundsXMin:
        fontBoundsXMin = glyph_to_check.xMax

      if glyph_to_check.yMax >= fontBoundsYMax:
        fontBoundsYMax = glyph_to_check.yMax

      if glyph_to_check.yMin <= fontBoundsYMin:
        fontBoundsYMin = glyph_to_check.yMin

  if ttFont[b'head'].xMin != fontBoundsXMin:
    yield ERROR, f"head table xMin is {ttFont[b'head'].xMin}, but calculated value is {fontBoundsXMin}"
  else:
    yield PASS, "head.xMin matches calculated xMin value."

  if ttFont[b'head'].xMax != fontBoundsXMax:
    yield ERROR, f"head table xMax is {ttFont[b'head'].xMax}, but calculated value is {fontBoundsXMax}"
  else:
    yield PASS, "head.xMax matches calculated xMax value."

  if ttFont[b'head'].yMin != fontBoundsYMin:
    yield ERROR, f"head table yMin is {ttFont[b'head'].yMin}, but calculated value is {fontBoundsYMin}"
  else:
    yield PASS, "head.yMin matches calculated yMin value."

  if ttFont[b'head'].yMax != fontBoundsYMax:
    yield ERROR, f"head table yMin is {ttFont[b'head'].yMax}, but calculated value is {fontBoundsYMax}"
  else:
    yield PASS, "head.yMax matches calculated yMax value."
