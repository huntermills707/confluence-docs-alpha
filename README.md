# confluence-docs-alpha

Dummy repository for the GitHub → Confluence docs-as-code proof of concept.
**GitHub is the source of truth**; Confluence Cloud is a one-way publishing
destination. Merging to `main` reconciles the `docs/` tree with this
repository's own root page in the `GHConfDocs` Confluence space.

The twin repository `confluence-docs-beta` publishes into the same space under
a different root page. The two can never see or delete each other's pages.
Both are content-only consumers of the canonical
[`confluence-docs-sync`](https://github.com/huntermills707/confluence-docs-sync)
tool, pinned to the same immutable release.

## How it works

```text
docs/*.md (front matter doc_id)
   → GitHub Action (on push to main / manual)
   → Markdown converted to Confluence storage format
   → Mermaid blocks rendered to SVG by mermaid-cli
   → Desired state reconciled against pages under this repo's root page
   → Pages created / updated / moved / trashed as needed
```

### Stable document identity

Every document starts with YAML front matter:

```yaml
---
doc_id: 98905d42-47e7-4633-beec-c2649cae354b
title: Alpha Documentation Home
---
```

* `doc_id` never changes when a file is renamed or moved — it is the page
  identity. The id and the owning repository are stored as a content property
  (`ghdocsync`) on the Confluence page, so matching never depends on titles,
  paths or Git rename detection.
* `title` becomes the page title. Titles must be **unique within the
  Confluence space** because internal links resolve by title.
* Directories become folder pages. A directory containing `_index.md` uses
  that file's `doc_id`/`title`/body for the folder page, so folder pages keep
  their identity across directory renames. Directories without `_index.md`
  get an auto-generated stub page (identity derived from the path).

### Conventions for splits and merges

* **Splitting** a document: one of the new documents keeps the original
  `doc_id`, the others get fresh ids.
* **Merging** documents: the surviving document keeps one of the original
  ids; the obsolete documents are simply deleted, so their pages are trashed
  on the next sync.

## Repository secrets

Settings → Secrets and variables → Actions:

| Secret | Example |
|---|---|
| `ATLASSIAN_BASE_URL` | `https://jaegermolino.atlassian.net` |
| `ATLASSIAN_USER_EMAIL` | you@example.com |
| `ATLASSIAN_API_TOKEN` | Atlassian Cloud API token |
| `CONFLUENCE_SPACE_KEY` | `GHConfDocs` |
| `CONFLUENCE_ROOT_PAGE_ID` | page id of *this repo's* root page |

The root page is created once (manually or via the API) and is never deleted
or modified by the sync.

Because the tool repository is private, configure
`CONFLUENCE_DOCS_SYNC_SSH_KEY` as the private key of a read-only deploy key on
`confluence-docs-sync`. Use a distinct key pair for this content repository.
This credential is separate from the Confluence credentials.

## Workflows

* **Sync docs to Confluence** — runs on pushes to `main` that touch `docs/`
  or the workflow itself, plus manual runs (`workflow_dispatch`) with two
  inputs:
  * `dry_run` — print the reconciliation plan without touching Confluence.
  * `force_delete` — authorise a deletion batch larger than the safeguard
    limits (see below).
* **Validate docs (PR)** — runs on pull requests; checks front matter, link
  targets, image references, Markdown conversion and Mermaid rendering. It
  receives no Confluence secrets and never publishes.

Both workflows check out `confluence-docs-sync` at `v1.0.0` into
`.confluence-docs-sync/` and pass this content workspace explicitly through
`--repo-root`. Upgrade or roll back the engine by changing the two workflow
pins together; never copy tool scripts into this repository. See the tool's
`RELEASING.md` for the complete process.

## Reconciliation guarantees

* Repeated runs against unchanged content make **no changes** (content hashes
  and content-addressed attachment names make it idempotent).
* Creations and updates complete **before** any deletion.
* Deletions:
  * only affect pages whose `ghdocsync` content property names **this
    repository**,
  * only operate **beneath this repository's root page** (re-verified against
    a freshly fetched page tree right before each delete),
  * never touch the root page, manually created pages, pages managed by the
    other repository, or pages with unmanaged children,
  * are **skipped entirely if any earlier step fails** (the script aborts
    before the deletion phase),
  * use Confluence's reversible trash (nothing is ever purged),
  * are **blocked** when more than 5 pages *or* more than 20% of managed
    pages would be trashed, unless `force_delete` is set.

## Recovery

* **Trashed page**: Confluence → Space → … → Trash → Restore. The page keeps
  its id; the next sync treats it as current again.
* **Wrong state / accidental mass delete**: restore from trash, fix the docs,
  re-run. Nothing is ever purged automatically.
* **Failed run**: the workflow fails visibly; Confluence may be missing the
  newest changes but nothing was half-deleted (deletions run last).
* **Unmanage a page**: remove its `ghdocsync` content property (Confluence
  REST or an admin macro) and the sync will ignore it forever.

## Limitations (known, accepted for the PoC)

* Internal links resolve **by page title**, so titles must be unique in the
  space (enforced per repository by validation; use a repo prefix like
  "Alpha …" / "Beta …").
* Heading anchors (`file.md#section`) are passed through as anchor parameters
  but Confluence's auto-generated anchors do not always match Markdown slugs.
* Raw HTML in Markdown is escaped as text (safe default).
* Only the Markdown subset listed in the PoC brief is converted (headings,
  paragraphs, emphasis, lists, quotes, tables, code, links, images, Mermaid).
* Attachments are content-addressed; superseded `ghsync-*` attachments are
  cleaned up automatically, but attachment *versions* remain in Confluence
  history.

## Cleanup

1. Revoke the API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Delete the GitHub secrets (or the whole repository).
3. Delete the two root pages in the space (sub-pages go to trash with them).

## Layout

```text
docs/
├── index.md                  home page
├── guide.md                  formatting sample
├── architecture/
│   ├── _index.md             folder page with stable identity
│   └── overview.md
├── policies/
│   ├── _index.md             folder page with stable identity
│   ├── deployment.md
│   └── retention.md
└── assets/
    └── example.png

.github/workflows/            thin pinned-tool consumers
```

The canonical scripts, dependencies, tests, and release documentation live only
in `confluence-docs-sync`.
