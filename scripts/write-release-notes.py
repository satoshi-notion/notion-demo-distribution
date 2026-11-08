"""Render release notes with copyable prompts for all supported languages."""
from pathlib import Path
import sys

version = sys.argv[1]
development_version = sys.argv[2]
repo = Path(__file__).resolve().parents[1]
out = repo / "packages/customer-hub-aimn" / version
url = f"https://raw.githubusercontent.com/satoshi-notion/notion-demo-distribution/customer-hub-aimn/v{version}/packages/customer-hub-aimn/{version}/SKILL.md"
prompts = [
    ("English", f"Run the skill at this URL:\n{url}"),
    ("日本語", f"次のURLのスキルを実行してください。\n{url}"),
    ("한국어", f"다음 URL의 스킬을 실행해 주세요.\n{url}"),
]

text = f"# Customer Hub with AIMN {version}\n\nOne package supports English, Japanese, and Korean. Based on development package {development_version}.\n\n## Copy a prompt into Notion Agent\n\nChoose one language below and copy the entire block into a new conversation. Verify the destination in the preview before approving.\n\n"
for title, prompt in prompts:
    text += f"### {title}\n\n```text\n{prompt}\n```\n\n"
text += "## After the run\n\nShare the conversation URL, new teamspace URL, and state/summary files privately with the evaluator. Do not publish state files or credentials. The evaluator separates scripted verification, remaining person steps, and actual demo behavior.\n\nThis build does not depend on the private Lumi Labs Deployments database. Local builds, tests, and dry runs passed; full Notion Agent execution is still awaiting validation.\n"
(out / "release-notes.md").write_text(text)
