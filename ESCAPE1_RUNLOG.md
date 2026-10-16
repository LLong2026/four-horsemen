| 2026-10-16 | MISSED (disclosed, run attempt 1) — instrument file unavailable: penta_v2 wiped by the git checkout incident (restored from clone, hash-verified). Re-run authorized. |
| 2026-10-16 | phaseA — FAIL — ESC-1:REJECTED, ESC-2:REJECTED, ESC-3:REJECTED, ESC-4:REJECTED, ESC-6:HELD/DETECTED, ESC-5:DETECTED |
MISSED (disclosed, run attempt 2) — runner-path scoring defect: verdict classifier ordered held-before-admitted, mislabeling ESC-6 positive control (adapter output was the exact frozen 8/2/2 tuple; cage verdict correct, scoring wrong). Runner v1.1 fix: ESC-6 scored against the frozen tuple. Amendment commit follows, then re-run.
| 2026-10-16 | phaseA — PASS — ESC-1:REJECTED, ESC-2:REJECTED, ESC-3:REJECTED, ESC-4:REJECTED, ESC-6:ADMITTED, ESC-5:DETECTED |
