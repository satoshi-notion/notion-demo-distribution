"""Write versioned test prompts and read-only evaluation instructions."""
from pathlib import Path
import sys
repo=Path(__file__).resolve().parents[1]
version=sys.argv[1];slug='customer-hub-aimn'
published='--published' in sys.argv
url=f'https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/{slug}/v{version}/packages/{slug}/{version}/SKILL.md'
intro=f'''# Customer Hub with AIMN {version}

One package supports English (`en`), Japanese (`ja`), and Korean (`ko`).

**Publication status:** this version is prepared locally and has not been published. Its version-pinned URLs will work only after the matching Git tag and release assets are published. For an immediate test, use the attachment prompt below. The previously published 1.5.0 test does not contain these multilingual changes.

## Test now with attachments

Attach both `SKILL.md` and `customer-hub-aimn-package.tar.gz` from this version to a new Notion Agent conversation. Paste this prompt:

```text
Use the attached SKILL.md to set up Customer Hub with AIMN, version {version}.
Create the environment in Japanese (ja), and reply to me in Japanese.
Use the attached customer-hub-aimn-package.tar.gz as the package; this version's public download URL is not published yet. Verify its SHA-256 using SKILL.md before extracting or running it.
Follow the instructions exactly. First show the destination workspace, environment language, and preview, then wait for my explicit approval before creating anything.
After approval, deploy exactly once and complete the numbered work order. Preserve the state and summary JSON files and provide them as downloadable files for evaluation. Report every task's actual result and all remaining person steps. If anything fails, follow the documented retry and stop rules and preserve the available evidence.
```

Change `Japanese (ja)` to `English (en)` or `Korean (ko)` to test another environment language. Reply language can be chosen independently. Use one fresh conversation and one new deployment per test.

## Test by URL after publication

Paste this prompt into a new Notion Agent conversation after publication:

```text
Read the complete instructions at this URL and set up Customer Hub with AIMN, version {version}:
{url}

Create the environment in Japanese (ja), and reply to me in Japanese.
Follow the instructions exactly. First show the destination workspace, environment language, and preview, then wait for my explicit approval before creating anything.
After approval, deploy exactly once and complete the numbered work order. Preserve the state and summary JSON files and provide them as downloadable files for evaluation. Report every task's actual result and all remaining person steps. If anything fails, follow the documented retry and stop rules and preserve the available evidence.
```

Change `Japanese (ja)` to `English (en)` or `Korean (ko)` as needed. Confirm that the preview shows the intended workspace before approving.

## Evaluation after the run

Give the evaluator:

1. The Notion Agent conversation URL and its final report. If the conversation is not readable through the connected tools, provide the relevant execution transcript.
2. The new teamspace URL and selected language.
3. The downloaded deployment state JSON and summary JSON. These identify the exact created resources; names alone are insufficient because deployments can share names.
4. Any final verification output, blocked-task errors, and which person steps you actually completed.

Send evaluation evidence privately; never commit state or summary files to the public distribution repository. Do not share tokens or credentials. Do not delete a failed deployment before evaluation. Do not rerun apply to repair it.

Keep the Step 3 baseline verification output before running the manual demo test. After a handoff or meeting test, distinguish the original 105 seeded records from legitimate projects, tasks, or SOWs created by that test; a strict verifier may report those as extra records. Evaluate the functional additions separately rather than deleting them or treating every addition as seed drift.

The evaluator checks only the identified deployment, read-only:

| Area | Evidence and acceptance criteria |
| --- | --- |
| Execution | Correct version, locale, destination, explicit approval, one apply, and documented retry/stop behavior |
| Structure | 134 resource identities in the expected structure, 105 demo records across 12 seed tables, 4 agents, sidebar order, and private teamspace evidence |
| Data | Seed properties and relations, templates, bodies, logos/files, and green Notion icons; compare against the selected locale's expected data |
| Work order | T1–T10 results; person cells, Meetings conversion, exact buttons, layouts, skill registration, draft agent access, Calendar connection, and linked event |
| Guardrails | Person cells were set with native page tools rather than bot scripts; no second apply or unapproved edits outside the new deployment; notification history is not inferred from final state |
| Localization | Names and schema references agree; content uses the selected language; IDs, formulas, numbers, and dates retain their meaning |
| Demo readiness | Agent publication, manual button actions, and the app-triggered handoff test, only after the person actually completes them |

Results are **Pass**, **Fail**, **Blocked**, or **Not tested**, with evidence for each finding. Script success does not prove the manual steps or the complete demo work. Inaccessible agent settings, calendar data, UI-only actions, or notification history remain unverified. Two independently evaluated runs per language are the repeatability target; one successful run is an initial validation.

Repairs, Notion writes, cleanup, publishing, or another deployment require a separate instruction. If the evaluator's connected workspace differs from the deployment workspace, stop and resolve access rather than inspecting an unrelated environment.

## Package files and requirements

- `SKILL.md`: complete deployment instructions, language selection, checks, guardrails, and evidence requirements.
- `customer-hub-aimn-package.tar.gz`: one archive containing all three languages.
- `SHA256SUMS`: archive checksum.
- `release-notes.md`: local validation and remaining limits.

Notion Agent needs web/file access, a shell sandbox, Node.js 20+, curl, tar, and Notion CLI 0.23+ with NaC and public API access. The user needs permission to create private teamspaces and Custom Agents and the in-app tools named in SKILL.md. Calendar setup, publishing agents, and button actions may require the person. This public test does not use the private Lumi Labs Deployments database.
'''
# Keep the entry prompts short; the hosted skill owns approval and evidence rules.
a=intro.index("## Test now with attachments")
b=intro.index("## Evaluation after the run", a)
short = "## Test now with attachments\n\nAttach this version's SKILL.md and customer-hub-aimn-package.tar.gz to a new conversation. Copy one prompt:\n\n"
for title, sentence in [("English", "Run the attached SKILL.md using the attached package."), ("日本語", "添付したSKILL.mdのスキルを、添付パッケージで実行してください。"), ("한국어", "첨부된 SKILL.md의 스킬을 첨부 패키지로 실행해 주세요.")]:
    short += f"### {title}\n\n```text\n{sentence}\n```\n\n"
short += "## Test by URL after publication\n\nCopy one prompt into a new conversation. The skill infers the environment language from the request and asks for explicit approval after the preview.\n\n"
for title, sentence in [("English", "Run the skill at this URL:"), ("日本語", "次のURLのスキルを実行してください。"), ("한국어", "다음 URL의 스킬을 실행해 주세요.")]:
    short += f"### {title}\n\n```text\n{sentence}\n{url}\n```\n\n"
intro = intro[:a] + short + intro[b:]
cleanup_url = url.removesuffix("SKILL.md") + "CLEANUP.md"
history = """## Private deployment history and cleanup

Setup reuses an explicitly identified private history database in your destination workspace, or offers to create one after approval. History stays outside demo teamspaces. Each environment gets its own record with workspace/teamspace IDs, timestamp, version, locale, state, summary, and cleanup manifest. Keep these records private; the author's central database is never required.

To remove one environment, copy its history-record URL and pass it with the cleanup skill. Cleanup first inspects and previews the exact current scope, then waits for explicit approval. Later user-created descendants are included in that preview. Unsupported agent/teamspace deletion remains a manual step; history and evidence are retained. Older deployments without a cleanup manifest need a separately reviewed inventory.

"""
for title, sentence in [("English", "Run the cleanup skill at this URL for the deployment history record below:"), ("日本語", "次のURLの削除スキルを、以下のデプロイ履歴に対して実行してください。"), ("한국어", "다음 URL의 정리 스킬을 아래 배포 기록에 대해 실행해 주세요.")]:
    history += f"### {title}\n\n```text\n{sentence}\n{cleanup_url}\n<HISTORY_RECORD_URL>\n```\n\n"
intro = intro.replace("## Evaluation after the run", history + "## Evaluation after the run")
intro = intro.replace("This public test does not use the private Lumi Labs Deployments database.", "This public test uses your approved private history database, not the author's Lumi Labs database.")
intro = intro.replace("- `SHA256SUMS`: archive checksum.", "- `CLEANUP.md`: separate cleanup skill; requires a deployment-history record and manifest.\n- `SHA256SUMS`: archive checksum.")

out=repo/'packages'/slug/version
out.mkdir(parents=True, exist_ok=True)
(out/'README.md').write_text(intro)
(repo/'README.md').write_text(f'''# Notion demo distribution

Versioned Notion demo packages and hosted Notion Agent instructions. Development stays in a separate private repository.

## Customer Hub with AIMN

- **Prepared multilingual test:** [{version}](packages/{slug}/{version}/README.md) — English, Japanese, and Korean in one archive. Not published yet. The version README contains copy-and-paste attachment and URL prompts, plus the evaluation procedure.
- **Previously published test:** [1.6.1-public-test.1](https://github.com/satoshi-notion/notion-demo-distribution/releases/tag/customer-hub-aimn/v1.6.1-public-test.1) — multilingual setup with native choice preferences; predates cleanup manifests.

Start with the [multilingual test README](packages/{slug}/{version}/README.md). For an immediate local-artifact test, attach its SKILL.md and package to Notion Agent and use the attachment prompt. Use the version-pinned URL prompt after that version is published.

## Maintainer export

Run `python3 scripts/export-package.py /path/to/private/notion-demo-packages`. Review the archive, checksums, hosted prompt, version README, and draft release notes. Export does not publish, push, or deploy to Notion. Archives are release assets rather than Git-tracked files.

Keep package-specific tags fixed after publication. Update publication labels only after the tag, prompt, and release assets are verified accessible without authentication. The full Notion Agent run is evaluated separately from local build and dry-run checks.
''')

if published:
    path=out/'README.md'
    text=path.read_text().replace('**Publication status:** this version is prepared locally and has not been published. Its version-pinned URLs will work only after the matching Git tag and release assets are published. For an immediate test, use the attachment prompt below. The previously published 1.5.0 test does not contain these multilingual changes.', '**Publication status:** published as a public prerelease. Use the URL prompt below for the complete public download flow. The older 1.5.0 test does not contain these multilingual changes.')
    text=text.replace("Use the attached customer-hub-aimn-package.tar.gz as the package; this version's public download URL is not published yet.", 'Use the attached customer-hub-aimn-package.tar.gz as the package rather than downloading another copy.')
    path.write_text(text)
    path=repo/'README.md'
    text=path.read_text().replace('Prepared multilingual test:', 'Published multilingual test:').replace('Not published yet.', 'Published prerelease.').replace('For an immediate local-artifact test, attach its SKILL.md and package to Notion Agent and use the attachment prompt. Use the version-pinned URL prompt after that version is published.', 'Use the version-pinned URL prompt for the complete public download flow. The attachment prompt is also available for a file-based test.')
    path.write_text(text)
