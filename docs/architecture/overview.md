---
doc_id: efc2c9f7-e709-4c58-af34-92600c1cd8ed
title: Alpha Architecture Overview
---

# Architecture Overview

Alpha is a small three-tier system:

```mermaid
flowchart TB
    U[Contributor] --> G[GitHub repository]
    G --> A[GitHub Actions]
    A --> S[(Confluence Cloud)]
    S --> R[Readers]
```

## Components

1. **GitHub repository** — stores Markdown, images and Mermaid sources.
2. **GitHub Actions** — renders diagrams and reconciles Confluence.
3. **Confluence Cloud** — read-only publishing destination.

## Identity model

Every document carries a `doc_id` in its front matter. The synchronizer
stores that id as a content property on the Confluence page, so renames and
moves never duplicate pages.

## Image attachment

![Alpha example diagram](../assets/example.png)

See also [Alpha Deployment Topology](../policies/deployment.md) or go back to
[Alpha Documentation Home](../index.md).
