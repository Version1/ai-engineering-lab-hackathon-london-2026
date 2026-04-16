#!/usr/bin/env python3
"""Summarise a scored Challenge 2 wiki evaluation run into a leaderboard."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.scoring import summarise_scores, write_leaderboard  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path, help="Evaluation run directory.")
    parser.add_argument(
        "--score-path",
        type=Path,
        help="CSV scoring sheet. Defaults to RUN_DIR/generated/scoring-sheet.csv.",
    )
    parser.add_argument("--expected-question-count", type=int, default=100)
    args = parser.parse_args(argv)

    score_path = args.score_path or args.run_dir / "generated" / "scoring-sheet.csv"
    summary = summarise_scores(score_path, expected_question_count=args.expected_question_count)
    json_path, md_path = write_leaderboard(summary, args.run_dir / "generated")
    print(json.dumps({"leaderboard_json": str(json_path), "leaderboard_md": str(md_path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
