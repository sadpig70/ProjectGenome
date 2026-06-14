"""Determinism tests for scripts/fingerprint.py (stdlib unittest)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from fingerprint import (  # noqa: E402
    normalize_name, tokenize_name, source_fingerprint, generated_fingerprint,
    is_valid_archetype, ARCHETYPES, LAYERS,
)


class TestNormalizeName(unittest.TestCase):
    def test_lowercase_and_strip(self):
        self.assertEqual(normalize_name("My-Project_42!"), "myproject42")

    def test_empty_and_none(self):
        self.assertEqual(normalize_name(""), "")
        self.assertEqual(normalize_name(None), "")

    def test_collision_after_normalize(self):
        self.assertEqual(normalize_name("Dwell Gate"), normalize_name("dwell-gate"))


class TestSourceFingerprint(unittest.TestCase):
    def test_order_independent(self):
        self.assertEqual(source_fingerprint(["C", "A", "B"]),
                         source_fingerprint(["A", "B", "C"]))

    def test_dedup(self):
        self.assertEqual(source_fingerprint(["A", "A", "B"]), "A+B")

    def test_drops_falsy(self):
        self.assertEqual(source_fingerprint(["A", "", None, "B"]), "A+B")

    def test_canonical_form(self):
        self.assertEqual(source_fingerprint(["B", "A"]), "A+B")

    def test_generated_namespace_same_algorithm(self):
        self.assertEqual(generated_fingerprint(["P2", "P1"]), "P1+P2")


class TestIsValidArchetype(unittest.TestCase):
    def test_single(self):
        for a in ARCHETYPES:
            self.assertTrue(is_valid_archetype(a))

    def test_composite(self):
        self.assertTrue(is_valid_archetype("Gate+Ledger"))

    def test_reject_unknown(self):
        self.assertFalse(is_valid_archetype("Banana"))
        self.assertFalse(is_valid_archetype("Gate+Banana"))

    def test_reject_triple(self):
        self.assertFalse(is_valid_archetype("Gate+Ledger+Index"))

    def test_reject_empty(self):
        self.assertFalse(is_valid_archetype(""))


class TestTokenizeName(unittest.TestCase):
    def test_camelcase_split(self):
        self.assertEqual(tokenize_name("DwellProvenanceGate"),
                         ["dwell", "provenance", "gate"])

    def test_delimiters_and_digits(self):
        self.assertEqual(tokenize_name("Gate2_Ledger-Mesh"),
                         ["gate2", "ledger", "mesh"])

    def test_empty(self):
        self.assertEqual(tokenize_name(""), [])

    def test_vocab_clash_use(self):
        registry = {"mesh", "clearing"}
        self.assertTrue(any(t in registry for t in tokenize_name("PowerMesh")))
        self.assertFalse(any(t in registry for t in tokenize_name("DwellGate")))


class TestLayers(unittest.TestCase):
    def test_five_layers(self):
        self.assertEqual(LAYERS,
                         {"Sensing", "Evidence", "Control", "Allocation", "Release"})


if __name__ == "__main__":
    unittest.main()
