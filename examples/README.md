# Worked examples

Two small, runnable demo agents built to show what actually applying
this framework's crystals looks like — structurally, in real code — not
just described in prose. No API key needed for either.

| Example | Shape | Crystals covered | Start here |
|---|---|---|---|
| [`issue-triage-agent/`](issue-triage-agent/) | Reactive, per-item classifier | 15 (governance/quality/safety fundamentals) | [`CASE-STUDY.md`](issue-triage-agent/CASE-STUDY.md) |
| [`research-digest-agent/`](research-digest-agent/) | Autonomous, recurring, self-improving loop | 12 more (2 deepened, 10 new — planning, chaos/red-team, context lifecycle, module packaging) | [`CASE-STUDY.md`](research-digest-agent/CASE-STUDY.md) |

Together they cover 25 of this framework's 37 crystals with real,
checkable code — each `CASE-STUDY.md` names its own honest remainder
rather than claiming full coverage.

Read `issue-triage-agent` first if you're new here — it's the simpler
shape. `research-digest-agent` is the complementary half, deliberately
covering what the first structurally can't (an agent that runs once per
item vs. one that runs repeatedly over time and has to remember what it
learned).
