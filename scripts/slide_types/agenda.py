"""Agenda slide — numbered list of topics."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP,
    FONT_BODY, FONT_SUBHEADER, LIGHT_GREY, WHITE,
)
from scripts.slide_builder import add_headline, add_divider_line, add_textbox, add_rounded_rectangle


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, items: [{title, description?}], current_item?: int}
    """
    add_headline(slide, data.get("headline", "Agenda"), ds)
    add_divider_line(slide, ds)

    items = data.get("items", [])
    current = data.get("current_item")  # 1-indexed; highlights this item

    y = CONTENT_TOP + Inches(0.2)
    item_height = Inches(0.7)
    gap = Inches(0.15)

    for i, item in enumerate(items):
        is_current = current is not None and (i + 1) == current

        # Background highlight for current item
        if is_current:
            add_rounded_rectangle(
                slide, CONTENT_LEFT, y - Inches(0.05),
                CONTENT_WIDTH, item_height + Inches(0.1),
                fill_color=LIGHT_GREY,
            )

        # Number circle
        num_size = Inches(0.45)
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            CONTENT_LEFT + Inches(0.1), y + Inches(0.12),
            num_size, num_size,
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = ds.accent1 if is_current else ds.primary
        circle.line.fill.background()

        # Number text
        add_textbox(
            slide, CONTENT_LEFT + Inches(0.1), y + Inches(0.12),
            num_size, num_size,
            str(i + 1), ds,
            font_size=Pt(16), color=WHITE, bold=True,
            alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        )

        # Item title
        title_left = CONTENT_LEFT + Inches(0.75)
        title_color = ds.primary if is_current else ds.secondary
        add_textbox(
            slide, title_left, y + Inches(0.05),
            CONTENT_WIDTH - Inches(1.0), Inches(0.35),
            item.get("title", item) if isinstance(item, dict) else str(item), ds,
            font_size=FONT_SUBHEADER if is_current else FONT_BODY,
            color=title_color, bold=is_current,
        )

        # Optional description
        if isinstance(item, dict) and item.get("description"):
            add_textbox(
                slide, title_left, y + Inches(0.38),
                CONTENT_WIDTH - Inches(1.0), Inches(0.3),
                item["description"], ds,
                font_size=Pt(12), color=ds.secondary,
            )

        y += item_height + gap

    return {}
