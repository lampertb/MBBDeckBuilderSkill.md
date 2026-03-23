"""Three-column layout — triple parallel concepts/options with card styling."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    FONT_BODY, FONT_SUBHEADER, FONT_SMALL, LIGHT_GREY, WHITE, MID_GREY, DARK_GREY, TABLE_BORDER,
)
from scripts.slide_builder import (
    add_headline, add_divider_line, add_source, add_footnotes,
    add_textbox, add_bullet_list, add_rounded_rectangle, add_rectangle, add_icon,
)


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, columns: [{title, bullets?, text?, metric?, metric_label?}], source?, footnotes?}
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    columns = data.get("columns", [])
    if not columns:
        return {}

    num_cols = len(columns)
    col_gap = Inches(0.25)
    total_gap = col_gap * (num_cols - 1)
    col_width = (CONTENT_WIDTH - total_gap) / num_cols
    col_height = CONTENT_HEIGHT - Inches(0.3)
    card_top = CONTENT_TOP + Inches(0.1)

    for i, col_data in enumerate(columns):
        if isinstance(col_data, str):
            col_data = {"title": col_data}

        col_x = CONTENT_LEFT + (col_width + col_gap) * i
        y = card_top

        # Card background
        add_rounded_rectangle(
            slide, col_x, y,
            col_width, col_height,
            fill_color=LIGHT_GREY,
        )

        # Accent bar at top of card
        accent_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            col_x, y, col_width, Pt(4),
        )
        accent_bar.fill.solid()
        # Vary accent color per column for visual distinction
        accent_colors = [ds.accent1, ds.accent3, ds.accent2]
        accent_bar.fill.fore_color.rgb = accent_colors[i % len(accent_colors)]
        accent_bar.line.fill.background()

        inner_left = col_x + Inches(0.2)
        inner_width = col_width - Inches(0.4)
        y += Inches(0.2)

        # Optional icon at top of card
        icon = col_data.get("icon")
        if icon:
            icon_size = Inches(0.45)
            add_icon(
                slide, inner_left, y, icon_size, icon, ds,
                color=accent_colors[i % len(accent_colors)],
            )
            y += Inches(0.55)

        # Optional hero metric at top of card
        metric = col_data.get("metric")
        if metric:
            add_textbox(
                slide, inner_left, y, inner_width, Inches(0.5),
                str(metric), ds,
                font_size=Pt(28), color=accent_colors[i % len(accent_colors)], bold=True,
                alignment=PP_ALIGN.LEFT,
            )
            metric_label = col_data.get("metric_label", "")
            if metric_label:
                add_textbox(
                    slide, inner_left, y + Inches(0.45), inner_width, Inches(0.25),
                    metric_label, ds,
                    font_size=FONT_SMALL, color=DARK_GREY,
                )
            y += Inches(0.8)

        # Column title
        title = col_data.get("title", "")
        if title:
            add_textbox(
                slide, inner_left, y, inner_width, Inches(0.45),
                title, ds,
                font_size=Pt(16), color=ds.primary, bold=True,
            )
            # Subtle separator under title
            add_rectangle(
                slide, inner_left, y + Inches(0.48), inner_width, Pt(1),
                fill_color=TABLE_BORDER,
            )
            y += Inches(0.6)

        # Bullets or text — use FONT_SMALL (11pt) for columns to avoid overflow
        bullets = col_data.get("bullets")
        text = col_data.get("text")
        remaining_height = (card_top + col_height) - y - Inches(0.2)

        if bullets:
            add_bullet_list(
                slide, inner_left, y,
                inner_width, remaining_height,
                bullets, ds,
                font_size=FONT_SMALL, spacing_pt=6,
            )
        elif text:
            add_textbox(
                slide, inner_left, y,
                inner_width, remaining_height,
                text, ds,
                font_size=FONT_SMALL,
            )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {}
