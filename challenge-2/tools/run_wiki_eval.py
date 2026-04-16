#!/usr/bin/env python3
"""Run Challenge 2 wiki evaluation questions through CLI AI clients."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CHALLENGE_ROOT.parent
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.audit import ChallengeAuditRecorder  # noqa: E402
from evaluation.clients import (  # noqa: E402
    ClientCommandContext,
    build_wiki_prompt,
    load_client_config,
    run_client,
)
from evaluation.questions import BENCHMARK_PATH, load_questions, select_questions  # noqa: E402


SUPPORTED_CLIENTS = ("codex", "gemini", "claude")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, default=BENCHMARK_PATH, help="Benchmark Markdown path.")
    parser.add_argument(
        "--clients",
        default="codex,gemini,claude",
        help="Comma-separated clients to run: codex, gemini, claude.",
    )
    parser.add_argument("--questions", help="Comma-separated question IDs, for example Q001,Q002.")
    parser.add_argument("--category", help="Category substring filter.")
    parser.add_argument("--limit", type=int, help="Limit the number of selected questions.")
    parser.add_argument("--output-root", type=Path, default=CHALLENGE_ROOT / "evaluation" / "runs")
    parser.add_argument("--run-id", help="Explicit run id. Defaults to a UTC timestamp.")
    parser.add_argument("--timeout-sec", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true", help="Write prompts and audit skeleton without invoking clients.")
    parser.add_argument("--client-config", type=Path, help="Optional JSON file overriding client argv templates.")
    parser.add_argument(
        "--model",
        action="append",
        default=[],
        metavar="CLIENT=MODEL",
        help="Override a client model. May be repeated.",
    )
    args = parser.parse_args(argv)

    clients = _parse_clients(args.clients)
    model_overrides = _parse_model_overrides(args.model)
    questions = load_questions(args.benchmark)
    selected = select_questions(
        questions,
        question_ids=_split_csv(args.questions),
        category=args.category,
        limit=args.limit,
    )
    if not selected:
        raise SystemExit("No questions selected.")

    run_id = args.run_id or f"wiki-eval-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    run_dir = args.output_root / run_id
    client_config = load_client_config(args.client_config)
    recorder = ChallengeAuditRecorder(
        run_dir,
        run_id=run_id,
        repo_root=REPO_ROOT,
        challenge_root=CHALLENGE_ROOT,
    )
    recorder.start_run(
        questions=selected,
        clients=clients,
        dry_run=args.dry_run,
        metadata={
            "benchmark": str(args.benchmark),
            "timeout_sec": args.timeout_sec,
            "client_config": str(args.client_config) if args.client_config else None,
        },
    )

    for question in selected:
        for client in clients:
            prompt = build_wiki_prompt(question, repo_root=REPO_ROOT, challenge_root=CHALLENGE_ROOT)
            prompt_path = recorder.write_prompt(client, question, prompt)
            assistant_response_path = run_dir / "raw" / client / f"{question.question_id}.assistant-response.txt"
            context = ClientCommandContext(
                client=client,
                model=model_overrides.get(client),
                prompt=prompt,
                question_id=question.question_id,
                run_dir=run_dir,
                repo_root=REPO_ROOT,
                challenge_root=CHALLENGE_ROOT,
                assistant_response_path=assistant_response_path,
            )
            result = run_client(
                context=context,
                prompt_path=prompt_path,
                config=client_config,
                timeout_sec=args.timeout_sec,
                dry_run=args.dry_run,
            )
            recorder.record_answer(question, result)
            print(
                json.dumps(
                    {
                        "run_id": run_id,
                        "client": client,
                        "question_id": question.question_id,
                        "status": result.status,
                        "exit_code": result.exit_code,
                    },
                    sort_keys=True,
                )
            )

    final = recorder.finalize()
    print(json.dumps({"run_dir": str(run_dir), "audit_card": final["audit_card"]}, sort_keys=True))
    return 0


def _parse_clients(raw: str) -> list[str]:
    clients = _split_csv(raw)
    if not clients:
        raise SystemExit("At least one client is required.")
    unsupported = sorted(set(clients) - set(SUPPORTED_CLIENTS))
    if unsupported:
        raise SystemExit(f"Unsupported client(s): {', '.join(unsupported)}")
    return clients


def _parse_model_overrides(values: list[str]) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Invalid --model value {value!r}; expected CLIENT=MODEL")
        client, model = value.split("=", 1)
        client = client.strip()
        if client not in SUPPORTED_CLIENTS:
            raise SystemExit(f"Unsupported --model client: {client}")
        overrides[client] = model.strip()
    return overrides


def _split_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
