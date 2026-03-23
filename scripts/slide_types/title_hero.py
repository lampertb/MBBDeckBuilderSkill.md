"""Title/cover slide."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, SLIDE_WIDTH, SLIDE_HEIGHT,
    CONTENT_LEFT, CONTENT_WIDTH, NAVY, WHITE, MID_GREY,
)
from scripts.slide_builder import add_textbox, add_rectangle


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, subtitle?, date?, author?, type}
    """
    # Navy background bar at bottom third
    bar_height = Inches(2.8)
    bar_top = SLIDE_HEIGHT - bar_height
    add_rectangle(slide, Inches(0), bar_top, SLIDE_WIDTH, bar_height, fill_color=ds.primary)

    # Title
    add_textbox(
        slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(1.8),
        data.get("headline", "Untitled Presentation"), ds,
        font_size=Pt(40), color=ds.primary, bold=True,
        alignment=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.BOTTOM,
    )

    # Subtitle
    subtitle = data.get("subtitle", "")
    if subtitle:
        add_textbox(
            slide, Inches(1.5), Inches(3.5), Inches(10.3), Inches(0.8),
            subtitle, ds,
            font_size=Pt(20), color=ds.secondary,
            alignment=PP_ALIGN.LEFT,
        )

    # Accent line
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(1.5), Inches(4.5), Inches(2.0), Pt(4),
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = ds.accent1
    accent.line.fill.background()

    # Date and author on the navy bar
    meta_parts = []
    if data.get("author"):
        meta_parts.append(data["author"])
    if data.get("date"):
        meta_parts.append(data["date"])
    if meta_parts:
        add_textbox(
            slide, Inches(1.5), bar_top + Inches(0.8), Inches(10.3), Inches(0.6),
            " | ".join(meta_parts), ds,
            font_size=Pt(16), color=WHITE,
            alignment=PP_ALIGN.LEFT,
        )

    return {}
