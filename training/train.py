#!/usr/bin/env python3
"""
Training loop — the core feedback cycle for improving the MBB PPTX generator.

Pipeline:
1. Take a reference MBB slide (.pptx) from training/reference_slides/
2. Extract its content into structured JSON
3. Run the generator to recreate the slide
4. Visual diff between reference and generated
5. Output a report with specific improvement suggestions

Usage:
    python3 training/train.py                              # Process all reference slides
    python3 training/train.py --input training/reference_slides/mckinsey_example.pptx
    python3 training/train.py --slide 3                    # Process specific slide from a deck
"""

import argparse
import json
import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.extract_slide import extract_presentation, to_plan_json
from scripts.generate import generate
from training.visual_diff import run_diff


REFERENCE_DIR = os.path.join(os.path.dirname(__file__), "reference_slides")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
DIFF_DIR = os.path.join(os.path.dirname(__file__), "diffs")


def train_on_file(ref_path, slide_number=None):
    """Run the full training pipeline on a single reference file."""
    name = os.path.splitext(os.path.basename(ref_path))[0]
    run_output = os.path.join(OUTPUT_DIR, name)
    run_diffs = os.path.join(DIFF_DIR, name)
    os.makedirs(run_output, exist_ok=True)
    os.makedirs(run_diffs, exist_ok=True)

    print(f"\n{'='*70}")
    print(f"TRAINING: {name}")
    print(f"{'='*70}")

    # Step 1: Extract
    print("\n--- Step 1: Extracting content from reference ---")
    extracted = extract_presentation(ref_path, slide_number)
    extracted_path = os.path.join(run_output, "extracted.json")
    with open(extracted_path, "w") as f:
        json.dump(extracted, f, indent=2, default=str)
    print(f"  Extracted {len(extracted['slides'])} slide(s) → {extracted_path}")

    # Step 2: Convert to plan.json
    print("\n--- Step 2: Converting to plan.json ---")
    plan = to_plan_json(extracted)
    plan_path = os.path.join(run_output, "plan.json")
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2, default=str)
    print(f"  Plan with {len(plan['slides'])} slide(s) → {plan_path}")

    # Show what was detected
    for i, slide in enumerate(plan["slides"]):
        print(f"    Slide {i+1}: type={slide['type']}, headline=\"{slide.get('headline', '')[:60]}\"")

    # Step 3: Generate
    print("\n--- Step 3: Generating PPTX ---")
    gen_path = os.path.join(run_output, "generated.pptx")
    try:
        generate(plan_path, gen_path)
    except Exception as e:
        print(f"  Generation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

    # Step 4: Visual diff
    print("\n--- Step 4: Visual diff ---")
    diff_report = run_diff(ref_path, gen_path, run_diffs, slide_number)

    # Step 5: Training report
    print("\n--- Step 5: Training report ---")
    report = generate_training_report(extracted, plan, diff_report, name)
    report_path = os.path.join(run_diffs, "training_report.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  Training report → {report_path}")

    return report


def generate_training_report(extracted, plan, diff_report, name):
    """Generate a markdown report with improvement suggestions."""
    lines = [
        f"# Training Report: {name}",
        f"",
        f"## Extraction Summary",
        f"",
        f"| Slide | Detected Type | Headline |",
        f"|-------|--------------|----------|",
    ]

    for slide in plan["slides"]:
        headline = slide.get("headline", "")[:50]
        lines.append(f"| {slide.get('_raw_extraction', {}).get('slide_number', '?')} "
                     f"| {slide['type']} | {headline} |")

    lines.extend([
        "",
        "## Comparison Summary",
        "",
    ])

    if diff_report:
        for s in diff_report.get("slides", []):
            sim = s.get("text_similarity", 0)
            status = "GOOD" if sim > 0.7 else "NEEDS WORK" if sim > 0.3 else "POOR"
            lines.append(f"- **Slide {s['slide_number']}**: text similarity={sim:.2f} [{status}]")
            if sim < 0.7:
                lines.append(f"  - Reference text: \"{s.get('ref_text', '')[:80]}...\"")
                lines.append(f"  - Generated text: \"{s.get('gen_text', '')[:80]}...\"")

    lines.extend([
        "",
        "## Improvement Suggestions",
        "",
        "Review the following and iterate on SKILL.md / slide type modules:",
        "",
    ])

    # Identify gaps
    unknown_types = [s for s in plan["slides"] if s["type"] == "unknown"]
    if unknown_types:
        lines.append(f"### Unrecognized Slide Types ({len(unknown_types)} slides)")
        lines.append("These slides couldn't be classified. Consider:")
        lines.append("- Adding new slide types to handle these layouts")
        lines.append("- Improving the classifier in `extract_slide.py`")
        lines.append("")

    missing_headlines = [s for s in plan["slides"] if not s.get("headline")]
    if missing_headlines:
        lines.append(f"### Missing Headlines ({len(missing_headlines)} slides)")
        lines.append("Headlines couldn't be extracted. Check:")
        lines.append("- Headline detection logic in `extract_slide.py`")
        lines.append("- Reference slide formatting (bold, large font at top)")
        lines.append("")

    lines.extend([
        "### Manual Review Checklist",
        "",
        "Open both PPTX files side-by-side and check:",
        "- [ ] Typography hierarchy matches (headline vs body sizing)",
        "- [ ] Color palette is consistent with reference",
        "- [ ] Table formatting matches (borders, shading, alignment)",
        "- [ ] Chart styling matches (colors, labels, gridlines)",
        "- [ ] Whitespace and margins feel right",
        "- [ ] Overlays/callouts are positioned correctly",
        "- [ ] Source and footnotes are present and formatted",
        "",
        "## Next Steps",
        "",
        "1. Fix the highest-priority issues identified above",
        "2. Re-run: `python3 training/train.py --input <ref_file>`",
        "3. Compare the new diff scores to this report",
        "4. Repeat until diff scores are acceptable",
    ])

    return "\n".join(lines)


def train_all():
    """Run training on all reference slides."""
    ref_files = sorted(glob.glob(os.path.join(REFERENCE_DIR, "*.pptx")))
    if not ref_files:
        print(f"No reference slides found in {REFERENCE_DIR}/")
        print("Add .pptx files from MBB presentations to start training.")
        return

    print(f"Found {len(ref_files)} reference file(s)")
    for ref in ref_files:
        train_on_file(ref)


def main():
    parser = argparse.ArgumentParser(description="Training loop for MBB PPTX generator")
    parser.add_argument("--input", help="Specific reference .pptx file to train on")
    parser.add_argument("--slide", type=int, help="Train on specific slide number only")
    args = parser.parse_args()

    if args.input:
        train_on_file(args.input, args.slide)
    else:
        train_all()


if __name__ == "__main__":
    main()
