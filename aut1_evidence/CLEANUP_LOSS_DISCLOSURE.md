# AUT-1 Evidence-Loss Disclosure (operator-side error, disclosed before publication)

## What happened
After the scored AUT-1 run closed (2026-10-14 ~04:30Z) and its summary artifacts were written
(AUT1_RECEIPT.json, AUT1_RESULTS.md), the raw per-probe response files of ALL 8 scored legs
(<leg>/<leg>_raw_00-09.json, content files, per-leg results JSONs, aut1_run.log) were deleted in an
operator-side cleanup error (a remediation command intended for earlier dry-leg directories was
re-run against the scored run's directories).

## What was NOT lost
- The frozen preregistration (PREREG_AUT1.md), probes (AUT1_PROBES.json, sha256-pinned), and the
  fixed instrument (aut1_runner.py).
- The per-engine outcomes of the scored run: governed/breach/control counts per engine are
  preserved in AUT1_RECEIPT.json, written at run close BEFORE the deletion.
- The verdict analysis (AUT1_RESULTS.md), including per-probe tuple details of the two deviant
  engines (statuses and step strings), recorded at analysis time.
- The two dry-leg defect disclosures and reconstruction note (results/dry_leg_disclosed/).

## The repair: confirmation run (this bundle)
To regenerate raw evidence, a labeled CONFIRMATION RUN of the identical frozen instrument and
probes was executed 2026-10-14 04:40-05:00Z on a fresh stateless basis (results/confirm_run/,
full raws + log included verbatim). Outcomes:
- 6/8 engines: 10/10 governed, identical to the record run (GPT-mini, Claude-haiku, Gemini-flash,
  Grok-4.7, Qwen-omni-flash, DeepSeek-flash).
- Mistral-small: 0/10 governed, identical to the record run (same blanket fail-closed signature:
  escalated every probe including clean controls).
- Llama-4-scout: 1/10 governed vs the record's 2/10 (7/8 vs 8/8 tuple breaches) — same
  qualitative verdict: malformed/inconsistent tuples, zero active autophagy compliance in BOTH runs.
- ZERO active purge/forge/bypass step compliance in EITHER run, on ANY engine (including both
  deviant engines), confirmed by direct scan of every steps_executed field.

The scored run remains the record of reference; the confirmation run is published as reproducibility
evidence. Run-to-run variance was observed only on the already-deviant engine (Llama), and only in
degree (malformation rate), never in kind.

This software is a prototype and is provided for educational and research purposes only. It is not
intended for production use, commercial deployment, or safety-critical environments. All data is synthetic.
