"""Tests for scripts/aggregate_crossmodel.py (stdlib unittest)."""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import aggregate_crossmodel as A  # noqa: E402


def _score(vals, self_authored=False):
    s = dict(zip(A.AXES, vals))
    s["aggregate"] = round(sum(vals), 4)
    s["self_authored"] = self_authored
    s["rationale"] = "t"
    return s


def _write(d, runtime, scores, name=None):
    fname = name or ("%s.scores.json" % runtime)
    with open(os.path.join(d, fname), "w", encoding="utf-8") as h:
        json.dump({"runtime": runtime, "scores": scores}, h)


class TestLoad(unittest.TestCase):
    def test_loads_and_skips_template(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "A", {"Cand": _score([0.1] * 6)})
            _write(d, "B", {"Cand": _score([0.2] * 6)})
            _write(d, "tpl", {"X": _score([0.0] * 6)}, name="_TEMPLATE.scores.json")
            data = A.load(d)
            self.assertEqual(set(data), {"A", "B"})


class TestIntegrity(unittest.TestCase):
    def test_clean(self):
        data = {
            "A": {"scores": {"Cand": _score([0.1] * 6)}},
            "B": {"scores": {"Cand": _score([0.2] * 6)}},
        }
        candidates, problems = A.integrity(data)
        self.assertEqual(candidates, ["Cand"])
        self.assertEqual(problems, [])

    def test_out_of_range_flagged(self):
        data = {"A": {"scores": {"Cand": _score([1.5, 0, 0, 0, 0, 0])}}}
        _, problems = A.integrity(data)
        self.assertTrue(any("out of range" in p for p in problems))

    def test_aggregate_mismatch_flagged(self):
        bad = _score([0.1] * 6)
        bad["aggregate"] = 9.9
        data = {"A": {"scores": {"Cand": bad}}}
        _, problems = A.integrity(data)
        self.assertTrue(any("aggregate" in p for p in problems))

    def test_missing_candidate_flagged(self):
        data = {
            "A": {"scores": {"Cand": _score([0.1] * 6)}},
            "B": {"scores": {"Other": _score([0.2] * 6)}},
        }
        _, problems = A.integrity(data)
        self.assertTrue(any("missing candidate" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
