---
doc_id: 54960bab-7394-430d-aa57-0eff3312f96e
title: Alpha Deployment Topology
---

# Deployment Topology

## Environments

| Environment | Branch | Confluence space |
|---|---|---|
| Test | `main` | GHConfDocs |

## Steps performed by the pipeline

```text
checkout -> install deps -> render mermaid -> reconcile confluence
```

Notes:

- Pages are matched by `doc_id`, never by title.
- Deletions happen last and only after every creation and update succeeded.
- More than five deletions, or more than 20% of managed pages, requires the
  `force_delete` override.

Related: [Alpha Architecture Overview](../architecture/overview.md),
[retention policy](retention.md).
