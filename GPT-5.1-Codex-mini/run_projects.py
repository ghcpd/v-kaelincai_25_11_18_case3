"""Entry point to execute both UI/UX improvement projects."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from project_alpha.run_alpha import run as run_alpha
from project_beta.run_beta import run as run_beta
from ux_optimizer import aggregate_metrics


def write_summary(output_root: Path, data: dict[str, Iterable[dict]]) -> None:
    summary = {}
    for project, entries in data.items():
        metrics = aggregate_metrics(entries)
        summary[project] = {
            "metrics": metrics,
            "processed_ids": [entry["id"] for entry in entries],
        }
    summary_path = output_root / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run both UI/UX improvement experiments.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd() / "artifacts",
        help="Root folder for generated folders and metadata.",
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    projects = {
        "project_alpha": run_alpha(args.output),
        "project_beta": run_beta(args.output),
    }
    write_summary(args.output, projects)


if __name__ == "__main__":
    main()
