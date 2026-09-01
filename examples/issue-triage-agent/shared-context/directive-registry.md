# Directive Registry — issue-triage-agent

> Instantiation of [02-directive-registry.md](../../../ko/02-directive-registry.md)'s
> template for this demo project. The rows below simulate what a real
> project's registry would look like after a few rounds of user
> corrections — they are illustrative fixture content written for this
> demo, not verbatim quotes from an actual person, but they follow the
> template's rules exactly (numbered, re-apply trigger, original wording
> preserved, confidence marked) so a reader can see the format in use.

| # | Directive / what was actually done | Re-apply trigger | User's original words (verbatim) | Confidence |
|---|---|---|---|---|
| 1 | **Billing-related tickets always get an extra `team:finance` label, on top of whatever category the classifier assigns** — implemented as a keyword check (`invoice`, `charged`, `billing`, `refund`) in `triage.py`'s `apply_directives()`. | Whenever a new ticket's title or body contains a billing-related keyword. | "Anything that smells like a billing dispute needs Finance's eyes on it immediately, don't wait for the categorizer to figure that out." | 🟢 explicitly confirmed |
| 2 | **Security-category tickets are never auto-resolved, regardless of how confident the classifier is** — enforced as a hardcoded branch in `decide_oversight_gate()`, not a configurable threshold. | Every run, for every ticket the classifier tags `security`. | "If it's a security report, I don't care how obvious the fix looks — a human confirms before anything closes." | 🟢 explicitly confirmed |
| 3 | **Contact info (email/phone) found in a ticket body is redacted before it is ever written to a log file or a public-facing label/comment** — implemented as `redact_pii()`, applied unconditionally before both `log_ticket()` and any public output, not only for tickets already suspected of containing PII. | Every ticket, every run — no exception carve-out. | "Whatever ends up in a log or a comment other people can see, it should never contain someone's email or phone number just because they pasted it into a bug report." | 🟢 explicitly confirmed |

## Conflict handling

None of the three rows above currently conflict with each other (row 1
only adds a label, rows 2 and 3 only tighten gates — none override each
other's output). If a future row ever changed the *category* a ticket
gets classified as (rather than adding a label or tightening a gate), that
would be exactly the kind of "does this rank above or below an existing
row" conflict [02](../../../ko/02-directive-registry.md) says isn't
resolved by row number alone — it would need an explicit human decision,
not an automatic "lower number wins."

## When to add a new row

Per the template: when the ticket-triage system's owner gives a new
standing instruction, when the agent itself makes a new routing judgment
call worth remembering, or when an existing row turns out to have an
exception. See `../shared-context/heuristics.md` for the sibling mechanism
this project uses for *corrections learned from actually running the
skill*, as opposed to directives given up front — the two files are not
duplicates of each other (registry = standing rules given or confirmed by
a person; heuristics = lessons the loop itself accumulated from watching
its own output).
