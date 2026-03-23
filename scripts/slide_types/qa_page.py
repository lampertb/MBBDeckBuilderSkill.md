"""Q&A / discussion closing slide."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import DesignSystem, SLIDE_WIDTH, SLIDE_HEIGHT, WHITE
from scripts.slide_builder import add_textbox, add_rectangle


def render(slide, data, ds: DesignSystem):
    """
    data: {headline?, subtitle?, contact?}
    """
    # Full navy background
    add_rectangle(slide, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT, fill_color=ds.primary)

    # Main text
    headline = data.get("headline", "Questions & Discussion")
    add_textbox(
        slide, Inches(1.5), Inches(2.5), Inches(10.3), Inches(1.5),
        headline, ds,
        font_size=Pt(40), color=WHITE, bold=True,
        alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
    )

    # Accent line
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(5.5), Inches(4.2), Inches(2.3), Pt(4),
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = ds.accent1
    accent.line.fill.background()

    # Subtitle / contact info
    subtitle = data.get("subtitle") or data.get("contact", "")
    if subtitle:
        add_textbox(
            slide, Inches(1.5), Inches(4.6), Inches(10.3), Inches(0.8),
            subtitle, ds,
            font_size=Pt(18), color=WHITE,
            alignment=PP_ALIGN.CENTER,
        )

    return {}
