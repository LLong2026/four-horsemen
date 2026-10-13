# Day Receipts — October 13, 2026 (working record, per Leon 11:14 CT)

> Transparency working record for the day. Zenodo uploads deferred to tonight
> (deposit API outage since ~10:50 CT); everything below is committed, hashed,
> and ledgered locally. Two-key gates noted per item.

## Receipts produced today

| # | Receipt | Evidence | Status |
|---|---|---|---|
| 1 | SBR-2 hot-state adversarial exam — mesh holds every invariant WHILE learning; trajectory byte-identical to clean under 20 mid-epoch probes | DOI 10.5281/zenodo.23345734 | Published |
| 2 | H-INV-2 lineage forgery battery — 48/48 forgeries rejected and journaled, 106/106 real crossings preserved; 2-round validator repair disclosed | DOI 10.5281/zenodo.23345859 | Published |
| 3 | DPP-1 data-plane poisoning — 67/67 poisoned instances zero decision effect, 7/7 canaries absent at ingestion | DOI 10.5281/zenodo.23345907 | Published |
| 4 | CCR-4X Copilot repair leg — honest tally closed with preregistered repair | DOI 10.5281/zenodo.23346047 | Published |
| 5 | Corpus round-trip re-verification — 5 records byte-identical to live Zenodo | ledger 0059 | Verified |
| 6 | LINDY-B 60-day sustained battery STARTED — prereg, runner, workflow (03:30 CT nightly), run 1/60 PASS (baseline ca575bb9) | ledger 0060, commit bc253e8 | Running |
| 7 | Adversarial Triad umbrella paper — SBR-2 + H-INV-2 + DPP-1 as one three-surface record | commit e1bf86f, bundle ready | Leon GO 10:50 CT — queued (Zenodo outage) |
| 8 | DPP-2 homoglyph & multilingual battery — 33/33 lookalikes rejected from roster, 66/66 canaries absent, unicode-nullity control PASS; prereg defect disclosed and repaired same-session | ledger 0061, commit 9202417 | Leon GO 11:11 CT — queued (Zenodo outage) |
| 9 | DPP-3 normalization & bidi forgery battery — 50/50 visual twins rejected, byte-exactness frozen with regression tripwire (NFKC/case-fold/trim patches each flip FAIL by construction) | ledger 0062 | Gabriel vet done — Leon GO pending |
| 10 | DPP-4 structural & numeric forgery battery — FIRST FALSIFIER FAILURE of the series, shipped as found: type-forged numbers crash the gate (fail-closed); infinity-forged metrics corrupt the shared weight to -inf (boundedness defeated by non-finite input); dup/missing ids silently consumed. SIP filed for ingestion guard; candidate leg closes all three gaps with conforming behavior byte-identical | ledger 0063/0064, guard deployed (ingestionGuard v1.1) | Leon GO 11:22 CT (papers + SIP) — staged |

## Adversarial surface coverage after today

1. Learning process (SBR-2) — held while learning
2. Audit ledger (H-INV-2) — cannot be forged
3. Data plane, ASCII poison (DPP-1) — poison-proof
4. Data plane, homoglyph/multilingual (DPP-2) — lookalikes rejected
5. Data plane, normalization/bidi (DPP-3) — byte-exact, tripwire armed
6. Data plane, structure/numerics (DPP-4) — three real gaps found (crash-on-type, inf-weight-corruption, id-integrity), SIP filed — OPEN, no runtime patch
6. Authority channel (AUTH-1) — 6/6 forgeries rejected, live-ACK contrast
7. Engine substrate (CCR series, 8 engines) — contract parity, honest failures
   published
8. Time axis (LINDY-B) — 60-night conformance watch, running

## Open gates tonight
- Zenodo publish: triad paper + DPP-2 + DPP-3 + DPP-4 — Leon GO 11:22 CT ("GO on the papers"); retry worker 12:45 CT publishes all four in order when the deposit API recovers, stray-draft cleanup + no-duplicate guards built in
- DPP-4 SIP: APPROVED and DEPLOYED (ingestion guard v1.1 live on the runtime path; instruments frozen; LINDY-B unaffected)

## Known residuals (honest)

- Font-level spoofing and ligature attacks: out of scope of DPP-3, untested.
- Human-reader bidi spoofing in dashboards: real residual risk, machine gate
  unaffected — noted in the DPP-3 receipt headline.
- Zenodo deposit API outage (~10:50 CT onward): triad paper + DPP-2 queued; one
  auto-retry worker armed (12:45 CT) with stray-draft cleanup and no-duplicate
  guards.

> This software is a prototype and is provided for educational and research
> purposes only. All data is synthetic.
