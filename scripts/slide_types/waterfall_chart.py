"""Waterfall chart — revenue walk / cost bridge using stacked bar trick."""

from pptx.util import Inches, Pt
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
    FONT_SMALL, SLATE, POSITIVE_COLOR, NEGATIVE_COLOR,
    resolve_color,
)
from scripts.slide_builder import add_headline, add_divider_line, add_source, add_footnotes


def render(slide, data, ds: DesignSystem):
    """
    data: {headline,
           categories: [str],
           values: [float],  -- positive = increase, negative = decrease
           total_indices?: [int],  -- indices that are running totals (not deltas)
           source?, footnotes?}

    Technique: stacked bar chart with invisible base + colored delta on top.
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    categories = data.get("categories", [])
    values = data.get("values", [])
    total_indices = set(data.get("total_indices", [0, len(values) - 1]))

    if not categories or not values:
        return {}

    # Calculate base (invisible) and delta (visible) for each bar
    bases = []
    deltas = []
    running = 0

    for i, val in enumerate(values):
        if i in total_indices:
            # This is a total bar — show from 0 to the value
            bases.append(0)
            deltas.append(val)
            running = val
        else:
            if val >= 0:
                bases.append(running)
                deltas.append(val)
                running += val
            else:
                running += val
                bases.append(running)
                deltas.append(abs(val))

    # Create stacked bar chart
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series("Base", bases)
    chart_data.add_series("Delta", deltas)

    chart_left = CONTENT_LEFT + Inches(0.2)
    chart_top = CONTENT_TOP + Inches(0.15)
    chart_width = CONTENT_WIDTH - Inches(0.4)
    chart_height = CONTENT_HEIGHT - Inches(0.6)

    chart_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_STACKED,
        chart_left, chart_top, chart_width, chart_height,
        chart_data,
    )
    chart = chart_frame.chart
    chart.has_legend = False

    # Make base series invisible
    base_series = chart.series[0]
    base_fill = base_series.format.fill
    base_fill.background()  # No fill
    base_series.format.line.fill.background()  # No border

    # Color delta series per bar
    delta_series = chart.series[1]
    for i, point in enumerate(delta_series.points):
        fill = point.format.fill
        fill.solid()
        if i in total_indices:
            fill.fore_color.rgb = ds.primary  # Totals in navy
        elif values[i] >= 0:
            fill.fore_color.rgb = POSITIVE_COLOR  # Increases in green
        else:
            fill.fore_color.rgb = NEGATIVE_COLOR  # Decreases in red

    # Data labels on delta series
    delta_series.has_data_labels = True
    labels = delta_series.data_labels
    labels.font.size = FONT_SMALL
    labels.font.name = ds.font_family
    labels.font.color.rgb = SLATE
    labels.position = XL_LABEL_POSITION.OUTSIDE_END

    # Remove gridlines
    chart.value_axis.has_major_gridlines = False
    chart.value_axis.visible = False
    chart.category_axis.tick_labels.font.size = FONT_SMALL
    chart.category_axis.tick_labels.font.name = ds.font_family
    chart.category_axis.tick_labels.font.color.rgb = SLATE

    # Gap width for waterfall appearance
    chart.plots[0].gap_width = 80

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {
        "chart_bounds": {
            "left": int(chart_left),
            "top": int(chart_top),
            "width": int(chart_width),
            "height": int(chart_height),
        },
        "categories": categories,
    }
