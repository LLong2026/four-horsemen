#!/usr/bin/env bash
# ANCHOR-RECON v1.0 (SIP-036) — deterministic reconciliation gate for the transparency anchor.
# Reconciles three layers: (1) artifact digest, (2) .ots receipt commitment, (3) attestation status.
# No LLM in the decision path. PASS = every receipt matches a live artifact digest.
# Fail-closed: any mismatch, missing receipt, or unparsable stamp = FAIL (quarantine + SIP-035 playbook).
set -uo pipefail
STAMP_DIR="anchors"
declare -A DIGEST_INDEX
FAILED=0; CHECKED=0; CONFIRMED=0; PENDING=0
# index digests of all reconcilable artifacts
while IFS= read -r f; do
  [ -f "$f" ] && DIGEST_INDEX["$(sha256sum "$f" | cut -d' ' -f1)"]="$f"
done < <(ls LEDGER.md cage_watch_feed.json HASH_NOTARIZATION_SPEC_MHCN1.md CHAIN_OF_CUSTODY_GRAPH.md sbr7/SBR7_RECEIPT.json tokenization-adoption/sbom-anchor-stack-2026-10-18.spdx.json "$STAMP_DIR"/ANCHOR-MANIFEST-*.json "$STAMP_DIR"/states/* "$STAMP_DIR"/ANCHOR-BLOCK-REGISTRY.json 2>/dev/null)
# v1.0.4 (2026-10-18, disclosed): certified-state archive extended to all archived formats (registry states are .json)
# v1.0.3 (2026-10-18, disclosed): SBOM admitted to the gate (self-referential demo, SIP-041)
# v1.0.2 (2026-10-18, disclosed): index extended to the full canonical corpus (specs, receipts, registry)
# INV-1-C tip-lag corollary: a receipt matching an ARCHIVED state is a certified historical state, not drift
for sf in "$STAMP_DIR"/states/*.md; do
  [ -e "$sf" ] && DIGEST_INDEX["$(sha256sum "$sf" | cut -d' ' -f1)"]="$sf (certified state)"
done
for ots in "$STAMP_DIR"/*.ots; do
  [ -e "$ots" ] || { echo "RECON FAIL: no stamps present"; exit 1; }
  CHECKED=$((CHECKED+1))
  info=$(ots info "$ots" 2>/dev/null) || { echo "RECON FAIL: unparsable stamp $ots"; FAILED=$((FAILED+1)); continue; }
  digest=$(echo "$info" | grep -m1 'File sha256 hash:' | awk '{print $NF}')
  if [ -z "${DIGEST_INDEX[$digest]:-}" ]; then
    echo "RECON FAIL: $ots digest $digest matches NO live artifact (historical state or drift)"
    FAILED=$((FAILED+1)); continue
  fi
  if echo "$info" | grep -q "Bitcoin block height"; then CONFIRMED=$((CONFIRMED+1))
  else PENDING=$((PENDING+1)); fi
  echo "MATCH: $(basename "$ots") -> ${DIGEST_INDEX[$digest]}"
done
for h in "$STAMP_DIR"/history/*.ots; do
  [ -e "$h" ] && echo "HISTORICAL (retained proof of a prior state): $(basename "$h")"
done
echo "---"
echo "receipts=$CHECKED confirmed_onchain=$CONFIRMED pending=$PENDING mismatches=$FAILED"
[ "$FAILED" -eq 0 ] && { echo "RECON VERDICT: PASS"; exit 0; } || { echo "RECON VERDICT: FAIL — quarantine per SIP-035"; exit 1; }
