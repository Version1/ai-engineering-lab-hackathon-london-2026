#!/usr/bin/env python3
"""Minimal stdio MCP server for Challenge 2 wiki evaluation audit runs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CHALLENGE_ROOT.parent
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.audit import ChallengeAuditRecorder, ClientRunResult, utc_now  # noqa: E402
from evaluation.clients import build_wiki_prompt  # noqa: E402
from evaluation.questions import BENCHMARK_PATH, EvaluationQuestion, load_questions, select_questions  # noqa: E402


class WikiEvalMcpServer:
    def __init__(self, *, run_root: Path, run_id: str | None = None) -> None:
        self.run_id = run_id or f"wiki-eval-mcp-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        self.run_dir = run_root / self.run_id
        self.questions = load_questions(BENCHMARK_PATH)
        self.recorder = ChallengeAuditRecorder(
            self.run_dir,
            run_id=self.run_id,
            repo_root=REPO_ROOT,
            challenge_root=CHALLENGE_ROOT,
        )
        self.recorder.start_run(
            questions=self.questions,
            clients=["mcp"],
            dry_run=False,
            metadata={"server": "challenge2-wiki-eval-mcp"},
        )

    def handle(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method = request.get("method")
        request_id = request.get("id")
        try:
            if method in {"notifications/initialized", "notifications/cancelled"}:
                return None
            if method == "initialize":
                return self._response(request_id, self._initialize())
            if method == "tools/list":
                return self._response(request_id, {"tools": self._tools()})
            if method == "tools/call":
                params = request.get("params") or {}
                return self._response(request_id, self._tool_call(params.get("name"), params.get("arguments") or {}))
            if method == "resources/list":
                return self._response(request_id, {"resources": self._resources()})
            if method == "resources/read":
                params = request.get("params") or {}
                return self._response(request_id, self._resource_read(str(params.get("uri") or "")))
            if method == "ping":
                return self._response(request_id, {})
            return self._error(request_id, -32601, f"Unsupported method: {method}")
        except Exception as exc:  # noqa: BLE001 - returned to the MCP client as JSON-RPC error.
            return self._error(request_id, -32000, str(exc))

    def _initialize(self) -> dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}, "resources": {}},
            "serverInfo": {"name": "challenge2-wiki-eval", "version": "0.1.0"},
        }

    def _tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "wiki_eval.list_questions",
                "description": "List Challenge 2 evaluation questions without exposing gold answers.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1},
                    },
                },
            },
            {
                "name": "wiki_eval.get_question",
                "description": "Get one benchmark question and the standard wiki-only prompt.",
                "inputSchema": {
                    "type": "object",
                    "required": ["question_id"],
                    "properties": {"question_id": {"type": "string"}},
                },
            },
            {
                "name": "wiki_eval.search_wiki",
                "description": "Search allowed Challenge 2 wiki files and record the source access event.",
                "inputSchema": {
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                        "client": {"type": "string"},
                        "question_id": {"type": "string"},
                    },
                },
            },
            {
                "name": "wiki_eval.read_wiki_file",
                "description": "Read an allowed wiki file or challenge-2/AGENTS.md and record the source access event.",
                "inputSchema": {
                    "type": "object",
                    "required": ["path"],
                    "properties": {
                        "path": {"type": "string"},
                        "offset": {"type": "integer", "minimum": 0},
                        "max_bytes": {"type": "integer", "minimum": 1},
                        "client": {"type": "string"},
                        "question_id": {"type": "string"},
                    },
                },
            },
            {
                "name": "wiki_eval.record_answer",
                "description": "Record a visible answer for audit and later scoring. Does not return the gold answer.",
                "inputSchema": {
                    "type": "object",
                    "required": ["question_id", "client", "answer_text"],
                    "properties": {
                        "question_id": {"type": "string"},
                        "client": {"type": "string"},
                        "model": {"type": "string"},
                        "answer_text": {"type": "string"},
                        "cited_sources": {"type": "array", "items": {"type": "string"}},
                        "elapsed_seconds": {"type": "number"},
                    },
                },
            },
            {
                "name": "wiki_eval.finalize_run",
                "description": "Seal the current evaluation audit pack and return its main artifact paths.",
                "inputSchema": {"type": "object", "properties": {}},
            },
        ]

    def _resources(self) -> list[dict[str, str]]:
        return [
            {
                "uri": "wiki-eval://questions",
                "name": "Public Challenge 2 questions",
                "mimeType": "application/json",
            },
            {
                "uri": f"wiki-eval://runs/{self.run_id}/audit-card",
                "name": "Current run audit card",
                "mimeType": "application/json",
            },
        ]

    def _tool_call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "wiki_eval.list_questions":
            result = self._list_questions(arguments)
        elif name == "wiki_eval.get_question":
            result = self._get_question(arguments)
        elif name == "wiki_eval.search_wiki":
            result = self._search_wiki(arguments)
        elif name == "wiki_eval.read_wiki_file":
            result = self._read_wiki_file(arguments)
        elif name == "wiki_eval.record_answer":
            result = self._record_answer(arguments)
        elif name == "wiki_eval.finalize_run":
            result = self.recorder.finalize()
        else:
            raise ValueError(f"Unknown tool: {name}")
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2, sort_keys=True)}]}

    def _list_questions(self, arguments: dict[str, Any]) -> dict[str, Any]:
        selected = select_questions(
            self.questions,
            category=arguments.get("category"),
            limit=int(arguments["limit"]) if arguments.get("limit") else None,
        )
        return {"questions": [question.to_public_dict() for question in selected], "count": len(selected)}

    def _get_question(self, arguments: dict[str, Any]) -> dict[str, Any]:
        question = self._find_question(str(arguments["question_id"]))
        return {
            **question.to_public_dict(),
            "prompt": build_wiki_prompt(question, repo_root=REPO_ROOT, challenge_root=CHALLENGE_ROOT),
        }

    def _search_wiki(self, arguments: dict[str, Any]) -> dict[str, Any]:
        query = str(arguments["query"])
        limit = min(int(arguments.get("limit") or 10), 50)
        matches: list[dict[str, Any]] = []
        for path in self._allowed_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for line_no, line in enumerate(text.splitlines(), start=1):
                if query.casefold() in line.casefold():
                    matches.append({"path": self._repo_rel(path), "line": line_no, "text": line[:500]})
                    break
            if len(matches) >= limit:
                break
        self.recorder.record_source_access(
            path=CHALLENGE_ROOT / "wiki",
            purpose=f"search:{query}",
            client=arguments.get("client"),
            question_id=arguments.get("question_id"),
            metadata={"match_count": len(matches)},
        )
        return {"query": query, "matches": matches, "count": len(matches)}

    def _read_wiki_file(self, arguments: dict[str, Any]) -> dict[str, Any]:
        path = self._resolve_allowed_path(str(arguments["path"]))
        offset = int(arguments.get("offset") or 0)
        max_bytes = int(arguments.get("max_bytes") or 30000)
        data = path.read_bytes()
        chunk = data[offset : offset + max_bytes]
        self.recorder.record_source_access(
            path=path,
            purpose="read_wiki_file",
            client=arguments.get("client"),
            question_id=arguments.get("question_id"),
            metadata={"offset": offset, "max_bytes": max_bytes},
        )
        return {
            "path": self._repo_rel(path),
            "offset": offset,
            "next_offset": offset + len(chunk) if offset + len(chunk) < len(data) else None,
            "byte_size": len(data),
            "text": chunk.decode("utf-8", errors="replace"),
        }

    def _record_answer(self, arguments: dict[str, Any]) -> dict[str, Any]:
        question = self._find_question(str(arguments["question_id"]))
        now = utc_now()
        result = ClientRunResult(
            run_id=self.run_id,
            client=str(arguments["client"]),
            question_id=question.question_id,
            model=arguments.get("model"),
            command=["mcp", "wiki_eval.record_answer"],
            status="recorded",
            answer_text=str(arguments["answer_text"]),
            elapsed_seconds=float(arguments.get("elapsed_seconds") or 0.0),
            started_at=now,
            finished_at=now,
            cited_sources=list(arguments.get("cited_sources") or []),
        )
        audit_path = self.recorder.record_answer(question, result)
        return {"run_id": self.run_id, "question_id": question.question_id, "audit_path": str(audit_path)}

    def _resource_read(self, uri: str) -> dict[str, Any]:
        if uri == "wiki-eval://questions":
            text = json.dumps([question.to_public_dict() for question in self.questions], indent=2)
            return {"contents": [{"uri": uri, "mimeType": "application/json", "text": text}]}
        if uri == f"wiki-eval://runs/{self.run_id}/audit-card":
            path = self.run_dir / "audit-card.json"
            text = path.read_text(encoding="utf-8") if path.exists() else "{}"
            return {"contents": [{"uri": uri, "mimeType": "application/json", "text": text}]}
        raise ValueError(f"Unknown resource URI: {uri}")

    def _find_question(self, question_id: str) -> EvaluationQuestion:
        wanted = question_id.upper()
        for question in self.questions:
            if question.question_id == wanted:
                return question
        raise ValueError(f"Unknown question id: {question_id}")

    def _allowed_files(self) -> list[Path]:
        files = [CHALLENGE_ROOT / "AGENTS.md"]
        files.extend(
            path
            for path in sorted((CHALLENGE_ROOT / "wiki").rglob("*"))
            if path.is_file() and path.resolve() != BENCHMARK_PATH.resolve()
        )
        return files

    def _resolve_allowed_path(self, raw_path: str) -> Path:
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = REPO_ROOT / raw_path
        resolved = candidate.resolve()
        allowed_wiki = (CHALLENGE_ROOT / "wiki").resolve()
        allowed_agents = (CHALLENGE_ROOT / "AGENTS.md").resolve()
        if resolved == allowed_agents:
            return resolved
        if resolved == BENCHMARK_PATH.resolve():
            raise ValueError("Benchmark file is not exposed to evaluated clients because it contains gold answers.")
        if allowed_wiki in resolved.parents or resolved == allowed_wiki:
            if not resolved.is_file():
                raise ValueError(f"Allowed path is not a file: {raw_path}")
            return resolved
        raise ValueError(f"Path is outside allowed Challenge 2 wiki scope: {raw_path}")

    def _repo_rel(self, path: Path) -> str:
        return str(path.resolve().relative_to(REPO_ROOT))

    def _response(self, request_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    def _error(self, request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, default=CHALLENGE_ROOT / "evaluation" / "runs")
    parser.add_argument("--run-id")
    args = parser.parse_args(argv)
    server = WikiEvalMcpServer(run_root=args.run_root, run_id=args.run_id)
    for raw_line in sys.stdin:
        if not raw_line.strip():
            continue
        try:
            request = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
        else:
            response = server.handle(request)
        if response is not None:
            print(json.dumps(response, separators=(",", ":")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
