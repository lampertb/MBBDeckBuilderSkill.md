"""Data table slide — clean MBB table with overlays support."""

from pptx.util import Inches, Pt
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    FONT_SMALL, LIGHT_GREY,
)
from scripts.slide_builder import add_headline, add_divider_line, add_source, add_footnotes, add_table, add_textbox


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, headers: [str], rows: [[str]], source?, footnotes?,
           col_widths?: [float in inches], subtitle?}
    Returns context with table reference for overlays.
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    headers = data.get("headers") or data.get("columns", [])
    rows = data.get("rows", [])

    if not headers or not rows:
        return {}

    # Optional subtitle / context line above table
    table_top = CONTENT_TOP + Inches(0.1)
    subtitle = data.get("subtitle")
    if subtitle:
        add_textbox(
            slide, CONTENT_LEFT, table_top, CONTENT_WIDTH, Inches(0.35),
            subtitle, ds, font_size=FONT_SMALL, color=ds.secondary, italic=True,
        )
        table_top += Inches(0.4)

    # Calculate table dimensions — fill available content area
    available_height = CONTENT_HEIGHT - (table_top - CONTENT_TOP) - Inches(0.3)
    num_data_rows = len(rows)
    total_rows = num_data_rows + 1  # +1 for header

    # Target comfortable row height, but expand to fill space
    min_row_height = Inches(0.40)
    target_row_height = available_height / total_rows
    row_height = max(min_row_height, min(target_row_height, Inches(0.65)))
    table_height = row_height * total_rows

    # Don't exceed available space
    if table_height > available_height:
        table_height = available_height

    col_widths = None
    if data.get("col_widths"):
        col_widths = [Inches(w) for w in data["col_widths"]]

    table_shape = add_table(
        slide,
        CONTENT_LEFT, table_top,
        CONTENT_WIDTH, table_height,
        headers, rows, ds,
        col_widths=col_widths,
    )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {"table": table_shape}
