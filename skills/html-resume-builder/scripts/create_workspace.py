#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy a bundled resume template into a working directory.")
    parser.add_argument("--template", default="basic-a4", help="Template name under assets/templates/.")
    parser.add_argument("--output", required=True, help="Destination directory for the editable resume workspace.")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "templates"
    source = (template_root / args.template).resolve()
    if source.parent != template_root.resolve():
        raise SystemExit("Template must be a name directly under assets/templates.")
    destination = Path(args.output).expanduser().resolve()

    if not source.exists():
        raise SystemExit(f"Template not found: {source}")

    resume_html = source / "resume.html"
    manifest_path = source / "template-manifest.json"
    if not resume_html.exists() or not manifest_path.exists():
        raise SystemExit(f"Template is incomplete: {source}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("template_id") != args.template:
        raise SystemExit(f"Template manifest id does not match directory: {manifest_path}")
    if manifest.get("status") not in {"baseline", "admitted"}:
        raise SystemExit(f"Template is not admitted: {args.template}")

    if destination.exists():
        raise SystemExit(f"Output already exists: {destination}. Choose a new directory; existing content is preserved.")

    shutil.copytree(source, destination)
    resume_html = destination / "resume.html"

    print(f"Created resume workspace: {destination}")
    print(f"Template: {args.template}")
    print(f"Editable HTML: {resume_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
