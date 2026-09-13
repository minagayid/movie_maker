"""Command-line interface for local story-to-production-package generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import ProjectSpec, SourceMaterial
from .pipeline import MovieMaker
from .reporting import production_plan_markdown
from .rights import RightsError
from .validation import validate_package_dict


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="movie-maker", description="Generate a rights-aware movie production package")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate a production package from a text source")
    generate.add_argument("--input", required=True, type=Path, help="UTF-8 text file containing the source story")
    generate.add_argument("--output", required=True, type=Path, help="directory for generated artifacts")
    generate.add_argument("--title", required=True)
    generate.add_argument("--author", required=True)
    generate.add_argument("--rights-status", required=True, choices=("public_domain", "licensed", "user_owned", "unknown", "blocked"))
    generate.add_argument("--rights-notes", default="")
    generate.add_argument("--runtime", type=int, default=90, help="target runtime in minutes")
    generate.add_argument("--rating", default="PG-13")
    generate.add_argument("--style", default="cinematic naturalism")

    validate = subparsers.add_parser("validate", help="validate a generated project.json")
    validate.add_argument("--project", required=True, type=Path)
    return parser


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def generate(args: argparse.Namespace) -> int:
    source_text = args.input.read_text(encoding="utf-8")
    source = SourceMaterial(args.title, args.author, source_text, args.rights_status, args.rights_notes)
    spec = ProjectSpec(args.title, source, args.runtime, args.rating, args.style)
    try:
        package = MovieMaker().generate(spec)
    except (RightsError, ValueError) as error:
        print(f"ERROR: {error}")
        return 2
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    manifest_dir = output / "manifests"
    manifest_dir.mkdir(exist_ok=True)
    _write_json(output / "project.json", package.to_dict())
    (output / "production_plan.md").write_text(production_plan_markdown(package), encoding="utf-8")
    for name, manifest in package.manifests.items():
        _write_json(manifest_dir / f"{name}.json", manifest)
    print(f"Generated {len(package.scenes)} scenes for {package.project.project_id}")
    print(f"Artifacts: {output.resolve()}")
    return 0


def validate(args: argparse.Namespace) -> int:
    package = json.loads(args.project.read_text(encoding="utf-8"))
    errors = validate_package_dict(package)
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: package structure and cross-manifest references are consistent")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "generate":
        return generate(args)
    return validate(args)


if __name__ == "__main__":
    raise SystemExit(main())
