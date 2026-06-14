#!/usr/bin/env python3
"""Deterministic identity primitives for ProjectGenome (stdlib only).

Coding these as functions (rather than leaving them to AI judgment each run)
keeps avoidance/registry behavior stable across runtimes. See
skills/recreate/reference/rerun-avoidance.md §6.1.

usage as a library:
    from fingerprint import normalize_name, source_fingerprint, generated_fingerprint
usage as a CLI (quick check):
    python scripts/fingerprint.py source ADPR ReleaseMesh PnR
    python scripts/fingerprint.py name "MyCandidateName"
"""

import re
import sys

ARCHETYPES = {"Gate", "Mesh", "Clearing", "Index", "Ledger", "Stage", "Appraisal"}
LAYERS = {"Sensing", "Evidence", "Control", "Allocation", "Release"}


def normalize_name(name: str) -> str:
    """Lowercase, strip everything non-alphanumeric. Used for name-collision checks."""
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def tokenize_name(name: str) -> list:
    """Split a CamelCase / delimited project name into lowercase word tokens.

    Deterministic basis for vocab_clash (see differentiation.md): no AI needed —
    e.g. 'DwellProvenanceGate' -> ['dwell', 'provenance', 'gate'].
    """
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", (name or ""))
    return [t for t in re.split(r"[^A-Za-z0-9]+", spaced.lower()) if t]


def source_fingerprint(parts) -> str:
    """Canonical key for a set of corpus source projects (order-independent, dedup)."""
    return "+".join(sorted(set(p for p in parts if p)))


def generated_fingerprint(parents) -> str:
    """Canonical key for a set of parent *generated* projects (integration namespace)."""
    return "+".join(sorted(set(p for p in parents if p)))


def is_valid_archetype(value: str) -> bool:
    """Accept a single archetype or a 'Primary+Secondary' composite."""
    parts = (value or "").split("+")
    return 1 <= len(parts) <= 2 and all(p in ARCHETYPES for p in parts)


def _main(argv) -> int:
    if len(argv) >= 3 and argv[1] == "source":
        print(source_fingerprint(argv[2:]))
        return 0
    if len(argv) >= 3 and argv[1] == "generated":
        print(generated_fingerprint(argv[2:]))
        return 0
    if len(argv) >= 3 and argv[1] == "name":
        print(normalize_name(argv[2]))
        return 0
    sys.stderr.write(
        "usage:\n"
        "  python scripts/fingerprint.py source <SrcA> <SrcB> ...\n"
        "  python scripts/fingerprint.py generated <ParentA> <ParentB> ...\n"
        "  python scripts/fingerprint.py name \"<Name>\"\n")
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
