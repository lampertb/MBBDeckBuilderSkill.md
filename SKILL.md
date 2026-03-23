---
name: mbb-pptx-generator
description: >
  Generate MBB consulting-quality PowerPoint presentations with native, editable slides.
  Use when the user asks to create presentations, slide decks, board papers, or strategy
  documents that need McKinsey/BCG/Bain-level quality. Produces native PPTX with real
  charts, tables, and a two-layer system (base data + insight overlays/callouts).
  Slides pass the MBB partner/EM test: takeaway headlines, layered data, sources,
  footnotes, and proper typography hierarchy.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
user-invocable: true
metadata:
  author: ben
  version: "1.0"
  requires:
    pip:
      - python-pptx
---

# MBB PPTX Generator

Generate consulting-grade PowerPoint presentations with native, fully-editable slides.

## When to Use

Activate when the user:
- Asks to create a presentation, slide deck, or PPT
- Needs "consulting quality", "MBB quality", "partner-ready", or "board-ready" slides
- Has data/research and wants it turned into a professional deck
- Asks for a strategy presentation, quarterly review, investment memo, etc.

## Invocation

```bash
/mbb-pptx-generator                          # Interactive: ask user for content
/mbb-pptx-generator "topic or content"        # Generate from provided content
```

## Core Principles (The Partner Test)

Every slide must pass these checks:

1. **Headline = Takeaway**: Every headline is an insight, not a label
   - BAD: "Revenue Analysis"
   - GOOD: "Enterprise revenue grew 18% driven by healthcare vertical expansion"

2. **Two Layers of Data**: Base data (chart, table) PLUS insight overlays on top
   - Callout annotations ("+$72M YoY")
   - Color-coded groupings ("Declining segments")
   - Metric badges ("$830M Total Revenue")
   - Delta indicators (▲ +18%, ▼ -3pp)

3. **Text Fits**: All text must be readable and within bounds

4. **Sources**: Every data slide must cite its source (8pt italic, bottom-left)

5. **Footnotes**: If caveats exist, add them (10pt, above source line)

6. **Typography Hierarchy**: Headlines are 28pt bold; body is 14pt (2x size difference)

## Workflow

### Step 1: Understand the Content

Ask the user:
- What is the presentation about? What story are we telling?
- What data/research do they have? (numbers, analyses, findings)
- Who is the audience? (board, investors, leadership team, clients)
- How many slides? (default: 10-15)
- Any specific theme/branding? (default: MBB Navy/Teal palette)

### Step 2: Create plan.json

Build the deck plan as JSON. This is where your judgment matters most — selecting the right slide types, writing insight-driven headlines, and deciding what overlays to add.

**Common deck structures:**

Executive Review (12-15 slides):
```
title_hero → agenda → section_divider → executive_summary →
key_stat → bar_chart (with overlays) → data_table (with overlays) →
section_divider → two_by_two_matrix → three_column →
timeline → quote_page → busybee_sources → qa_page
```

Strategy Presentation (10-12 slides):
```
title_hero → executive_summary → key_stat →
section_divider → two_column → bar_chart →
waterfall_chart → two_by_two_matrix → timeline →
busybee_sources → qa_page
```

### Step 3: Generate

Determine this SKILL.md file's directory path as `{baseDir}`.

```bash
python3 {baseDir}/scripts/generate.py --plan plan.json --output deck.pptx
```

### Step 4: Review Quality Output

The generator prints quality warnings. Fix any issues by modifying plan.json and regenerating.

### Step 5: Deliver & Iterate

Share the .pptx. User can edit natively in PowerPoint — all text, charts, tables are editable.

## plan.json Specification

```json
{
  "title": "Deck Title",
  "author": "Author Name",
  "date": "March 2026",
  "theme": {
    "font": "Calibri",
    "primary": "#1B2A4A",
    "accent1": "#0D9488",
    "accent2": "#D97706",
    "accent3": "#2563EB"
  },
  "slides": [...]
}
```

**Theme is optional.** Defaults to MBB Navy/Teal palette with Calibri. Override any field to customize.

### Common Fields (all slide types)

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | Slide type name |
| `headline` | Yes* | Takeaway message (*optional for title_hero, section_divider, qa_page, quote_page) |
| `source` | No | Source attribution (8pt italic at bottom) |
| `footnotes` | No | Array of footnote strings |
| `overlays` | No | Array of overlay specs (Layer 2) |

## Slide Types

### Structure Slides

#### `title_hero`
Cover slide with title, subtitle, date, author.
```json
{"type": "title_hero", "headline": "Deck Title", "subtitle": "...", "author": "...", "date": "..."}
```

#### `executive_summary`
3-5 key takeaway bullets.
```json
{"type": "executive_summary", "headline": "Three forces reshaping...", "bullets": ["...", "..."], "source": "..."}
```

#### `section_divider`
Navy background section break.
```json
{"type": "section_divider", "headline": "Financial Performance", "subtitle": "...", "section_number": 1}
```

#### `agenda`
Numbered agenda with optional highlight.
```json
{"type": "agenda", "headline": "Today's Discussion",
 "items": [{"title": "Topic", "description": "Details"}], "current_item": 1}
```

#### `quote_page`
Featured quote with attribution.
```json
{"type": "quote_page", "quote": "...", "attribution": "Name", "title": "Role"}
```

#### `qa_page`
Discussion closing slide.
```json
{"type": "qa_page", "headline": "Questions & Discussion", "subtitle": "contact@email.com"}
```

#### `busybee_sources`
Auto-collects all sources cited in the deck. Place as the second-to-last slide.
```json
{"type": "busybee_sources"}
```

### Data-Heavy Slides

#### `data_table`
Clean MBB table (no vertical borders, alternating rows, right-aligned numbers).
```json
{"type": "data_table", "headline": "Mid-market churn concentrated in accounts under $50K",
 "headers": ["Segment", "Lost", "Revenue Impact"],
 "rows": [["<$25K", "180", "$3.2M"], ["$25-50K", "110", "$4.1M"]],
 "col_widths": [2.5, 1.5, 2.0],
 "source": "Customer Success, H2 FY2024",
 "overlays": [
   {"type": "color_band", "row_indices": [1, 2], "color": "crimson"},
   {"type": "callout_annotation", "text": "85% under $50K ACV", "x": 8.5, "y": 1.5}
 ]}
```

#### `bar_chart`
Native bar/column chart with overlay support.
```json
{"type": "bar_chart", "headline": "Enterprise drove 72% of growth",
 "categories": ["Enterprise", "Mid-Market", "SMB"],
 "series": [{"name": "FY24 ($M)", "values": [480, 210, 95], "color": "blue"}],
 "orientation": "vertical", "show_values": true,
 "source": "Finance, FY2024",
 "overlays": [
   {"type": "callout_annotation", "text": "+$72M", "x": 2.0, "y": 1.5, "color": "teal"},
   {"type": "metric_badge", "value": "$830M", "label": "Total", "x": 10.0, "y": 1.4}
 ]}
```

#### `line_chart`
Trend lines with annotations.
```json
{"type": "line_chart", "headline": "Growth accelerated each quarter",
 "categories": ["Q1", "Q2", "Q3", "Q4"],
 "series": [{"name": "Revenue", "values": [195, 205, 212, 218], "color": "blue"}],
 "source": "Finance, quarterly actuals"}
```

#### `waterfall_chart`
Revenue walk / cost bridge.
```json
{"type": "waterfall_chart", "headline": "EBITDA declined $8M due to AI investment",
 "categories": ["FY23 EBITDA", "Revenue", "COGS", "AI Invest", "FY24 EBITDA"],
 "values": [177, 48, -12, -42, 186],
 "total_indices": [0, 4],
 "source": "Finance, P&L bridge"}
```

#### `two_by_two_matrix`
BCG-style matrix with items plotted in quadrants.
```json
{"type": "two_by_two_matrix", "headline": "Two high-impact, high-feasibility initiatives",
 "x_axis_label": "Feasibility", "y_axis_label": "Impact",
 "quadrants": [
   {"label": "Invest", "description": "High impact, hard"},
   {"label": "Quick Wins", "description": "High impact, easy"},
   {"label": "Deprioritize", "description": "Low impact, hard"},
   {"label": "Incremental", "description": "Low impact, easy"}
 ],
 "items": [
   {"name": "AI Platform", "quadrant": "TL", "x": 0.3, "y": 0.3},
   {"name": "Healthcare", "quadrant": "TR", "x": 0.6, "y": 0.4}
 ]}
```

### Layout Slides

#### `key_stat`
1-3 hero metrics with delta indicators.
```json
{"type": "key_stat", "headline": "Revenue reached $830M, up 15% YoY",
 "stats": [
   {"value": "$830M", "label": "Revenue", "delta": "+15%", "context": "vs $722M FY23"},
   {"value": "87%", "label": "Retention", "delta": "-3pp"}
 ], "source": "Finance"}
```

#### `two_column`
Left/right comparison.
```json
{"type": "two_column", "headline": "Healthcare presents $2.4B TAM",
 "left": {"title": "Opportunity", "bullets": ["$2.4B TAM", "12% CAGR"]},
 "right": {"title": "Advantages", "bullets": ["6 of top 10 relationships", "HIPAA ready"]}}
```

#### `three_column`
Triple parallel concepts with card-style layout.
```json
{"type": "three_column", "headline": "Three bets drive next phase",
 "columns": [
   {"title": "AI Platform", "bullets": ["$50M ARR target", "$28M investment"]},
   {"title": "Healthcare", "bullets": ["$35M ARR target", "$15M investment"]},
   {"title": "International", "bullets": ["$150M ARR target", "$20M investment"]}
 ]}
```

#### `timeline`
Horizontal milestones (alternating above/below for readability).
```json
{"type": "timeline", "headline": "18-month implementation roadmap",
 "milestones": [
   {"date": "Q1 FY25", "title": "Foundation", "description": "Hire key roles"},
   {"date": "Q2 FY25", "title": "Alpha", "description": "First pilot customers"}
 ]}
```

## Overlay System (Layer 2)

Overlays add insight annotations on top of base data. Add to any slide via `"overlays": [...]`.

| Type | Fields | Example |
|------|--------|---------|
| `callout_annotation` | text, x, y, color?, width?, height? | `{"type": "callout_annotation", "text": "+$72M", "x": 2.0, "y": 1.5}` |
| `highlight_box` | x, y, width, height, color?, opacity?, label? | `{"type": "highlight_box", "x": 1, "y": 2, "width": 3, "height": 2, "label": "Focus area"}` |
| `metric_badge` | value, label, x, y, color?, delta? | `{"type": "metric_badge", "value": "$830M", "label": "Revenue", "x": 10, "y": 1.4}` |
| `bracket_group` | x, y_start, y_end, label, color? | `{"type": "bracket_group", "x": 11, "y_start": 2, "y_end": 4, "label": "Core"}` |
| `color_band` | row_indices, color | `{"type": "color_band", "row_indices": [1, 2], "color": "crimson"}` |
| `delta_indicator` | value, x, y, label? | `{"type": "delta_indicator", "value": "+18%", "x": 5, "y": 2}` |

**Coordinates**: x, y are in inches from top-left of slide. Use the content area (starts ~1.2" from top, 0.75" from left) as your reference.

## Design System Defaults

| Element | Default |
|---------|---------|
| Primary | Navy `#1B2A4A` |
| Accent | Teal `#0D9488` |
| Body text | Slate `#334155`, 14pt Calibri |
| Headline | Navy, 28pt bold |
| Source | 8pt italic, bottom-left |
| Tables | No vertical borders, alternating `#F8FAFC`/white rows |
| Charts | Max 3 colors, direct labels, no gridlines |

Override via `"theme"` in plan.json.

## Dependencies

- Python 3.8+
- `python-pptx` (`pip install python-pptx`)
