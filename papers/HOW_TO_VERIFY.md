# HOW TO VERIFY — The Hash Is the Artifact (30 seconds, any browser)

1. Open the Genesis Viewer page on the Deterministic Coding public site (linked from the Squirl OS Vault Public Links page, https://squirl-vault-core.base44.app).
2. Paste this fingerprint into the HASH DROP:
   81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c
3. The artwork reconstructs in your browser. Press "Verify canonical artifact": your browser fetches the published PNG, hashes the raw bytes with SHA-256, and compares to the pinned digest 3c130d6626fb78956a35dd177a7be2bd34d80be66104d94dee37ce7d5bd2de69.
4. For byte-level reproduction from source: download the DOI bundle (10.5281/zenodo.23447609), run the pinned generator v1.1 on the included 32-byte seed with stock Python, and compare the output hash.
No account, no install, no trust in the authors required.
