# M2 citation-detector Stage-A metrics

Detection is scored separately from parsing: find USC/CFR citation spans inside free
prose (`detect_mentions`), and do **not** fire on citation-shaped noise. The gold set
is hand-curated — realistic legal sentences plus adversarial distractors (dates,
dollar amounts, `Rule 12(b)(6)`, Public Law / Fed. Reg. numbers, version strings,
phone numbers) whose expected result is empty. A detection matches a gold citation on
its `(corpus, title, section)` identity. Gold labels are independent ground truth,
never derived from the detector's own output.

Gold set: **31 passages**, **31 citations**, **9 pure-distractor passages**.

| Corpus | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| USC | 20 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| CFR | 11 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| **all** | 31 | 0 | 0 | 1.000 | 1.000 | 1.000 |

## False positives (precision failures)

None — the detector fired on no distractor.

## False negatives (recall gaps)

None.

## Empirical baseline targets

Recorded after commissioning (not hardcoded legal rules): precision `>= 1.00`, recall `>= 0.98`. The
detector is deliberately precision-first — abstaining on ambiguous prose beats a
false citation edge. The free-text scan covers ABSOLUTE citations, including
enumerated `§§ a, b` lists (each member emitted, a following bare number that is
itself a new citation is not mis-attributed); the qualified prose form (`section
1983 of title 42`) and full corpus-scale in-body detection are deferred.

