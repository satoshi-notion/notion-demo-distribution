# Customer Hub with AIMN 1.6.0-public-test.1

One package supports English (`en`), Japanese (`ja`), and Korean (`ko`).

**Publication status:** published as a public prerelease. Use the URL prompt below for the complete public download flow. The older 1.5.0 test does not contain these multilingual changes.

## Test now with attachments

Attach both `SKILL.md` and `customer-hub-aimn-package.tar.gz` from this version to a new Notion Agent conversation. Paste this prompt:

```text
Use the attached SKILL.md to set up Customer Hub with AIMN, version 1.6.0-public-test.1.
Create the environment in Japanese (ja), and reply to me in Japanese.
Use the attached customer-hub-aimn-package.tar.gz as the package rather than downloading another copy. Verify its SHA-256 using SKILL.md before extracting or running it.
Follow the instructions exactly. First show the destination workspace, environment language, and preview, then wait for my explicit approval before creating anything.
After approval, deploy exactly once and complete the numbered work order. Preserve the state and summary JSON files and provide them as downloadable files for evaluation. Report every task's actual result and all remaining person steps. If anything fails, follow the documented retry and stop rules and preserve the available evidence.
```

Change `Japanese (ja)` to `English (en)` or `Korean (ko)` to test another environment language. Reply language can be chosen independently. Use one fresh conversation and one new deployment per test.

## Test by URL after publication

Paste this prompt into a new Notion Agent conversation after publication:

```text
Read the complete instructions at this URL and set up Customer Hub with AIMN, version 1.6.0-public-test.1:
https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v1.6.0-public-test.1/packages/customer-hub-aimn/1.6.0-public-test.1/SKILL.md

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
