# Notion demo distribution

Versioned Notion demo packages and hosted Notion Agent instructions. Development stays in a separate private repository.

## Customer Hub with AIMN

- **Prepared multilingual test:** [1.7.0-public-test.1](packages/customer-hub-aimn/1.7.0-public-test.1/README.md) — English, Japanese, and Korean in one archive. Not published yet. The version README contains copy-and-paste attachment and URL prompts, plus the evaluation procedure.
- **Previously published test:** [1.6.1-public-test.1](https://github.com/satoshi-notion/notion-demo-distribution/releases/tag/customer-hub-aimn/v1.6.1-public-test.1) — multilingual setup with native choice preferences; predates cleanup manifests.

Start with the [multilingual test README](packages/customer-hub-aimn/1.7.0-public-test.1/README.md). For an immediate local-artifact test, attach its SKILL.md and package to Notion Agent and use the attachment prompt. Use the version-pinned URL prompt after that version is published.

## Maintainer export

Run `python3 scripts/export-package.py /path/to/private/notion-demo-packages`. Review the archive, checksums, hosted prompt, version README, and draft release notes. Export does not publish, push, or deploy to Notion. Archives are release assets rather than Git-tracked files.

Keep package-specific tags fixed after publication. Update publication labels only after the tag, prompt, and release assets are verified accessible without authentication. The full Notion Agent run is evaluated separately from local build and dry-run checks.
