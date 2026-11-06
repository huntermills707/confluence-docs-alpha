---
title: "Pipeline: Authoring Rules (Alpha)"
---

# Authoring rules

Everything under `docs/` that matches `*.md` is published. Documents are
plain Markdown plus one required metadata block.

## Every page needs a title

Each file starts with YAML front matter containing a `title`:

```markdown
---
title: Alpha Deployment Topology
---

# Deployment Topology

Body text…
```

Rules for titles:

- The `title` becomes the Confluence page title. It is also the page's
  **identity**: mark matches pages by title within the space.
- Titles must be **unique across the whole space** — this repository
  shares `GHConfDocs` with `confluence-docs-beta`, hence the "Alpha …"
  and "(Alpha)" naming convention.
- Changing a title renames the existing page (the manifest tracks it);
  it never creates a second page.
- No other front matter keys are needed — the space, the parent root page
  and the tree position all come from the workflow and the file's path.
  Unknown keys are ignored with a warning.

## The directory tree becomes the page tree

- `docs/index.md` is the page for `docs/` itself — the documentation home
  page. Top-level documents sit under it.
- A directory containing `index.md` uses that file as the folder's page:
  its title and body become the folder page.
- A directory without `index.md` gets an auto-generated folder page named
  after the directory (title-cased).
- Moving a file moves its page on the next publish; deleting a file moves
  its page to the trash.

## Links

- Relative links to other Markdown files become Confluence page links
  (stable tiny links that survive renames and moves):

  ```markdown
  See the [architecture overview](../architecture/overview.md).
  ```

- Anchors work too: `[setup section](other.md#setup)` resolves to the
  matching heading on that page.
- External `http(s)` and `mailto:` links are kept as-is.
- A relative link that points at a missing file, or at a document without
  a title, **fails PR validation**. Links to documents that exist in the
  branch but are not published yet only warn.

## Images

- `![Alt text](assets/example.png)` — local images are uploaded as page
  attachments automatically. Keep them under `docs/assets/`.
- Remote image URLs are displayed from the remote location.

## Mermaid diagrams

Fenced ` ```mermaid ` blocks are rendered to PNG images by the Chrome
bundled in the mark image and attached to the page. The Markdown source
stays the source of truth in Git.

## Other formatting

- Fenced code blocks with a language tag become Confluence code macros.
- GFM tables, nested lists, task lists (`- [x]`) and blockquotes are
  supported; GitHub-style alerts (`> [!NOTE]`) render as Confluence
  panels in recent mark versions.
- Raw HTML is mostly stripped by Confluence's sanitizer — avoid it.
- `@mentions` and emoji shortcodes are deliberately not enabled in this
  repository (the workflow enables only the `mermaid` and `frontmatter`
  features).

## What fails validation

| Problem | Result |
|---|---|
| Missing or empty `title` | PR validation fails |
| Duplicate title in the space | Publish run fails |
| Relative link to a missing/untitled document | PR validation fails |
| Missing image file | Warning; image degrades |
| Unknown front matter key | Warning; key ignored |
