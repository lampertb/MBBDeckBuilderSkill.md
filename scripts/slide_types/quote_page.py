"""Quote page — featured quote with attribution."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, SLIDE_WIDTH, SLIDE_HEIGHT,
    CONTENT_LEFT, CONTENT_WIDTH, NAVY, WHITE, MID_GREY, LIGHT_GREY,
)
from scripts.slide_builder import add_textbox, add_rectangle, add_source


def render(slide, data, ds: DesignSystem):
    """
    data: {quote, attribution, title?, source?, headline?}
    """
    # Light grey background
    add_rectangle(slide, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT, fill_color=LIGHT_GREY)

    # Left accent bar
    add_rectangle(
        slide, Inches(1.5), Inches(2.0), Pt(6), Inches(3.5),
        fill_color=ds.accent1,
    )

    # Opening quotation mark
    add_textbox(
        slide, Inches(1.8), Inches(1.5), Inches(1.0), Inches(1.0),
        "\u201C", ds,
        font_size=Pt(72), color=ds.accent1, bold=True,
    )

    # Quote text
    add_textbox(
        slide, Inches(2.0), Inches(2.3), Inches(9.0), Inches(2.5),
        data.get("quote", ""), ds,
        font_size=Pt(22), color=ds.primary, italic=True,
        alignment=PP_ALIGN.LEFT,
    )

    # Attribution
    attribution = data.get("attribution", "")
    title = data.get("title", "")
    attr_text = attribution
    if title:
        attr_text = f"{attribution}, {title}" if attribution else title

    if attr_text:
        add_textbox(
            slide, Inches(2.0), Inches(4.9), Inches(9.0), Inches(0.5),
            f"\u2014 {attr_text}", ds,
            font_size=Pt(16), color=ds.secondary, bold=True,
        )

    add_source(slide, data.get("source"), ds)

    return {}
