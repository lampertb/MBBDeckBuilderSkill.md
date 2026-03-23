"""Timeline slide — horizontal milestones with content cards and visual connectors."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    FONT_BODY, FONT_SMALL, FONT_SUBHEADER, FONT_FOOTNOTE,
    LIGHT_GREY, WHITE, MID_GREY, DARK_GREY,
)
from scripts.slide_builder import (
    add_headline, add_divider_line, add_source, add_footnotes,
    add_textbox, add_rectangle, add_rounded_rectangle,
)


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, milestones: [{date, title, description?, status?}],
           source?, footnotes?}
    status: "complete" | "in_progress" | "upcoming" (affects styling)
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    milestones = data.get("milestones", [])
    if not milestones:
        return {}

    num = len(milestones)

    # Layout geometry
    line_y = CONTENT_TOP + Inches(1.6)  # Horizontal timeline bar
    line_left = CONTENT_LEFT + Inches(0.3)
    line_width = CONTENT_WIDTH - Inches(0.6)
    bar_height = Inches(0.08)

    # Timeline progress bar background (grey)
    add_rounded_rectangle(
        slide, line_left, line_y, line_width, bar_height,
        fill_color=MID_GREY,
    )

    # Colored progress overlay (if any milestones have status)
    complete_count = sum(1 for m in milestones if m.get("status") == "complete")
    if complete_count > 0:
        progress_width = line_width * (complete_count / num)
        add_rounded_rectangle(
            slide, line_left, line_y, progress_width, bar_height,
            fill_color=ds.accent1,
        )

    # Space milestones evenly
    if num > 1:
        spacing = line_width / (num - 1)
    else:
        spacing = Inches(0)

    # Card dimensions
    card_width = min(Inches(2.2), line_width / num - Inches(0.05))
    card_above_height = Inches(1.1)
    card_below_height = Inches(2.8)

    for i, ms in enumerate(milestones):
        status = ms.get("status", "upcoming")

        # X position
        if num == 1:
            cx = line_left + line_width / 2
        else:
            cx = line_left + spacing * i

        # Dot on timeline
        dot_size = Inches(0.2)
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            cx - dot_size / 2, line_y - dot_size / 2 + bar_height / 2,
            dot_size, dot_size,
        )
        dot.fill.solid()
        if status == "complete":
            dot.fill.fore_color.rgb = ds.accent1
        elif status == "in_progress":
            dot.fill.fore_color.rgb = ds.accent3
        else:
            dot.fill.fore_color.rgb = WHITE
        dot.line.color.rgb = ds.accent1
        dot.line.width = Pt(2)

        # Date label — always above the timeline
        date_y = line_y - Inches(0.4)
        add_textbox(
            slide, cx - card_width / 2, date_y,
            card_width, Inches(0.25),
            ms.get("date", ""), ds,
            font_size=FONT_SMALL, color=ds.accent1, bold=True,
            alignment=PP_ALIGN.CENTER,
        )

        # Vertical connector line from dot down to card
        connector_top = line_y + bar_height + dot_size / 2
        connector_height = Inches(0.3)
        add_rectangle(
            slide, cx - Pt(1), connector_top,
            Pt(2), connector_height,
            fill_color=MID_GREY,
        )

        # Content card below timeline
        card_top = connector_top + connector_height
        card_x = cx - card_width / 2

        # Card background with left accent border
        add_rounded_rectangle(
            slide, card_x, card_top,
            card_width, card_below_height,
            fill_color=LIGHT_GREY,
        )

        # Left accent bar on card
        accent_colors = [ds.accent1, ds.accent3, ds.accent2, ds.primary, ds.accent1]
        accent = accent_colors[i % len(accent_colors)]
        add_rectangle(
            slide, card_x, card_top,
            Pt(4), card_below_height,
            fill_color=accent,
        )

        # Title in card
        add_textbox(
            slide, card_x + Inches(0.15), card_top + Inches(0.1),
            card_width - Inches(0.3), Inches(0.35),
            ms.get("title", ""), ds,
            font_size=FONT_BODY, color=ds.primary, bold=True,
        )

        # Description in card
        desc = ms.get("description", "")
        if desc:
            add_textbox(
                slide, card_x + Inches(0.15), card_top + Inches(0.5),
                card_width - Inches(0.3), card_below_height - Inches(0.65),
                desc, ds,
                font_size=FONT_SMALL, color=ds.secondary,
            )

        # Status badge (if provided)
        if status == "complete":
            badge_text = "\u2713 Complete"
            badge_color = ds.accent1
        elif status == "in_progress":
            badge_text = "\u25CB In Progress"
            badge_color = ds.accent3
        else:
            badge_text = ""
            badge_color = DARK_GREY

        if badge_text:
            add_textbox(
                slide, card_x + Inches(0.15),
                card_top + card_below_height - Inches(0.35),
                card_width - Inches(0.3), Inches(0.25),
                badge_text, ds,
                font_size=FONT_FOOTNOTE, color=badge_color, bold=True,
            )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {}
