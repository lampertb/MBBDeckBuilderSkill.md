#!/usr/bin/env python3
"""
MBB PPTX Generator — Entry point.
Reads a plan.json and generates a native, editable PowerPoint presentation.

Usage:
    python scripts/generate.py --plan plan.json --output output.pptx
"""

import argparse
import json
import sys
import os

# Add parent dir to path so scripts package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pptx import Presentation
from pptx.util import Inches

from scripts.design_system import SLIDE_WIDTH, SLIDE_HEIGHT, DesignSystem
from scripts.slide_builder import new_blank_slide
from scripts.slide_types import get_render_fn
from scripts.overlays import apply_overlays
from scripts.quality_checks import validate_slide, validate_deck


def generate(plan_path: str, output_path: str):
    """Generate a PPTX from a plan JSON file."""

    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    # Initialize design system with optional theme overrides
    theme = plan.get("theme", {})
    ds = DesignSystem(theme)

    # Create presentation
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    slides_data = plan.get("slides", [])
    all_warnings = {}

    # Collect all sources for busybee_sources slides
    all_sources = []

    for i, slide_data in enumerate(slides_data):
        slide_type = slide_data.get("type")
        if not slide_type:
            print(f"  Warning: Slide {i+1} has no type, skipping.")
            continue

        # Track sources
        if slide_data.get("source"):
            all_sources.append({
                "slide": i + 1,
                "source": slide_data["source"],
                "headline": slide_data.get("headline", ""),
            })

        # Inject collected sources for busybee_sources type
        if slide_type == "busybee_sources":
            slide_data["_all_sources"] = all_sources

        # Create blank slide
        slide = new_blank_slide(prs)

        # Render base layer
        try:
            render_fn = get_render_fn(slide_type)
            context = render_fn(slide, slide_data, ds)
        except KeyError as e:
            print(f"  Error on slide {i+1}: {e}")
            continue
        except Exception as e:
            print(f"  Error rendering slide {i+1} ({slide_type}): {e}")
            import traceback
            traceback.print_exc()
            continue

        # Render overlay layer
        overlays = slide_data.get("overlays")
        if overlays:
            ctx = context if isinstance(context, dict) else {}
            apply_overlays(slide, overlays, ds, ctx)

        # Quality checks
        warnings = validate_slide(slide, i + 1, slide_data)
        if warnings:
            all_warnings[i + 1] = warnings

    # Save
    prs.save(output_path)
    print(f"\n  Generated: {output_path} ({len(slides_data)} slides)")

    # Print quality report
    validate_deck(all_warnings)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate MBB-quality PPTX from plan.json")
    parser.add_argument("--plan", required=True, help="Path to plan.json")
    parser.add_argument("--output", required=True, help="Output .pptx path")
    args = parser.parse_args()

    try:
        generate(args.plan, args.output)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
