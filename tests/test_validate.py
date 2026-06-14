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


if __name__ == "__main__":
    unittest.main()
