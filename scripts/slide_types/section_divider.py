"""Section divider slide — navy background with section title."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import DesignSystem, SLIDE_WIDTH, SLIDE_HEIGHT, WHITE
from scripts.slide_builder import add_textbox, add_rectangle


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, subtitle?}
    """
    # Full navy background
    add_rectangle(slide, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT, fill_color=ds.primary)

    # Section number or icon (optional)
    section_num = data.get("section_number")
    if section_num:
        add_textbox(
            slide, Inches(1.5), Inches(2.0), Inches(2.0), Inches(1.0),
            f"{section_num:02d}", ds,
            font_size=Pt(60), color=ds.accent1, bold=True,
            alignment=PP_ALIGN.LEFT,
        )

    # Title
    title_top = Inches(3.0) if section_num else Inches(2.8)
    add_textbox(
        slide, Inches(1.5), title_top, Inches(10.3), Inches(1.5),
        data.get("headline", ""), ds,
        font_size=Pt(36), color=WHITE, bold=True,
        alignment=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE,
    )

    # Accent line
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(1.5), title_top + Inches(1.6), Inches(2.0), Pt(4),
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = ds.accent1
    accent.line.fill.background()

    # Subtitle
    subtitle = data.get("subtitle", "")
    if subtitle:
        add_textbox(
            slide, Inches(1.5), title_top + Inches(2.0), Inches(10.3), Inches(0.8),
            subtitle, ds,
            font_size=Pt(18), color=WHITE,
            alignment=PP_ALIGN.LEFT,
        )

    return {}
