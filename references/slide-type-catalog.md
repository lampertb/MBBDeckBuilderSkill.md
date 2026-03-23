# Slide Type Catalog

Data contracts for all 16 slide types. Every slide type receives a `data` dict and a `DesignSystem` instance.

## Common Fields

All types support:
- `headline` (str) — Takeaway message
- `source` (str) — Source attribution
- `footnotes` ([str]) — Footnote list
- `overlays` ([dict]) — Layer 2 overlay specs

## Structure Slides

### title_hero
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| headline | str | Yes | Deck title |
| subtitle | str | No | Subtitle or tagline |
| author | str | No | Author name/team |
| date | str | No | Presentation date |

### executive_summary
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| headline | str | Yes | Summary takeaway |
| bullets | [str] | Yes | 3-5 key findings |
| subtitle | str | No | Framing text above bullets |

### section_divider
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| headline | str | Yes | Section title |
| subtitle | str | No | Section description |
| section_number | int | No | Displayed as large number |

### agenda
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| headline | str | Yes | "Today's Discussion" etc. |
| items | [dict/str] | Yes | Each: {title, description?} or plain string |
| current_item | int | No | 1-indexed; highlights this item |

### quote_page
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| quote | str | Yes | The quote text |
| attribution | str | No | Who said it |
| title | str | No | Their role/title |

### qa_page
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| headline | str | No | Default: "Questions & Discussion" |
| subtitle | str | No | Contact info |

### busybee_sources
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| headline | str | No | Default: "Sources & References" |

Sources auto-collected from all prior slides in the deck.

## Data-Heavy Slides

### data_table
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| headers | [str] | Yes | Column headers |
| rows | [[str]] | Yes | Row data (list of lists) |
| col_widths | [float] | No | Column widths in inches |

**Returns context:** `{"table": table_shape}` for color_band overlays.

### bar_chart
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| categories | [str] | Yes | Category labels |
| series | [dict] | Yes | Each: {name, values: [num], color?} |
| orientation | str | No | "vertical" (default) or "horizontal" |
| show_values | bool | No | Show data labels (default: true) |
| value_format | str | No | Number format string |

**Returns context:** `{"chart_bounds": {left, top, width, height}, "categories": [...]}` for overlays.

### line_chart
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| categories | [str] | Yes | X-axis labels (time periods) |
| series | [dict] | Yes | Each: {name, values: [num], color?} |
| show_values | bool | No | Show data labels (default: false) |
| value_format | str | No | Number format string |

### waterfall_chart
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| categories | [str] | Yes | Bar labels |
| values | [float] | Yes | Positive = increase, negative = decrease |
| total_indices | [int] | No | Indices that are totals, not deltas (default: first and last) |

### two_by_two_matrix
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| x_axis_label | str | No | X-axis label |
| y_axis_label | str | No | Y-axis label |
| quadrants | [dict] | No | 4 items (TL, TR, BL, BR): {label, description?, color?} |
| items | [dict] | No | Plotted items: {name, quadrant: "TL"/"TR"/"BL"/"BR", x?: 0-1, y?: 0-1} |

## Layout Slides

### key_stat
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| stats | [dict] | Yes | 1-3 items: {value, label, delta?, context?} |

### two_column
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| left | dict/str | Yes | {title?, bullets?, text?} |
| right | dict/str | Yes | {title?, bullets?, text?} |
| divider | bool | No | Show center divider (default: true) |

### three_column
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| columns | [dict] | Yes | Each: {title, bullets?, text?} |

### timeline
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| milestones | [dict] | Yes | Each: {date, title, description?} |
