# M2 citation-detector Stage-A metrics

Detection is scored separately from parsing: find USC/CFR citation spans inside free
prose (`detect_mentions`), and do **not** fire on citation-shaped noise. The gold set
is hand-curated — realistic legal sentences plus adversarial distractors (dates,
dollar amounts, `Rule 12(b)(6)`, Public Law / Fed. Reg. numbers, version strings,
phone numbers) whose expected result is empty. A detection matches a gold citation on
its `(corpus, title, section)` identity. Gold labels are independent ground truth,
never derived from the detector's own output.

Gold set: **28 passages**, **23 citations**, **9 pure-distractor passages**.

| Corpus | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| USC | 13 | 0 | 1 | 1.000 | 0.929 | 0.963 |
| CFR | 9 | 0 | 0 | 1.000 | 1.000 | 1.000 |
| **all** | 22 | 0 | 1 | 1.000 | 0.957 | 0.978 |

## False positives (precision failures)

None — the detector fired on no distractor.

## False negatives (recall gaps)

- `usc 42 1985` missed in: 'Brought under 42 U.S.C. §§ 1983, 1985 jointly.'

The remaining gap is the 2nd+ section of an enumerated `§§ a, b` list — a known,
deferred detection feature (each list member is a distinct citation).

## Empirical baseline targets

Recorded after commissioning (not hardcoded legal rules): precision `>= 1.00`, recall `>= 0.95`. The
detector is deliberately precision-first — abstaining on ambiguous prose beats a
false citation edge. The free-text scan covers ABSOLUTE forms only; the qualified
prose form (`section 1983 of title 42`) and enumerated `§§` lists are deferred.

