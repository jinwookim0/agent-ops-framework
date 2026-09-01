<!-- translated-from: f50ae882e38151ea4b5a844ad9a14dcd72e876ce -->
# AI Risk Management 4-Function Index — Reorganizing the Other Crystals Around the NIST AI RMF Skeleton

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/17-ai-risk-management-index.md)**

**Version**: 1.1.0
**Content hash**: sha256:ed44652ab65b (of the body below, excluding the stamp comment, this line, and the version line)

This crystal doesn't add new content — instead, it's an index that
reorganizes the other crystals according to **where each one falls
within an internationally recognized risk-management framework**.
Instead of consulting each document separately, the goal is to see at a
glance "which of these four functions is currently empty in our
project."

**Scope of this index**: only crystals actually placed under the four
functions below are covered — this is a subset of the full crystal list
(README.md), not all of it. NIST AI RMF is a risk-focused skeleton, so
crystals that would be distorted rather than clarified by forcing them
into a risk-management function — the structure/reuse/documentation axis
([08-module-format.md](08-module-format.md), [09-project-structure-template.md](09-project-structure-template.md),
[16-context-engineering-principles.md](16-context-engineering-principles.md),
[28-writing-craft-guardrails.md](28-writing-craft-guardrails.md),
[30-shared-context-lifecycle-management.md](30-shared-context-lifecycle-management.md),
[33-sandboxed-harness-duplication-sync.md](33-sandboxed-harness-duplication-sync.md)) —
are deliberately left outside this index. [01-definition-of-done.md](01-definition-of-done.md)
is left out for the same reason — "How to use this 4-function index"
below already explains why ("is it done" vs. "is it done safely" are
different axes). [24-application-deadline-rule.md](24-application-deadline-rule.md)
is also left out — it's a research/application habit, not a
risk-management function. **This out-of-scope list itself needs
re-checking as more crystals are added** — see "This crystal's own
limits" below for that re-check rule.

## Basis (primary source verified — stated honestly)

🟢 **Verified**: That NIST's (the U.S. National Institute of Standards
and Technology) AI Risk Management Framework (AI RMF 1.0) consists of
four core functions — **Govern, Map, Measure, and Manage** — was
verified directly against the original on the official nist.gov page.

⚪ **Not verified**: The official detailed definitions of each function
could not be viewed in the original within this session's tool-access
scope at the time of writing (the document page moved/404'd). The
"This document's interpretation" section below is **not NIST's official
wording, but this document's own reconstruction, drawing on the four
function names and generally known AI risk-management practice** —
so as not to appear to quote NIST, the section title below is
explicitly marked "This document's interpretation."

## This document's interpretation — practical questions and related crystals mapped to the four functions

### Govern — "Who makes this decision, and under what authority?"
Practical questions: Who defines the scope of autonomous execution? Who
approves irreversible actions? Is there an organization-level policy?

Related crystals: [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
(principle 0, unknown-unknowns gating), [RISK-ANALYSIS.md](../ko/RISK-ANALYSIS.md)
(the process of deciding whether to publish this very framework is
itself a real-world case of governance),
[10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md)
G17 (provide a global control), [02-directive-registry.md](02-directive-registry.md)
(indexing decisions/directives themselves with priority and
re-application triggers), [20-decision-rights-raci.md](20-decision-rights-raci.md)
(who holds approval/review/execution authority when several people share
the same agent), [25-directive-editing-delegation-levels.md](25-directive-editing-delegation-levels.md)
(the delegation level for how much an AI may edit the directive
documents themselves), [36-execution-mode-escalation-ladder.md](36-execution-mode-escalation-ladder.md)
(deciding, on a signal basis, who has the authority to escalate the
level of execution parallelization — also a form of autonomy-scope
governance).

### Map — "In what situations, and in what ways, can this system fail?"
Practical questions: What is this feature's threat surface? What inputs
could cause the system to misbehave? Where is the boundary between
intended and unintended use?

Related crystals: [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md)
(threat modeling based on the OWASP LLM Top 10),
[15-model-card-template.md](15-model-card-template.md) (Intended Use —
spelling out unintended use), [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md)
(a map of the 12 patterns by which AI fails), [19-chaos-engineering-for-agents.md](19-chaos-engineering-for-agents.md)
(actively searching out the failure surface by deliberately breaking
things before a real incident), [27-premortem-planning.md](27-premortem-planning.md)
(assuming failure, without optimism, before execution), [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md)
(the pattern where individually-safe information becomes a
re-identification threat surface once combined).

### Measure — "How do you know how well this actually works?"
Practical questions: What are the pass criteria? Did you actually
measure it, or just assume it seemed plausible? Does the measurement
hold up across subgroups too?

Related crystals: [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)
(the 9-stage verification pipeline), [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md)
(logs, not claims), [15-model-card-template.md](15-model-card-template.md)
(Metrics/Quantitative Analyses), [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md)
(how much you can trust the measurement itself when the same input
yields a different answer), [21-spec-first-implementation.md](21-spec-first-implementation.md)
(quantitatively measuring the effect of writing a spec first), [22-llm-benchmark-literacy.md](22-llm-benchmark-literacy.md)
(reading a benchmark number's credibility, contamination, and
absolute-vs-relative framing), [26-grounding-validity-audit.md](26-grounding-validity-audit.md)
(periodically re-checking whether an already-written guide's citations
still hold), [34-self-experiment-reporting-standard.md](34-self-experiment-reporting-standard.md)
(honestly measuring and reporting a self-experiment that has no
predefined test case).

### Manage — "How do you actually reduce a risk once it's found?"
Practical questions: In what order do you address discovered
vulnerabilities/debt? How do you prevent recurrence? How does an
incident get turned into learning?

Related crystals: [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md)
(debt repayment prioritization), [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)
(turning incidents into recurrence-prevention actions),
[06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)
(feeding learned lessons back into the next run), [07-prompt-guardrails/](07-prompt-guardrails/)
(actually lowering information-leak risk with executable code),
[23-confidential-project-protection.md](23-confidential-project-protection.md)
(managing project-level confidentiality that pattern-matching can't
catch, by enforcing it at the git-push level), [29-agent-cost-and-budget-management.md](29-agent-cost-and-budget-management.md)
(managing the risk of runaway token/cost spend through caching and
distinguishing limit signals), [31-synthetic-data-memory-isolation.md](31-synthetic-data-memory-isolation.md)
(the preventive procedure for the specific risk of synthetic eval data
contaminating permanent memory), [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md)
(managing the risk of an employer's confidential information bleeding
into content meant for publication, via a scrub/review/disclaimer
procedure — not the publish decision itself, cited under Govern via
RISK-ANALYSIS.md, but the concrete mitigation procedure that carries it
out).

## How to use this 4-function index

When building a new AI agent feature, ask one question per function to
check completeness:
- [ ] **Govern**: Who set the scope of autonomous execution for this
      feature, and where is that recorded?
- [ ] **Map**: Have you thought through the ways this feature could
      fail in advance (using the red-team checklist)?
- [ ] **Measure**: Did you actually run verification cases, or did you
      just stop at "it'll probably be fine"?
- [ ] **Manage**: If a failure is found, where does it get recorded and
      what's the plan to prevent recurrence?

If any one of the four is entirely blank, that feature is still in a
state of "risk not managed" — a different axis from the structural
completeness criteria in
[01-definition-of-done.md](01-definition-of-done.md) (that one asks "is
it done," this one asks "is it done safely") — but the two complement
each other.

## This crystal's own limits (stated honestly)

This document is **not an official explainer of the NIST AI RMF** —
only the four function names are taken from NIST; what's filled inside
them comes from this framework's own other crystals. If you want to
directly consult NIST's actual detailed guidance (subcategories, actual
evaluation criteria, etc.) in the original, you need to separately view
the AI RMF 1.0 document on nist.gov — this crystal is not a substitute
for that, but a table of contents that reorganizes the existing crystals
from a different angle.

**This index's own staleness risk — stated honestly**: because this
crystal "adds no new content, only reorganizes existing crystals," it's
easy to forget that this document also needs updating every time a new
crystal is added — in fact, this document was once left with more than
half of the newly-added crystals missing from its 4-function mapping (a
case of this framework missing, in itself, exactly the drift it warns
projects to watch for). When a newly added crystal clearly falls under
one of governance/threat-surface/measurement/mitigation, adding one line
to the matching section here should be part of that crystal's own
"integration" step checklist (BLUEPRINT.md section 3).
