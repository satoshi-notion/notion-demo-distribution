---
name: remove-demo-deployment
description: Preview and remove one identified demo deployment using its private deployment-history record and cleanup manifest.
---

# Remove one demo deployment

Use only when the user explicitly asks to remove a deployed demo. This is separate from setup and evaluation. Reply in the user's language (English, Japanese, or Korean); prefer available native choice controls, otherwise short numbered choices. Never invent a tool or clickable UI.

## Identify and inspect (read-only)

1. Ask for the deployment-history record URL, or the private cleanup manifest and state/summary files. If several environments exist, show a choice with each record's timestamp, workspace, teamspace ID, version, and locale. Select exactly one. Names alone never identify a deployment. Do not use workspace-wide search to guess its resources.
2. Download that record's latest cleanup manifest. Run `node scripts/kit/cleanup-plan.mjs --manifest <cleanup.json>` from the matching extracted package. This only prints a preview and checks the CLI workspace. Confirm your native tools use the same workspace. If the manifest is missing, predates cleanup support, was inferred during evaluation, or contains unresolved/mismatched identities, stop as Blocked. Do not manufacture ownership from page titles. Older deployments require a separately reviewed inventory.
3. Fetch every exact agent, page/database trash root, and recorded external artifact. Inspect the complete current descendant tree, including paginated database rows and nested pages/databases. Compare with the manifest. Identify additions, moved resources, shared descendants, and access changes. Never treat 404/access denied as proof of deletion. A resource moved outside its recorded deployment, unreadable subtree, or unexplained ownership conflict blocks removal of that subtree. Do not remove shared history or any source/package page.
4. Show workspace, teamspace ID, package/version/locale, timestamp, exact roots and agent URLs, descendant counts, additions since deployment, calendar events/attendees, and irreversible or unsupported actions. State that trashing a parent includes its current descendants, including later user data. Shared uploaded assets, personal calendars, OAuth connections, other deployments, and the history database stay intact. If any operation is unsupported, list the manual step with the exact URL.

## Approval

Offer **Remove this deployment / Choose another environment / Cancel**. Bind approval to the displayed deployment ID, manifest digest, and live inventory. A preselected choice, silence, selection of an environment, or earlier setup approval is not consent. Changed targets, new descendants, or new invitees require a refreshed preview and fresh approval. Calendar cancellation can notify invitees: include the exact event and recipients in approval, or leave it for the person. Never permanently delete pages or empty Trash.

## Execute only the approved plan

1. Recheck identity and live inventory. Stop on drift. Using only tools actually available, disable the exact deployment agents' triggers before removing any content. If this cannot be verified, stop content removal and report the required manual action. Never reapply Notion as Code to clean up.
2. Remove only recorded, deployment-created calendar events by exact event AND calendar ID when explicitly included in approval. An event title or matching date is insufficient. Never delete a calendar or disconnect an account. If a response is uncertain, reconcile by ID before any retry.
3. Move the approved page/database roots to Trash with native tools. Their descendants are included; do not delete schema properties, views, or records individually. Do not delete relocated resources outside the approved subtree. Read back status where supported. On permission errors or uncertain outcomes, stop, preserve the partial result, and do not silently broaden scope.
4. Delete the exact approved Custom Agents only if a supported tool exists and approval covered that operation; otherwise give their exact URLs for manual deletion. Agents survive teamspace removal. Archive/remove the teamspace only if supported, its contents were inspected, and approval covered it; otherwise give its ID as a manual step. Never infer success from a missing search result.
5. Keep history, original state, summary, and manifest. Attach a timestamped cleanup result with each operation's ID and **Removed / Already removed (verified) / Blocked / Not attempted**, evidence, remaining manual steps, and the approved digest. Set history Status to **Removed** only after every intended object, including agents/events/teamspace, is confirmed removed; otherwise **Partially removed**. Do not overwrite an older manifest/result or delete the history record. Retrying requires the remaining-item preview and approval, not another deployment.

## History and later artifacts

Use the history record in the deployment summary; never assume Lumi Labs or a central author's database. Keep history private and outside the demo teamspace. The original manifest covers NaC resources. During setup or companion-skill execution, immediately append newly created external artifacts to that deployment's private manifest: `type`, exact `id`, `calendarId` for events, URL if returned, `createdByDeployment: true`, timestamp, and originating task. Never record a pre-existing/reused event as owned. Attach the updated manifest to the same history record and label the newest attachment with its timestamp; keep previous versions. If an event ID is unavailable, record an unresolved artifact and report cleanup as Blocked for that item. Do not mark complete while ignoring unresolved artifacts.

## Minimal entry prompts

Supply the history-record URL with one of these prompts and this file (or its published version-pinned URL):

- English: `Run this cleanup skill for the deployment history record below.`
- Japanese: `この削除スキルを、以下のデプロイ履歴に対して実行してください。`
- Korean: `아래 배포 기록에 대해 이 정리 스킬을 실행해 주세요.`
