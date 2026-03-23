"""
Slide type registry. Maps type names to render functions.
Each slide type module exports: render(slide, data, ds)
"""

from scripts.slide_types.title_hero import render as render_title_hero
from scripts.slide_types.executive_summary import render as render_executive_summary
from scripts.slide_types.section_divider import render as render_section_divider
from scripts.slide_types.agenda import render as render_agenda
from scripts.slide_types.quote_page import render as render_quote_page
from scripts.slide_types.qa_page import render as render_qa_page
from scripts.slide_types.busybee_sources import render as render_busybee_sources
from scripts.slide_types.data_table import render as render_data_table
from scripts.slide_types.bar_chart import render as render_bar_chart
from scripts.slide_types.line_chart import render as render_line_chart
from scripts.slide_types.waterfall_chart import render as render_waterfall_chart
from scripts.slide_types.two_by_two_matrix import render as render_two_by_two_matrix
from scripts.slide_types.key_stat import render as render_key_stat
from scripts.slide_types.two_column import render as render_two_column
from scripts.slide_types.three_column import render as render_three_column
from scripts.slide_types.timeline import render as render_timeline

REGISTRY = {
    "title_hero": render_title_hero,
    "executive_summary": render_executive_summary,
    "section_divider": render_section_divider,
    "agenda": render_agenda,
    "quote_page": render_quote_page,
    "qa_page": render_qa_page,
    "busybee_sources": render_busybee_sources,
    "data_table": render_data_table,
    "bar_chart": render_bar_chart,
    "line_chart": render_line_chart,
    "waterfall_chart": render_waterfall_chart,
    "two_by_two_matrix": render_two_by_two_matrix,
    "key_stat": render_key_stat,
    "two_column": render_two_column,
    "three_column": render_three_column,
    "timeline": render_timeline,
}


def get_render_fn(slide_type: str):
    """Look up a slide type render function. Raises KeyError if not found."""
    if slide_type not in REGISTRY:
        available = ", ".join(sorted(REGISTRY.keys()))
        raise KeyError(f"Unknown slide type '{slide_type}'. Available: {available}")
    return REGISTRY[slide_type]
