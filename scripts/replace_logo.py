#!/usr/bin/env python3
"""Replace navbar img logo with inline SVG text logo across all HTML files."""
import os
import glob

SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="190" height="32" '
    'viewBox="0 0 190 32" aria-label="Unblocked Games G+">'
    '<defs><linearGradient id="lg" x1="0%" y1="0%" x2="100%" y2="0%">'
    '<stop offset="0%" stop-color="#a855f7"/>'
    '<stop offset="100%" stop-color="#22d3ee"/>'
    '</linearGradient></defs>'
    '<text y="24" font-family="Segoe UI,Arial,sans-serif" font-size="17" '
    'font-weight="700" fill="url(#lg)">Unblocked Games G+</text>'
    '</svg>'
)

OLD_VARIANTS = [
    '<img src="/assets/img/favicon.png" height="32" style="border-radius:6px" alt="Unblocked Games G+">',
    '<img src="/assets/img/logo.png" height="30">',
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)

changed = 0
for path in files:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    new = content
    for old in OLD_VARIANTS:
        new = new.replace(old, SVG)
    if new != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        changed += 1

print(f'Updated {changed} / {len(files)} files')
