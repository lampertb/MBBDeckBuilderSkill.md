"""Two-column layout — left/right split with card styling and visual hierarchy."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    FONT_BODY, FONT_SUBHEADER, FONT_SMALL, LIGHT_GREY, MID_GREY, DARK_GREY, TABLE_BORDER,
)
from scripts.slide_builder import (
    add_headline, add_divider_line, add_source, add_footnotes,
    add_textbox, add_bullet_list, add_rectangle, add_rounded_rectangle,
)


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, left: {title?, bullets?, text?, metric?, metric_label?},
           right: {title?, bullets?, text?, metric?, metric_label?},
           source?, footnotes?, divider?: bool}
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    col_gap = Inches(0.3)
    col_width = (CONTENT_WIDTH - col_gap) / 2
    col_height = CONTENT_HEIGHT - Inches(0.2)
    col_top = CONTENT_TOP + Inches(0.1)

    accent_colors = [ds.accent1, ds.accent3]

    for i, (side_key, col_x) in enumerate([
        ("left", CONTENT_LEFT),
        ("right", CONTENT_LEFT + col_width + col_gap),
    ]):
        col_data = data.get(side_key, {})
        if isinstance(col_data, str):
            col_data = {"text": col_data}

        # Card background
        add_rounded_rectangle(
            slide, col_x, col_top,
            col_width, col_height,
            fill_color=LIGHT_GREY,
        )

        # Top accent bar
        add_rectangle(
            slide, col_x, col_top, col_width, Pt(4),
            fill_color=accent_colors[i],
        )

        y = col_top + Inches(0.25)
        inner_left = col_x + Inches(0.25)
        inner_width = col_width - Inches(0.5)

        # Optional metric at top
        metric = col_data.get("metric")
        if metric:
            add_textbox(
                slide, inner_left, y, inner_width, Inches(0.5),
                str(metric), ds,
                font_size=Pt(28), color=accent_colors[i], bold=True,
            )
            if col_data.get("metric_label"):
                add_textbox(
                    slide, inner_left, y + Inches(0.45), inner_width, Inches(0.25),
                    col_data["metric_label"], ds,
                    font_size=FONT_SMALL, color=DARK_GREY,
                )
            y += Inches(0.8)

        # Column title
        title = col_data.get("title")
        if title:
            add_textbox(
                slide, inner_left, y, inner_width, Inches(0.4),
                title, ds,
                font_size=Pt(16), color=ds.primary, bold=True,
            )
            # Separator
            add_rectangle(
                slide, inner_left, y + Inches(0.45), inner_width, Pt(1),
                fill_color=TABLE_BORDER,
            )
            y += Inches(0.6)

        # Bullets or text
        bullets = col_data.get("bullets")
        text = col_data.get("text")
        remaining = (col_top + col_height) - y - Inches(0.2)

        if bullets:
            add_bullet_list(
                slide, inner_left, y,
                inner_width, remaining,
                bullets, ds,
                font_size=FONT_BODY, spacing_pt=8,
            )
        elif text:
            add_textbox(
                slide, inner_left, y,
                inner_width, remaining,
                text, ds,
                font_size=FONT_BODY,
            )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {}
