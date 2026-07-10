# Publication Audit

Audit date: 2026-07-10

## Scope

The review covers the installable skill, bundled templates, regression fixtures, documentation, scripts, and repository metadata intended for a public GitHub repository.

## Result

No API keys, passwords, access tokens, private keys, email addresses, local usernames, home-directory paths, temporary-directory paths, or remote customer URLs are intentionally included in this public tree.

The public regression fixtures are generated from code. They use generic English content and programmatically drawn geometric artwork. No customer slide, corporate logo, proprietary screenshot, or organization-specific copy is included.

## Material Removed From The Private Working Copy

- organization-specific slide references and screenshots;
- branded icons and logos;
- customer and project copy;
- absolute paths containing a local account name;
- source-specific regression metadata;
- build timestamps and author metadata in base PPTX templates.

## Third-Party Code

The bundled `ppt-master` converter subset is MIT-licensed. Its original license file is retained and the dependency is listed in `THIRD_PARTY_NOTICES.md`.

## Residual Risk

Users can still place confidential content into run directories when using the skill. Before publishing examples or bug reports, scan generated `design-contract.json`, `scene.json`, manifests, traces, PPTX metadata, and image assets for private content and absolute paths.

Recommended release scan:

```bash
rg -n --hidden -S \
  '(api[_-]?key|secret|token|password|private key|authorization:|/Users/|/home/|file://|https?://[^ )]+@)' .
```

Also inspect binary metadata with `exiftool` and PPTX package metadata in `docProps/core.xml` before a release.
