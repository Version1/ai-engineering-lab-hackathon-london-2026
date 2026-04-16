"""DSAP-shaped audit recording for Challenge 2 wiki evaluations."""

from __future__ import annotations

import hashlib
import json
import time
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

from .questions import EvaluationQuestion, dump_questions_jsonl


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass
class ClientRunResult:
    """One client answer attempt."""

    run_id: str
    client: str
    question_id: str
    model: str | None
    command: list[str]
    status: str
    answer_text: str
    elapsed_seconds: float
    started_at: str
    finished_at: str
    exit_code: int | None = None
    timed_out: bool = False
    prompt_path: str | None = None
    stdout_path: str | None = None
    stderr_path: str | None = None
    error: str | None = None
    cited_sources: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ChallengeAuditRecorder:
    """Write audit artifacts for a Challenge 2 evaluation run."""

    def __init__(
        self,
        run_dir: Path,
        *,
        run_id: str,
        repo_root: Path,
        challenge_root: Path,
        source_policy: str = "wiki_only",
        retention_class: str = "evaluation_foi_audit",
        disclosure_profile: str = "internal_full",
        legal_hold: bool = False,
    ) -> None:
        self.run_dir = run_dir
        self.run_id = run_id
        self.repo_root = repo_root
        self.challenge_root = challenge_root
        self.source_policy = source_policy
        self.retention_class = retention_class
        self.disclosure_profile = disclosure_profile
        self.legal_hold = legal_hold
        self.started_at = utc_now()
        self.run_dir.mkdir(parents=True, exist_ok=True)
        for name in ("audit", "prompts", "raw", "generated", "bundle"):
            (self.run_dir / name).mkdir(parents=True, exist_ok=True)

    @property
    def event_ledger_path(self) -> Path:
        return self.run_dir / "event-ledger.jsonl"

    @property
    def source_register_path(self) -> Path:
        return self.run_dir / "source-register.json"

    def start_run(
        self,
        *,
        questions: Iterable[EvaluationQuestion],
        clients: Iterable[str],
        dry_run: bool,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        question_list = list(questions)
        run_record = {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "repo_root": str(self.repo_root),
            "challenge_root": str(self.challenge_root),
            "benchmark_path": str(self.challenge_root / "wiki" / "evaluation-benchmark.md"),
            "clients": list(clients),
            "dry_run": dry_run,
            "question_count": len(question_list),
            "source_policy": self.source_policy,
            "retention_class": self.retention_class,
            "disclosure_profile": self.disclosure_profile,
            "legal_hold": self.legal_hold,
            "metadata": metadata or {},
        }
        self._write_json(self.run_dir / "run.json", run_record)
        dump_questions_jsonl(question_list, self.run_dir / "questions.jsonl")
        self._append_event(
            "conversation.started",
            {
                "run_id": self.run_id,
                "question_count": len(question_list),
                "clients": list(clients),
                "dry_run": dry_run,
            },
        )
        self._write_source_register([])

    def write_prompt(self, client: str, question: EvaluationQuestion, prompt: str) -> Path:
        path = self.run_dir / "prompts" / client / f"{question.question_id}.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prompt, encoding="utf-8")
        self._append_event(
            "message.user_visible",
            {
                "client": client,
                "question_id": question.question_id,
                "prompt_path": self._rel(path),
                "prompt_sha256": sha256_file(path),
            },
        )
        return path

    def record_source_access(
        self,
        *,
        path: Path,
        purpose: str,
        client: str | None = None,
        question_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        item = {
            "event_type": "source.file.read",
            "timestamp": utc_now(),
            "run_id": self.run_id,
            "client": client,
            "question_id": question_id,
            "source_path": str(path),
            "relative_path": self._rel(path),
            "sha256": sha256_file(path) if path.exists() and path.is_file() else None,
            "byte_size": path.stat().st_size if path.exists() and path.is_file() else None,
            "held_status": "held",
            "purpose": purpose,
            "source_policy": self.source_policy,
            "metadata": metadata or {},
        }
        self._append_event("source.file.read", item)
        register = self._read_json(self.source_register_path, default=[])
        register.append(item)
        self._write_source_register(register)

    def record_answer(self, question: EvaluationQuestion, result: ClientRunResult) -> Path:
        record = {
            **asdict(result),
            "category": question.category,
            "question": question.question,
            "gold_answer": question.gold_answer,
            "specific_rubric": question.specific_rubric,
            "gold_source_refs": list(question.source_refs),
            "source_policy": self.source_policy,
            "retention_class": self.retention_class,
            "disclosure_profile": self.disclosure_profile,
            "held_status": "held",
            "redactions_applied": [],
        }
        self._append_jsonl(self.run_dir / "answers.jsonl", record)
        self._append_event(
            "message.assistant_visible",
            {
                "client": result.client,
                "question_id": result.question_id,
                "status": result.status,
                "exit_code": result.exit_code,
                "elapsed_seconds": result.elapsed_seconds,
                "stdout_path": result.stdout_path,
                "stderr_path": result.stderr_path,
            },
        )
        self._append_event(
            "decision.conclusion_recorded",
            {
                "client": result.client,
                "question_id": result.question_id,
                "answer_present": bool(result.answer_text.strip()),
                "cited_sources": result.cited_sources,
            },
        )
        audit_path = self.run_dir / "audit" / f"{result.client}-{question.question_id}.txt"
        audit_path.write_text(self.format_answer_audit(question, result), encoding="utf-8")
        return audit_path

    def finalize(self) -> dict[str, Any]:
        finished_at = utc_now()
        self._append_event("conversation.closed", {"run_id": self.run_id, "finished_at": finished_at})
        self._append_event("audit_pack.created", {"run_id": self.run_id, "created_at": finished_at})
        self._append_event("audit_pack.sealed", {"run_id": self.run_id, "sealed_at": finished_at})
        self._write_transcript()
        evidence_register = self._build_evidence_register()
        self._write_json(self.run_dir / "evidence-register.json", evidence_register)
        self._write_decision_record(finished_at)
        from .scoring import write_scoring_sheet

        scoring_sheet = write_scoring_sheet(self.run_dir)
        card = self._build_audit_card(finished_at, evidence_register)
        card["integrity_manifest"] = self._rel(self.run_dir / "integrity-manifest.json")
        card["bundle_path"] = self._rel(self.run_dir / "bundle" / f"DSAP-{self.run_id}.zip")
        card["scoring_sheet"] = self._rel(scoring_sheet)
        self._write_json(self.run_dir / "audit-card.json", card)
        (self.run_dir / "audit-card.md").write_text(self._format_audit_card_md(card), encoding="utf-8")
        self._write_redaction_manifest()
        self._write_report(card)
        integrity = self._write_integrity_manifest()
        bundle_path = self._write_bundle()
        (self.run_dir / "bundle" / f"DSAP-{self.run_id}.zip.sha256").write_text(
            f"{sha256_file(bundle_path)}  {bundle_path.name}\n",
            encoding="utf-8",
        )
        return {"audit_card": card, "integrity_manifest": integrity, "bundle_path": str(bundle_path)}

    def format_answer_audit(self, question: EvaluationQuestion, result: ClientRunResult) -> str:
        sections = [
            "=" * 72,
            f"CHALLENGE 2 WIKI EVALUATION AUDIT: {self.run_id}/{result.client}/{question.question_id}",
            f"Timestamp: {result.finished_at}",
            "=" * 72,
            "",
            "## 1. QUERY",
            "-" * 72,
            f"Question ID: {question.question_id}",
            f"Category: {question.category}",
            f'Question: "{question.question}"',
            "",
            "## 2. SOURCE POLICY",
            "-" * 72,
            "Allowed sources: challenge-2/wiki/, challenge-2/wiki/data/, challenge-2/AGENTS.md",
            "Outside knowledge and web search are not authoritative for scoring.",
            f"Gold source refs: {', '.join(question.source_refs) if question.source_refs else 'not extracted'}",
            "",
            "## 3. CLIENT EXECUTION",
            "-" * 72,
            f"Client: {result.client}",
            f"Model: {result.model or ''}",
            f"Command: {result.command}",
            f"Status: {result.status}",
            f"Exit code: {result.exit_code}",
            f"Elapsed seconds: {result.elapsed_seconds:.3f}",
            f"Prompt path: {result.prompt_path or ''}",
            f"Stdout path: {result.stdout_path or ''}",
            f"Stderr path: {result.stderr_path or ''}",
            f"Timed out: {result.timed_out}",
            f"Error: {result.error or ''}",
            "",
            "## 4. RESPONSE",
            "-" * 72,
            result.answer_text,
            "",
            "## 5. GOLD ANSWER AND RUBRIC",
            "-" * 72,
            f"Gold answer: {question.gold_answer}",
            f"Specific rubric: {question.specific_rubric}",
            "",
            "## 6. FOI AND DISCLOSURE",
            "-" * 72,
            f"Held status: held",
            f"Retention class: {self.retention_class}",
            f"Disclosure profile: {self.disclosure_profile}",
            f"Legal hold: {self.legal_hold}",
            "Redactions applied: []",
        ]
        return "\n".join(sections) + "\n"

    def _append_event(self, event_type: str, payload: dict[str, Any]) -> None:
        event = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": utc_now(),
            "run_id": self.run_id,
            "payload": payload,
        }
        self._append_jsonl(self.event_ledger_path, event)

    def _build_audit_card(self, finished_at: str, evidence_register: list[dict[str, Any]]) -> dict[str, Any]:
        answer_count = self._jsonl_count(self.run_dir / "answers.jsonl")
        return {
            "pack_id": f"DSAP-{self.run_id}",
            "run_id": self.run_id,
            "scope": "challenge_2_wiki_evaluation",
            "created_at": finished_at,
            "started_at": self.started_at,
            "completeness_grade": "A",
            "completeness_reasons": [
                "Benchmark questions, prompts, captured client outputs, event ledger, evidence register, and integrity hashes are retained.",
                "Model private reasoning is not captured and is not part of the audit record.",
            ],
            "question_count": self._jsonl_count(self.run_dir / "questions.jsonl"),
            "answer_count": answer_count,
            "evidence_item_count": len(evidence_register),
            "source_policy": self.source_policy,
            "retention_class": self.retention_class,
            "disclosure_profile": self.disclosure_profile,
            "legal_hold": self.legal_hold,
            "integrity_status": "sealed",
            "redaction_profile": "none",
        }

    def _build_evidence_register(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for path in sorted(self.run_dir.rglob("*")):
            if not path.is_file():
                continue
            if path.name in {"evidence-register.json", "integrity-manifest.json"}:
                continue
            if "bundle" in path.relative_to(self.run_dir).parts:
                continue
            items.append(
                {
                    "evidence_id": f"E{len(items) + 1:04d}",
                    "path": self._rel(path),
                    "byte_size": path.stat().st_size,
                    "sha256": sha256_file(path),
                    "held_status": "held",
                    "evidence_class": self._evidence_class(path),
                    "captured_at": utc_now(),
                }
            )
        return items

    def _write_decision_record(self, finished_at: str) -> None:
        decision_record = {
            "run_id": self.run_id,
            "created_at": finished_at,
            "decision_type": "comparative_ai_wiki_evaluation",
            "assumptions": [
                "The benchmark Markdown is the scoring source of truth.",
                "Evaluated clients were instructed to use only the Challenge 2 wiki and Challenge 2 operating rules.",
            ],
            "uncertainties": [
                "The harness cannot prove a CLI client avoided outside knowledge unless the client is run through the MCP wiki read/search tools or an external trace proxy.",
                "Semantic scoring remains a scorer or downstream evaluator responsibility.",
            ],
            "conclusions": [
                "The run artifacts are sufficient to compare captured answers against the gold answers and rubrics.",
            ],
            "completeness_statement": "The pack records prompts, visible outputs, run metadata, and file/source access observed through this harness.",
        }
        self._write_json(self.run_dir / "decision-record.json", decision_record)
        self._write_json(
            self.run_dir / "conversation-record.json",
            {
                "run_id": self.run_id,
                "started_at": self.started_at,
                "finished_at": finished_at,
                "event_ledger": self._rel(self.event_ledger_path),
                "visible_transcript": self._rel(self.run_dir / "transcript-visible.md"),
            },
        )

    def _write_integrity_manifest(self) -> dict[str, Any]:
        entries: list[dict[str, Any]] = []
        for path in sorted(self.run_dir.rglob("*")):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(self.run_dir).parts
            if path.name == "integrity-manifest.json" or "bundle" in rel_parts:
                continue
            entries.append(
                {
                    "path": self._rel(path),
                    "byte_size": path.stat().st_size,
                    "sha256": sha256_file(path),
                    "verification_status": "verified_at_seal",
                }
            )
        manifest = {
            "run_id": self.run_id,
            "created_at": utc_now(),
            "algorithm": "sha256",
            "manifest_excludes_self": True,
            "entries": entries,
        }
        self._write_json(self.run_dir / "integrity-manifest.json", manifest)
        return manifest

    def _write_redaction_manifest(self) -> None:
        self._write_json(
            self.run_dir / "redaction-manifest.json",
            {
                "run_id": self.run_id,
                "created_at": utc_now(),
                "profile": "none",
                "redactions": [],
                "notes": "No derivative FOI redaction has been applied to this sealed internal pack.",
            },
        )

    def _write_report(self, card: dict[str, Any]) -> None:
        report = [
            f"# Challenge 2 Wiki Evaluation Audit Report",
            "",
            f"- Run ID: `{self.run_id}`",
            f"- Pack ID: `{card['pack_id']}`",
            f"- Completeness: `{card['completeness_grade']}`",
            f"- Question count: `{card['question_count']}`",
            f"- Answer count: `{card['answer_count']}`",
            f"- Source policy: `{self.source_policy}`",
            "",
            "This report is a generated summary. The event ledger and retained evidence files are the source of truth.",
        ]
        (self.run_dir / "generated" / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    def _write_transcript(self) -> None:
        lines = [f"# Challenge 2 Wiki Evaluation Transcript", ""]
        for answer in self._iter_jsonl(self.run_dir / "answers.jsonl"):
            lines.extend(
                [
                    f"## {answer.get('client')} {answer.get('question_id')}",
                    "",
                    f"Question: {answer.get('question')}",
                    "",
                    str(answer.get("answer_text") or "").strip(),
                    "",
                ]
            )
        (self.run_dir / "transcript-visible.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    def _write_bundle(self) -> Path:
        bundle_path = self.run_dir / "bundle" / f"DSAP-{self.run_id}.zip"
        with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(self.run_dir.rglob("*")):
                if not path.is_file() or path == bundle_path:
                    continue
                if "bundle" in path.relative_to(self.run_dir).parts:
                    continue
                archive.write(path, path.relative_to(self.run_dir))
        return bundle_path

    def _format_audit_card_md(self, card: dict[str, Any]) -> str:
        lines = [
            f"# Audit Card: {card['pack_id']}",
            "",
            f"- Scope: `{card['scope']}`",
            f"- Run ID: `{card['run_id']}`",
            f"- Created at: `{card['created_at']}`",
            f"- Completeness grade: `{card['completeness_grade']}`",
            f"- Question count: `{card['question_count']}`",
            f"- Answer count: `{card['answer_count']}`",
            f"- Evidence items: `{card['evidence_item_count']}`",
            f"- Source policy: `{card['source_policy']}`",
            f"- Retention class: `{card['retention_class']}`",
            f"- Disclosure profile: `{card['disclosure_profile']}`",
            f"- Legal hold: `{card['legal_hold']}`",
            f"- Integrity status: `{card['integrity_status']}`",
            "",
            "## Completeness Reasons",
            "",
        ]
        lines.extend(f"- {reason}" for reason in card["completeness_reasons"])
        return "\n".join(lines) + "\n"

    def _write_source_register(self, records: list[dict[str, Any]]) -> None:
        self._write_json(self.source_register_path, records)

    def _evidence_class(self, path: Path) -> str:
        rel = path.relative_to(self.run_dir)
        first = rel.parts[0]
        if first == "prompts":
            return "prompt"
        if first == "raw":
            return "client_output"
        if first == "audit":
            return "per_answer_audit"
        if path.name.endswith(".jsonl"):
            return "ledger"
        if path.name.endswith(".json"):
            return "metadata"
        return "derived_report"

    def _jsonl_count(self, path: Path) -> int:
        if not path.exists():
            return 0
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

    def _iter_jsonl(self, path: Path) -> Iterable[dict[str, Any]]:
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
        return records

    def _append_jsonl(self, path: Path, record: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def _write_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _read_json(self, path: Path, *, default: Any) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def _rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.run_dir))
        except ValueError:
            try:
                return str(path.relative_to(self.repo_root))
            except ValueError:
                return str(path)
