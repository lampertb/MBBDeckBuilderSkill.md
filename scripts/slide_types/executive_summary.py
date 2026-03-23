"""Executive summary slide — headline + key takeaway bullets with visual hierarchy."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH,
    CONTENT_TOP, CONTENT_HEIGHT,
    FONT_BODY, FONT_SUBHEADER, FONT_SMALL, LIGHT_GREY, MID_GREY, WHITE,
)
from scripts.slide_builder import (
    add_headline, add_divider_line, add_source, add_footnotes,
    add_textbox, add_rectangle, add_rounded_rectangle, add_icon,
)


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, bullets: [str], source?, footnotes?, subtitle?}
    """
    add_headline(slide, data.get("headline", "Executive Summary"), ds)
    add_divider_line(slide, ds)

    # Optional subtitle / framing text
    y = CONTENT_TOP + Inches(0.1)
    subtitle = data.get("subtitle")
    if subtitle:
        add_textbox(
            slide, CONTENT_LEFT, y, CONTENT_WIDTH, Inches(0.4),
            subtitle, ds,
            font_size=FONT_SMALL, color=ds.secondary, italic=True,
        )
        y += Inches(0.5)

    # Bullet points as individual styled items (not a single textbox)
    bullets = data.get("bullets", [])
    if not bullets:
        return {}

    # Calculate spacing to fill content area
    available_height = CONTENT_HEIGHT - (y - CONTENT_TOP) - Inches(0.3)
    item_height = min(available_height / len(bullets), Inches(1.0))
    item_gap = Inches(0.08)

    for i, bullet in enumerate(bullets):
        # Support both string bullets and dict bullets with icon
        if isinstance(bullet, dict):
            bullet_text = bullet.get("text", "")
            bullet_icon = bullet.get("icon")
        else:
            bullet_text = str(bullet)
            bullet_icon = None

        item_y = y + (item_height + item_gap) * i

        # Icon or number indicator on left
        num_size = Inches(0.35)
        num_x = CONTENT_LEFT

        if bullet_icon:
            add_icon(
                slide, num_x, item_y + Inches(0.03),
                num_size, bullet_icon, ds, color=ds.accent1,
            )
        else:
            circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL,
                num_x, item_y + Inches(0.03),
                num_size, num_size,
            )
            circle.fill.solid()
            circle.fill.fore_color.rgb = ds.accent1
            circle.line.fill.background()

            add_textbox(
                slide, num_x, item_y + Inches(0.03),
                num_size, num_size,
                str(i + 1), ds,
                font_size=Pt(12), color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER,
                anchor=None,
            )

        # Bullet text
        text_left = CONTENT_LEFT + Inches(0.55)
        text_width = CONTENT_WIDTH - Inches(0.65)
        add_textbox(
            slide, text_left, item_y,
            text_width, item_height,
            bullet_text, ds,
            font_size=FONT_BODY, color=ds.secondary,
        )

        # Subtle separator line
        if i < len(bullets) - 1:
            sep_y = item_y + item_height + item_gap / 2
            add_rectangle(
                slide, text_left, sep_y,
                text_width, Pt(0.5),
                fill_color=LIGHT_GREY,
            )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {}
