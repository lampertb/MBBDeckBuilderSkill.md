"""2x2 matrix — BCG matrix, priority matrix with quadrant labels and item placement."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    FONT_BODY, FONT_SMALL, FONT_SUBHEADER, FONT_FOOTNOTE,
    LIGHT_GREY, WHITE, MID_GREY, NAVY, resolve_color,
)
from scripts.slide_builder import (
    add_headline, add_divider_line, add_source, add_footnotes,
    add_textbox, add_rectangle, add_rounded_rectangle,
)


def render(slide, data, ds: DesignSystem):
    """
    data: {headline,
           x_axis_label, y_axis_label,
           quadrants: [{label, description?, color?}],  -- TL, TR, BL, BR order
           items?: [{name, quadrant: "TL"|"TR"|"BL"|"BR", x?: float, y?: float}],
           source?, footnotes?}
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    # Matrix dimensions
    matrix_left = CONTENT_LEFT + Inches(0.8)  # Leave room for Y axis label
    matrix_top = CONTENT_TOP + Inches(0.3)
    matrix_width = CONTENT_WIDTH - Inches(1.6)
    matrix_height = Inches(4.6)

    half_w = matrix_width / 2
    half_h = matrix_height / 2
    gap = Inches(0.06)

    # Quadrant positions: TL, TR, BL, BR
    quadrant_positions = [
        (matrix_left, matrix_top),                              # TL
        (matrix_left + half_w + gap, matrix_top),               # TR
        (matrix_left, matrix_top + half_h + gap),               # BL
        (matrix_left + half_w + gap, matrix_top + half_h + gap), # BR
    ]

    quadrants = data.get("quadrants", [
        {"label": ""}, {"label": ""}, {"label": ""}, {"label": ""},
    ])

    # Default quadrant colors (light tints)
    default_colors = [
        LIGHT_GREY, LIGHT_GREY, LIGHT_GREY, LIGHT_GREY,
    ]

    for i, (qx, qy) in enumerate(quadrant_positions):
        q_data = quadrants[i] if i < len(quadrants) else {"label": ""}
        color = resolve_color(q_data["color"]) if "color" in q_data else default_colors[i]

        # Quadrant background
        add_rounded_rectangle(
            slide, qx, qy, half_w - gap, half_h - gap,
            fill_color=color,
        )

        # Quadrant label
        if q_data.get("label"):
            add_textbox(
                slide, qx + Inches(0.2), qy + Inches(0.15),
                half_w - gap - Inches(0.4), Inches(0.4),
                q_data["label"], ds,
                font_size=FONT_SUBHEADER, color=ds.primary, bold=True,
            )

        # Quadrant description
        if q_data.get("description"):
            add_textbox(
                slide, qx + Inches(0.2), qy + Inches(0.55),
                half_w - gap - Inches(0.4), Inches(0.6),
                q_data["description"], ds,
                font_size=FONT_SMALL, color=ds.secondary,
            )

    # Axis labels
    # X-axis (bottom)
    x_label = data.get("x_axis_label", "")
    if x_label:
        add_textbox(
            slide, matrix_left, matrix_top + matrix_height + Inches(0.15),
            matrix_width, Inches(0.35),
            x_label, ds,
            font_size=FONT_BODY, color=ds.secondary, bold=True,
            alignment=PP_ALIGN.CENTER,
        )
        # Arrow indicator (Low → High)
        add_textbox(
            slide, matrix_left, matrix_top + matrix_height + Inches(0.4),
            matrix_width, Inches(0.25),
            "Low  \u2192  High", ds,
            font_size=FONT_FOOTNOTE, color=MID_GREY,
            alignment=PP_ALIGN.CENTER,
        )

    # Y-axis (left, rotated text simulated with narrow box)
    y_label = data.get("y_axis_label", "")
    if y_label:
        # Place vertically along left side
        add_textbox(
            slide, CONTENT_LEFT, matrix_top + matrix_height / 2 - Inches(0.5),
            Inches(0.7), Inches(1.0),
            y_label, ds,
            font_size=FONT_BODY, color=ds.secondary, bold=True,
            alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        )
        add_textbox(
            slide, CONTENT_LEFT, matrix_top + matrix_height / 2 + Inches(0.4),
            Inches(0.7), Inches(0.25),
            "Low \u2192 High", ds,
            font_size=FONT_FOOTNOTE, color=MID_GREY,
            alignment=PP_ALIGN.CENTER,
        )

    # Plot items as dots/labels
    items = data.get("items", [])
    quadrant_map = {"TL": 0, "TR": 1, "BL": 2, "BR": 3}

    for item in items:
        q_key = item.get("quadrant", "TL")
        q_idx = quadrant_map.get(q_key, 0)
        qx, qy = quadrant_positions[q_idx]

        # Position within quadrant (0-1 scale, default center)
        rel_x = item.get("x", 0.5)
        rel_y = item.get("y", 0.5)
        item_x = qx + Inches(0.3) + (half_w - gap - Inches(0.6)) * rel_x
        item_y = qy + Inches(0.8) + (half_h - gap - Inches(1.2)) * rel_y

        # Dot
        dot_size = Inches(0.25)
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, item_x, item_y, dot_size, dot_size,
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = ds.accent1
        dot.line.fill.background()

        # Label
        add_textbox(
            slide, item_x + Inches(0.3), item_y - Inches(0.05),
            Inches(1.5), Inches(0.3),
            item.get("name", ""), ds,
            font_size=FONT_SMALL, color=ds.primary, bold=True,
        )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {}
