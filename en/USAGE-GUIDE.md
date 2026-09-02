<!-- translated-from: ssot=sha256:4e3c584c1ebe own=sha256:7d5aac23e0f0 -->
# Usage Guide — Five Perspectives: Planning, Design, Implementation, Improvement, Reference

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/USAGE-GUIDE.md)**

This lays out what and how to use, from each of five perspectives, when
introducing this framework (`agent-ops-framework/`) into a new project.
There's no need to read it in order — just read whichever section matches
the stage you're at right now.

> If you're in the middle of bringing this folder into a project for the
> first time and need the literal, in-order "what do I do starting from
> step 1" procedure, read
> [GETTING-STARTED.md](GETTING-STARTED.md) first — this document explains
> by perspective, that one is a step-by-step checklist.

## Planning perspective — "why and when should we adopt this"

**When does adopting this become worthwhile**: from the moment an AI agent
(Claude Code, etc.) starts repeatedly managing multiple tasks for one
person across multiple sessions. The whole framework is overkill for a
one-off question-and-answer — the "13-step rebuild sequence" in section 4
of [09-project-structure-template.md](09-project-structure-template.md)
works precisely as a timeline of "what becomes necessary, and when."

**Minimum starting point**: there's no need to bring everything in at
once. Priority order:
1. [07-prompt-guardrails/](07-prompt-guardrails/) — must be installed
   **before** even a single task touching personal data comes up (adding
   it after the fact means erasing something already exposed, which is a
   much more expensive job).
2. [01-definition-of-done.md](01-definition-of-done.md) — once tasks start
   exceeding 3-5.
3. [02-directive-registry.md](02-directive-registry.md) — once user
   directives start needing repeated re-confirmation.
4. The rest (04, 05, 06, 08, 09) — whenever the "why this is needed"
   opening of each document actually applies to your own project.

**Basis for the decision**: the trigger for adoption should be "this
debt/problem has actually happened," not "it would be nice to have this
feature" — the same spirit as the "the ultimate beneficiary is the user"
principle in
[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md):
don't let the governance infrastructure itself become the goal.

## Design perspective — "how do I fit this into my project's structure"

**Bring the schema over as-is and just change the values**: the metadata
fields in sections 3.1-3.4 of
[09-project-structure-template.md](09-project-structure-template.md)
(oversight grade, confidence grade, domain, etc.) mostly work fine kept
with the same names and value sets. Try them as-is first rather than
redesigning, and adjust only the parts that genuinely don't fit ("if you
don't check an existing standard first and just name things arbitrarily,
you pay a renaming cost later" is a lesson the original project has
learned too).

**Which layer to map to the 5 layers first**: if a project already exists,
don't force its existing folder structure to fit the 5 layers ([09](09-project-structure-template.md)
section 1). Instead, ask first: "does this project have something that
corresponds to this layer right now? If not, is it actually needed?"
Example: it's fine not to have a product layer (a finished deliverable
shown to users) yet — a project runs perfectly well with just a task layer
and a governance layer.

**Guardrails get live-fire tested the moment they're installed**: don't
skip step 4 of the "Installation" section in
[07-prompt-guardrails/README.md](07-prompt-guardrails/README.md)
(confirming an actual block using a dummy sensitive file) — a config file
being syntactically correct is no guarantee it actually works.

## Implementation perspective — "what do I actually copy and modify"

| Crystal | Copy as-is? | What needs modifying |
|---|---|---|
| [07-prompt-guardrails/](07-prompt-guardrails/) | Almost as-is (code) | The path examples in `settings.json`, the matcher names in the hooks |
| [01](01-definition-of-done.md), [02](02-directive-registry.md), [03](03-epistemic-immunity-catalog.md), [04](04-eval-engineering-methodology.md), [05](05-autonomous-agent-operating-principles.md), [06](06-self-improving-heuristics-loop.md) | Principle/methodology (document) | Adoptable as-is — the "why" is universal. Just fill in the real-examples section with your own project's cases over time |
| [08](08-module-format.md) | Convention (document) | Adjust only the extensions/paths to match the target project's executable file format |
| [09](09-project-structure-template.md) | Template (document + schema) | Fit the actual folder names to this project's naming conventions |

**Implementation order**: follow the same "minimum starting point" order
from the planning perspective. Don't install all 9 documents at once and
start from there — that itself becomes "infrastructure that's too early"
([09](09-project-structure-template.md) section 4, warning #13).

**Don't mark it complete without verification**: if you've only copied
something and never actually used it in the project, don't call it
"adopted" — for example, with [07-prompt-guardrails/](07-prompt-guardrails/),
a live check that the block actually works, via a real publish/commit
attempt, is part of installation.

## Improvement perspective — "how do you grow this to fit your own project"

Each crystal is designed as a **growing document, not a static template**:

- [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) and
  [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)
  explicitly instruct "grow this with cases discovered in your actual
  project" — don't leave only the abstract principles in place; add your
  own project's cases as soon as the first real failure/discovery happens
  after porting.
- [02-directive-registry.md](02-directive-registry.md) — just start
  filling it in from row 1 with the new project's actual directives.
- [07-prompt-guardrails/](07-prompt-guardrails/)'s `PATTERNS`/`check(...)`
  lists — add to them immediately whenever a sensitive-info pattern common
  to that project (an internal token format, etc.) is discovered.

**Also guard against bloat** — [02](02-directive-registry.md) and
[06](06-self-improving-heuristics-loop.md) each carry a "bloat prevention"
section and a "memory cap" section respectively. A document that only
grows and never gets pruned repeats the same cognitive-debt problem the
original project actually ran into.

## Reference perspective — "what should I look up quickly"

| Situation you're in right now | Crystal to check |
|---|---|
| "Is this task actually done?" | [01-definition-of-done.md](01-definition-of-done.md) |
| "Wasn't this principle already decided?" | [02-directive-registry.md](02-directive-registry.md) |
| "This claim seems too plausible — I'm suspicious" | [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) |
| "How do I verify the quality of this output?" | [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md) |
| "It feels wasteful to spend the same verification cost on every target" | [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)'s "scale verification strength to the target's risk level" |
| "Is it okay for this automated run to proceed without human confirmation?" | [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) |
| "An automated loop keeps stopping itself / how should I set the rescheduling interval?" | [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)'s "self-rescheduling backstop" / "automatic interval adjustment" |
| "A long-running agent seems to be drifting off goal, or keeps piling up ungrounded claims — I want to stop it in real time" | [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)'s "extending stop triggers to epistemic signals too" |
| "How do I make sure this failure doesn't happen again?" | [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) |
| "I want to stop secrets/personal data from leaking" | [07-prompt-guardrails/](07-prompt-guardrails/) |
| "I want to move this feature to another project" | [08-module-format.md](08-module-format.md) |
| "How do I structure the whole project?" | [09-project-structure-template.md](09-project-structure-template.md) |
| "Is there something this feature is missing from a user-experience standpoint?" | [10-human-ai-interaction-guidelines.md](10-human-ai-interaction-guidelines.md) |
| "Is there any real basis for trusting the AI's claim that it 'finished'?" | [11-observability-and-agent-tracing.md](11-observability-and-agent-tracing.md) |
| "How should I record this incident so it doesn't happen again?" | [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) |
| "How much debt has built up right now, and is it okay to ship this as a service?" | [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) |
| "If someone deliberately tried to attack this system, where would it break?" | [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) |
| "I want to document exactly what this AI feature does and doesn't do" | [15-model-card-template.md](15-model-card-template.md) |
| "I'm not sure what to put into the agent's context window" | [16-context-engineering-principles.md](16-context-engineering-principles.md) |
| "A shared document has crossed a size threshold — I want to first decide whether it's even a document that's safe to compress" | [16-context-engineering-principles.md](16-context-engineering-principles.md)'s "before compressing" |
| "I want to see at a glance which risk-management function our project is currently missing" | [17-ai-risk-management-index.md](17-ai-risk-management-index.md) |
| "Why did what just worked stop working now?" | [18-determinism-and-reproducibility.md](18-determinism-and-reproducibility.md) |
| "I want to deliberately break something before a real incident happens" | [19-chaos-engineering-for-agents.md](19-chaos-engineering-for-agents.md) |
| "Our team shares this AI agent — who's actually responsible for the output?" | [20-decision-rights-raci.md](20-decision-rights-raci.md) |
| "Does having the AI do the planning/design first actually work?" | [21-spec-first-implementation.md](21-spec-first-implementation.md) |
| "How much should I trust this benchmark number?" | [22-llm-benchmark-literacy.md](22-llm-benchmark-literacy.md) |
| "There's no personal-data pattern here, but this whole project/folder still shouldn't be published" | [23-confidential-project-protection.md](23-confidential-project-protection.md) |
| "Research ideas keep piling up but never actually get applied" | [24-application-deadline-rule.md](24-application-deadline-rule.md) |
| "Is it okay for the AI to edit the directive documents themselves? How far can it go?" | [25-directive-editing-delegation-levels.md](25-directive-editing-delegation-levels.md) |
| "I want to check whether the grounding of a guide document written a while ago still holds up" | [26-grounding-validity-audit.md](26-grounding-validity-audit.md) |
| "Before executing this plan, I want to spot, without optimism, what could go wrong" | [27-premortem-planning.md](27-premortem-planning.md) |
| "This output is factually correct but boring to read — it smells like AI" | [28-writing-craft-guardrails.md](28-writing-craft-guardrails.md) |
| "Token/API costs suddenly spiked — how should I handle a rate-limit error?" | [29-agent-cost-and-budget-management.md](29-agent-cost-and-budget-management.md) |
| "A shared context file keeps growing, and I'm worried compressing it will leave the next session unable to keep up" | [30-shared-context-lifecycle-management.md](30-shared-context-lifecycle-management.md) |
| "A new session started with 'continue from where we left off' but can't keep up with the previous session's level" | [30-shared-context-lifecycle-management.md](30-shared-context-lifecycle-management.md)'s "fixed bootstrap order at session start" |
| "It looks like an eval test left fake records in an actual user-history file" | [31-synthetic-data-memory-isolation.md](31-synthetic-data-memory-isolation.md) |
| "No single field trips the personal-data scanner, but the document as a whole seems like it could narrow down to a specific individual" | [32-quasi-identifier-aggregation-risk.md](32-quasi-identifier-aggregation-risk.md) |
| "This execution environment blocks local imports, so I have to copy the same logic into multiple files, and I'm worried about drift" | [33-sandboxed-harness-duplication-sync.md](33-sandboxed-harness-duplication-sync.md) |
| "I'm about to open-source a personal project and I'm worried my employer's confidential information is mixed in" | [35-personal-oss-employer-confidentiality-separation.md](35-personal-oss-employer-confidentiality-separation.md) |
| "How do I honestly report the results of an ad-hoc experiment that has no predefined test case?" | [34-self-experiment-reporting-standard.md](34-self-experiment-reporting-standard.md) |
| "I'm deciding, by gut feel every time, whether to do this task alone and sequentially or escalate it to parallelization/separate execution" | [36-execution-mode-escalation-ladder.md](36-execution-mode-escalation-ladder.md) |
| "If I optimize this goal/completion-criterion exactly as written, I suspect it'll get gamed into hitting the metric instead of the real outcome" | [37-target-metric-gaming-safeguards.md](37-target-metric-gaming-safeguards.md) |
| "I want to add a new crystal but don't know the criteria / how do I reflect another project's evolution into this folder?" | [BLUEPRINT.md](BLUEPRINT.md) |

## Related documents

- [GETTING-STARTED.md](GETTING-STARTED.md) — the step-by-step procedure to
  follow from step 1 when first adopting this
- [README.md](README.md) — overview of this whole folder
- [RISK-ANALYSIS.md](../ko/RISK-ANALYSIS.md) — risk analysis for open-source
  release
