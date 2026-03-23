"""
MBB Design System — single source of truth for all visual constants.
Defaults follow McKinsey/BCG/Deloitte design principles.
All values overridable via theme block in plan.json.
"""

from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


# ---------------------------------------------------------------------------
# Slide dimensions (16:9)
# ---------------------------------------------------------------------------
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# ---------------------------------------------------------------------------
# Margins & zones
# ---------------------------------------------------------------------------
MARGIN_LEFT = Inches(0.75)
MARGIN_RIGHT = Inches(0.75)
MARGIN_TOP = Inches(0.4)
MARGIN_BOTTOM = Inches(0.35)

CONTENT_LEFT = MARGIN_LEFT
CONTENT_WIDTH = SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT  # ~11.833"

# Headline zone — tall enough for 2 lines of 24pt wrapped text
HEADLINE_TOP = Inches(0.25)
HEADLINE_HEIGHT = Inches(0.85)
HEADLINE_LEFT = MARGIN_LEFT
HEADLINE_WIDTH = CONTENT_WIDTH

# Divider line below headline
DIVIDER_TOP = Inches(1.15)

# Content zone (below divider, above footnote)
CONTENT_TOP = Inches(1.30)
CONTENT_BOTTOM = Inches(6.45)
CONTENT_HEIGHT = CONTENT_BOTTOM - CONTENT_TOP  # ~5.15"

# Footnote zone
FOOTNOTE_TOP = Inches(6.55)
FOOTNOTE_HEIGHT = Inches(0.35)

# Source zone
SOURCE_TOP = Inches(6.95)
SOURCE_HEIGHT = Inches(0.3)

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONT_FAMILY = "Calibri"

FONT_HEADLINE = Pt(28)
FONT_SECTION_HEADER = Pt(24)
FONT_SUBHEADER = Pt(18)
FONT_BODY = Pt(14)
FONT_SMALL = Pt(11)
FONT_FOOTNOTE = Pt(10)
FONT_SOURCE = Pt(8)

# ---------------------------------------------------------------------------
# Colors — Dark Authority palette
# ---------------------------------------------------------------------------
NAVY = RGBColor(0x1B, 0x2A, 0x4A)
SLATE = RGBColor(0x33, 0x41, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY = RGBColor(0xF8, 0xFA, 0xFC)
MID_GREY = RGBColor(0xCB, 0xD5, 0xE1)
DARK_GREY = RGBColor(0x64, 0x74, 0x8B)

# Accent palette
TEAL = RGBColor(0x0D, 0x94, 0x88)
AMBER = RGBColor(0xD9, 0x77, 0x06)
BLUE = RGBColor(0x25, 0x63, 0xEB)
CRIMSON = RGBColor(0xDC, 0x26, 0x26)
PURPLE = RGBColor(0x7C, 0x3A, 0xED)
GREEN = RGBColor(0x05, 0x96, 0x69)

# Data visualization palette (sequential, max 3 per chart)
VIZ_PALETTE = [BLUE, TEAL, PURPLE, AMBER, CRIMSON, GREEN]

# Table styling
TABLE_HEADER_BG = NAVY
TABLE_HEADER_FG = WHITE
TABLE_ALT_ROW = LIGHT_GREY
TABLE_BORDER = RGBColor(0xE2, 0xE8, 0xF0)

# Positive / negative indicators
POSITIVE_COLOR = GREEN
NEGATIVE_COLOR = CRIMSON

# ---------------------------------------------------------------------------
# Icon map — Unicode symbols for native PowerPoint rendering
# ---------------------------------------------------------------------------
ICON_MAP = {
    "chart": "\u2637",       # ☷ trigram (clean geometric)
    "growth": "\u2197",      # ↗ arrow
    "decline": "\u2198",     # ↘ arrow
    "target": "\u25CE",      # ◎ bullseye
    "check": "\u2713",       # ✓ checkmark
    "warning": "\u26A0",     # ⚠ warning
    "people": "\u2616",      # ☖ (person-like)
    "gear": "\u2699",        # ⚙ gear
    "dollar": "$",           # dollar sign
    "euro": "\u20AC",        # € euro
    "clock": "\u23F1",       # ⏱ stopwatch
    "globe": "\u2295",       # ⊕ circled plus (clean geometric)
    "lock": "\u2317",        # ⌗ viewdata square
    "lightbulb": "\u2605",   # ★ star (substitute)
    "arrow_right": "\u2192", # → right arrow
    "arrow_up": "\u2191",    # ↑ up arrow
    "arrow_down": "\u2193",  # ↓ down arrow
    "star": "\u2605",        # ★ filled star
    "diamond": "\u25C6",     # ◆ filled diamond
    "square": "\u25A0",      # ■ filled square
    "circle": "\u25CF",      # ● filled circle
    "triangle": "\u25B2",    # ▲ filled triangle
    "minus": "\u2212",       # − minus
    "plus": "+",             # plus
    "bar_chart": "\u2581\u2583\u2585\u2587",  # ▁▃▅▇ block bar chart
    "shield": "\u25B3",      # △ triangle (shield-like)
    "building": "\u25A3",    # ▣ square with grid
    "handshake": "\u2194",   # ↔ bidirectional arrow
    "rocket": "\u25B2",      # ▲ upward triangle
}

# ---------------------------------------------------------------------------
# Named color lookup (for plan.json references)
# ---------------------------------------------------------------------------
COLOR_MAP = {
    "navy": NAVY,
    "slate": SLATE,
    "white": WHITE,
    "light_grey": LIGHT_GREY,
    "mid_grey": MID_GREY,
    "dark_grey": DARK_GREY,
    "teal": TEAL,
    "amber": AMBER,
    "blue": BLUE,
    "crimson": CRIMSON,
    "purple": PURPLE,
    "green": GREEN,
}


def resolve_color(value):
    """Resolve a color from name string, hex string, or RGBColor."""
    if isinstance(value, RGBColor):
        return value
    if isinstance(value, str):
        # Named color
        lower = value.lower().replace("-", "_").replace(" ", "_")
        if lower in COLOR_MAP:
            return COLOR_MAP[lower]
        # Hex color
        hex_str = value.lstrip("#")
        if len(hex_str) == 6:
            return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))
    raise ValueError(f"Cannot resolve color: {value}")


# ---------------------------------------------------------------------------
# Theme override support
# ---------------------------------------------------------------------------
class DesignSystem:
    """Holds all design constants. Initialize with optional theme overrides."""

    def __init__(self, theme: dict | None = None):
        theme = theme or {}

        # Font
        self.font_family = theme.get("font", FONT_FAMILY)

        # Colors
        self.primary = resolve_color(theme["primary"]) if "primary" in theme else NAVY
        self.secondary = resolve_color(theme["secondary"]) if "secondary" in theme else SLATE
        self.accent1 = resolve_color(theme["accent1"]) if "accent1" in theme else TEAL
        self.accent2 = resolve_color(theme["accent2"]) if "accent2" in theme else AMBER
        self.accent3 = resolve_color(theme["accent3"]) if "accent3" in theme else BLUE
        self.accent4 = resolve_color(theme["accent4"]) if "accent4" in theme else CRIMSON
        self.background = resolve_color(theme["background"]) if "background" in theme else WHITE
        self.alt_row = resolve_color(theme["alt_row"]) if "alt_row" in theme else TABLE_ALT_ROW

        self.viz_palette = [self.accent3, self.accent1, PURPLE, self.accent2, self.accent4, GREEN]

        # Typography sizes (allow override)
        self.font_headline = Pt(theme.get("headline_size", 28))
        self.font_body = Pt(theme.get("body_size", 14))
        self.font_source = FONT_SOURCE
        self.font_footnote = FONT_FOOTNOTE
