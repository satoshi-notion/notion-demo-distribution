"""Export a standalone public test package from a private development checkout."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

source = Path(sys.argv[1]).resolve()
# Accept either the consolidated private root or the original project-local layout.
if (source / "demo-deployment-packages" / "solutions").is_dir():
    source = source / "demo-deployment-packages"
if not (source / "kit").is_dir() or not (source / "solutions").is_dir():
    raise SystemExit("Choose the private operations root or its demo-deployment-packages directory.")
repo = Path(__file__).resolve().parents[1]
slug = "customer-hub-aimn"
development_version = json.loads((source / "solutions" / slug / "solution.json").read_text())["version"]
version = f"{development_version}-public-test.1"
tag = f"{slug}/v{version}"
base = "https://github.com/satoshi-notion/notion-demo-distribution"
release = f"{base}/releases/download/{tag}"
out = repo / "packages" / slug / version
out.mkdir(parents=True, exist_ok=True)
subprocess.run([sys.executable, str(repo / "scripts/write-readme.py"), version, *(["--published"] if "--published" in sys.argv[2:] else [])], check=True)
with tempfile.TemporaryDirectory(prefix="notion-public-export-") as temporary:
    stage = Path(temporary) / slug
    ignore = shutil.ignore_patterns(".notion-state", ".notion-source", "dist", "node_modules", ".env*", "*.log", "*.DS_Store", "skeleton", "docs", "reviewed-files", "reviewed")
    shutil.copytree(source / "kit", stage, ignore=ignore)
    shutil.copytree(source / "solutions" / slug, stage, dirs_exist_ok=True, ignore=ignore)
    package = json.loads((stage / "package.json").read_text())
    package.update(name=slug, version=version)
    (stage / "package.json").write_text(json.dumps(package, indent=2) + "\n")
    solution = json.loads((stage / "solution.json").read_text())
    solution["version"] = version
    (stage / "solution.json").write_text(json.dumps(solution, indent=2) + "\n")
    skill_path = stage / "source/skill.json"
    skill = json.loads(skill_path.read_text())
    skill["explainer"] = f"{base}/tree/{tag}"
    skill["companionSkills"] = []
    skill["packageNotes"] = ["Public multilingual test distribution. Supports en, ja, and ko. Full deployment from a public URL has not yet been validated. No central Deployments database is used; retain the state and summary files from this run."]
    skill["personSteps"] = [s.replace(" The package page shows each setting with screenshots.", "") for s in skill["personSteps"]]
    skill_path.write_text(json.dumps(skill, indent=2) + "\n")
    # Remove private source URLs while retaining local snapshot generation.
    for path in [stage / "source/build-snapshot.mjs", stage / "notion-code.config.json"]:
        path.write_text(re.sub(r"https://app\.notion\.com/p/[a-f0-9]+", base, path.read_text()))
    companion = stage / "source/skills/schedule-demo-call.md"
    text = companion.read_text()
    start = text.index("1. <b>Find the deployment.</b>")
    end = text.index("2. <b>Choose the slot.</b>")
    text = text[:start] + "1. <b>Find the deployment.</b> Use the teamspace URL from the user's request or this conversation's deployment summary. If neither is available, stop with template R2 and ask the user to provide the deployment teamspace URL. Never select a teamspace by name alone. Open that teamspace and locate its Sales Meetings database.\n" + text[end:]
    companion.write_text(text)
    for locale in ["ja", "ko"]:
        catalog_path = stage / "source/locales" / f"{locale}.json"
        catalog = json.loads(catalog_path.read_text())
        path = "source/skills/schedule-demo-call.md"
        replacement = {
            "ja": "1. <b>デプロイ先を確認する。</b> ユーザーの依頼またはこの会話のデプロイ結果にあるチームスペースURLを使ってください。URLがなければテンプレートR2で停止し、ユーザーにURLの提示を依頼してください。名前だけでチームスペースを選ばないでください。そのチームスペース内の営業ミーティングデータベースを確認してください。\\n",
            "ko": "1. <b>배포 위치 확인.</b> 사용자 요청 또는 이 대화의 배포 결과에 있는 팀스페이스 URL을 사용하세요. URL이 없으면 템플릿 R2로 중단하고 사용자에게 URL을 요청하세요. 이름만으로 팀스페이스를 선택하지 마세요. 해당 팀스페이스의 영업 회의 데이터베이스를 확인하세요.\\n",
        }[locale]
        catalog["files"][path] = re.sub(r"(?ms)^1[.] <b>.*?(?=^2[.] <b>)", lambda _: replacement.removesuffix(r"\n") + chr(10), catalog["files"][path])
        catalog["provenance"]["sourceFiles"][path] = hashlib.sha256(text.encode()).hexdigest()
        catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + chr(10))
    template = stage / "scripts/kit/skill-template.md"
    text = template.read_text()
    mention = '<mention url="{{deploymentsDatabase}}">Deployments</mention>'
    text = text.replace(f"except the deployment record in {mention} and the agents the work order names", "except this deployment's record and evidence in the approved private history database, and the agents the work order names")
    text = text.replace(f", and can add records to {mention}", "")
    text = text.replace("edit the package and attach a new version to this page", "publish a new version of the package and these instructions")
    text = text.replace("Download and extract the attached archive <b>{{packageFile}}</b>. If more than one package is attached, use the newest. It has no npm dependencies.", f"Download the version-pinned archive from {release}/{{{{packageFile}}}}. It has no npm dependencies. If the user attached this exact package version, save that archive under the same filename and use it instead of downloading. In either mode, verify its SHA-256 against the value below before extracting it.")
    text = text.replace("{{packageBlock}}", "PACKAGE_CHECKSUM")
    text = text.replace("Notion AI with web access and a sandbox", "Notion AI with access to the attached instructions/package (or web access for URL mode) and a sandbox")
    text = text.replace("Node.js 20 or later, `tar`", "Node.js 20 or later, `curl`, `tar`")
    text = text.replace("tar -xzf {{packageFile}}", f"if [ ! -f {{{{packageFile}}}} ]; then curl --fail --location --output {{{{packageFile}}}} '{release}/{{{{packageFile}}}}'; fi\n" + "CHECKSUM_COMMAND\ntar -xzf {{packageFile}}")
    text = text.replace('node scripts/kit/deploy-new.mjs --record-in "{{deploymentsDatabase}}"', 'node scripts/kit/deploy-new.mjs --record-in "HISTORY_DATABASE_URL"')
    text = text.replace("## Step 1 — Check and preview", """## Private deployment history

Before the preview, resolve the user's private history database URL in this destination workspace. Reuse the exact URL supplied in this conversation or a prior saved summary; never select by name alone. If unknown, offer **Use existing history / Create private history / Cancel**, using native choices when available. Existing history requires its exact URL and confirmation of private access outside demo teamspaces. The choice alone does not approve creation.

For a new history, include **Demo Deployment History**, private access, and its creation in the deployment preview. Only after approval, create it with native tools outside the demo teamspace, with green Notion icons. Use columns: Name (title); Deployment ID, Workspace ID, Teamspace ID, Version (text); Locale (select: en, ja, ko); Workspace (select); Deployed at (date); Deployed by (person); Verification (select: Passed, Problems, Not run); Status (select: Active, Partially removed, Removed); Open (URL). No Package relation is required. If private placement or required tools cannot be verified, stop before deployment. Do not create a public/shared history or silently omit recording.

Replace HISTORY_DATABASE_URL in Step 2 with that exact database URL. Show it in the approval preview for existing history. The approved scope includes adding this deployment's history record and private recovery attachments. The database itself survives demo cleanup. A different history destination requires a new preview and approval.

## Step 1 — Check and preview""")
    a = text.index("The script uses a new state file", text.index("## Step 2"))
    b = text.index("\n| Exit code", a)
    text = text[:a] + "The script builds and checks the package, applies it once to the CLI login's workspace, completes and verifies the records, and writes one record to the approved private history database. It prints a summary with deploymentId, teamspace, sidebar, agents, verify, statePath, cleanupManifestPath, deploymentRecord, and finish. Preserve the state, final summary, and cleanup manifest privately before the sandbox expires. If history recording fails, report Blocked, preserve downloads, and never deploy again. Use only this run's IDs and URLs.\n" + text[b:]
    text = text.replace("its deployment record lists the failed step as a problem", "the summary lists the failed step as a problem")
    text = text.replace("the deployment record's Deployed by", "any person properties listed in the work order")
    text = text.replace("and its deployment record lists the problem", "and the summary lists the problem")
    text = text.replace("check the agent URLs on the deployment record", "check the agent URLs in the saved deployment summary")
    text = text.replace("3. Set the deployment record's Status to Removed. Keep the record: Deployments is the history of who deployed which package and when.", "3. Keep the saved state and summary for your records.")
    text += "\n\n## Evaluation evidence\n\nAt the end, provide the teamspace URL, selected locale, package version, the complete T1–T10 results, and the remaining person steps. Make the deployment state JSON and its summary JSON available as downloadable files before the sandbox expires. Include the full final verify --finish output in the chat or a downloadable text file. If blocked, preserve available evidence and report the exact failure. Never include authentication tokens, credentials, or environment-variable dumps. A pending person step is not completed merely because the scripted checks pass.\n"
    template.write_text(text)
    shutil.copyfile(stage / "CLEANUP.md", out / "CLEANUP.md")
    subprocess.run(["node", "scripts/kit/render-skill.mjs", "--deployments", base, "--out", str(out / "SKILL.md")], cwd=stage, check=True)
    subprocess.run(["npm", "run", "build"], cwd=stage, check=True)
    subprocess.run(["node", "scripts/kit/check-locales.mjs"], cwd=stage, check=True)
    subprocess.run(["npm", "test"], cwd=source / "kit", check=True)
    shutil.copyfile(out / "README.md", stage / "README.md")
    archive = out / f"{slug}-package.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for path in sorted(stage.rglob("*")):
            relative = path.relative_to(stage)
            if path.is_file() and not any(x in relative.parts for x in ["dist", ".notion-source", ".notion-state", "node_modules"]):
                tar.add(path, arcname=str(Path(slug) / relative), recursive=False)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    prompt = (out / "SKILL.md").read_text().replace("PACKAGE_CHECKSUM", f"SHA-256: `{digest}`")
    command = f"node --input-type=module -e \"import {{readFileSync}} from 'node:fs'; import {{createHash}} from 'node:crypto'; if(createHash('sha256').update(readFileSync('{slug}-package.tar.gz')).digest('hex') !== '{digest}') throw new Error('Package checksum mismatch');\""
    prompt = prompt.replace("CHECKSUM_COMMAND", command)
    (out / "SKILL.md").write_text(prompt)
    (out / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n")
    subprocess.run([sys.executable, str(repo / "scripts/write-release-notes.py"), version, development_version], check=True)

bundle = out / f"{slug}-{version}-distribution.zip"
with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as zip:
    for name in ["README.md", "SKILL.md", "CLEANUP.md", f"{slug}-package.tar.gz", "SHA256SUMS", "release-notes.md"]:
        zip.write(out / name, arcname=f"{slug}-{version}/{name}")
print(out)
print(bundle)
