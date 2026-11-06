---
title: "Pipeline: How Publishing Works (Alpha)"
---

# How publishing works

GitHub is the **source of truth**; Confluence Cloud is a one-way mirror.
Publishing is done by [mark](https://github.com/kovetskiy/mark) `v16.25.0`,
run from its pinned Docker image — the image bundles a headless Chrome that
renders Mermaid diagrams, so no extra tools are installed by the workflows.

```mermaid
flowchart LR
    A["Edit docs on a branch"] --> B["Open pull request"]
    B --> C["Validate docs — compile only"]
    C -->|"review + merge to main"| D["Sync docs to Confluence"]
    D --> E["mark publish"]
    E --> F["Confluence Cloud mirror"]
```

## Workflow 1: Validate docs (PR)

Runs on every pull request touching `docs/`. It executes
`mark publish --compile-only --check-links internal`, which:

- converts every page to Confluence storage format (Mermaid rendering
  included) without sending anything,
- fails on internal links that do not resolve to a document with a title,
- performs **read-only** Confluence lookups to resolve links between
  documents (links to pages that do not exist yet are warnings, not
  errors).

## Workflow 2: Sync docs to Confluence

Runs when a merged pull request (any push) lands on `main` touching
`docs/`. Runs are queued (never run concurrently) via a concurrency group.
A manual run is available with a `dry_run` input that reports what would
change without touching Confluence.

On each run `mark publish`:

1. Discovers `docs/**/*.md` and reads each file's front matter title.
2. Derives the page tree from the directory structure
   (`--parents-from-path`) under this repository's root page in the space.
3. Matches pages by **title**; the page manifest it keeps in Confluence
   (`--track-pages --manifest-prefix alpha.sync`) maps each file to its
   page so renames and retitles update pages in place.
4. Converts Markdown to Confluence storage format; renders Mermaid blocks
   to PNG images and uploads them, plus any referenced images, as page
   attachments.
5. Rewrites relative links between documents into stable Confluence
   "tiny" links.
6. Creates missing pages, updates changed ones (`--changes-only` skips
   unchanged pages), and moves pages whose location changed.
7. Trashes the pages of files that were deleted (`--on-orphan delete`),
   scoped to pages beneath this repository's root page. A run in which
   any document failed removes nothing, and pages with children outside
   the removal are left alone. Nothing is ever purged — trash only.

## Pinning and rollback

Both workflows pin the same image tag (`env.MARK_IMAGE` in the workflow
files). Upgrade or roll back the publisher by changing the two tags
together. Bad pages can be restored from the space trash; the next sync
treats them as current again.
