"""Client command helpers for the Challenge 2 wiki evaluation harness."""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .audit import ClientRunResult, utc_now
from .questions import EvaluationQuestion


DEFAULT_MODELS = {
    "codex": os.environ.get("CODEX_MODEL", "gpt-5.4"),
    "gemini": os.environ.get("GEMINI_MODEL", ""),
    "claude": os.environ.get("CLAUDE_MODEL", ""),
}


@dataclass(frozen=True)
class ClientCommandContext:
    client: str
    model: str | None
    prompt: str
    question_id: str
    run_dir: Path
    repo_root: Path
    challenge_root: Path
    assistant_response_path: Path


def build_wiki_prompt(question: EvaluationQuestion, *, repo_root: Path, challenge_root: Path) -> str:
    """Build the per-question prompt sent to each CLI client."""

    return "\n".join(
        [
            "You are answering a Challenge 2 wiki evaluation question.",
            "",
            "Use only these local repository sources as authority:",
            f"- {challenge_root / 'wiki'}",
            f"- {challenge_root / 'wiki' / 'data'}",
            f"- {challenge_root / 'AGENTS.md'}",
            "",
            "Do not use web search or outside knowledge. Do not inspect raw source files unless the question explicitly asks about provenance back to a raw file path.",
            "Do not inspect challenge-2/wiki/evaluation-benchmark.md or challenge-2/evaluation/ while answering; those are benchmark harness artifacts and contain gold-answer or scoring material.",
            "Cite the source IDs or wiki paths you used. Preserve any caveat the wiki flags, including draft, stale, superseded, synthetic, low OCR quality, past review, contradictory, or incomplete material.",
            "",
            "Return concise JSON with this shape:",
            '{"question_id":"Q000","answer":"...","cited_sources":["..."],"caveats":["..."]}',
            "",
            f"Repository root: {repo_root}",
            f"Question ID: {question.question_id}",
            f"Category: {question.category}",
            f"Question: {question.question}",
        ]
    )


def load_client_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_command(context: ClientCommandContext, config: dict[str, Any] | None = None) -> list[str]:
    """Build a client command, using optional JSON config overrides."""

    config = config or {}
    client_config = config.get(context.client, {}) if isinstance(config, dict) else {}
    if "argv" in client_config:
        return [
            _expand_token(str(token), context)
            for token in client_config["argv"]
            if _expand_token(str(token), context) != ""
        ]
    model = context.model
    if model is None:
        model = str(client_config.get("model") or DEFAULT_MODELS.get(context.client, ""))
    if context.client == "codex":
        model = model or DEFAULT_MODELS["codex"]
        return [
            "codex",
            "exec",
            "-m",
            model,
            "--json",
            "-o",
            str(context.assistant_response_path),
            "-C",
            str(context.repo_root),
            context.prompt,
        ]
    if context.client == "gemini":
        command = [
            "gemini",
            "--approval-mode",
            "yolo",
            "--output-format",
            "json",
            "--include-directories",
            str(context.challenge_root),
        ]
        if model:
            command.extend(["--model", model])
        command.extend(["--prompt", context.prompt])
        return command
    if context.client == "claude":
        command = ["claude"]
        if model:
            command.extend(["--model", model])
        command.extend(["-p", "--output-format", "json", context.prompt])
        return command
    raise ValueError(f"Unsupported client: {context.client}")


def run_client(
    *,
    context: ClientCommandContext,
    prompt_path: Path,
    config: dict[str, Any] | None,
    timeout_sec: int,
    dry_run: bool,
) -> ClientRunResult:
    """Run a client command and capture visible output."""

    command = build_command(context, config)
    stdout_path = context.run_dir / "raw" / context.client / f"{context.question_id}.stdout.txt"
    stderr_path = context.run_dir / "raw" / context.client / f"{context.question_id}.stderr.txt"
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    started = time.monotonic()
    if dry_run:
        finished_at = utc_now()
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=context.model,
            command=command,
            status="dry_run",
            answer_text="",
            elapsed_seconds=0.0,
            started_at=started_at,
            finished_at=finished_at,
            prompt_path=str(prompt_path),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
        )
    try:
        proc = subprocess.run(
            command,
            cwd=context.repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=max(timeout_sec, 1),
        )
        elapsed = time.monotonic() - started
        stdout_path.write_text(proc.stdout or "", encoding="utf-8")
        stderr_path.write_text(proc.stderr or "", encoding="utf-8")
        answer_text = _read_answer_text(context.assistant_response_path, proc.stdout)
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=context.model,
            command=command,
            status="completed" if proc.returncode == 0 else "failed",
            answer_text=answer_text,
            elapsed_seconds=elapsed,
            started_at=started_at,
            finished_at=utc_now(),
            exit_code=proc.returncode,
            prompt_path=str(prompt_path),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            error=None if proc.returncode == 0 else f"{context.client} exited with {proc.returncode}",
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started
        stdout_path.write_text(_coerce_output(exc.stdout), encoding="utf-8")
        stderr_path.write_text(_coerce_output(exc.stderr), encoding="utf-8")
        return ClientRunResult(
            run_id=context.run_dir.name,
            client=context.client,
            question_id=context.question_id,
            model=context.model,
            command=command,
            status="timeout",
            answer_text=_coerce_output(exc.stdout),
            elapsed_seconds=elapsed,
            started_at=started_at,
            finished_at=utc_now(),
            exit_code=124,
            timed_out=True,
            prompt_path=str(prompt_path),
            stdout_path=str(stdout_path),
            stderr_path=str(stderr_path),
            error=f"{context.client} timed out after {timeout_sec}s",
        )


def _read_answer_text(assistant_response_path: Path, stdout: str) -> str:
    if assistant_response_path.exists() and assistant_response_path.stat().st_size:
        return assistant_response_path.read_text(encoding="utf-8", errors="replace")
    return stdout or ""


def _coerce_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _expand_token(token: str, context: ClientCommandContext) -> str:
    model = context.model or DEFAULT_MODELS.get(context.client, "")
    values = {
        "client": context.client,
        "model": model,
        "prompt": context.prompt,
        "question_id": context.question_id,
        "run_dir": str(context.run_dir),
        "repo_root": str(context.repo_root),
        "challenge_root": str(context.challenge_root),
        "wiki_root": str(context.challenge_root / "wiki"),
        "assistant_response_path": str(context.assistant_response_path),
    }
    return token.format(**values)
