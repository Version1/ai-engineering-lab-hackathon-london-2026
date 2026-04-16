from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MCP_SCRIPT = REPO_ROOT / "challenge-2" / "tools" / "wiki_eval_mcp.py"


class Challenge2McpTest(unittest.TestCase):
    def test_stdio_server_lists_and_reads_question_without_gold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            requests = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "wiki_eval.get_question",
                        "arguments": {"question_id": "Q001"},
                    },
                },
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "wiki_eval.read_wiki_file",
                        "arguments": {"path": "challenge-2/wiki/evaluation-benchmark.md"},
                    },
                },
            ]
            proc = subprocess.run(
                [sys.executable, str(MCP_SCRIPT), "--run-root", tmp, "--run-id", "mcp-test"],
                input="\n".join(json.dumps(request) for request in requests) + "\n",
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
                check=False,
                timeout=10,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr)
            responses = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
            self.assertEqual(len(responses), 3)
            payload = json.loads(responses[1]["result"]["content"][0]["text"])
            self.assertEqual(payload["question_id"], "Q001")
            self.assertIn("prompt", payload)
            self.assertNotIn("gold_answer", payload)
            self.assertNotIn("source_refs", payload)
            self.assertIn("error", responses[2])
            self.assertIn("gold answers", responses[2]["error"]["message"])


if __name__ == "__main__":
    unittest.main()
