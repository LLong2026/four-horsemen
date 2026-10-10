# PENTA-CL audited interim results, October 10, 2026

Four platform-configured engine pairs recorded, two canonical-target passes, two failures. DeepSeek pending. This is not completed PENTA certification or a stress/load test.

Read [the report](PENTA_CL_INTERIM_REPORT.md), [the PDF](PENTA_CL_INTERIM_REPORT.pdf), and [the machine-readable receipt](PENTA_CL_INTERIM_RECEIPT.json). [The archive](PENTA_CL_EVIDENCE.zip) preserves the frozen prompt, rendered captures, setup receipts, offline verifier and excluded attempts. [Manifest](SHA256_MANIFEST.json).

Zenodo DOI: https://doi.org/10.5281/zenodo.23286324
DCAI: https://zenodo.org/communities/dcai

Run `python3 evidence/verify_fresh_legs.py`. Exit status 1 is expected: Luna and GLM fail the registered canonical target. Files in `evidence/excluded_attempts/` are historical non-qualifying attempts with superseded success claims, not qualifying engine evidence.

This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.
