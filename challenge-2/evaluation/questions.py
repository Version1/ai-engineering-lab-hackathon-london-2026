"""Question parsing for the Challenge 2 wiki evaluation benchmark."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_PATH = CHALLENGE_ROOT / "wiki" / "evaluation-benchmark.md"
QUESTION_HEADING_RE = re.compile(r"^### (Q\d{3})\s*$", re.MULTILINE)
FIELD_NAMES = ("Category", "Question", "Gold answer", "Specific rubric")
SOURCE_ID_RE = re.compile(r"\b(?:DOC-[A-Z0-9-]+|UF-[A-Z0-9-]+)\b")
WIKI_PATH_RE = re.compile(r"challenge-2/(?:AGENTS\.md|wiki/[A-Za-z0-9_./*\-]+)")


@dataclass(frozen=True)
class EvaluationQuestion:
    """One source-backed benchmark question."""

    question_id: str
    category: str
    question: str
    gold_answer: str
    specific_rubric: str
    source_refs: tuple[str, ...]

    def to_public_dict(self) -> dict[str, object]:
        """Return the fields safe to expose to evaluated clients."""

        return {
            "question_id": self.question_id,
            "category": self.category,
            "question": self.question,
            "specific_rubric": self.specific_rubric,
        }

    def to_scoring_dict(self) -> dict[str, object]:
        """Return all benchmark fields, including the gold answer."""

        return asdict(self)


def load_questions(path: Path | str = BENCHMARK_PATH) -> list[EvaluationQuestion]:
    """Load all benchmark questions from the Markdown benchmark note."""

    benchmark_path = Path(path)
    text = benchmark_path.read_text(encoding="utf-8")
    questions = parse_questions(text)
    if not questions:
        raise ValueError(f"No benchmark questions found in {benchmark_path}")
    return questions


def parse_questions(markdown: str) -> list[EvaluationQuestion]:
    """Parse benchmark questions from Markdown text."""

    matches = list(QUESTION_HEADING_RE.finditer(markdown))
    parsed: list[EvaluationQuestion] = []
    for index, match in enumerate(matches):
        question_id = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        block = markdown[start:end]
        fields = _parse_fields(block)
        missing = [field for field in FIELD_NAMES if not fields.get(field)]
        if missing:
            raise ValueError(f"{question_id} is missing field(s): {', '.join(missing)}")
        gold_answer = fields["Gold answer"]
        rubric = fields["Specific rubric"]
        parsed.append(
            EvaluationQuestion(
                question_id=question_id,
                category=fields["Category"],
                question=fields["Question"],
                gold_answer=gold_answer,
                specific_rubric=rubric,
                source_refs=tuple(_extract_source_refs(f"{gold_answer}\n{rubric}")),
            )
        )
    return parsed


def select_questions(
    questions: Iterable[EvaluationQuestion],
    *,
    question_ids: Iterable[str] | None = None,
    category: str | None = None,
    limit: int | None = None,
) -> list[EvaluationQuestion]:
    """Filter questions by id, category substring, and optional limit."""

    selected = list(questions)
    if question_ids:
        wanted = {qid.upper() for qid in question_ids}
        selected = [question for question in selected if question.question_id in wanted]
        found = {question.question_id for question in selected}
        missing = sorted(wanted - found)
        if missing:
            raise ValueError(f"Unknown question id(s): {', '.join(missing)}")
    if category:
        needle = category.casefold()
        selected = [question for question in selected if needle in question.category.casefold()]
    if limit is not None:
        selected = selected[: max(limit, 0)]
    return selected


def dump_questions_jsonl(questions: Iterable[EvaluationQuestion], path: Path) -> None:
    """Write benchmark questions to JSONL for a run artifact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for question in questions:
            handle.write(json.dumps(question.to_scoring_dict(), sort_keys=True) + "\n")


def _parse_fields(block: str) -> dict[str, str]:
    fields: dict[str, list[str]] = {field: [] for field in FIELD_NAMES}
    current: str | None = None
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        matched_field = None
        for field in FIELD_NAMES:
            prefix = f"{field}:"
            if line.startswith(prefix):
                matched_field = field
                fields[field].append(line[len(prefix) :].strip())
                current = field
                break
        if matched_field:
            continue
        if current is not None:
            fields[current].append(line)
    return {field: _normalise_text(lines) for field, lines in fields.items()}


def _normalise_text(lines: list[str]) -> str:
    text = "\n".join(lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _extract_source_refs(text: str) -> list[str]:
    refs: list[str] = []
    for match in SOURCE_ID_RE.finditer(text):
        refs.append(match.group(0))
    for match in WIKI_PATH_RE.finditer(text):
        refs.append(match.group(0).rstrip(".,;:"))
    for backticked in re.findall(r"`([^`]+)`", text):
        if backticked.startswith("challenge-2/"):
            refs.append(backticked.rstrip(".,;:"))
    return _dedupe(refs)


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result
