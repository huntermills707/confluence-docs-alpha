---
title: "Pipeline: Secrets and Permissions (Alpha)"
---

# Secrets and permissions

Only secret **names** appear in this repository; values live in GitHub and
Atlassian. The workflows read five GitHub secrets — nothing else is
configurable from outside.

## Atlassian side

### Space and root page

The publishing identity needs, in the target space:

- permission to view and browse the space,
- permission to **create and edit pages** beneath this repository's root
  page, and to **attach files** to them,
- **space administration** — only because `--track-pages` stores its page
  manifest as space properties on Confluence Cloud. If that is too much,
  drop space admin and switch the workflows to `--manifest-page <page>`,
  which keeps the manifest as content properties of one ordinary page.

The root page itself was created once by hand; mark never writes to it or
deletes it — it is only the parent of this repository's pages.

### API tokens

Create tokens at
<https://id.atlassian.com/manage-profile/security/api-tokens>.

**Copy the complete value.** A token ends in a `=XXXXX`-style segment that
is part of the credential, not an ID. Stripping it causes confusing 403
errors on some tenants.

Two kinds of token work with mark on Confluence Cloud:

| | Classic (unscoped) | Scoped (granular) |
|---|---|---|
| Auth | Basic `email:token` | Bearer, via the gateway |
| Base URL | `https://SITE.atlassian.net/wiki` | `https://api.atlassian.com/ex/confluence/CLOUD-ID` |
| Permissions | Full account permissions | Only the granted scopes |
| Page manifest | Space properties (needs space admin) | Use `--manifest-page` (space properties are not grantable) |

This repository currently uses a **classic** token: simplest, and the
token user is an admin of the PoC site anyway.

For least privilege in a real deployment, use a **scoped** token with:

- `read:space:confluence`, `read:page:confluence`,
  `write:page:confluence` — find, read, create, update pages,
- `read:attachment:confluence` — list page attachments,
- `read:label:confluence` — read page labels,
- `read:content.property:confluence`,
  `write:content.property:confluence` — content appearance and emoji
  title,

plus the classic-equivalent scopes for the operations mark still performs
through the v1 API (attachment uploads, moving pages among siblings,
orphan handling): `read:confluence-content.all`,
`write:confluence-content`, `read:confluence-user`. Prefer a dedicated
publishing account over a personal one, and rotate the token regularly —
replacing the token only means updating the GitHub secret.

## GitHub side

Settings → Secrets and variables → Actions, per repository:

| Secret | Example | Used for |
|---|---|---|
| `ATLASSIAN_BASE_URL` | `https://jaegermolino.atlassian.net` | Site URL; the workflow appends `/wiki` |
| `ATLASSIAN_USER_EMAIL` | you@example.com | Basic-auth username |
| `ATLASSIAN_API_TOKEN` | Atlassian API token | Basic-auth password |
| `CONFLUENCE_SPACE_KEY` | `GHConfDocs` | Target space |
| `CONFLUENCE_ROOT_PAGE_ID` | page id of this repo's root page | Scopes orphan deletion to this repo's subtree |

Notes:

- The workflow grants the job only `contents: read` — the `GITHUB_TOKEN`
  is never used for anything but the checkout.
- Secrets are available to pull-request workflows only for branches of
  this repository; forks cannot run validation. That matches the branch
  protection setup (in-repo branches, one required review).
- To rotate: create the new token, update `ATLASSIAN_API_TOKEN`, revoke
  the old one. No workflow change is needed.
