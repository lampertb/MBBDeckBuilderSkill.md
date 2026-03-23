# Training Loop

Train the MBB PPTX generator by comparing against real consulting slides.

## Setup

```bash
pip install python-pptx Pillow
# Optional for visual diff (recommended):
brew install --cask libreoffice
```

## How It Works

```
reference_slides/     →  extract_slide.py  →  plan.json  →  generate.py  →  generated.pptx
     ↓                                                                          ↓
     └────────────────────── visual_diff.py ←───────────────────────────────────┘
                                  ↓
                          diffs/ (comparison images + report)
```

1. **Drop reference MBB slides** into `training/reference_slides/`
2. **Run training**: `python3 training/train.py`
3. **Review diffs** in `training/diffs/` — side-by-side comparisons + training report
4. **Fix issues** in slide type modules or SKILL.md
5. **Re-run** and iterate until quality matches

## Commands

```bash
# Train on all reference slides
python3 training/train.py

# Train on a specific file
python3 training/train.py --input training/reference_slides/example.pptx

# Train on a specific slide within a deck
python3 training/train.py --input training/reference_slides/example.pptx --slide 3

# Extract content only (for inspection)
python3 training/extract_slide.py --input example.pptx --output extracted.json
python3 training/extract_slide.py --input example.pptx --plan --output plan.json

# Visual diff only (between any two PPTX files)
python3 training/visual_diff.py --reference ref.pptx --generated gen.pptx --output diffs/
```

## Directory Structure

```
training/
├── reference_slides/    # Drop real MBB .pptx files here
├── output/              # Generated plans and PPTX files
├── diffs/               # Visual diff results and training reports
├── extract_slide.py     # Extracts content from PPTX → JSON
├── visual_diff.py       # Compares two PPTX files visually
└── train.py             # Orchestrates the full training pipeline
```
