---
title: Data Retention Policy (Alpha)
---

# Data Retention Policy

## Retention classes

| Data class | Retention | Storage |
|---|---|---|
| Page bodies | Indefinite | Confluence Cloud |
| Trashed pages | 30 days | Confluence trash |
| Diagram sources | Indefinite | Git |

## Deletion safeguards

1. Only pages this repository published (tracked in its mark manifest) are
   ever trashed.
2. The repository root page is never deleted; its body and title are never
   changed. Only its manifest content properties are maintained.
3. A run in which any document failed to publish removes nothing.

Start from the [documentation home page](../index.md).
