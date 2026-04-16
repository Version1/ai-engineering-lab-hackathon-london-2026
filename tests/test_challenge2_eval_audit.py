from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_ROOT = REPO_ROOT / "challenge-2"
sys.path.insert(0, str(CHALLENGE_ROOT))

from evaluation.audit import ChallengeAuditRecorder, ClientRunResult, utc_now  # noqa: E402
from evaluation.questions import load_questions  # noqa: E402


class Challenge2AuditTest(unittest.TestCase):
    def test_recorder_writes_dsap_shaped_artifacts(self) -> None:
        question = load_questions()[0]
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            recorder = ChallengeAuditRecorder(
                run_dir,
                run_id="test-run",
                repo_root=REPO_ROOT,
                challenge_root=CHALLENGE_ROOT,
            )
            recorder.start_run(questions=[question], clients=["codex"], dry_run=True)
            prompt_path = recorder.write_prompt("codex", question, "Question prompt")
            now = utc_now()
            result = ClientRunResult(
                run_id="test-run",
                client="codex",
                question_id=question.question_id,
                model="test-model",
                command=["codex", "exec"],
                status="dry_run",
                answer_text="",
                elapsed_seconds=0.0,
                started_at=now,
                finished_at=now,
                prompt_path=str(prompt_path),
            )

            audit_path = recorder.record_answer(question, result)
            final = recorder.finalize()

            self.assertTrue(audit_path.exists())
            self.assertTrue((run_dir / "audit-card.json").exists())
            self.assertTrue((run_dir / "event-ledger.jsonl").exists())
            self.assertTrue((run_dir / "integrity-manifest.json").exists())
            self.assertTrue(Path(final["bundle_path"]).exists())
            card = json.loads((run_dir / "audit-card.json").read_text(encoding="utf-8"))
            self.assertEqual(card["pack_id"], "DSAP-test-run")
            self.assertEqual(card["answer_count"], 1)
            manifest = json.loads((run_dir / "integrity-manifest.json").read_text(encoding="utf-8"))
            manifest_paths = {entry["path"] for entry in manifest["entries"]}
            self.assertIn("answers.jsonl", manifest_paths)
            self.assertIn("audit-card.json", manifest_paths)


if __name__ == "__main__":
    unittest.main()
