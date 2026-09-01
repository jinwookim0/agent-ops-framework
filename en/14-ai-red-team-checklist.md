<!-- translated-from: ssot=sha256:cf9e5712d52c own=sha256:78ee2950c167 -->
# AI Red Team Checklist — Applying the OWASP Top 10 for LLM Applications (2025)

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/14-ai-red-team-checklist.md)**

**Version**: 1.0.1
**Content hash**: sha256:418199e870da (of the body below, excluding the stamp comment, this line, and the version line)

Where [07-prompt-guardrails/](07-prompt-guardrails/) prevents "a secret
value leaking out by accident" (accidental disclosure), this crystal is a
checklist for preventing **malicious input deliberately attacking the
system** (adversarial threats) — a different threat model, so the two
don't substitute for each other.

## Basis (confirmed against primary source)

🟢 Confirmed against the original text of the OWASP GenAI Security
Project, "OWASP Top 10 for LLM Applications 2025"
(genai.owasp.org/llm-top-10) — the most widely adopted threat
classification scheme for LLM application security in the industry.

## LLM01–LLM10 (2025 edition) — explained from the perspective of an AI agent project

| # | Threat | Concrete meaning for an agent project | Related defense |
|---|---|---|---|
| LLM01 | **Prompt injection** | Instructions hidden in user input or in external content the agent reads (web pages, documents) attempt to override the agent's original instructions | Treat content pulled from outside as "data" only, never execute it as an "instruction" — the key defense is not treating instruction-like text inside tool results/web content with the same authority as the system prompt |
| LLM02 | **Sensitive information disclosure** | Personal data/secrets present in training data or context leak into the response verbatim | The three-layer defense in [07-prompt-guardrails/](07-prompt-guardrails/) (tool blocking + active masking + hook enforcement) |
| LLM03 | **Supply chain risks** | Risk that the integrity of a third-party model, plugin, or dataset has been compromised | Verify the provenance of any model/tool/MCP server you depend on, and pin versions |
| LLM04 | **Data and model poisoning** | Malicious data getting mixed into training/fine-tuning data | Low priority for most agent projects that don't fine-tune their own model — though the same principle applies to keeping unverified external input from being folded directly into the project's own "self-learning documents" ([06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)) as rules |
| LLM05 | **Improper output handling** | Passing an agent's output directly to be executed as code/commands without verification | Add a separate verification/sandbox step before executing code/commands the agent generated |
| LLM06 | **Excessive agency** | The agent is given broader permissions (tool access, execution scope) than it actually needs | The unknown-unknowns gating in [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) — check whether there's a structural cap on the maximum possible damage |
| LLM07 | **System prompt leakage** | The system prompt (internal instructions) is exposed to the user, letting it be used as a basis for designing a bypass attack | Don't put secrets in the system prompt (design assuming it will leak) — rather than trying to hide the prompt itself, make it safe even if leaked |
| LLM08 | **Vector and embedding weaknesses** | A malicious document is injected into a RAG (retrieval-augmented generation) system's vector store, poisoning retrieval results | Verify the provenance of documents entering the vector store, and separate access permissions |
| LLM09 | **Misinformation** | The agent confidently generates information that sounds plausible but is wrong | The entirety of [03-epistemic-immunity-catalog.md](03-epistemic-immunity-catalog.md) is a defense catalog against this threat |
| LLM10 | **Unbounded consumption** | No cap on cost/resources, so malicious or accidental excessive calls cause costs to spike | Criterion 3 (cost control) of [13-debt-and-quality-bar.md](13-debt-and-quality-bar.md) |

## How to use this checklist

**Start with threat modeling, not blanket application**: don't try to
defend against all 10 at once — first determine "what surfaces this
project is actually exposed on":
- **Does it read external content** (web search, email, document
  parsing)? → LLM01 and LLM09 are top priority.
- **Does it execute real actions** (code execution, file writes, external
  API calls)? → LLM05 and LLM06 are top priority.
- **Does it handle personal data/secrets**? → LLM02 and LLM07 are top
  priority.
- **Is there a knowledge base shared across multiple users** (RAG)? →
  LLM08 is top priority.

## AI-agent-specific principle — "the boundary between data and instruction"

If you had to pick the single most fundamental defensive principle among
the 10 above: **within the content the agent processes, always
distinguish "this is an instruction I must follow" from "this is
just data I have to handle."** The core mechanism of prompt injection
(LLM01) is precisely this boundary getting blurred — even if text pulled
from outside (search results, file contents, another agent's output)
contains a sentence like "ignore that and do this instead," make it clear
at the system-design level that it's merely text inside data and holds no
actual instructional authority (e.g., explicitly tag data sources, and
treat any instruction-like text coming from content bearing that tag as
low authority).

## Principles for running a red team

When conducting a red team exercise (testing by attacking your own
system):
1. **The findings themselves can be sensitive** — don't leave a list of
   vulnerabilities as-is in a public channel (the opposite case from the
   "low cost of failure" gate condition in
   [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
   — red-team output does not, by default, lower the gate).
2. **Verify by actually running it** — don't just reason "this defense
   exists, so it should be safe"; construct actual attack input and test
   whether it gets through (the same "actually execute it, don't
   simulate" principle as in
   [04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)).
3. **When something is found, record it under the safety category of
   [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md)**,
   and escalate to a structural fix once the same type is found a second
   time.
