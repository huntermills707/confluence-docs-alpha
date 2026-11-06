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
- permission to **edit the root page**, because Mark stores the page manifest
  as content properties on it,
- **Delete pages** permission while `--on-orphan delete` is enabled. This
  moves pages to recoverable trash; Mark never purges them.

**Space administration is not required** for the page manifest. If it was
granted only for the old space-property manifest, remove it after the first
successful live publication with the scoped configuration.

The root page was created once by hand. Mark stores `alpha.sync` content
properties on it but never changes its body or title and never deletes it.

### Scoped API token

Create an **API token with scopes** at
<https://id.atlassian.com/manage-profile/security/api-tokens> and select the
Confluence app. Use a dedicated publishing account where possible.

**Copy the complete value.** A token ends in a `=XXXXX`-style segment that
is part of the credential, not an ID. Stripping it causes confusing 403
errors on some tenants.

Mark v16.25.0 uses both v2 and v1 APIs, so the token needs granular **and**
classic scopes. Select these granular scopes:

- `read:space:confluence` — resolve the space,
- `read:page:confluence` and `write:page:confluence` — find, read, create,
  update, and move pages,
- `read:hierarchical-content:confluence` — check children before orphan
  handling,
- `read:attachment:confluence` — list existing attachments,
- `read:label:confluence` — read page labels,
- `read:content.property:confluence` and
  `write:content.property:confluence` — read and write page metadata,
  including the root-page manifest.

Also select these classic scopes for operations Mark still performs through
v1:

- `read:confluence-content.all`,
- `write:confluence-content`,
- `read:confluence-user`,
- `write:confluence-file` — attachment uploads.

**No additional granular delete scope is needed for this setup.** Mark
v16.25.0 trashes orphans through v1 `DELETE /rest/api/content/{id}`, covered
by classic `write:confluence-content`. The account still needs the native
**Delete pages** space permission. `delete:page:confluence` applies to the
v2 deletion endpoint, which this Mark version does not use for orphan cleanup.

The workflows use Basic authentication with the account email and scoped
token through the Atlassian gateway. Keep `ATLASSIAN_USER_EMAIL` set; do not
switch to Bearer merely because the token is scoped.

## GitHub side

Settings → Secrets and variables → Actions, per repository:

| Secret | Example | Used for |
|---|---|---|
| `ATLASSIAN_BASE_URL` | `https://api.atlassian.com/ex/confluence/CLOUD-ID` | Complete gateway URL; **no `/wiki` suffix** |
| `ATLASSIAN_USER_EMAIL` | you@example.com | Basic-auth username |
| `ATLASSIAN_API_TOKEN` | Scoped Atlassian API token | Basic-auth password |
| `CONFLUENCE_SPACE_KEY` | `GHConfDocs` | Target space |
| `CONFLUENCE_ROOT_PAGE_ID` | page id of this repo's root page | Manifest location and orphan-deletion boundary |

Notes:

- The workflow grants the job only `contents: read` — the `GITHUB_TOKEN`
  is never used for anything but the checkout.
- Secrets are available to pull-request workflows only for branches of
  this repository; forks cannot run validation. That matches the branch
  protection setup (in-repo branches, one required review).
- To rotate: create a new scoped token with the same scopes, update
  `ATLASSIAN_API_TOKEN` in both repositories, validate, then revoke the old
  token. No workflow change is needed.
