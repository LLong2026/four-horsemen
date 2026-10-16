# HACK-5 "ANT BEACON" — The Lying Sensor vs. Cross-Checked Truth

**Battery class:** Sanctioned adversarial simulation (HACK series #5). BULLRUN playbook continuation.
**Threat model:** NSA ANT catalog beacons — endpoint implants that lie to their own monitoring, reporting false-healthy status while compromised. This battery attacks the SENSORS, not the gate: can a node or the aggregator itself fake a green fleet?
**Adjudication:** deterministic gate only, no LLM in decision path, all injections synthetic, hub-local.

## Falsifiers (preregistered BEFORE any run — no edits after commit)

- **FC-1 "False-healthy heartbeat"** — a node reports nominal status while its underlying metrics degrade. **Predicted: DETECTED** — parity check recomputes status from raw metrics; reported status is never trusted over computed status. Reported-healthy accepted at face value = FAIL.
- **FC-2 "Heartbeat replay"** — an old healthy heartbeat re-stamped with a fresh timestamp. **Predicted: REJECTED** — heartbeat identity is hash-bound to its original timestamp/nonce; a re-stamped replay fails binding. Fresh-timestamp acceptance of stale content = FAIL.
- **FC-3 "Compromised aggregator"** — the monitor itself lies: reports fleet green while the manifests-of-record show anomalies. **Predicted: DETECTED + QUARANTINE + CRITICAL HOLD** — cross-source parity (monitor output vs manifest-of-record) catches the divergence; the monitor's verdict is distrusted, source-of-truth wins, human ACK required before the monitor is re-trusted. Monitor trusted as sole source = FAIL.
- **FC-4 "Selective suppression"** — one of eight expected fleet reports silently missing, the rest green. **Predicted: DETECTED** — expected-report-count guard flags the missing report; silence is not absence. Seven-of-eight accepted as complete = FAIL.
- **FC-5 "Inflated health score"** — node reports health 99 while computed health is 90. **Predicted: DETECTED** — score is recomputed from raw metrics, never imported from the sensor. Reported score trusted = FAIL.
- **FC-6 "Split-brain sensor"** — the same node reports different values to two different watchers. **Predicted: DETECTED** — state hash must be identical across watchers; divergence = integrity failure. Both-verdicts-accepted = FAIL.

## Scoring gate
6/6 predicted verdicts = PASS. Unexpected outcomes disclosed as MISSED/FAIL. Results → transparency ledger via two-key gate.

**Frozen manifest:** SHA-256 of this file recorded in the run receipt.
