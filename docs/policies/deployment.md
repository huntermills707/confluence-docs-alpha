---
title: Alpha Deployment Topology
---

# Deployment Topology

## Environments

| Environment | Branch | Confluence space |
|---|---|---|
| Test | `main` | GHConfDocs |

## Steps performed by the pipeline

```text
checkout -> mark publish (render mermaid, reconcile confluence)
```

Notes:

- Pages are matched by title in the space; the page manifest mark keeps in
  Confluence tracks each file's page across renames and retitles.
- Removed files have their pages moved to the trash, and only if every other
  step of the run succeeded.
- Deletions are scoped to pages beneath this repository's root page and are
  always reversible (trash, never purge).

Related: [Alpha Architecture Overview](../architecture/overview.md),
[retention policy](retention.md).
