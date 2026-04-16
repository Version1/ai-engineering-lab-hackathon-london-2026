"""Scoring-sheet and leaderboard helpers for Challenge 2 wiki evaluation runs."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


SCORING_COLUMNS = [
    "client",
    "model",
    "question_id",
    "category",
    "question",
    "answer_text",
    "gold_answer",
    "specific_rubric",
    "gold_source_refs",
    "score_0_to_5",
    "scorer_notes",
    "hallucination_count",
    "missed_source_risk",
]


def write_scoring_sheet(run_dir: Path) -> Path:
    """Write a CSV scoring sheet from captured answers."""

    answers_path = run_dir / "answers.jsonl"
    scoring_path = run_dir / "generated" / "scoring-sheet.csv"
    scoring_path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(_iter_jsonl(answers_path))
    with scoring_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCORING_COLUMNS)
        writer.writeheader()
        for answer in rows:
            writer.writerow(
                {
                    "client": answer.get("client", ""),
                    "model": answer.get("model") or "",
                    "question_id": answer.get("question_id", ""),
                    "category": answer.get("category", ""),
                    "question": answer.get("question", ""),
                    "answer_text": answer.get("answer_text", ""),
                    "gold_answer": answer.get("gold_answer", ""),
                    "specific_rubric": answer.get("specific_rubric", ""),
                    "gold_source_refs": "; ".join(answer.get("gold_source_refs") or []),
                    "score_0_to_5": "",
                    "scorer_notes": "",
                    "hallucination_count": "",
                    "missed_source_risk": "",
                }
            )
    return scoring_path


def summarise_scores(score_path: Path, *, expected_question_count: int = 100) -> dict[str, Any]:
    """Summarise a completed scoring CSV into leaderboard data."""

    with score_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("client", "")].append(row)
    leaderboard: list[dict[str, Any]] = []
    categories: dict[str, dict[str, dict[str, float | int]]] = {}
    for client, client_rows in grouped.items():
        scored_rows = [row for row in client_rows if _parse_score(row.get("score_0_to_5")) is not None]
        raw_points = sum(_parse_score(row.get("score_0_to_5")) or 0.0 for row in scored_rows)
        hallucination_count = sum(int(float(row.get("hallucination_count") or 0)) for row in scored_rows)
        missed_source_risk = sum(int(float(row.get("missed_source_risk") or 0)) for row in scored_rows)
        benchmark_max = expected_question_count * 5
        scored_max = len(scored_rows) * 5
        leaderboard.append(
            {
                "client": client,
                "captured_answers": len(client_rows),
                "scored_answers": len(scored_rows),
                "raw_points": round(raw_points, 2),
                "benchmark_max_points": benchmark_max,
                "final_score_percent": round((raw_points / benchmark_max) * 100, 1) if benchmark_max else 0.0,
                "scored_subset_percent": round((raw_points / scored_max) * 100, 1) if scored_max else None,
                "hallucination_count": hallucination_count,
                "missed_source_risk_count": missed_source_risk,
            }
        )
        categories[client] = _category_breakdown(scored_rows)
    leaderboard.sort(
        key=lambda item: (
            item["final_score_percent"],
            -item["hallucination_count"],
            -item["missed_source_risk_count"],
            item["captured_answers"],
        ),
        reverse=True,
    )
    return {"leaderboard": leaderboard, "categories": categories, "score_path": str(score_path)}


def write_leaderboard(summary: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    """Write leaderboard JSON and Markdown outputs."""

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "leaderboard.json"
    md_path = output_dir / "leaderboard.md"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Challenge 2 Wiki Evaluation Leaderboard",
        "",
        "| Rank | Client | Captured | Scored | Raw Points | Final % | Scored Subset % | Hallucinations | Missed Source Risks |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rank, item in enumerate(summary["leaderboard"], start=1):
        subset = "" if item["scored_subset_percent"] is None else item["scored_subset_percent"]
        lines.append(
            "| {rank} | {client} | {captured} | {scored} | {points} | {final} | {subset} | {hallucinations} | {risks} |".format(
                rank=rank,
                client=item["client"],
                captured=item["captured_answers"],
                scored=item["scored_answers"],
                points=item["raw_points"],
                final=item["final_score_percent"],
                subset=subset,
                hallucinations=item["hallucination_count"],
                risks=item["missed_source_risk_count"],
            )
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def _category_breakdown(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("category", "")].append(row)
    result: dict[str, dict[str, float | int]] = {}
    for category, category_rows in grouped.items():
        points = sum(_parse_score(row.get("score_0_to_5")) or 0.0 for row in category_rows)
        max_points = len(category_rows) * 5
        result[category] = {
            "scored_answers": len(category_rows),
            "raw_points": round(points, 2),
            "max_points": max_points,
            "percent": round((points / max_points) * 100, 1) if max_points else 0.0,
        }
    return result


def _parse_score(raw: str | None) -> float | None:
    if raw is None or str(raw).strip() == "":
        return None
    value = float(raw)
    if value < 0 or value > 5:
        raise ValueError(f"score_0_to_5 must be between 0 and 5, got {raw!r}")
    return value


def _iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows
