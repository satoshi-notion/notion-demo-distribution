# Notion demo distribution

Public, versioned skill instructions and deployment packages. Development remains in a separate private repository.

## Try Customer Hub with AIMN

Public test version: **1.5.0-public-test.1**, based on development package 1.5.0.

Give Notion AI this URL and ask it to follow the instructions:

https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.5.0-public-test.1/packages/customer-hub-aimn/1.5.0-public-test.1/SKILL.md

[Read the skill](packages/customer-hub-aimn/1.5.0-public-test.1/SKILL.md) · [Download the release](https://github.com/satoshi-notion/notion-demo-distribution/releases/tag/customer-hub-aimn/v1.5.0-public-test.1)

The instructions download a version-pinned package, verify its SHA-256, show the destination workspace and preview, and wait for your approval. Nothing is deployed until you approve in Notion AI. The package creates a new private teamspace in the workspace authenticated by the Notion CLI. It does not modify an earlier deployment.

## Requirements and limits

- Notion AI with web access and a shell sandbox, Node.js 20+, curl, tar, and Notion CLI 0.23+ with Notion as Code and public API access enabled.
- Permission to create private teamspaces and Custom Agents, and the in-app tools described in the skill.
- Calendar setup may require user action. Agent publishing and button actions remain manual.
- No central Deployments database is used in this public test. Keep the generated state and summary files before the sandbox expires.
- A URL provides instructions; it does not automatically register a Notion skill.
- Build, shared-kit tests (10/10), checksum verification, and an extracted-package dry run passed. The full Notion AI public-URL deployment and deployment outside Lumi Labs are not yet validated.

## Maintainer export

Run `python3 scripts/export-package.py /path/to/private/notion-demo-packages` to produce the public package and prompt. The exporter assembles a separate temporary package, removes private source-page references, and adapts the prompt and companion skill for standalone use. It does not edit the development checkout or deploy to Notion. Review outputs before publishing. Archives are release assets, not Git-tracked files.

Use package-specific tags such as `customer-hub-aimn/v1.5.0-public-test.1`. Keep published tags fixed so existing URLs remain usable.
