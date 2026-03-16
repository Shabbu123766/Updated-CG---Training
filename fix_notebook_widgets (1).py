#!/usr/bin/env python3
"""
Fixes the missing 'state' key in metadata.widgets for Jupyter notebooks
exported from Google Colab. Run this on any .ipynb file before pushing to GitHub.

Usage:
    python fix_notebook_widgets.py                  # fixes all .ipynb in current folder
    python fix_notebook_widgets.py notebook.ipynb   # fixes a specific file
"""

import json
import sys
import os
from pathlib import Path


def fix_notebook(path: str) -> bool:
    """Returns True if the file was modified, False if it was already valid."""
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    key = "application/vnd.jupyter.widget-state+json"
    widgets = nb.get("metadata", {}).get("widgets", {})

    if key not in widgets:
        return False  # no widgets metadata, nothing to fix

    widget_data = widgets[key]

    if "state" in widget_data:
        return False  # already valid

    # Wrap all widget states under the required 'state' key
    nb["metadata"]["widgets"][key] = {
        "state": widget_data,
        "version_major": 2,
        "version_minor": 0
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)

    return True


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(Path(".").rglob("*.ipynb"))

    if not targets:
        print("No .ipynb files found.")
        return

    for target in targets:
        path = str(target)
        if not os.path.isfile(path):
            print(f"  skipped (not found): {path}")
            continue
        try:
            fixed = fix_notebook(path)
            status = "fixed" if fixed else "already valid"
            print(f"  {status}: {path}")
        except Exception as e:
            print(f"  error in {path}: {e}")


if __name__ == "__main__":
    main()
