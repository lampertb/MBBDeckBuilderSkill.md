# Adding New Slide Types

## Steps

1. **Create** `scripts/slide_types/{type_name}.py`
2. **Implement** the `render(slide, data, ds)` function
3. **Register** in `scripts/slide_types/__init__.py`
4. **Document** the data contract in `references/slide-type-catalog.md`

## Template

```python
"""Description of this slide type."""

from pptx.util import Inches, Pt
from scripts.design_system import (
    DesignSystem, CONTENT_LEFT, CONTENT_WIDTH, CONTENT_TOP, CONTENT_HEIGHT,
)
from scripts.slide_builder import add_headline, add_divider_line, add_source, add_footnotes


def render(slide, data, ds: DesignSystem):
    """
    data: {headline, ...type-specific fields..., source?, footnotes?}
    Returns: dict context for overlays, or empty dict.
    """
    add_headline(slide, data.get("headline", ""), ds)
    add_divider_line(slide, ds)

    # Build your slide content here using slide_builder primitives

    add_footnotes(slide, data.get("footnotes"), ds)
    add_source(slide, data.get("source"), ds)

    return {}  # Return context dict if overlays need positioning info
```

## Registration

In `scripts/slide_types/__init__.py`:

```python
from scripts.slide_types.{type_name} import render as render_{type_name}

# Add to REGISTRY dict:
"{type_name}": render_{type_name},
```

## Guidelines

- Use `slide_builder` primitives — don't call python-pptx directly unless necessary
- Return a context dict if your slide type supports overlays (e.g., table or chart reference)
- Keep coordinates within CONTENT_TOP to CONTENT_BOTTOM, CONTENT_LEFT to CONTENT_LEFT + CONTENT_WIDTH
- Use `ds.primary`, `ds.accent1`, etc. for colors (not hardcoded values) to respect theme overrides
