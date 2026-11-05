---
doc_id: 941d35ea-e724-48c6-acf9-f0487ab2604f
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

1. Only pages managed by this repository are ever trashed.
2. The repository root page is never deleted.
3. Mass deletions are blocked unless explicitly authorised.

Start from the [documentation home page](../index.md).
