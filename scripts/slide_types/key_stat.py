"""Key stat slide — 1-3 hero metrics with full-height cards and visual accents."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    FONT_BODY, FONT_SMALL, FONT_FOOTNOTE, WHITE, LIGHT_GREY, MID_GREY, DARK_GREY, TABLE_BORDER,
    POSITIVE_COLOR, NEGATIVE_COLOR,
)
from scripts.slide_builder import (
    add_headline, add_divider_line, add_source, add_footnotes,
    add_textbox, add_rounded_rectangle, add_rectangle, add_icon,
)


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, stats: [{value, label, delta?, context?}], source?, footnotes?}
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    stats = data.get("stats", [])
    num_stats = len(stats)
    if num_stats == 0:
        return {}

    # Cards fill the full content area
    card_gap = Inches(0.3)
    total_gap = card_gap * (num_stats - 1)
    card_width = (CONTENT_WIDTH - total_gap) / num_stats
    card_height = CONTENT_HEIGHT - Inches(0.2)
    card_y = CONTENT_TOP + Inches(0.1)

    accent_colors = [ds.accent1, ds.accent3, ds.accent2]

    for i, stat in enumerate(stats):
        card_x = CONTENT_LEFT + (card_width + card_gap) * i
        accent = accent_colors[i % len(accent_colors)]

        # Card background
        add_rounded_rectangle(
            slide, card_x, card_y, card_width, card_height,
            fill_color=LIGHT_GREY,
        )

        # Top accent bar
        add_rectangle(
            slide, card_x, card_y, card_width, Pt(5),
            fill_color=accent,
        )

        # Optional icon
        icon = stat.get("icon")
        if icon:
            icon_size = Inches(0.5)
            add_icon(
                slide, card_x + (card_width - icon_size) / 2, card_y + Inches(0.25),
                icon_size, icon, ds, color=accent,
            )

        # Big number — centered in upper portion
        num_top = card_y + Inches(0.85) if icon else card_y + Inches(0.6)
        add_textbox(
            slide, card_x + Inches(0.2), num_top,
            card_width - Inches(0.4), Inches(1.2),
            str(stat.get("value", "")), ds,
            font_size=Pt(54), color=ds.primary, bold=True,
            alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        )

        # Label — larger, bolder
        add_textbox(
            slide, card_x + Inches(0.2), card_y + Inches(1.9),
            card_width - Inches(0.4), Inches(0.5),
            str(stat.get("label", "")).upper(), ds,
            font_size=FONT_SMALL, color=DARK_GREY, bold=True,
            alignment=PP_ALIGN.CENTER,
        )

        # Separator
        add_rectangle(
            slide, card_x + Inches(0.4), card_y + Inches(2.5),
            card_width - Inches(0.8), Pt(1),
            fill_color=TABLE_BORDER,
        )

        # Delta indicator
        delta = stat.get("delta")
        if delta:
            delta_str = str(delta)
            is_positive = not delta_str.startswith("-")
            arrow = "\u25B2" if is_positive else "\u25BC"
            color = POSITIVE_COLOR if is_positive else NEGATIVE_COLOR
            add_textbox(
                slide, card_x, card_y + Inches(2.7), card_width, Inches(0.45),
                f"{arrow}  {delta_str}", ds,
                font_size=Pt(18), color=color, bold=True,
                alignment=PP_ALIGN.CENTER,
            )

        # Context line
        context = stat.get("context")
        if context:
            add_textbox(
                slide, card_x + Inches(0.2), card_y + Inches(3.3),
                card_width - Inches(0.4), Inches(0.8),
                context, ds,
                font_size=FONT_SMALL, color=ds.secondary,
                alignment=PP_ALIGN.CENTER,
            )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {}
