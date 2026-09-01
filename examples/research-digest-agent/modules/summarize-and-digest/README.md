# summarize-and-digest (module)

Portable paper-filtering/summarization/grounding-audit functions, exported
from the [research-digest-agent](../../) demo per
[08-module-format.md](../../../../ko/08-module-format.md).

## Install

Copy `digest_core.py` into your project. That's the whole install — no
configuration, no other files required.

```python
from digest_core import matches_interest, detect_injection, summarize, audit_grounding, is_duplicate

relevant, matched_keywords = matches_interest(paper, ["your", "keywords", "here"])
```

## Verify it works in your environment

```bash
python3 digest_core.py
```
Should print a relevance verdict, a summary, and a grounding check for
one built-in demo paper, ending with a line confirming no shared-context
file was read. If this doesn't run standalone in your environment, don't
trust the rest of the module until you find out why (per this whole
framework's "verify live, not by claim" principle,
[03-epistemic-immunity-catalog.md](../../../../ko/03-epistemic-immunity-catalog.md)
item 8).

See `MODULE.md` for the full manifest (dependencies, verification status,
what degrades gracefully vs. what simply isn't included).
