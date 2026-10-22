import json, hashlib, base64
import ecdsa
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_string_canonize

key = json.load(open("keys/atom_writer_key_mainnet.json"))
privkey = bytes.fromhex(key["privkey_hex"])
ADDR = "cosmos1eyplx3a0rskyes6zmqu9pll03uchf8mclrh0gd"
PUB = bytes.fromhex(key["pubkey_compressed_hex"])
MEMO = "535144520799e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6"


def varint(n):
    out = b""
    while True:
        b = n & 0x7F
        n >>= 7
        out += bytes([b | 0x80]) if n else bytes([b])
        if not n:
            return out


def tag(f, w):
    return varint((f << 3) | w)


def s(f, v):  # string/bytes field (ints coerced to decimal strings)
    if isinstance(v, int):
        v = str(v)
    if isinstance(v, str):
        v = v.encode("utf-8")
    return tag(f, 2) + varint(len(v)) + v


def u(f, v):  # uint64 varint field
    return tag(f, 0) + varint(v)


def m(f, v):  # nested message field
    return tag(f, 2) + varint(len(v)) + v


def coin(denom, amount):
    return s(1, denom) + s(2, amount)


def msg_send(frm, to, amt):
    return s(1, frm) + s(2, to) + m(3, coin("uatom", amt))


def any_(url, val):
    return s(1, url) + s(2, val)


def body(msgs, memo):
    return b"".join(m(1, x) for x in msgs) + s(2, memo)


def pub_key_any(pub):
    return any_("/cosmos.crypto.secp256k1.PubKey", s(1, pub))


def mode_info_direct():
    return m(1, u(1, 1))  # single{mode: SIGN_MODE_DIRECT=1}


def signer_info(pub, seq):
    return m(1, pub_key_any(pub)) + m(2, mode_info_direct()) + u(3, seq)


def fee(amt, gas):
    return m(1, coin("uatom", amt)) + u(2, gas)


def auth_info(pub, seq, fee_amt, gas):
    return m(1, signer_info(pub, seq)) + m(2, fee(fee_amt, gas))


def sign_doc(bb, aib, chain, acct):
    return s(1, bb) + s(2, aib) + s(3, chain) + u(4, acct)


msg = any_("/cosmos.bank.v1beta1.MsgSend", msg_send(ADDR, ADDR, "1000"))
bb = body([msg], MEMO)
aib = auth_info(PUB, 0, 2500, 200000)
sd = sign_doc(bb, aib, "cosmoshub-4", 3725178)

sk = SigningKey.from_string(privkey, curve=SECP256k1)
digest = hashlib.sha256(sd).digest()
sig = sk.sign_digest_deterministic(digest, hashfunc=hashlib.sha256, sigencode=sigencode_string_canonize)
assert len(sig) == 64

# local verify before broadcast
assert sk.get_verifying_key().verify_digest(sig, digest), "local sig verify failed"
# envelope integrity check
assert bytes.fromhex(MEMO) == b"SQDR" + b"\x07" + bytes.fromhex(
    "99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6")

txraw = s(1, bb) + s(2, aib) + s(3, sig)
open("atom_cert1_tx_b64.txt", "w").write(base64.b64encode(txraw).decode())
print("TxRaw built:", len(txraw), "bytes; sig verified locally; envelope byte-exact; READY TO BROADCAST")
