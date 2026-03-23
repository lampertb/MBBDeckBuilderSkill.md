#!/usr/bin/env python3
"""
QA Test Runner — generates slides from standard fixture inputs and produces
PNG screenshots for visual inspection.

Usage:
    python3 qa/run_qa.py                     # Run all fixtures
    python3 qa/run_qa.py --fixture bar_chart  # Run one fixture
    python3 qa/run_qa.py --list              # List available fixtures

Outputs go to qa/output/ as .pptx files.
To visually inspect, open in PowerPoint or use the thumbnail export.
"""

import argparse
import json
import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generate import generate


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def list_fixtures():
    """List all available fixture files."""
    fixtures = sorted(glob.glob(os.path.join(FIXTURE_DIR, "*.json")))
    if not fixtures:
        print("No fixtures found in qa/fixtures/")
        print("Add .json plan files to qa/fixtures/ to create test cases.")
        return []
    for f in fixtures:
        name = os.path.splitext(os.path.basename(f))[0]
        with open(f) as fh:
            data = json.load(fh)
        num_slides = len(data.get("slides", []))
        types = [s.get("type", "?") for s in data.get("slides", [])]
        print(f"  {name}: {num_slides} slides — {', '.join(types)}")
    return fixtures


def run_fixture(fixture_path):
    """Generate output from a single fixture."""
    name = os.path.splitext(os.path.basename(fixture_path))[0]
    output_path = os.path.join(OUTPUT_DIR, f"{name}.pptx")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"QA: {name}")
    print(f"{'='*60}")

    try:
        generate(fixture_path, output_path)
        print(f"  Output: {output_path}")
        return True
    except Exception as e:
        print(f"  FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all():
    """Run all fixtures and report results."""
    fixtures = sorted(glob.glob(os.path.join(FIXTURE_DIR, "*.json")))
    if not fixtures:
        print("No fixtures found. Add .json files to qa/fixtures/")
        return

    results = {}
    for f in fixtures:
        name = os.path.splitext(os.path.basename(f))[0]
        results[name] = run_fixture(f)

    # Summary
    print(f"\n{'='*60}")
    print("QA SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
    print(f"\n  {passed}/{total} passed")


def main():
    parser = argparse.ArgumentParser(description="QA test runner for MBB PPTX generator")
    parser.add_argument("--fixture", help="Run a specific fixture by name")
    parser.add_argument("--list", action="store_true", help="List available fixtures")
    args = parser.parse_args()

    if args.list:
        list_fixtures()
    elif args.fixture:
        path = os.path.join(FIXTURE_DIR, f"{args.fixture}.json")
        if not os.path.exists(path):
            print(f"Fixture not found: {path}")
            sys.exit(1)
        run_fixture(path)
    else:
        run_all()


if __name__ == "__main__":
    main()
