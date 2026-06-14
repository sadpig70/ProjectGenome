"""Contract tests for scripts/validate_projectgenome.py (stdlib unittest)."""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import validate_projectgenome as V  # noqa: E402


class TestValidateBundledArtifacts(unittest.TestCase):
    def test_repo_root_passes(self):
        """The shipped schemas/ + examples/example-run/ must validate cleanly."""
        argv = sys.argv
        try:
            sys.argv = ["validate", ROOT]
            self.assertEqual(V.main(), 0)
        finally:
            sys.argv = argv


class TestValidateDetectsProblems(unittest.TestCase):
    def _run(self, root):
        argv = sys.argv
        try:
            sys.argv = ["validate", root]
            return V.main()
        finally:
            sys.argv = argv

    def test_invalid_archetype_fails(self):
        with tempfile.TemporaryDirectory() as d:
            gene = [{
                "project": "X", "repo": "x", "domain": "d",
                "archetype": "Banana", "mechanism": "m", "layer": "Sensing",
                "verdict_scheme": ["ok"], "vocab": ["x"],
            }]
            with open(os.path.join(d, "genes.json"), "w", encoding="utf-8") as h:
                json.dump(gene, h)
            self.assertEqual(self._run(d), 1)

    def test_missing_required_field_fails(self):
        with tempfile.TemporaryDirectory() as d:
            gene = [{"project": "X", "archetype": "Gate", "layer": "Sensing"}]
            with open(os.path.join(d, "genes.json"), "w", encoding="utf-8") as h:
                json.dump(gene, h)
            self.assertEqual(self._run(d), 1)

    def test_noncanonical_fingerprint_key_fails(self):
        with tempfile.TemporaryDirectory() as d:
            reg = {
                "schema_version": "1.1", "version": 0,
                "source_fingerprints": {"B+A": {"project": "P"}},
                "generated_fingerprints": {},
                "generated_projects": {},
            }
            with open(os.path.join(d, "registry.empty.json"), "w", encoding="utf-8") as h:
                json.dump(reg, h)
            self.assertEqual(self._run(d), 1)

    def test_empty_dir_passes_with_no_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self._run(d), 0)


_GOOD_SEED = """# DESIGN-SEED-DwellGate
## 한 질문
> q?
## 분류
- archetype: Gate+Ledger
- layers_used: Control, Evidence
## 재사용 계획 (reuse_plan)
| 부품 | source project | kind | reuse_cost |
|---|---|---|---|
| rules | A | engine | copy |
| ledger | B | ledger | copy |
## 판정 (verdict_scheme)
allow / block
## 경계 (boundary)
> 이것은 결제 처리기가 아니다.
"""


class TestCheckSeedStructure(unittest.TestCase):
    def _seed_run(self, text):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "DESIGN-SEED-X.md"), "w", encoding="utf-8") as h:
                h.write(text)
            argv = sys.argv
            try:
                sys.argv = ["validate", d]
                return V.main()
            finally:
                sys.argv = argv

    def test_good_seed_passes(self):
        self.assertEqual(self._seed_run(_GOOD_SEED), 0)

    def test_invalid_archetype_fails(self):
        self.assertEqual(self._seed_run(_GOOD_SEED.replace("Gate+Ledger", "Banana")), 1)

    def test_invalid_layer_fails(self):
        self.assertEqual(self._seed_run(_GOOD_SEED.replace("Control, Evidence", "Control, Bogus")), 1)

    def test_single_reuse_row_fails(self):
        one = _GOOD_SEED.replace("| ledger | B | ledger | copy |\n", "")
        self.assertEqual(self._seed_run(one), 1)

    def test_boundary_without_negation_fails(self):
        weak = _GOOD_SEED.replace("> 이것은 결제 처리기가 아니다.", "> 이것은 결제 처리기다.")
        self.assertEqual(self._seed_run(weak), 1)


if __name__ == "__main__":
    unittest.main()
