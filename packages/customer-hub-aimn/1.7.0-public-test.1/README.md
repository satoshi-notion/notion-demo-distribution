# Customer Hub with AIMN 1.7.0-public-test.1

One package supports English (`en`), Japanese (`ja`), and Korean (`ko`).

**Publication status:** this version is prepared locally and has not been published. Its version-pinned URLs will work only after the matching Git tag and release assets are published. For an immediate test, use the attachment prompt below. The previously published 1.5.0 test does not contain these multilingual changes.

## Test now with attachments

Attach this version's SKILL.md and customer-hub-aimn-package.tar.gz to a new conversation. Copy one prompt:

### English

```text
Run the attached SKILL.md using the attached package.
```

### 日本語

```text
添付したSKILL.mdのスキルを、添付パッケージで実行してください。
```

### 한국어

```text
첨부된 SKILL.md의 스킬을 첨부 패키지로 실행해 주세요.
```

## Test by URL after publication

Copy one prompt into a new conversation. The skill infers the environment language from the request and asks for explicit approval after the preview.

### English

```text
Run the skill at this URL:
https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.7.0-public-test.1/packages/customer-hub-aimn/1.7.0-public-test.1/SKILL.md
```

### 日本語

```text
次のURLのスキルを実行してください。
https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.7.0-public-test.1/packages/customer-hub-aimn/1.7.0-public-test.1/SKILL.md
```

### 한국어

```text
다음 URL의 스킬을 실행해 주세요.
https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.7.0-public-test.1/packages/customer-hub-aimn/1.7.0-public-test.1/SKILL.md
```

## Private deployment history and cleanup

Setup reuses an explicitly identified private history database in your destination workspace, or offers to create one after approval. History stays outside demo teamspaces. Each environment gets its own record with workspace/teamspace IDs, timestamp, version, locale, state, summary, and cleanup manifest. Keep these records private; the author's central database is never required.

To remove one environment, copy its history-record URL and pass it with the cleanup skill. Cleanup first inspects and previews the exact current scope, then waits for explicit approval. Later user-created descendants are included in that preview. Unsupported agent/teamspace deletion remains a manual step; history and evidence are retained. Older deployments without a cleanup manifest need a separately reviewed inventory.

### English

```text
Run the cleanup skill at this URL for the deployment history record below:
https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.7.0-public-test.1/packages/customer-hub-aimn/1.7.0-public-test.1/CLEANUP.md
<HISTORY_RECORD_URL>
```

### 日本語

```text
次のURLの削除スキルを、以下のデプロイ履歴に対して実行してください。
https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.7.0-public-test.1/packages/customer-hub-aimn/1.7.0-public-test.1/CLEANUP.md
<HISTORY_RECORD_URL>
```

### 한국어

```text
다음 URL의 정리 스킬을 아래 배포 기록에 대해 실행해 주세요.
https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.7.0-public-test.1/packages/customer-hub-aimn/1.7.0-public-test.1/CLEANUP.md
<HISTORY_RECORD_URL>
```

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
- `CLEANUP.md`: separate cleanup skill; requires a deployment-history record and manifest.
- `SHA256SUMS`: archive checksum.
- `release-notes.md`: local validation and remaining limits.

Notion Agent needs web/file access, a shell sandbox, Node.js 20+, curl, tar, and Notion CLI 0.23+ with NaC and public API access. The user needs permission to create private teamspaces and Custom Agents and the in-app tools named in SKILL.md. Calendar setup, publishing agents, and button actions may require the person. This public test uses your approved private history database, not the author's Lumi Labs database.
