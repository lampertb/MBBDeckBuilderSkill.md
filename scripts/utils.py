"""
Utility helpers — unit conversions, XML manipulation for borders and transparency.
"""

from lxml import etree
from pptx.oxml.ns import qn, nsmap
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor


def set_shape_transparency(shape, alpha_pct):
    """
    Set fill transparency on a shape. alpha_pct is 0-100 where 0=fully transparent, 100=opaque.
    python-pptx doesn't expose alpha natively, so we manipulate XML.
    """
    fill = shape.fill
    if not fill.type:
        return
    # Access the solidFill element
    solid_fill = fill._fill
    if solid_fill is None:
        return
    # Find the srgbClr or other color element
    for color_elem in solid_fill.iter():
        tag = etree.QName(color_elem.tag).localname
        if tag in ("srgbClr", "schemeClr", "sysClr"):
            # Remove existing alpha
            for child in list(color_elem):
                if etree.QName(child.tag).localname == "alpha":
                    color_elem.remove(child)
            # Add alpha element
            alpha_elem = etree.SubElement(color_elem, qn("a:alpha"))
            alpha_elem.set("val", str(int(alpha_pct * 1000)))  # val is in 1/1000ths of percent
            break


def remove_table_borders(table):
    """Remove all borders from a python-pptx table."""
    for row in table.rows:
        for cell in row.cells:
            _set_cell_borders(cell, top=None, bottom=None, left=None, right=None)


def set_table_mbb_borders(table, border_color=None):
    """
    Apply MBB-style borders: no vertical borders, light horizontal rules,
    bold header bottom border.
    """
    from scripts.design_system import TABLE_BORDER, NAVY
    color = border_color or TABLE_BORDER
    num_rows = len(table.rows)

    for row_idx, row in enumerate(table.rows):
        for cell in row.cells:
            if row_idx == 0:
                # Header row: bold bottom border
                _set_cell_borders(
                    cell,
                    top={"color": color, "width": Pt(0.5)},
                    bottom={"color": NAVY, "width": Pt(1.5)},
                    left=None,
                    right=None,
                )
            elif row_idx == num_rows - 1:
                # Last row: bottom border
                _set_cell_borders(
                    cell,
                    top={"color": color, "width": Pt(0.5)},
                    bottom={"color": color, "width": Pt(0.5)},
                    left=None,
                    right=None,
                )
            else:
                # Middle rows: light horizontal only
                _set_cell_borders(
                    cell,
                    top={"color": color, "width": Pt(0.5)},
                    bottom={"color": color, "width": Pt(0.5)},
                    left=None,
                    right=None,
                )


def _set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """
    Set individual cell borders. Each border arg is None (no border) or
    {"color": RGBColor, "width": Pt}.
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    for side, spec in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        tag = f"a:ln{side.capitalize()}" if side != "left" else "a:lnL"
        if side == "right":
            tag = "a:lnR"
        elif side == "top":
            tag = "a:lnT"
        elif side == "bottom":
            tag = "a:lnB"

        # Remove existing border element
        for existing in tcPr.findall(qn(tag)):
            tcPr.remove(existing)

        ln = etree.SubElement(tcPr, qn(tag))
        if spec is None:
            ln.set("w", "0")
            no_fill = etree.SubElement(ln, qn("a:noFill"))
        else:
            ln.set("w", str(int(spec["width"])))
            solid = etree.SubElement(ln, qn("a:solidFill"))
            srgb = etree.SubElement(solid, qn("a:srgbClr"))
            srgb.set("val", str(spec["color"]))


def set_cell_fill(cell, color):
    """Set the fill color of a table cell."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    # Remove existing fill
    for existing in tcPr.findall(qn("a:solidFill")):
        tcPr.remove(existing)
    solid = etree.SubElement(tcPr, qn("a:solidFill"))
    srgb = etree.SubElement(solid, qn("a:srgbClr"))
    srgb.set("val", str(color))


def is_numeric(value):
    """Check if a string value looks numeric (for right-alignment in tables)."""
    if not isinstance(value, str):
        return isinstance(value, (int, float))
    cleaned = value.replace(",", "").replace("$", "").replace("%", "").replace("(", "").replace(")", "").replace("-", "").replace("+", "").strip()
    if not cleaned:
        return False
    try:
        float(cleaned)
        return True
    except ValueError:
        return False
