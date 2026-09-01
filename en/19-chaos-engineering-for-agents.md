<!-- translated-from: ssot=sha256:1c950bfcdc25 own=sha256:b98f3047a9a7 -->
# Chaos Engineering for Agents — Deliberately Breaking Things Before an Incident Does

> 🌐 **[한국어 원본 보기 (SSOT)](../ko/19-chaos-engineering-for-agents.md)**

**Version**: 1.0.2
**Content hash**: sha256:47e833e89be5 (of the body below, excluding the stamp comment, this line, and the version line)

Where [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) covers
**malicious attacks** (someone deliberately trying to trick the
system), this crystal addresses a different threat model —
**environmental failures that nobody intended but that actually
occur** (tool timeouts, API outages, budget exhaustion, malformed
responses) — by deliberately experimenting against them before an
incident happens, to see whether the system holds up.

## Basis (primary source verified)

🟢 Verified against the original at ["Principles of Chaos
Engineering"](https://principlesofchaos.org/) — Netflix pioneered this field, and the site itself is a community document that captures the industry-wide consensus formed since then. Quoting the definition verbatim:
**"Chaos Engineering is the discipline of experimenting on a system in
order to build confidence in the system's capability to withstand
turbulent conditions in production."**

## The 5 principles (verified against the original, applied to AI agents)

### 1. First form a hypothesis about steady state
Define "the system is working normally" in terms of **measurable
output** (throughput, error rate, response latency) rather than
internal mechanics. Applied to AI agents: first set a concrete baseline
such as "this feature normally completes successfully 95% of the time
or more" — connects to the quality baseline in
[13-debt-and-quality-bar.md](13-debt-and-quality-bar.md).

### 2. Inject a variety of real-world events
Prioritize by impact and frequency, and inject disruptions that could
realistically occur — hardware failure, software malfunction, traffic
spikes. Applied to AI agents:
- What happens if a tool call times out?
- What happens if an external API returns a malformed response?
- What happens if the search budget suddenly drops to zero?
- If one branch of a parallel execution returns null, does that
  propagate to the rest?
  ([06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md)'s
  "hidden crash points from null propagation" item is exactly the same
  category of thing discovered through a chaos experiment like this)

### 3. Experiment in production
Experiment against the actually deployed system with real traffic,
rather than a controlled test environment — "because system behavior
varies with environment and traffic patterns." Applied to AI agents:
don't test only with mocked tool responses; run failure scenarios
against the real external API/tool (with the "risk controls" section
below being mandatory).

### 4. Automate experiments to run continuously
Replace manual testing with automated, continuous verification.
Registering "deliberate failure injection" cases alongside standard
cases in the evaluation pipeline of
[04-eval-engineering-methodology.md](04-eval-engineering-methodology.md)
lets you implement this principle in a reusable form.

### 5. Minimize blast radius
Ensure the fallout of an experiment is minimized and contained — some
short-term loss is acceptable, but customer impact must be limited.
Applied to AI agents: this connects directly to the unknown-unknowns
gating in
[05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md)
(only allow actions with a structural upper bound as experiment
targets) — don't run chaos experiments by actually executing
irreversible real-world actions (payments, sending messages).

## How this crystal differs from #14 (red team) and #12 (postmortem)

| | Nature of the threat/event | Timing |
|---|---|---|
| [14-ai-red-team-checklist.md](14-ai-red-team-checklist.md) | Malicious (someone deliberately attacking) | Proactive defensive design |
| **This crystal (19)** | Accidental/environmental (nobody intended it) | **Deliberately reproduced and experimented with in advance** |
| [12-blameless-postmortem-template.md](12-blameless-postmortem-template.md) | Anything (malicious or accidental) | **After the fact** (once it has already happened) |

All three crystals cover the same subject — "the ways a system fails" —
but look at different axes (threat model, timing). Merging them into
one would erase a distinction needed when diagnosing "why did it fail."

## Risk controls — AI-agent-specific cautions

Applying chaos engineering to AI agents requires more caution than
general software:
- **Never run an experiment that actually triggers an irreversible
  action** — for example, don't send a real mass email just to
  experiment with "how the actual email-sending feature behaves under
  failure conditions." Substitute a mock, or reproduce only up to the
  step just before sending.
- **Isolate experiment results so they never leak into user-visible
  output** — keep a dedicated experiment channel separate so that a
  deliberately injected failure never ends up contaminating an actual
  deliverable (a report, a publication).

## Related crystals
- [05-autonomous-agent-operating-principles.md](05-autonomous-agent-operating-principles.md) —
  The gating condition "does the blast radius have a structural upper
  bound?" connects directly to this crystal's "risk controls" section.
- [06-self-improving-heuristics-loop.md](06-self-improving-heuristics-loop.md) —
  The path by which a defect actually discovered through a chaos
  experiment is folded back into this loop as a new rule.
