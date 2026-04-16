from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_ROOT = REPO_ROOT / "challenge-2"
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.questions import load_questions, select_questions  # noqa: E402


class Challenge2QuestionParsingTest(unittest.TestCase):
    def test_loads_all_100_questions(self) -> None:
        questions = load_questions()

        self.assertEqual(len(questions), 100)
        self.assertEqual(questions[0].question_id, "Q001")
        self.assertEqual(questions[-1].question_id, "Q100")
        self.assertIn("source of truth", questions[0].question)
        self.assertIn("challenge-2/AGENTS.md", questions[0].source_refs)

    def test_select_questions_rejects_unknown_ids(self) -> None:
        questions = load_questions()

        with self.assertRaisesRegex(ValueError, "Unknown question id"):
            select_questions(questions, question_ids=["Q999"])

    def test_public_dict_excludes_gold_answer(self) -> None:
        question = load_questions()[0]

        public = question.to_public_dict()

        self.assertIn("question", public)
        self.assertNotIn("gold_answer", public)
        self.assertNotIn("source_refs", public)


if __name__ == "__main__":
    unittest.main()
