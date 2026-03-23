"""BusyBee sources slide — collects all cited sources from the deck."""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP,
    FONT_SMALL, FONT_FOOTNOTE, MID_GREY,
)
from scripts.slide_builder import add_headline, add_divider_line, add_textbox


def render(slide, data, ds: DesignSystem):
    """
    data: {headline?, _all_sources: [{slide, source, headline}]}
    """
    add_headline(slide, data.get("headline", "Sources & References"), ds)
    add_divider_line(slide, ds)

    sources = data.get("_all_sources", [])
    y = CONTENT_TOP + Inches(0.2)

    if not sources:
        add_textbox(
            slide, CONTENT_LEFT, y, CONTENT_WIDTH, Inches(0.4),
            "No sources cited in this presentation.", ds,
            font_size=FONT_SMALL, color=MID_GREY, italic=True,
        )
        return {}

    for src in sources:
        # Source entry: "[Slide N] Source text — context"
        text = f"[Slide {src['slide']}]  {src['source']}"
        if src.get("headline"):
            text += f"  —  {src['headline'][:80]}"

        add_textbox(
            slide, CONTENT_LEFT + Inches(0.1), y,
            CONTENT_WIDTH - Inches(0.2), Inches(0.35),
            text, ds,
            font_size=FONT_SMALL, color=ds.secondary,
        )
        y += Inches(0.38)

        # Safety: don't overflow the slide
        if y > Inches(6.3):
            add_textbox(
                slide, CONTENT_LEFT + Inches(0.1), y,
                CONTENT_WIDTH - Inches(0.2), Inches(0.3),
                f"... and {len(sources) - sources.index(src) - 1} more sources", ds,
                font_size=FONT_FOOTNOTE, color=MID_GREY, italic=True,
            )
            break

    return {}
