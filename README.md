# MBB Deck Builder

Generate McKinsey/BCG/Bain-quality PowerPoint presentations with native, fully-editable slides. Every element — text, charts, tables, shapes — is a real PowerPoint object you can edit after generation.

## What Makes This Different

Most AI slide generators produce images or non-editable content. This tool generates **native PPTX** with a **two-layer system** that mirrors how MBB consultants actually build slides:

- **Layer 1 (Base Data)**: Charts, tables, structured content
- **Layer 2 (Insight Overlays)**: Callout annotations, color-coded highlights, metric badges, delta indicators — layered on top

Every slide enforces the MBB partner test: headline is a takeaway message (not a label), data has sources, typography has proper hierarchy, and content fills the page.

## Quick Start

```bash
git clone https://github.com/lampertb/MBBDeckBuilderSkill.md.git
cd MBBDeckBuilderSkill.md
pip install -r requirements.txt

# Generate the example FY2024 Strategic Review deck (17 slides)
python3 scripts/generate.py --plan examples/strategic_review.json --output deck.pptx

# Or the PE Due Diligence deck (16 slides)
python3 scripts/generate.py --plan examples/pe_due_diligence.json --output diligence.pptx
```

Open the `.pptx` in PowerPoint — everything is editable.

## 16 Slide Types

| Category | Types |
|----------|-------|
| **Structure** | `title_hero`, `executive_summary`, `section_divider`, `agenda`, `quote_page`, `qa_page`, `busybee_sources` |
| **Data** | `data_table`, `bar_chart`, `line_chart`, `waterfall_chart`, `two_by_two_matrix` |
| **Layout** | `key_stat`, `two_column`, `three_column`, `timeline` |

## 6 Overlay Types

Add to any slide via the `"overlays"` field:

| Overlay | Use Case |
|---------|----------|
| `callout_annotation` | "+$72M YoY" pointing at a chart bar |
| `highlight_box` | Semi-transparent rectangle grouping items |
| `metric_badge` | Big number badge ("$830M Total Revenue") |
| `bracket_group` | Bracket grouping table rows with a label |
| `color_band` | Color-code specific table rows |
| `delta_indicator` | ▲/▼ arrows with values |

## How It Works

You write a `plan.json` describing your deck, and the generator renders it:

```json
{
  "title": "Q4 Board Review",
  "slides": [
    {
      "type": "bar_chart",
      "headline": "Enterprise segment drove 72% of revenue growth in FY2024",
      "categories": ["Enterprise", "Mid-Market", "SMB"],
      "series": [{"name": "Revenue ($M)", "values": [480, 210, 95]}],
      "source": "Finance, FY2024 actuals",
      "overlays": [
        {"type": "callout_annotation", "text": "+$72M YoY", "x": 2.0, "y": 1.5, "color": "teal"},
        {"type": "metric_badge", "value": "$830M", "label": "Total Revenue", "x": 10.0, "y": 1.4}
      ]
    }
  ]
}
```

```bash
python3 scripts/generate.py --plan plan.json --output deck.pptx
```

The generator also runs quality checks — warns if headlines are labels instead of insights, data slides are missing sources, or text may overflow.

## Theme Override

Default palette is MBB Navy/Teal/Amber. Override per deck:

```json
{
  "theme": {
    "font": "Inter",
    "primary": "#1A365D",
    "accent1": "#38B2AC",
    "accent2": "#D97706"
  },
  "slides": [...]
}
```

## Using with Claude Code

This project is also a Claude Code skill. Add the `SKILL.md` to your Claude Code setup, and Claude will:
1. Take your data/research
2. Write the `plan.json` (choosing slide types, writing takeaway headlines, placing overlays)
3. Run the generator
4. Iterate based on your feedback

## Icons

53 [Lucide](https://lucide.dev/) SVG icons included (`assets/icons/`, ISC license). Pass `"icon": "trending-up"` on supported slide types (exec summary, three-column, key stat).

## Training Loop

Improve the generator by comparing against real MBB slides:

```bash
# Drop reference .pptx files into training/reference_slides/
python3 training/train.py
```

Pipeline: extract content → regenerate → visual diff → training report with improvement suggestions.

## QA Suite

```bash
python3 qa/run_qa.py           # Run all 17 fixtures
python3 qa/run_qa.py --fixture bar_chart  # Run one
```

## Project Structure

```
scripts/
├── generate.py          # Entry point: plan.json → .pptx
├── design_system.py     # Colors, fonts, spacing, icons (theme-overridable)
├── slide_builder.py     # Primitives: add_headline, add_table, add_chart, add_icon
├── overlays.py          # Layer 2: callouts, highlights, badges, brackets
├── quality_checks.py    # MBB partner-test validation
├── utils.py             # XML helpers for borders, transparency
└── slide_types/         # One module per slide type
examples/                # Ready-to-run plan.json files
qa/                      # Test fixtures and runner
training/                # Extract → regenerate → diff loop
assets/icons/            # 53 Lucide SVG icons (ISC license)
```

## Adding Slide Types

1. Create `scripts/slide_types/{name}.py` with `def render(slide, data, ds)`
2. Register in `scripts/slide_types/__init__.py`
3. Add a fixture in `qa/fixtures/{name}.json`

See `references/adding-slide-types.md` for the template.

## License

MIT
