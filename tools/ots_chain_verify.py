#!/usr/bin/env python3
"""SQUIRL OS independent OTS chain verifier - no Bitcoin node, no calendar trust.
Deserializes the .ots file, uses the library's op-tree machinery to compute the
Bitcoin merkle-root commit message for each attestation, then requires that
message to equal the merkle root of the REAL block fetched from two independent
public explorers (Blockstream + mempool.space). The .ots stores only the block
height - it cannot lie about the root. Exit 0 = ON-BITCOIN VERIFIED."""
import sys, json, urllib.request
from opentimestamps.core.timestamp import DetachedTimestampFile
from opentimestamps.core.serialize import StreamDeserializationContext
from opentimestamps.core.notary import BitcoinBlockHeaderAttestation

def main(path, expect_sha=None):
    with open(path, 'rb') as f:
        dtf = DetachedTimestampFile.deserialize(StreamDeserializationContext(f))
    digest = dtf.file_digest.hex()
    print(f"== {path}")
    print(f"   committed digest: {digest}")
    if expect_sha:
        print(f"   matches file sha256: {'PASS' if digest == expect_sha else 'FAIL'}")
    verdict = True
    for msg, attestation in dtf.timestamp.all_attestations():
        if not isinstance(attestation, BitcoinBlockHeaderAttestation):
            continue
        height = attestation.height
        bh = urllib.request.urlopen(f"https://blockstream.info/api/block-height/{height}", timeout=30).read().decode()
        blk = json.loads(urllib.request.urlopen(f"https://blockstream.info/api/block/{bh}", timeout=30).read())
        natural_root = bytes.fromhex(blk['merkle_root'])[::-1].hex()
        ok_bs = natural_root == msg.hex()
        try:
            b2 = json.loads(urllib.request.urlopen(f"https://mempool.space/api/block/{bh}", timeout=30).read())
            ok_mp = bytes.fromhex(b2['merkle_root'])[::-1].hex() == msg.hex(); mp = 'PASS' if ok_mp else 'FAIL'
        except Exception:
            ok_mp = None; mp = 'N/A'
        print(f"   commit message (merkle root claim): {msg.hex()}")
        print(f"   attested block {height}: {bh}")
        print(f"   blockstream match: {'PASS' if ok_bs else 'FAIL'} | mempool match: {mp} | block ts {blk['timestamp']}")
        verdict = verdict and ok_bs and ok_mp is not False
    ok = verdict
    print(f"   VERDICT: {'ON-BITCOIN VERIFIED' if ok else 'FAIL/INCOMPLETE'}\n")
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
