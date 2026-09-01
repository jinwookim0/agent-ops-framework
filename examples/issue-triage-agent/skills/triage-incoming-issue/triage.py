#!/usr/bin/env python3
"""triage.py — the runnable classification/routing logic behind the
"triage-incoming-issue" skill (see ../SKILL.md for the procedural
description this implements).

This is deliberately a plain keyword-rule classifier, not a call to an
LLM API — the point of this demo is to show how agent-ops-framework's
crystals shape an agent's *structure and governance* (what gets logged,
what requires human confirmation, how corrections get remembered), and
that holds regardless of whether the classification step underneath is
a keyword ruleset (this script) or a real LLM call. See SKILL.md's
"swapping in a real classifier" note for exactly where that plugs in
without touching anything built below.

Demonstrates, in the order they run:
  - crystal 02 (directive-registry.md)   -> apply_directives()
  - crystal 05 / 20 (oversight & RACI)   -> decide_oversight_gate()
  - crystal 07 (prompt-guardrails)       -> redact_pii()
  - crystal 31 (synthetic-data isolation)-> log path picked by --eval vs default
  - crystal 11 (observability)           -> log_ticket()
  - crystal 37 (target-metric-gaming)    -> check_trip_wire()

Usage:
  ./triage.py            # process sample-tickets.json, write to the EVAL
                          # memory file (default — safe, never touches
                          # the "real" ticket-history file)
  ./triage.py --eval     # same as above, explicit
  ./triage.py --real <tickets.json>
                          # process a real ticket batch and append to the
                          # real ticket-history file — never used with
                          # sample-tickets.json

Exit code: always 0 (advisory report, same convention as this repo's
scripts/*.py checkers).
"""
import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_TICKETS = HERE / "sample-tickets.json"
EVAL_LOG = HERE.parent.parent / "observability" / "sample-run.jsonl"
REAL_LOG = (
    HERE.parent.parent / "observability" / "real-run.jsonl"
)  # never committed with real data

# ---------------------------------------------------------------------------
# crystal 07 (prompt-guardrails) — redact contact info before it is ever
# logged or would be posted publicly. Same spirit as
# ko/07-prompt-guardrails/scripts/mask-sensitive-output.py's PATTERNS list,
# scoped down to the two fields this ticket-triage domain actually produces
# (email, phone) rather than secrets/API keys (this agent never touches
# those).
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\b\d{3}[-.\s]?\d{4}\b")


def redact_pii(text: str) -> str:
    text = EMAIL_RE.sub("[redacted-email]", text)
    text = PHONE_RE.sub("[redacted-phone]", text)
    return text


# ---------------------------------------------------------------------------
# Classifier (the piece a real deployment would swap for an LLM call —
# see SKILL.md). Kept as plain keyword rules here so this file has zero
# external dependencies and runs the same way every time (crystal 13's
# "reproducibility" quality-bar criterion, satisfied trivially by being
# rule-based rather than by proving an LLM call is deterministic).
SECURITY_KEYWORDS = [
    "auth bypass",
    "vulnerability",
    "exploit",
    "cve",
    "security",
    "bypass",
]
BUG_KEYWORDS = [
    "crash",
    "error",
    "bug",
    "traceback",
    "typeerror",
    "stack trace",
    "broken",
]
FEATURE_KEYWORDS = ["would be great", "nice to have", "feature", "request", "wish"]
QUESTION_KEYWORDS = ["how do i", "how do you", "is this possible", "?"]
BILLING_KEYWORDS = ["invoice", "charged", "billing", "refund"]

REPRO_SIGNALS = ["repro:", "steps to reproduce", "console shows", "stack trace"]


def classify(ticket: dict) -> tuple[str, float]:
    """Returns (category, confidence). confidence is a crude proxy — the
    fraction of category-defining keyword families found — not a
    calibrated probability; see epistemic-check.md's note on not
    presenting this as more precise than it is (crystal 03, item 2:
    false precision)."""
    text = (ticket["title"] + " " + ticket["body"]).lower()

    if any(k in text for k in SECURITY_KEYWORDS):
        return "security", 0.9
    if any(k in text for k in BUG_KEYWORDS):
        has_repro = any(s in text for s in REPRO_SIGNALS)
        return "bug", 0.85 if has_repro else 0.4
    if any(k in text for k in BILLING_KEYWORDS):
        return "billing", 0.8
    if any(k in text for k in FEATURE_KEYWORDS):
        return "feature-request", 0.8
    if any(k in text for k in QUESTION_KEYWORDS):
        return "question", 0.75
    return "needs-human-review", 0.2


def apply_directives(ticket: dict, category: str) -> list[str]:
    """crystal 02 (directive-registry.md) — check the standing registry
    BEFORE finalizing routing, instead of only relying on the
    classifier's own default. Hardcodes the same 3 rules
    shared-context/directive-registry.md rows 1-3 declare in prose; a
    production version would parse the table directly so the registry
    file is the single source of truth, but hardcoding keeps this demo
    dependency-free and readable top-to-bottom without a markdown
    parser."""
    labels = [category]
    text = (ticket["title"] + " " + ticket["body"]).lower()
    if any(k in text for k in BILLING_KEYWORDS):  # registry row 1
        labels.append("team:finance")
    return labels


def decide_oversight_gate(category: str, confidence: float) -> tuple[str, str]:
    """crystal 05 (0th principle + Unknown-Unknowns matrix) and crystal 20
    (A is always a human) — returns (oversight_gate, reason).

    security is a hardcoded branch, not a configurable confidence
    threshold (registry row 2) — precisely so that a future change to
    the confidence formula above can never silently loosen this gate."""
    if category == "security":
        return (
            "confirm",
            "security reports are never auto-resolved regardless of classifier confidence (directive-registry row 2)",
        )
    if category == "needs-human-review":
        return (
            "ask",
            "confidence too low to route with any default action (crystal 04 'boundary zone' equivalent)",
        )
    if confidence >= 0.7:
        return (
            "notify",
            "clear-confidence routing decision; a human is informed but not blocked on",
        )
    return (
        "notify",
        "moderate confidence; routed but flagged for spot-check in the weekly review",
    )


def log_ticket(
    ticket: dict,
    category: str,
    confidence: float,
    labels: list[str],
    gate: str,
    gate_reason: str,
) -> dict:
    """crystal 11 (observability-and-agent-tracing) — one structured log
    line per ticket, matching observability/log-schema.md's field list
    (and, loosely, the OpenTelemetry GenAI attribute names that table
    maps to)."""
    return {
        "gen_ai.operation.name": "triage-incoming-issue",
        "task_id": ticket["id"],
        "intent": f"classify and route {ticket['id']}",
        "tool_calls": [
            "classify()",
            "apply_directives()",
            "decide_oversight_gate()",
            "redact_pii()",
        ],
        "result": {
            "category": category,
            "confidence": round(confidence, 2),
            "labels": labels,
            "oversight_gate": gate,
            "oversight_gate_reason": gate_reason,
            "body_excerpt_redacted": redact_pii(ticket["body"])[:160],
        },
        "timestamp": ticket["created_at"],
        "cost": {
            "tool_calls": 4,
            "tokens": None,
            "note": "rule-based classifier — no LLM tokens spent",
        },
    }


def naive_baseline(ticket: dict, category: str, confidence: float) -> list[str]:
    """What this same ticket would get if none of the governance layers
    below were there — just a classifier wired straight to auto-action,
    the shape a first draft of this agent plausibly looks like before any
    crystal is applied. Returns a list of concrete harms this specific
    ticket would have caused under that naive version, or [] if this
    ticket happens not to exercise any of them (most don't — the point is
    not "everything is dangerous," it's "here are the specific cases
    where it would have mattered").

    This function changes nothing about how the ticket is actually
    routed — decide_oversight_gate() and redact_pii() above are still
    what runs. This is purely a counterfactual for the report, so a
    reader doesn't have to take "this framework helps" on faith."""
    harms = []
    if category == "security":
        harms.append(
            "a naive always-auto-act agent would have closed this security report on its own "
            f"(confidence {confidence:.2f} clears any reasonable auto-approve bar) — no human "
            "would have seen it unless they went looking"
        )
    if category == "needs-human-review":
        harms.append(
            "a naive agent has no 'I don't know' category — it would have forced this into "
            "whatever category scored highest anyway and auto-resolved it, silently, with no "
            "signal that the classifier was actually guessing"
        )
    if EMAIL_RE.search(ticket["body"]) or PHONE_RE.search(ticket["body"]):
        harms.append(
            "a naive agent logs the raw ticket body — this reporter's email/phone would sit in "
            "plaintext in a log file (and in a real deployment, potentially in a public comment)"
        )
    return harms


def check_trip_wire(log_lines: list[dict]) -> list[str]:
    """crystal 37 (target-metric-gaming-safeguards), mechanism 2 (trip
    wires) — a perfect "auto-resolution rate" for some category is not
    automatically good news: it can also mean that category has never
    once been escalated for a human look, which is exactly the kind of
    thing a gamed metric would hide. Flags any category where every
    single ticket got oversight_gate=notify and none ever hit
    ask/confirm."""
    warnings = []
    by_category: dict[str, list[str]] = {}
    for line in log_lines:
        cat = line["result"]["category"]
        by_category.setdefault(cat, []).append(line["result"]["oversight_gate"])
    for cat, gates in by_category.items():
        if len(gates) >= 3 and all(g == "notify" for g in gates):
            warnings.append(
                f"trip wire: category '{cat}' auto-resolved 100% of {len(gates)} tickets with zero "
                "escalations this run — worth a spot-check that this isn't a classifier blind spot "
                "rather than genuinely easy tickets"
            )
    return warnings


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("tickets_file", nargs="?", type=pathlib.Path, default=None)
    ap.add_argument(
        "--real",
        action="store_true",
        help="write to the real ticket-history log instead of the eval log",
    )
    args = ap.parse_args()

    tickets_file = args.tickets_file or DEFAULT_TICKETS
    if args.real and tickets_file == DEFAULT_TICKETS:
        print(
            "error: refusing to run --real against sample-tickets.json — synthetic fixtures must never "
            "reach the real ticket-history log (crystal 31). Pass an explicit real tickets file.",
            file=sys.stderr,
        )
        return 1

    data = json.loads(tickets_file.read_text(encoding="utf-8"))
    if not args.real and not data.get("_synthetic"):
        print(
            f"error: {tickets_file} is not marked _synthetic:true, but --eval mode (default) only "
            "accepts synthetic fixtures. Use --real for a genuine ticket batch.",
            file=sys.stderr,
        )
        return 1

    log_path = REAL_LOG if args.real else EVAL_LOG
    log_lines = []
    print(
        f"=== triage-incoming-issue: {len(data['tickets'])} ticket(s), writing log to {log_path.relative_to(HERE.parent.parent)} ===\n"
    )

    all_harms = []
    for ticket in data["tickets"]:
        category, confidence = classify(ticket)
        labels = apply_directives(ticket, category)
        gate, reason = decide_oversight_gate(category, confidence)
        line = log_ticket(ticket, category, confidence, labels, gate, reason)
        log_lines.append(line)
        print(
            f"{ticket['id']}: category={category} confidence={confidence:.2f} labels={labels} gate={gate}"
        )
        print(f"  reason: {reason}")
        harms = naive_baseline(ticket, category, confidence)
        for h in harms:
            print(f"  ⚠️  without this framework's governance layer: {h}")
        all_harms.extend((ticket["id"], h) for h in harms)

    warnings = check_trip_wire(log_lines)
    if warnings:
        print("\n⚠️ trip wires triggered:")
        for w in warnings:
            print(f"  {w}")
    else:
        print("\n✅ no trip wires triggered this run.")

    print(
        f"\n=== what this run actually demonstrates ===\n"
        f"{len(all_harms)} concrete harm(s) avoided out of {len(data['tickets'])} ticket(s) — "
        "the other tickets routed the same way a naive version would have, which is the point: "
        "this framework's mechanisms are supposed to be invisible on the easy cases and only "
        "change behavior on the ones that would otherwise go wrong. See CASE-STUDY.md for how "
        "each mechanism below maps to a specific crystal."
    )
    for ticket_id, h in all_harms:
        print(f"  - [{ticket_id}] {h}")

    with open(log_path, "w", encoding="utf-8") as f:
        for line in log_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
