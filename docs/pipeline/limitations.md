---
title: "Pipeline: Limitations and Roadmap (Alpha)"
---

# Limitations and roadmap

## Known limitations

- **Identity is the title.** Confluence allows one page per title per
  space, and this space is shared with `confluence-docs-beta`, so titles
  must stay globally unique (hence the "Alpha …" prefixes). A retitle
  combined with a heavy rewrite in the same change can defeat mark's
  rename detection and read as delete + create.
- **No numeric mass-deletion cap.** The safeguards are structural: a run
  with any failure removes nothing, pages with children outside the
  removal are untouched, and everything goes to recoverable trash. Use
  the workflow's `dry_run` input to preview large refactors first.
- **Root-page edit permission.** The page manifest lives in content
  properties on this repository's root page, so the publishing identity
  must be able to edit that page. Its body and title are not changed.
- **One-way sync.** Manual edits made directly in Confluence are
  overwritten by the next publish. `--no-overwrite` exists but is not
  enabled.
- **PR validation needs credentials.** Resolving links between documents
  performs read-only Confluence lookups, so fork pull requests (which
  never see secrets) cannot run it.
- **Mermaid is rasterised.** Diagrams publish as PNG images (sharp, but
  not editable in Confluence and re-rendered on every change).
- **Attachments are never garbage-collected.** Superseded attachments
  stay on the page; in particular, artifacts from the previous custom
  engine (`ghdocsync` properties, `ghsync-*` files) remain until removed
  by hand.
- **Publisher pinned to mark v16.25.0.** v17 is a major release with
  breaking changes (admonition syntax, stricter configuration, CLI
  reorganisation) — upgrading is deliberate work, not a tag bump; see
  `MARK-V17-NOTES.md` at the PoC root for the analysis and upgrade path.

## Potential improvements

- Enable `--no-overwrite` so hand-edited pages are flagged instead of
  silently reverted (works with the already-enabled page manifest).
- Use a separate read-only scoped token for PR validation so those jobs do
  not receive publishing credentials (see [secrets and permissions](setup.md)).
- Pin the Docker image **by digest** rather than tag for supply-chain
  hardening.
- Extend the PR gate with `--check-links confluence` (and `external`,
  accepting the network dependency) once enough pages exist.
- Switch to `--mermaid-output=svg` for sharper, lighter diagrams.
- Add Confluence **labels** per repository for filtering and search.
- Add a scheduled dry-run workflow that reports drift between `main` and
  Confluence without publishing.
- Write a one-off cleanup script for the old-engine artifacts and run it
  once after the first mark sync.
- Plan the mark v17 upgrade on a branch, using the dry-run input to
  diff behaviour before merging.
