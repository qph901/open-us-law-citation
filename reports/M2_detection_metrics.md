# M2 citation-detector Stage-A metrics

Detection is scored separately from parsing: find USC/CFR citation spans inside free
prose (`detect_mentions`), and do **not** fire on citation-shaped noise. The gold set
is hand-curated — realistic legal sentences plus adversarial distractors (dates,
dollar amounts, `Rule 12(b)(6)`, Public Law / Fed. Reg. numbers, version strings,
phone numbers) whose expected result is empty. A detection matches a gold citation on
its `(corpus, title, section)` identity. Gold labels are independent ground truth,
never derived from the detector's own output.

Gold set: **36 passages**, **34 citations**, **11 pure-distractor passages**.

| Corpus | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| USC | 22 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| CFR | 12 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| **all** | 34 | 0 | 0 | 1.000 | 1.000 | 1.000 |

## False positives (precision failures)

None — the detector fired on no distractor.

## False negatives (recall gaps)

None.

## Empirical baseline targets

Recorded after commissioning (not hardcoded legal rules): precision `>= 1.00`, recall `>= 0.98`. The
detector is deliberately precision-first — abstaining on ambiguous prose beats a
false citation edge. The free-text scan covers ABSOLUTE citations, enumerated
`§§ a, b` lists (each member emitted; a following bare number that is itself a new
citation is not mis-attributed), and the qualified prose form (`section 1983 of
title 42, United States Code`) — which fires only when the spelled-out code name is
present, so `section 5 of title I of the Act` never does. Full corpus-scale in-body
detection (over the `text` column) is deferred — it overlaps M4.

