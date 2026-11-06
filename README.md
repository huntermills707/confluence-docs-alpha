# confluence-docs-alpha

Content repository for the GitHub → Confluence docs-as-code pipeline.
**GitHub is the source of truth**; Confluence Cloud is a one-way publishing
destination. Publishing is done by [mark](https://github.com/kovetskiy/mark)
from a pinned Docker image — no custom sync code lives in this repository.

When a pull request to `main` is merged, the **Sync docs to Confluence**
workflow runs `mark publish` over `docs/**/*.md` and reconciles this
repository's subtree under its own root page in the `GHConfDocs` Confluence
space. The twin repository `confluence-docs-beta` publishes into the same
space under a different root page; each repository keeps its own page
manifest, so neither can rename or delete the other's pages.

## How it works

```text
docs/**/*.md  (YAML front matter with title)
   → mark publish (GitHub Action, runs when a PR to main merges)
   → Markdown converted to Confluence storage format
   → Mermaid blocks rendered to images by the bundled headless Chrome
   → directory tree mirrored as the page tree
   → pages created / updated / moved; pages of removed files trashed
```

* Every document starts with YAML front matter containing a `title`. Titles
  must be **unique within the Confluence space** — Confluence allows one page
  per title per space, and mark refuses duplicates.
* `docs/index.md` is the page for `docs/` itself; a directory containing
  `index.md` uses that file as the folder's page (title and body).
* Relative links between documents become Confluence page links; images are
  uploaded as attachments automatically.
* `mark --track-pages` keeps a file → page manifest **in Confluence**
  (prefix `alpha.sync`), so renamed files and retitled documents update the
  existing page instead of creating a second one.
* Files deleted from the repository have their pages moved to the **trash**
  (`--on-orphan delete`), scoped to pages beneath this repository's root
  page. A run in which any document failed to publish removes nothing, and
  pages with children outside the removal are left alone.

## Repository secrets

Settings → Secrets and variables → Actions:

| Secret | Example |
|---|---|
| `ATLASSIAN_BASE_URL` | `https://jaegermolino.atlassian.net` |
| `ATLASSIAN_USER_EMAIL` | you@example.com |
| `ATLASSIAN_API_TOKEN` | Atlassian Cloud API token |
| `CONFLUENCE_SPACE_KEY` | `GHConfDocs` |
| `CONFLUENCE_ROOT_PAGE_ID` | page id of *this repo's* root page |

The root page was created once by hand and is only ever used as the parent of
this repository's pages — mark never writes to it or deletes it.

## Workflows

* **Sync docs to Confluence** — triggered when a merged PR (or any push)
  lands on `main` touching `docs/`, plus manual runs with a `dry_run` input.
* **Validate docs (PR)** — runs on pull requests: `mark publish
  --compile-only --check-links internal` renders every page (Mermaid
  included) and fails on broken internal links. It receives no Confluence
  credentials and never publishes.

Both workflows pin the same mark image tag (`env.MARK_IMAGE`); change the two
pins together to upgrade or roll back the publisher.

## Recovery

* **Trashed page**: Confluence → Space → … → Trash → Restore. The next sync
  treats it as current again.
* **Wrong state / accidental trash**: restore from trash, fix the docs,
  re-run. Nothing is ever purged automatically.
* **Failed run**: the workflow fails visibly; documents that failed were not
  published, and no removals happen in a failed run.

## Layout

```text
docs/
├── index.md                  page for docs/ itself (documentation home)
├── guide.md                  formatting sample
├── architecture/
│   ├── index.md              folder page for architecture/
│   └── overview.md
├── policies/
│   ├── index.md              folder page for policies/
│   ├── deployment.md
│   └── retention.md
└── assets/
    └── example.png

.github/workflows/            thin mark consumers (pinned image tag)
```

## Cleanup

1. Revoke the API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Delete the GitHub secrets (or the whole repository).
3. Delete this repository's root page in the space (sub-pages go to trash
   with it).
