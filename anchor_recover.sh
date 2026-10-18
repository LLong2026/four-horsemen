#!/usr/bin/env bash
# ANCHOR-RECOVER v1.0 (SIP-035) — deterministic re-anchor runner for the transparency corpus.
# Doctrine: chain blocks are UNREPAIRABLE by design. "Repair" = re-anchor the drifted artifact:
# seal the new state with a fresh OpenTimestamps stamp. Old stamps remain historical proof.
# Usage: ./anchor_recover.sh [artifact ...]   (no args = re-anchor the full corpus set)
set -euo pipefail
CALS=(-c https://alice.btc.calendar.opentimestamps.org -c https://bob.btc.calendar.opentimestamps.org)
STAMP_DIR="anchors"
TS=$(date -u +%Y-%m-%dT%H%MZ)
DEFAULTS=("LEDGER.md" "cage_watch_feed.json")
TARGETS=("${@:-${DEFAULTS[@]}}")
mkdir -p "$STAMP_DIR"
MANIFEST="$STAMP_DIR/ANCHOR-MANIFEST-$TS.json"
echo "{\"anchor_date_utc\": \"$TS\", \"purpose\": \"SIP-035 re-anchor (drift or recovery)\", \"files\": {" > "$MANIFEST.tmp"
for f in "${TARGETS[@]}"; do
  [ -f "$f" ] || { echo "MISSING: $f"; exit 1; }
  sha=$(sha256sum "$f" | cut -d' ' -f1)
  ots stamp "${CALS[@]}" "$f"
  mv "$f.ots" "$STAMP_DIR/OTS-$TS-$(basename "$f").ots"
  echo "RE-ANCHORED: $f sha256 $sha"
  echo "  \"$f\": \"$sha\"," >> "$MANIFEST.tmp"
done
sed -i '$ s/,$//' "$MANIFEST.tmp"; echo "}}" >> "$MANIFEST.tmp"; mv "$MANIFEST.tmp" "$MANIFEST"
echo "Manifest: $MANIFEST — commit both artifact state and stamp, append ledger entry."
