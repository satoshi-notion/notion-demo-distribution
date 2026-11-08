"""Export a standalone public test package from a private development checkout."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

source = Path(sys.argv[1]).resolve()
repo = Path(__file__).resolve().parents[1]
slug = "customer-hub-aimn"
version = "1.5.0-public-test.1"
tag = f"{slug}/v{version}"
base = "https://github.com/satoshi-notion/notion-demo-distribution"
release = f"{base}/releases/download/{tag}"
out = repo / "packages" / slug / version
out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="notion-public-export-") as temporary:
    stage = Path(temporary) / slug
    ignore = shutil.ignore_patterns(".notion-state", ".notion-source", "dist", "node_modules", ".env*", "*.log", "*.DS_Store", "skeleton", "docs")
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
    skill["packageNotes"] = ["Public test distribution based on 1.5.0. Full deployment from a public URL has not yet been validated. No central Deployments database is used; retain the state and summary files from this run."]
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
    template = stage / "scripts/kit/skill-template.md"
    text = template.read_text()
    mention = '<mention url="{{deploymentsDatabase}}">Deployments</mention>'
    text = text.replace(f"except the deployment record in {mention} and the agents the work order names", "except the agents the work order names")
    text = text.replace(f", and can add records to {mention}", "")
    text = text.replace("edit the package and attach a new version to this page", "publish a new version of the package and these instructions")
    text = text.replace("Download and extract the attached archive <b>{{packageFile}}</b>. If more than one package is attached, use the newest. It has no npm dependencies.", f"Download the version-pinned archive from {release}/{{{{packageFile}}}}. It has no npm dependencies. Verify its SHA-256 against the value below before extracting it.")
    text = text.replace("{{packageBlock}}", "PACKAGE_CHECKSUM")
    text = text.replace("Node.js 20 or later, `tar`", "Node.js 20 or later, `curl`, `tar`")
    text = text.replace("tar -xzf {{packageFile}}", f"curl --fail --location --output {{{{packageFile}}}} '{release}/{{{{packageFile}}}}'\n" + "CHECKSUM_COMMAND\ntar -xzf {{packageFile}}")
    text = text.replace('node scripts/kit/deploy-new.mjs --record-in "{{deploymentsDatabase}}"', 'node scripts/kit/deploy-new.mjs')
    a = text.index("The script uses a new state file", text.index("## Step 2"))
    b = text.index("\n| Exit code", a)
    text = text[:a] + "The script builds and checks the package, applies it once to the CLI login's workspace, completes and verifies the records, and prints a JSON summary with teamspace, sidebar, agents, verify, statePath, and finish. This public test does not write to a Deployments database. Preserve the state file and summary as downloadable files for the user before the sandbox expires. Use only the URLs in this run's summary.\n" + text[b:]
    text = text.replace("If it passes, set the deployment record's Verification to Passed. ", "")
    text = text.replace("its deployment record lists the failed step as a problem", "the summary lists the failed step as a problem")
    text = text.replace("the deployment record's Deployed by", "any person properties listed in the work order")
    text = text.replace("Deployment record: [deploymentRecord.url]. ", "")
    text = text.replace("Deployment record: [deploymentRecord.url] · ", "")
    text = text.replace("and its deployment record lists the problem", "and the summary lists the problem")
    text = text.replace("check the agent URLs on the deployment record", "check the agent URLs in the saved deployment summary")
    text = text.replace("3. Set the deployment record's Status to Removed. Keep the record: Deployments is the history of who deployed which package and when.", "3. Keep the saved state and summary for your records.")
    template.write_text(text)
    subprocess.run(["node", "scripts/kit/render-skill.mjs", "--deployments", base, "--out", str(out / "SKILL.md")], cwd=stage, check=True)
    subprocess.run(["npm", "run", "build"], cwd=stage, check=True)
    subprocess.run(["npm", "test"], cwd=source / "kit", check=True)
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
    (out / "release-notes.md").write_text(f"# Customer Hub with AIMN {version}\n\nPublic URL deployment test based on package 1.5.0.\n\nRead [the full skill instructions]({base}/blob/{tag}/packages/{slug}/{version}/SKILL.md) in Notion AI. Follow the preview and approval steps before creating anything.\n\nThis build has no dependency on the private Lumi Labs Deployments database. Keep the generated state and summary files. The end-to-end Notion AI URL flow is not yet validated.\n")
print(out)
