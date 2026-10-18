#!/usr/bin/env bash
# EXAMINER MODE v1.0 (SIP-039) — one-command, zero-trust evidence file for auditors.
# Compiles the full verification state of the anchored corpus into a single evidence
# file an examiner can re-produce independently. Deterministic; no LLM in any verdict.
set -uo pipefail
OUT="EXAMINER-EVIDENCE-$(date -u +%Y%m%dT%H%M%SZ).md"
{
echo "# SQUIRL OS Examiner Evidence File"
echo "**Generated (UTC):** $(date -u +%Y-%m-%dT%H:%M:%SZ)  |  **Mode:** zero-trust examiner (SIP-039)"
echo
echo "## Corpus inventory (anchored receipts)"
for f in anchors/*.ots; do
  INFO=$(ots info "$f" 2>/dev/null)
  DIG=$(echo "$INFO" | grep -o "[a-f0-9]\{64\}" | head -1)
  HT=$(echo "$INFO" | grep -o "Bitcoin block height.*" | head -1)
  if [ -n "$HT" ]; then ST="CONFIRMED_ONCHAIN ($HT)"; else ST="pending calendar confirmation"; fi
  echo "- $(basename "$f"): digest ${DIG:0:16}... — $ST"
done
echo
echo "## Reconciliation gate verdict (MHCN-1 R3)"
./anchor_recon.sh 2>&1 | grep -E "RECON VERDICT|receipts=|mismatches" || echo "gate did not run"
echo
echo "## Block registry"
python3 -c "import json;r=json.load(open('anchors/ANCHOR-BLOCK-REGISTRY.json'));print('receipts tracked:',len(r['receipts']));print('confirmed:',sum(1 for e in r['receipts'].values() if e.get('status')=='confirmed_onchain'),'pending:',sum(1 for e in r['receipts'].values() if e.get('status')=='pending'))"
echo
echo "## Independent verification (trusts no third party)"
echo '1. pip install opentimestamps-client'
echo '2. ots upgrade <receipt>.ots   (fetches the confirmed Bitcoin attestation)'
echo '3. ots verify <receipt>.ots    (against a Bitcoin full node)'
echo
echo "## Disclosures (load-bearing)"
echo "- Pending receipts confirm on Bitcoin within hours of stamping; pending is never reported as settled."
echo "- Anchoring notarizes EXISTENCE. Authority is retained in the separate PQC layer (MHCN-1 R5);"
echo "  the reference chain's signatures are not post-quantum."
echo "- Prototype software, educational/research purposes only; no production warranty."
} > "$OUT"
echo "EXAMINER EVIDENCE FILE: $OUT"
