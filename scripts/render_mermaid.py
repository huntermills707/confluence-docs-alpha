#!/usr/bin/env python3
"""Render every ```mermaid fenced block under docs/ to an SVG.

Uses @mermaid-js/mermaid-cli (mmdc) via npx, so Node.js must be available
(true on GitHub-hosted runners). Output and a manifest mapping
sha256(source) -> svg path are written to build/mermaid/ so that sync.py can
embed the diagrams as page attachments.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

MERMAID_CLI = os.environ.get("MERMAID_CLI", "@mermaid-js/mermaid-cli@11.12.0")
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
OUT = REPO_ROOT / "build" / "mermaid"

FENCE = re.compile(r"```mermaid[ \t]*\r?\n(.*?)```", re.S)


def collect_blocks():
    blocks = {}
    for p in sorted(DOCS.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        for i, m in enumerate(FENCE.finditer(text)):
            src = m.group(1)
            h = hashlib.sha256(src.encode()).hexdigest()
            blocks.setdefault(h, src)
    return blocks


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    puppeteer_cfg = OUT / "puppeteer.json"
    puppeteer_cfg.write_text('{"args": ["--no-sandbox", "--disable-setuid-sandbox"]}',
                             encoding="utf-8")
    blocks = collect_blocks()
    if not blocks:
        print("render_mermaid: no mermaid blocks found")
        (OUT / "manifest.json").write_text("{}", encoding="utf-8")
        return

    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    failures = []
    for h, src in sorted(blocks.items()):
        svg = OUT / f"{h}.svg"
        if svg.exists() and h in manifest:
            continue  # already rendered in an earlier local run
        mmd = OUT / f"{h}.mmd"
        mmd.write_text(src, encoding="utf-8")
        cmd = ["npx", "--yes", MERMAID_CLI, "-i", str(mmd), "-o", str(svg),
               "-p", str(puppeteer_cfg), "-b", "transparent", "--quiet"]
        print(f"rendering mermaid {h[:12]}...", flush=True)
        proc = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if proc.returncode != 0 or not svg.exists():
            failures.append(f"mermaid block {h[:12]} failed to render:\n"
                            f"{(proc.stderr or proc.stdout)[-1500:]}")
            continue
        manifest[h] = {"svg": str(svg), "mmd": src}

    if failures:
        for f in failures:
            print("ERROR " + f, file=sys.stderr)
        raise SystemExit(1)

    manifest_path.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"render_mermaid: {len(blocks)} diagram(s) rendered to {OUT}")


if __name__ == "__main__":
    main()
