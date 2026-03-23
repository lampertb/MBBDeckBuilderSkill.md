# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An MBB consulting-quality PowerPoint generator that produces **native, fully-editable PPTX files** using `python-pptx`. Unlike image-based generators, every element (text, charts, tables, shapes) is a real PowerPoint object that can be edited after generation.

The core innovation is a **two-layer system**: base data (charts, tables) rendered first, then insight overlays (callouts, highlights, metric badges) added on top — the same pattern used by McKinsey, BCG, and Bain consultants.

## Commands

```bash
# Install
pip install -r requirements.txt

# Generate a deck from a plan.json
python3 scripts/generate.py --plan examples/strategic_review.json --output deck.pptx

# Run the QA test suite (regenerates all fixtures)
python3 qa/run_qa.py

# Run a single QA fixture
python3 qa/run_qa.py --fixture bar_chart

# Training loop (extract → regenerate → visual diff)
python3 training/train.py --input training/reference_slides/example.pptx
```

## Architecture

```
scripts/
├── generate.py              # Entry point: plan.json → .pptx
├── design_system.py         # Colors, fonts, spacing, icon map (MBB defaults, theme-overridable)
├── slide_builder.py         # Core primitives: add_headline, add_table, add_chart, add_icon, etc.
├── overlays.py              # Layer 2: callout_annotation, highlight_box, metric_badge, etc.
├── quality_checks.py        # Validates: headline=insight, source present, text fits, color contrast
├── utils.py                 # XML helpers for borders, transparency, cell formatting
└── slide_types/             # One module per slide type, each exports render(slide, data, ds)
    ├── __init__.py          # Registry mapping type names → render functions
    └── *.py                 # 16 slide types
```

**Data flow**: Claude writes a `plan.json` (slide types, headlines, data, overlays) → `generate.py` reads it → dispatches each slide to its type's `render()` function → overlays applied on top → quality checks run → `.pptx` saved.

## The 16 Slide Types

**Structure**: `title_hero`, `executive_summary`, `section_divider`, `agenda`, `quote_page`, `qa_page`, `busybee_sources`

**Data-heavy** (two-layer system): `data_table`, `bar_chart`, `line_chart`, `waterfall_chart`, `two_by_two_matrix`

**Layout**: `key_stat`, `two_column`, `three_column`, `timeline`

## Adding a New Slide Type

1. Create `scripts/slide_types/{name}.py` with `def render(slide, data, ds): ...`
2. Register in `scripts/slide_types/__init__.py`
3. Add a QA fixture in `qa/fixtures/{name}.json`
4. Document the data contract in `references/slide-type-catalog.md`

Use `slide_builder` primitives — don't call python-pptx directly. Use `ds.*` for colors/fonts (not hardcoded values) to respect theme overrides. Return a context dict if the slide type supports overlays.

## MBB Design Principles Encoded

These are baked into `design_system.py` and enforced by `quality_checks.py`:

- **Headline = Takeaway**: Every headline must be an insight ("Revenue grew 18% driven by enterprise expansion"), never a label ("Revenue Analysis"). Quality checker warns if <6 words or missing a verb.
- **Two Layers**: Base data first, then overlays (callouts, highlights, badges) on top via z-order insertion.
- **Source Required**: Every data slide must cite its source (8pt italic, bottom-left). Quality checker warns if missing.
- **Typography Hierarchy**: Headlines 28pt bold Navy, body 14pt Slate, source 8pt italic — headers always ≥2 sizes larger than body.
- **Color Contrast**: Navy (#1B2A4A) on white, Slate (#334155) on light grey. Never MID_GREY text on LIGHT_GREY backgrounds (discovered and fixed in testing).
- **Whitespace**: 0.75" side margins, content area fills 1.30"-6.45" vertically. Cards/columns expand to fill available space.
- **Tables**: No vertical borders, alternating row shading (#F8FAFC/white), right-aligned numbers, bold header with navy bottom border.
- **Charts**: Max 3 colors from viz palette, direct value labels (no legends when single series), no gridlines on bar charts.

## Theme Override

Any deck can override the MBB defaults via a `"theme"` block in plan.json:

```json
{
  "theme": {
    "font": "Inter",
    "primary": "#1A365D",
    "accent1": "#38B2AC"
  },
  "slides": [...]
}
```

## Icons

53 Lucide SVG icons in `assets/icons/` (ISC/MIT license). The `add_icon()` function tries SVG first (if `cairosvg` installed), falls back to Unicode characters from the `ICON_MAP` in `design_system.py`. Icons are optional on all slide types — pass `"icon": "trending-up"` in the data.

## Training Loop

Drop real MBB slides (`.pptx`) into `training/reference_slides/`, then run `python3 training/train.py`. The pipeline: extracts content → converts to plan.json → regenerates → visual diff → training report with specific improvement suggestions.
