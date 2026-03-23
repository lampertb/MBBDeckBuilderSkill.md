"""Bar/column chart slide with overlay support."""

from pptx.util import Inches, Pt
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
)
from scripts.slide_builder import (
    add_headline, add_divider_line, add_source, add_footnotes,
    add_bar_chart,
)


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, categories: [str], series: [{name, values, color?}],
           orientation?: "vertical"|"horizontal", show_values?: bool,
           value_format?: str, source?, footnotes?}
    Returns context with chart bounds for overlay positioning.
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    categories = data.get("categories", [])
    series_list = data.get("series", [])

    if not categories or not series_list:
        return {}

    chart_left = CONTENT_LEFT + Inches(0.2)
    chart_top = CONTENT_TOP + Inches(0.15)
    chart_width = CONTENT_WIDTH - Inches(0.4)
    chart_height = CONTENT_HEIGHT - Inches(0.6)

    chart_frame = add_bar_chart(
        slide, chart_left, chart_top, chart_width, chart_height,
        categories, series_list, ds,
        orientation=data.get("orientation", "vertical"),
        show_values=data.get("show_values", True),
        value_format=data.get("value_format"),
    )

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    # Return chart bounds for overlay positioning
    return {
        "chart_bounds": {
            "left": int(chart_left),
            "top": int(chart_top),
            "width": int(chart_width),
            "height": int(chart_height),
        },
        "categories": categories,
    }
