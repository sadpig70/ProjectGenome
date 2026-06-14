"""OCC contract tests for scripts/concurrency.py (stdlib unittest)."""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import concurrency as C  # noqa: E402


def _empty_registry(d):
    path = os.path.join(d, "registry.json")
    with open(path, "w", encoding="utf-8") as h:
        json.dump({
            "schema_version": "1.1", "version": 0, "active_runs": [],
            "source_projects": {}, "generated_projects": {},
            "blocked_names": [], "source_fingerprints": {}, "generated_fingerprints": {},
        }, h)
    return path


class TestLock(unittest.TestCase):
    def test_lock_is_reentrant_serially(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            with C.registry_lock(p):
                self.assertTrue(os.path.exists(p + ".lock"))
            self.assertFalse(os.path.exists(p + ".lock"))

    def test_lock_busy_times_out(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            with C.registry_lock(p):
                with self.assertRaises(TimeoutError):
                    with C.registry_lock(p, timeout=0.2):
                        pass


class TestClaim(unittest.TestCase):
    def test_claim_bumps_version_and_appends(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            r1 = C.claim_run(p, "alpha")
            self.assertEqual(r1["claim_seq"], 1)
            self.assertEqual(r1["run_id"], "001-alpha-pending")
            reg = C.read_registry(p)
            self.assertEqual(reg["version"], 1)
            self.assertEqual(len(reg["active_runs"]), 1)
            self.assertEqual(reg["active_runs"][0]["status"], "active")

    def test_sequential_claims_distinct(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            r1 = C.claim_run(p, "alpha")
            r2 = C.claim_run(p, "beta")
            self.assertNotEqual(r1["run_id"], r2["run_id"])
            self.assertEqual(r2["claim_seq"], 2)
            self.assertEqual(r2["run_id"], "002-beta-pending")


class TestCommit(unittest.TestCase):
    def test_clean_commit(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            run = C.claim_run(p, "alpha")
            winner = {"name": "DwellGate", "consumed_sources": ["A", "B"], "slug": "dwell-gate"}
            self.assertEqual(C.commit_run(p, run, winner), "committed")
            reg = C.read_registry(p)
            self.assertIn("DwellGate", reg["generated_projects"])
            self.assertIn("DwellGate", reg["blocked_names"])
            self.assertIn("A+B", reg["source_fingerprints"])
            self.assertEqual(reg["source_projects"]["A"]["use_count"], 1)
            self.assertEqual(reg["active_runs"][0]["status"], "committed")
            latest = C.read_registry(os.path.join(d, "latest.json"))
            self.assertEqual(latest["winner"], "DwellGate")

    def test_name_collision_aborts(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            run1 = C.claim_run(p, "alpha")
            C.commit_run(p, run1, {"name": "DwellGate", "consumed_sources": ["A", "B"]})
            run2 = C.claim_run(p, "beta")
            # different sources, same (normalized) name → hard collision
            self.assertEqual(
                C.commit_run(p, run2, {"name": "dwell gate", "consumed_sources": ["C", "D"]}),
                "collision")
            reg = C.read_registry(p)
            self.assertEqual(len(reg["generated_projects"]), 1)
            statuses = {ar["run_id"]: ar["status"] for ar in reg["active_runs"]}
            self.assertEqual(statuses[run2["run_id"]], "aborted")

    def test_source_fingerprint_collision_aborts(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            run1 = C.claim_run(p, "alpha")
            C.commit_run(p, run1, {"name": "GateOne", "consumed_sources": ["A", "B"]})
            run2 = C.claim_run(p, "beta")
            # same source set (order-independent) → fingerprint collision
            self.assertEqual(
                C.commit_run(p, run2, {"name": "GateTwo", "consumed_sources": ["B", "A"]}),
                "collision")

    def test_run_dir_renamed_on_commit(self):
        with tempfile.TemporaryDirectory() as d:
            p = _empty_registry(d)
            runs = os.path.join(d, "runs")
            os.makedirs(runs)
            run = C.claim_run(p, "alpha", runs_dir=runs)
            os.makedirs(os.path.join(runs, run["run_id"]))
            C.commit_run(p, run, {"name": "DwellGate", "consumed_sources": ["A", "B"],
                                  "slug": "dwell-gate"}, runs_dir=runs)
            nnn = run["run_id"][:3]
            self.assertTrue(os.path.isdir(os.path.join(runs, "%s-dwell-gate" % nnn)))


if __name__ == "__main__":
    unittest.main()
