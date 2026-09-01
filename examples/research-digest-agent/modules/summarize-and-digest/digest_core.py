#!/usr/bin/env python3
"""digest_core.py — the portable subset of research-digest-agent's
summarize-and-digest skill, packaged per
ko/08-module-format.md. See MODULE.md in this same folder for the
packaging manifest.

This file contains ONLY the pure functions from the original
skills/summarize-and-digest/digest.py — no file I/O, no shared-context
dependency, no project-specific paths. `HeuristicsStore` and
`ContextStore` (the original's self-improving-loop and context-lifecycle
machinery) are deliberately NOT included here — a project adopting this
module without those files still gets correct filtering/summarization/
audit behavior, just without cross-run memory (graceful degradation, per
crystal 08 principle 1 — never crash for a missing dependency, only lose
the enhancement it would have provided).

Usage as a library:
    from digest_core import matches_interest, detect_injection, summarize, audit_grounding, is_duplicate
"""
import re
import unicodedata


def normalize(text: str) -> str:
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )


CITATION_RE = re.compile(r"['\"]([^'\"]{15,120})['\"]")


def matches_interest(paper: dict, interest_keywords: list) -> tuple[bool, list]:
    title = paper.get("title") or ""
    abstract = paper.get("abstract") or ""
    text_without_citations = CITATION_RE.sub(" ", title + " " + abstract)
    normalized = normalize(text_without_citations)
    matched = [k for k in interest_keywords if k in normalized]
    return (len(matched) > 0, matched)


INJECTION_SIGNALS = [
    "ignore all prior",
    "system note",
    "disregard",
    "auto-publish without review",
    "system:",
]


def detect_injection(paper: dict) -> bool:
    text = normalize((paper.get("title") or "") + " " + (paper.get("abstract") or ""))
    return any(sig in text for sig in INJECTION_SIGNALS)


SUMMARY_MAX_CHARS = 220


def summarize(paper: dict) -> str:
    abstract = paper.get("abstract") or ""
    sentences = [s.strip() for s in abstract.split(". ") if s.strip()]
    if not sentences:
        return ""
    picked = [sentences[0]] + [s for s in sentences[1:] if any(c.isdigit() for c in s)]
    summary = ". ".join(picked)
    if len(summary) > SUMMARY_MAX_CHARS:
        summary = summary[:SUMMARY_MAX_CHARS].rstrip() + "… [truncated]"
    return summary


NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?%?\b")


def audit_grounding(paper: dict, summary: str) -> tuple[bool, list]:
    abstract = paper.get("abstract") or ""
    summary_numbers = set(NUMBER_RE.findall(summary))
    abstract_numbers = set(NUMBER_RE.findall(abstract))
    unverified = sorted(summary_numbers - abstract_numbers)
    return (len(unverified) == 0, unverified)


def is_duplicate(paper: dict, seen_titles: list) -> bool:
    norm = normalize(paper.get("title") or "")
    stripped = re.sub(r"\s*\(v\d+\)\s*$", "", norm).strip()
    for seen in seen_titles:
        seen_stripped = re.sub(r"\s*\(v\d+\)\s*$", "", seen).strip()
        if stripped == seen_stripped:
            return True
    return False


if __name__ == "__main__":
    # Graceful-degradation self-check: prove this module works with ZERO
    # shared-context files present -- no import of HeuristicsStore/
    # ContextStore, no file path referenced anywhere above this line.
    demo_paper = {
        "title": "Retrieval-Augmented Planning for Long-Horizon Agents",
        "abstract": "We study agents that retrieve prior plans before acting. Across 3 benchmark suites, improvement of 12 percentage points.",
    }
    relevant, matched = matches_interest(demo_paper, ["retrieval", "agent"])
    summary = summarize(demo_paper)
    grounded, unverified = audit_grounding(demo_paper, summary)
    print(f"relevant={relevant} matched={matched}")
    print(f"summary={summary!r}")
    print(f"grounded={grounded} unverified={unverified}")
    print(
        "\n(no shared-context/ directory was read anywhere above -- this ran standalone.)"
    )
