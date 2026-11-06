---
title: Documentation Pipeline (Alpha)
---

# Documentation Pipeline

These pages explain how this repository's documentation reaches Confluence,
how to write and structure documents so the pipeline handles them, and how
the credentials behind it are set up.

- [How publishing works](workflow.md) — the two GitHub workflows and what
  `mark` does on every run.
- [Authoring rules](authoring.md) — front matter, links, images, Mermaid,
  and what makes validation fail.
- [Secrets and permissions](setup.md) — Atlassian API tokens, their
  scoping, and the GitHub secrets the workflows read.
- [Limitations and roadmap](limitations.md) — known limits of the current
  setup and candidate improvements.

The same pipeline runs in the twin repository `confluence-docs-beta` with
its own root page, secrets, and page manifest.

See also the [formatting sample](../guide.md) for a quick tour of the
supported Markdown.
