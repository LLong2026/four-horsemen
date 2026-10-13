# DHB-3 PREREGISTRATION — The Convergence Battery (Keys + Commit, Both Planes, Simultaneously)

Series: DHB-3 (dual-hemispheric standing format) | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 12:26 CT) —
the convergence battery directive. Operator wording not quoted per the standing
privacy rule; the GO + timestamp is the audit record.

## Purpose

Every rung below keys+commit has been measured and closed across the series.
DHB-3 runs the MAXIMAL attacker on BOTH hemispheres simultaneously: the
signing key (.gov_release_key) AND the issuance key (.issuance_key) AND git
commit access — governance release forgery (relaxed roster, re-signed,
committed) AND issuance forgery (minted id block, re-signed, committed) at
the same time, against the full deployed stack (guard v2.3, SIP-4 signed
releases from the git anchor, SIP-3 reconciliation, SIP-6 signed issuance).

## The question, and the one number

With both keys and commit access, how many software layers resist? And what
remains after that? The battery prices the final floor as ONE NUMBER: the
count of external append-only surfaces, not controlled by the attacker, that
must ALSO fall for the forgery to be undetectable in retrospect. Every layer's
behavior is MEASURED, not asserted.

## Frozen falsifiers (Run A — maximal two-floor attacker)

- **FD-1 (governance plane):** the in-process release verification
  (git-anchored, key-pinned, signature-checked) PREDICTED to ACCEPT the
  forged relaxed roster (thresholds 0.80 -> 0.10): the attacker re-signs with
  the stolen key and commits the registry. FAIL AS FOUND expected.
- **FD-2 (data plane):** the ingestion guard PREDICTED to ACCEPT all minted
  records (40 new ids added to a re-signed issuance block). FAIL AS FOUND
  expected.
- **FD-3 (measured damage):** heal volume and weight trajectory under the
  forged relaxed roster + minted traffic — whatever the numbers are, they
  ship, including boundedness under the clamp.
- **FD-4 (external anchors — the one number):** after the forgery, count the
  detection surfaces that do NOT depend on anything the attacker controls:
  (a) in-run verification: defeated (FD-1); (b) git history: change visible
  (attribution only, and the attacker can forge ledger entries with commit
  access too); (c) DOI-bound records on Zenodo: checked for anchor-fingerprint
  coverage — PREDICTED NOT COVERED (the registries/key pins were never
  DOI-bound). The one number: the count of attacker-independent immutable
  surfaces, and whether they currently see the forgery.
- **FD-5 (fail-safe residual):** the final residual is human review over
  append-only history — verify the forensics are AT LEAST possible (the
  forgery is attributable from history).
- **FD-6 (hygiene):** synthetic only; no operator text; prototype disclaimer.

Any failure ships as found. The predicted result: the LOCAL stack is fully
subverted (that is GOV-3's floor, now measured on both planes at once), and
the one number is whatever the external-anchor audit actually finds.

## Scope honesty (frozen)

The attack executes in an ISOLATED CLONE of the repository — the attacker's
commits land in the clone's history, modeling full commit access without
corrupting the production anchors. The external-anchor check compares the
attacker state against the production state and the DOI-bound corpus. This
isolation is disclosed; it models, not performs, the corruption. The damage
numbers under the forged roster are upper bounds on a real attack's speed,
not a production prediction.
