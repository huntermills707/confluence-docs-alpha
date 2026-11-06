---
title: Alpha User Guide
---

# Alpha User Guide

This guide demonstrates the Markdown features the sync converts to
Confluence storage format.

## Formatting basics

You can use **bold**, *italic*, ~~strikethrough~~ and `inline code`.
Links like the one back to [Alpha Documentation Home](index.md) become real
Confluence page links.

## Lists

Unordered list:

- First item
- Second item with a nested list
  - Nested item one
  - Nested item two
- Third item

Ordered list:

1. Install the tool
2. Configure credentials
3. Run the synchronizer

## Task checklist

- [x] Write documentation
- [ ] Review pull request
- [ ] Merge to main

> Blockquotes are supported and render as Confluence quote blocks.

## Code blocks

```python
def reconcile(manifest, confluence):
    for doc in manifest.docs.values():
        publish(confluence, doc)
```

```bash
gh workflow run "Sync docs to Confluence" --ref main
```

## Tables

| Change type | Confluence action |
|---|---|
| Document added | Create page |
| Document edited | Update page |
| Document moved | Move page |

Horizontal rules work too:

---

Return to the [documentation home page](index.md).

Merge-publication marker: scenario 3.
