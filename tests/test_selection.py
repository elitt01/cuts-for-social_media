import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "score_candidates.py"
SPEC = importlib.util.spec_from_file_location("score_candidates", SCRIPT)
selection = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(selection)


def candidate(candidate_id="a", score=4):
    return {
        "candidate_id": candidate_id,
        "source_url": "https://example.org/live",
        "source_start_seconds": 10,
        "source_end_seconds": 30,
        "context_reviewed": {"start_seconds": 0, "end_seconds": 45, "mode": "audiovisual"},
        "potential": {"criteria": {
            key: {"score": score, "evidence": "Evidência fictícia para teste, no segundo 12.",
                  "timecode_seconds": 12} for key in selection.WEIGHTS
        }},
    }


class SelectionTests(unittest.TestCase):
    def test_known_weighted_score(self):
        item = candidate()
        item["potential"]["criteria"]["gancho"]["score"] = 2
        item["potential"]["criteria"]["adequacao"]["score"] = 0
        result = selection.rank_candidates([item])["candidates"][0]
        self.assertEqual(result["potential"]["score"], 75)
        self.assertEqual(result["potential"]["range_min"], 75)
        self.assertEqual(result["potential"]["range_max"], 75)
        self.assertEqual(result["potential"]["evidence_coverage_pct"], 100)

    def test_missing_values_have_interval_not_renormalized_score(self):
        item = candidate(score=3)
        item["potential"]["criteria"]["gancho"] = None
        p = selection.rank_candidates([item])["candidates"][0]["potential"]
        self.assertIsNone(p["score"])
        self.assertEqual((p["range_min"], p["range_max"]), (60, 80))
        self.assertEqual(p["evidence_coverage_pct"], 80)
        self.assertEqual(p["assessment_status"], "incomplete")

    def test_absent_criteria_remain_unknown(self):
        item = candidate()
        item["potential"]["criteria"] = {}
        result = selection.rank_candidates([item])
        p = result["candidates"][0]["potential"]
        self.assertEqual((p["range_min"], p["range_max"]), (0, 100))
        self.assertIsNone(p["score"])
        self.assertEqual(result["status"], "research_required")

    def test_missing_evidence_fails_even_with_high_score(self):
        for bad_evidence in (None, "", "   ", 3):
            item = candidate()
            item["potential"]["criteria"]["gancho"]["evidence"] = bad_evidence
            with self.subTest(evidence=bad_evidence), self.assertRaisesRegex(ValueError, "evidence"):
                selection.rank_candidates([item])

    def test_invalid_scores_fail(self):
        for score in (-1, 5, 3.5, True, "4", None):
            item = candidate()
            item["potential"]["criteria"]["gancho"]["score"] = score
            with self.subTest(score=score), self.assertRaisesRegex(ValueError, "score"):
                selection.rank_candidates([item])

    def test_unknown_criterion_and_duplicate_id_fail(self):
        item = candidate()
        item["potential"]["criteria"]["ganhco"] = None
        with self.assertRaisesRegex(ValueError, "desconhecidos"):
            selection.rank_candidates([item])
        with self.assertRaisesRegex(ValueError, "duplicado"):
            selection.rank_candidates([candidate(), candidate()])

    def test_bad_timing_and_non_finite_data_fail(self):
        for value in (-1, True, float("nan"), float("inf"), 10 ** 1000):
            item = candidate()
            item["source_start_seconds"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                selection.rank_candidates([item])
        item = candidate()
        item["potential"]["criteria"]["gancho"]["timecode_seconds"] = 31
        with self.assertRaisesRegex(ValueError, "fora do intervalo"):
            selection.rank_candidates([item])

    def test_tie_break_is_candidate_id_not_input_order(self):
        left = selection.rank_candidates([candidate("z"), candidate("a")])
        right = selection.rank_candidates([candidate("a"), candidate("z")])
        self.assertEqual(left, right)
        self.assertEqual(left["selected_candidate_id"], "a")

    def test_incomplete_upper_bound_cannot_beat_confirmed_candidate(self):
        incomplete = candidate("incomplete")
        incomplete["potential"]["criteria"] = {}
        result = selection.rank_candidates([incomplete, candidate("confirmed", score=3)])
        self.assertEqual(result["selected_candidate_id"], "confirmed")
        self.assertEqual(result["candidates"][0]["candidate_id"], "confirmed")

    def test_only_viable_candidates_can_win(self):
        uninspected = candidate("uninspected")
        uninspected["context_reviewed"]["mode"] = "transcript_only"
        weak_hook = candidate("weak_hook")
        weak_hook["potential"]["criteria"]["gancho"]["score"] = 1
        result = selection.rank_candidates([uninspected, weak_hook, candidate("viable", score=3)])
        self.assertEqual(result["selected_candidate_id"], "viable")
        for item in result["candidates"][1:]:
            self.assertFalse(item["selection_eligible"])
        self.assertEqual(selection.rank_candidates([uninspected, weak_hook])["status"], "research_required")

    def test_partial_context_and_unknown_source_do_not_qualify(self):
        item = candidate()
        item["context_reviewed"]["start_seconds"] = 11
        item["source_url"] = None
        result = selection.rank_candidates([item])
        self.assertIsNone(result["selected_candidate_id"])
        blockers = result["candidates"][0]["selection_blockers"]
        self.assertIn("contexto_nao_cobre_o_corte", blockers)
        self.assertIn("fonte_nao_informada", blockers)

    def test_performance_is_separate_and_does_not_determine_score_or_rank(self):
        unseen = candidate("a", score=3)
        popular = candidate("z", score=3)
        popular["observed_performance"] = {
            "label": "viral_observado",
            "snapshots": [{"observed_at": "2026-11-20T13:00:00-03:00", "views": 10_000_000}],
        }
        result = selection.rank_candidates({"candidates": [popular, unseen]})
        self.assertEqual(result["selected_candidate_id"], "a")
        self.assertEqual(result["candidates"][0]["observed_performance"]["label"], "desempenho_desconhecido")
        self.assertEqual(result["candidates"][1]["observed_performance"]["label"], "tracao_observada_sem_base")
        self.assertEqual(result["candidates"][1]["potential"]["score"], 75)

    def test_performance_requires_timestamp_and_real_counts(self):
        for snapshot in ({"views": 3}, {"observed_at": "2026-11-20T13:00:00", "views": 3},
                         {"observed_at": "2026-11-20T13:00:00Z", "views": -1}):
            item = candidate()
            item["observed_performance"] = {"snapshots": [snapshot]}
            with self.subTest(snapshot=snapshot), self.assertRaises(ValueError):
                selection.rank_candidates([item])

    def test_empty_input_requests_research_and_does_not_mutate_input(self):
        self.assertEqual(selection.rank_candidates([])["status"], "research_required")
        item = candidate()
        original = copy.deepcopy(item)
        selection.rank_candidates([item])
        self.assertEqual(item, original)

    def test_cli_writes_valid_output_and_invalid_input_has_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / "input.json", Path(directory) / "output.json"
            source.write_text(json.dumps([candidate()]), encoding="utf-8")
            run = subprocess.run([sys.executable, str(SCRIPT), str(source), "--output", str(output)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(output.read_text())["selected_candidate_id"], "a")
            source.write_text('[{"candidate_id": "a", "source_start_seconds": NaN}]', encoding="utf-8")
            run = subprocess.run([sys.executable, str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn("constante JSON inválida", run.stderr)
            self.assertEqual(run.stdout, "")

    def test_duplicate_json_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            source.write_text('{"candidates": [], "candidates": []}', encoding="utf-8")
            run = subprocess.run([sys.executable, str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn("campo duplicado", run.stderr)


if __name__ == "__main__":
    unittest.main()
