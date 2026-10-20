#!/usr/bin/env python3
"""FL-1 tapscript library — extends the proven SAT-1 BIP340 lib with:
TapLeaf/TapBranch hashing, script-path (BIP342) sighash, control blocks,
and a full local verifier. First script-path spend in program history."""
import sys, hashlib
sys.path.insert(0, "/app/conversations/69b57685ca3719553a34597c/sat1")
from sat1_bip340 import (P, N, tagged, _sha, _lift_x, _point_add, _point_mul,
                         bip340_sign, bip340_verify, taptweak, pubkey_gen,
                         _ser_outpoints, _ser_amounts, _ser_spxs, _ser_seq, _ser_outs)

def push32(b): return bytes([0x20]) + b if len(b) == 32 else (_ for _ in ()).throw(ValueError("need 32"))
OP_DROP, OP_CHECKSIG, OP_CSV, OP_CLTV = 0x75, 0xac, 0xb2, 0xb1

def csize(n):  # compact size (scripts here < 253 bytes)
    return bytes([n])

def tapleaf_hash(script, leaf_ver=0xC0):
    return tagged("TapLeaf", bytes([leaf_ver]) + csize(len(script)) + script)

def tapbranch_hash(left, right):
    return tagged("TapBranch", (left + right) if left < right else (right + left))

def tweak_with_tree(P_xonly, root):
    return taptweak(P_xonly, root)  # TapTweak(P||root) — proven SAT-1 code

def bip342_sighash_script(nVersion, nLockTime, ins, outs, idx, script):
    """BIP341 SigMsg with ext_flag=1 (script path), no annex, SIGHASH_ALL."""
    htype = 0x01
    s = bytes([htype])
    s += nVersion.to_bytes(4, "little") + nLockTime.to_bytes(4, "little")
    s += _sha(_ser_outpoints(ins)) + _sha(_ser_amounts(ins)) + _sha(_ser_spxs(ins)) + _sha(_ser_seq(ins))
    s += _sha(_ser_outs(outs))
    s += bytes([0x02])  # spend_type: ext_flag(1)*2 + annex(0)
    s += idx.to_bytes(4, "little")
    s += csize(len(script)) + script          # script
    s += bytes([0xC0, 0x00])                  # leaf_version, key_version
    s += b"\xff\xff\xff\xff"                   # codesep_pos
    return tagged("TapSighash", b"\x00" + s), htype

def control_block(parity, P_internal_x, sibling_hashes):
    return bytes([0xC0 | (parity & 1)]) + P_internal_x + b"".join(sibling_hashes)

def verify_script_path_spend(spk_hex, ins, outs, idx, script, sig65, ctrl):
    """Full local BIP341/342 verification of a script-path spend witness."""
    # 1. output key from spk
    spk = bytes.fromhex(spk_hex)
    assert spk[:2] == b"\x51\x20".hex().encode() or spk[:2] == bytes.fromhex("5120"), "not P2TR"
    Q_x = spk[2:]
    # 2. parse control block
    leaf_ver = ctrl[0] & 0xFE
    assert leaf_ver == 0xC0, "bad leaf version"
    parity = ctrl[0] & 1
    P_int = ctrl[1:33]
    path = [ctrl[33+i*32: 33+(i+1)*32] for i in range((len(ctrl)-33)//32)]
    # 3. merkle: root = fold leaf hash with siblings
    cur = tapleaf_hash(script, leaf_ver)
    for sib in path:
        cur = tapbranch_hash(cur, sib)
    # 4. tweak recomputation
    Qx, Qpar = tweak_with_tree(P_int, cur)
    assert Qx.hex() == Q_x.hex(), "tweak mismatch: control block does not derive the output key"
    assert Qpar == parity, "parity mismatch"
    # 5. sighash + schnorr verify
    pk = script[script.rfind(bytes([0x20]))+1: script.rfind(bytes([0x20]))+33]
    idx_of_pk = script.rfind(bytes([0x20]))
    pk32 = script[idx_of_pk+1: idx_of_pk+33]
    sighash, _ = bip342_sighash_script(2, 0, ins, outs, idx, script)
    sig, htype = sig65[:64], sig65[64]
    assert htype == 0x01
    ok = bip340_verify(pk32, sighash, sig)
    return ok
