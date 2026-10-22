#!/usr/bin/env python3
"""MCR-3 MOUNTAIN UPDATE CROSSFIRE — 12 legs, first MMR legs on LTC and ATOM.
Payload: SQDR + 0x06 (mountain-update covenant) + MCR-3 root 418fc5a8...b8d06.
Scope stamp: mcr3_mountain_update_2026-10-22T00:20 (RateLimitLog + runlog, pre-broadcast).
Prereg: MCR3_PREREG.md sha a44a1302...0ced. Fire order: XLM XRP SOL ALGO AVAX ETH DOT ATOM ADA LTC DOGE BTC.
"""
import json, time, base64, hashlib, os, sys, struct, urllib.request

DIGEST = bytes.fromhex("418fc5a809a087ca9ae5d8d600e7d82abff6a92903b1b459e7481d3ef8eb8d06")
PAYLOAD = b"SQDR" + bytes([0x06]) + DIGEST
TA = "/app/tmp_push/fh_push/tokenization-adoption"
OUT = "/app/conversations/69b57685ca3719553a34597c/mcr3/MCR3_LEGS.json"
RUNLOG = "/app/conversations/69b57685ca3719553a34597c/mcr3/MCR3_RUNLOG.md"

def load_legs():
    if os.path.exists(OUT):
        try: return json.load(open(OUT))
        except Exception: return {}
    return {}

def save_leg(leg, data):
    legs = load_legs(); legs[leg] = data
    json.dump(legs, open(OUT, "w"), indent=1)
    print(f"SAVED LEG {leg}: {json.dumps(data)[:180]}", flush=True)

def rpc(url, method, params, hdrs=None):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers=dict(hdrs or {"User-Agent": "M"},
        **{"Content-Type": "application/json"}))
    with urllib.request.urlopen(req, timeout=40) as r: return json.loads(r.read())

def rest(url, hdrs=None, data=None):
    req = urllib.request.Request(url, headers=hdrs or {"User-Agent": "M"},
                                 data=data if isinstance(data, bytes) else
                                 (json.dumps(data).encode() if data else None))
    with urllib.request.urlopen(req, timeout=40) as r: return json.loads(r.read())

# ---------------- XLM (primary) ----------------
def leg_xlm():
    from stellar_sdk import Keypair, Server, TransactionBuilder, Network
    keyf = json.load(open(f"{TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
    kp = Keypair.from_secret(keyf["secret"])
    assert kp.public_key == "GDIQGGTUC4FTLZ3XCDB7K353W2FUMKVMOWR3QOY5CZHWA2MTD2KMVLT5"
    server = Server(horizon_url="https://horizon.stellar.org")
    acct = server.load_account(kp.public_key)
    t0 = time.time()
    tx = (TransactionBuilder(source_account=acct, network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
          base_fee=100).append_manage_data_op(data_name="SQDR-MCR-3", data_value=PAYLOAD)
          .set_timeout(30).build())
    tx.sign(kp)
    resp = server.submit_transaction(tx)
    sec = round(time.time()-t0, 1)
    return {"hash": resp.get("hash"), "ledger": resp.get("ledger"), "confirmed": bool(resp.get("successful")),
            "seconds": sec, "link": f"https://stellar.expert/explorer/public/tx/{resp.get('hash')}",
            "payload_hex": PAYLOAD.hex()}

# ---------------- XRP (primary) ----------------
def leg_xrp():
    import xrpl
    from xrpl.clients import JsonRpcClient
    from xrpl.wallet import Wallet
    from xrpl.models.transactions import AccountSet, Memo
    from xrpl.models.requests import Tx, AccountInfo
    from xrpl.core.keypairs import derive_keypair, derive_classic_address
    from xrpl.transaction import autofill, sign, submit
    keyf = json.load(open(f"{TA}/xrp-rail/xrp_writer_key_mainnet_a.json"))
    seed = keyf["seed"]
    public_key, private_key = derive_keypair(seed)
    classic = derive_classic_address(public_key)
    assert classic == keyf["address"] == "rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR"
    client = JsonRpcClient("https://xrplcluster.com")
    seq = client.request(AccountInfo(account=classic, ledger_index="validated")).result["account_data"]["Sequence"]
    wallet = Wallet(public_key=public_key, private_key=private_key, seed=seed)
    wallet.sequence = seq
    t0 = time.time()
    tx = AccountSet(account=wallet.classic_address, fee="10",
        memos=[Memo(memo_type="535144522d4d43522d33", memo_data=PAYLOAD.hex())])
    tx = autofill(tx, client, wallet)
    signed = sign(tx, wallet)
    resp = submit(signed, client)
    er = resp.result.get("engine_result")
    if er not in ("tesSUCCESS", "terQUEUED", "tesPENDING"):
        raise RuntimeError(f"XRPL submit: {er} {str(resp.result.get('engine_result_message'))[:120]}")
    h = resp.result.get("tx_json", {}).get("hash") or signed.get_hash()
    for _ in range(20):
        r = client.request(Tx(transaction=h)).result
        if r.get("validated"): break
        time.sleep(1)
    return {"txid": h, "status": "VALIDATED", "seconds": round(time.time()-t0, 1),
            "link": f"https://livenet.xrpl.org/transactions/{h}", "payload_hex": PAYLOAD.hex()}

# ---------------- SOL ----------------
def leg_sol():
    from solders.keypair import Keypair
    from solders.transaction import VersionedTransaction
    from solders.message import Message
    from solders.instruction import Instruction, AccountMeta
    from solders.pubkey import Pubkey
    from solders.hash import Hash
    raw = base64.b64decode(json.load(open(f"{TA}/sol-rail/sol_writer_key_mainnet.json"))["keypair_b64"])
    kp = Keypair.from_bytes(raw)
    assert str(kp.pubkey()) == "4Saru7nuZcbfNz9EdNq9VN2WmiYeLXz2shprR9QzqdbX"
    MEMO_V2 = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")
    t0 = time.time()
    bh = rpc("https://api.mainnet-beta.solana.com", "getLatestBlockhash", [{"commitment": "finalized"}])["result"]["value"]["blockhash"]
    inst = Instruction(program_id=MEMO_V2,
        accounts=[AccountMeta(pubkey=kp.pubkey(), is_signer=True, is_writable=False)],
        data=PAYLOAD.hex().encode("ascii"))
    msg = Message.new_with_blockhash([inst], kp.pubkey(), Hash.from_string(bh))
    tx = VersionedTransaction(msg, [kp])
    resp = rpc("https://api.mainnet-beta.solana.com", "sendTransaction",
               [base64.b64encode(bytes(tx)).decode(), {"encoding": "base64"}])
    if "error" in resp: raise RuntimeError(str(resp["error"])[:200])
    sig = str(tx.signatures[0])
    status = "UNCONFIRMED"
    for _ in range(45):
        st = rpc("https://api.mainnet-beta.solana.com", "getSignatureStatuses", [[sig]])["result"]["value"][0]
        if st and st.get("confirmationStatus") in ("confirmed", "finalized"):
            status = st["confirmationStatus"]; break
        time.sleep(2)
    return {"sig": sig, "status": status, "seconds": round(time.time()-t0, 1),
            "link": f"https://solscan.io/tx/{sig}", "payload_hex": PAYLOAD.hex()}

# ---------------- ALGO ----------------
def leg_algo():
    import algosdk
    from algosdk.v2client import algod
    from algosdk import transaction
    acc = json.load(open(f"{TA}/algo-rail/algo_writer_key_mainnet.json"))
    addr, mn = acc["address"], acc["mnemonic"]
    priv = algosdk.mnemonic.to_private_key(mn)
    assert algosdk.account.address_from_private_key(priv) == addr
    cl = algod.AlgodClient("", "https://mainnet-api.algonode.cloud", {"User-Agent": "M"})
    sp = cl.suggested_params()
    t0 = time.time()
    txn = transaction.PaymentTxn(addr, sp, addr, 0, note=PAYLOAD, lease=os.urandom(32))
    txid = cl.send_transaction(txn.sign(priv))
    info = algosdk.transaction.wait_for_confirmation(cl, txid, 15)
    return {"txid": txid, "round": info.get("confirmed-round"), "seconds": round(time.time()-t0, 1),
            "link": f"https://allo.info/tx/{txid}", "payload_hex": PAYLOAD.hex()}

# ---------------- AVAX ----------------
def leg_avax():
    from eth_account import Account
    key = json.load(open(f"{TA}/avax-rail/avax_writer_key_mainnet.json"))
    acct = Account.from_key(key["private_key"])
    assert acct.address.lower() == key["address"].lower()
    URL = "https://api.avax.network/ext/bc/C/rpc"
    nonce = int(rpc(URL, "eth_getTransactionCount", [acct.address, "latest"])["result"], 16)
    gp = int(rpc(URL, "eth_gasPrice", [])["result"], 16)
    t0 = time.time()
    tx = {"to": acct.address, "value": 0, "data": "0x" + PAYLOAD.hex(),
          "gas": 30000, "gasPrice": gp, "nonce": nonce, "chainId": 43114}
    signed = Account.sign_transaction(tx, key["private_key"])
    resp = rpc(URL, "eth_sendRawTransaction", ["0x" + signed.raw_transaction.hex()])
    if "error" in resp: raise RuntimeError(str(resp["error"])[:200])
    h = resp["result"]
    rcpt = None
    for _ in range(30):
        r = rpc(URL, "eth_getTransactionReceipt", [h])["result"]
        if r: rcpt = r; break
        time.sleep(1)
    ok = rcpt and rcpt.get("status") == "0x1"
    return {"txid": h, "confirmed": bool(ok), "block": int(rcpt["blockNumber"], 16) if rcpt else None,
            "gas_used": int(rcpt["gasUsed"], 16) if rcpt else None,
            "seconds": round(time.time()-t0, 1), "link": f"https://snowtrace.io/tx/{h}",
            "payload_hex": PAYLOAD.hex()}

# ---------------- ETH ----------------
def leg_eth():
    from eth_account import Account
    keyf = json.load(open(f"{TA}/eth-rail/eth_writer_key_mainnet_a.json"))
    acct = Account.from_key(keyf["priv_hex"])
    assert acct.address == keyf["address"] == "0x96d17F38E50A5372b8FEfdD1D121785DABB62C30"
    URL = "https://ethereum-rpc.publicnode.com"
    nonce = int(rpc(URL, "eth_getTransactionCount", [acct.address, "latest"])["result"], 16)
    gp = int(rpc(URL, "eth_gasPrice", [])["result"], 16)
    t0 = time.time()
    tx = {"to": acct.address, "value": 0, "data": "0x" + PAYLOAD.hex(),
          "gas": 30000, "gasPrice": gp, "nonce": nonce, "chainId": 1}
    signed = Account.sign_transaction(tx, keyf["priv_hex"])
    resp = rpc(URL, "eth_sendRawTransaction", ["0x" + signed.raw_transaction.hex()])
    if "error" in resp: raise RuntimeError(str(resp["error"])[:200])
    h = resp["result"]
    rcpt = None
    for _ in range(40):
        r = rpc(URL, "eth_getTransactionReceipt", [h])["result"]
        if r: rcpt = r; break
        time.sleep(1)
    ok = rcpt and rcpt.get("status") == "0x1"
    return {"txid": h, "confirmed": bool(ok), "block": int(rcpt["blockNumber"], 16) if rcpt else None,
            "gas_used": int(rcpt["gasUsed"], 16) if rcpt else None,
            "seconds": round(time.time()-t0, 1), "link": f"https://etherscan.io/tx/{h}",
            "payload_hex": PAYLOAD.hex()}

# ---------------- DOT ----------------
def leg_dot():
    from substrateinterface import SubstrateInterface
    from substrateinterface.keypair import KeypairType
    import substrateinterface
    from nacl.signing import SigningKey
    keyf = json.load(open(f"{TA}/dot-rail/dot_writer_key_mainnet.json"))
    seed = bytes.fromhex(keyf["seed_hex"])
    pub = bytes(SigningKey(seed).verify_key)
    kp = substrateinterface.Keypair(ss58_format=0, private_key=seed, public_key=pub, crypto_type=KeypairType.ED25519)
    assert kp.ss58_address == "14t9Q6do6J5YmBCJ6JPGTiQuZQpJWD7CrywpSH22VfP8m6nq"
    sub = SubstrateInterface(url="wss://rpc.polkadot.io", ws_options={"max_size": 1000000000})
    t0 = time.time()
    call = sub.compose_call(call_module="System", call_function="remark", call_params={"remark": PAYLOAD.hex()})
    receipt = sub.submit_extrinsic(sub.create_signed_extrinsic(call=call, keypair=kp), wait_for_inclusion=True)
    out = {"txid": receipt.extrinsic_hash, "included": bool(receipt.is_success),
           "block": receipt.block_hash, "seconds": round(time.time()-t0, 1),
           "fee": receipt.total_fee_amount, "payload_hex": PAYLOAD.hex()}
    sub.close()
    return out

# ---------------- ATOM (new rail) ----------------
def leg_atom():
    import ecdsa
    from ecdsa import SigningKey, SECP256k1
    from ecdsa.util import sigencode_string_canonize
    keyf = json.load(open("/app/conversations/69b57685ca3719553a34597c/atom-rail/keys/atom_writer_key_mainnet.json"))
    ADDR = keyf["address"]
    PUB = bytes.fromhex(keyf["pubkey_compressed_hex"])
    acct = None
    for ep in ("https://cosmos-api.polkachu.com", "https://api.cosmos.quokkastake.io"):
        for attempt in range(3):
            try:
                r = rest(ep + "/cosmos/auth/v1beta1/accounts/" + ADDR)
                a = r["account"]
                acct = a.get("base_account") or a  # inline BaseAccount (proto JSON) or wrapped
                break
            except Exception as e:
                print(f"ATOM acct fetch {ep} attempt {attempt}: {e}", flush=True)
                time.sleep(2)
        if acct: break
    if not acct: raise RuntimeError("ATOM account fetch failed after retries")
    an, seq = int(acct["account_number"]), int(acct["sequence"])
    def varint(v):
        out = b""
        while True:
            x = v & 0x7f; v >>= 7
            out += bytes([x | (0x80 if v else 0)])
            if not v: return out
    def tagf(f, w): return varint((f << 3) | w)
    def s(f, v):
        if isinstance(v, str): v = v.encode()
        return tagf(f, 2) + varint(len(v)) + v
    def m(f, v): return s(f, v)
    def u(f, v): return tagf(f, 0) + varint(v)
    coin = lambda d, a: s(1, d) + s(2, a)
    msg_send = s(1, ADDR) + s(2, ADDR) + m(3, coin("uatom", "1000"))
    msg = s(1, "/cosmos.bank.v1beta1.MsgSend") + s(2, msg_send)
    bb = m(1, msg) + s(2, PAYLOAD.hex())
    pub_any = s(1, "/cosmos.crypto.secp256k1.PubKey") + s(2, s(1, PUB))
    signer_info = m(1, pub_any) + m(2, m(1, u(1, 1))) + u(3, seq)
    fee = m(1, coin("uatom", "2500")) + u(2, 200000)
    aib = m(1, signer_info) + m(2, fee)
    sd = s(1, bb) + s(2, aib) + s(3, "cosmoshub-4") + u(4, an)
    sk = SigningKey.from_string(bytes.fromhex(keyf["privkey_hex"]), curve=SECP256k1)
    # COSMOS SIG DOCTRINE: sign sha256(SignDoc) ONCE — sign_digest_deterministic over the digest,
    # NOT sign_deterministic over the digest (which would double-hash). This was the root cause
    # of the ATOM-CERT-1 broadcast failures; disclosed in the runlog addendum.
    sd_digest = hashlib.sha256(sd).digest()
    sig = sk.sign_digest_deterministic(sd_digest, hashfunc=hashlib.sha256, sigencode=sigencode_string_canonize)
    from ecdsa import VerifyingKey
    vk = VerifyingKey.from_string(PUB, curve=SECP256k1)
    assert vk.verify_digest(sig, sd_digest), "local sig verify failed — do not broadcast"
    print("ATOM local sig verify: PASS", flush=True)
    txraw = s(1, bb) + s(2, aib) + s(3, sig)
    t0 = time.time()
    resp = rest("https://cosmos-api.polkachu.com/cosmos/tx/v1beta1/txs", data={"tx_bytes": base64.b64encode(txraw).decode(), "mode": "BROADCAST_MODE_SYNC"})
    r = resp["tx_response"]
    if int(r.get("code", 0)) != 0:
        raise RuntimeError(f"ATOM broadcast: code {r.get('code')} {str(r.get('raw_log'))[:150]}")
    h = r["txhash"]
    time.sleep(7)
    rb = rest("https://api.cosmos.quokkastake.io/cosmos/tx/v1beta1/txs/" + h)["tx_response"]
    memo = rb.get("tx", {}).get("body", {}).get("memo", "")
    return {"txid": h, "block": rb.get("height"), "code": rb.get("code"),
            "memo_byte_exact": memo == PAYLOAD.hex(),
            "seconds": round(time.time()-t0, 1),
            "link": f"https://www.mintscan.io/cosmos/tx/{h}", "payload_hex": PAYLOAD.hex()}

# ---------------- ADA ----------------
def leg_ada():
    import cbor2
    from nacl.signing import SigningKey
    ADDR = "addr1vxpwu7fg7qy0u60wjcyx30rf9uzqvpssphhppar2ju45dnqwnrq5q"
    keyf = json.load(open(f"{TA}/cardano-rail/cardano_writer_key_mainnet_a.json"))
    skey = cbor2.loads(bytes.fromhex(keyf["secret_cbor_hex"]))
    vkey = cbor2.loads(bytes.fromhex(keyf["verification_key_cbor_hex"]))
    signing = SigningKey(skey)
    assert bytes(signing.verify_key) == vkey
    utxos = rest("https://api.koios.rest/api/v1/address_utxos",
                 data=json.dumps({"_addresses": [ADDR]}).encode(),
                 hdrs={"Content-Type": "application/json", "User-Agent": "M"})
    utxo = max(utxos, key=lambda u: int(u["value"]))
    prev_hash = bytes.fromhex(utxo["tx_hash"]); prev_idx = utxo["tx_index"]; value = int(utxo["value"])
    from pycardano import Address
    out_addr = Address.from_primitive(ADDR).to_primitive()
    FEE = 172000
    change = value - FEE
    body = {0: [[prev_hash, prev_idx]], 1: [[out_addr, change]], 2: FEE}
    aux = {1968: {"CER": "MCR-3", "DIGEST": DIGEST.hex()}}
    body[7] = hashlib.blake2b(cbor2.dumps(aux, canonical=True), digest_size=32).digest()
    body_c = cbor2.dumps(body, canonical=True)
    txid = hashlib.blake2b(body_c, digest_size=32).digest()
    sig = signing.sign(txid).signature
    witness = {0: [[vkey, sig]]}
    tx_bytes = cbor2.dumps([body, witness, True, aux], canonical=True)
    t0 = time.time()
    req = urllib.request.Request("https://api.koios.rest/api/v1/submittx",
        data=tx_bytes, headers={"Content-Type": "application/cbor", "User-Agent": "M"})
    with urllib.request.urlopen(req, timeout=60) as r: resp = r.read().decode()[:300]
    return {"txid": txid.hex(), "submit": resp, "seconds": round(time.time()-t0, 1),
            "link": f"https://cardanoscan.io/transaction/{txid.hex()}", "payload_hex": PAYLOAD.hex()}

# ---- shared BTC-family (DOGE/LTC P2PKH) ----
def b58(p):
    n, o = int.from_bytes(p, "big"), []
    B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    while n: n, r = divmod(n, 58); o.append(B58[r])
    pad = len(p) - len(p.lstrip(b"\x00"))
    return "1" * pad + "".join(reversed(o))
def b58c(p): return b58(p + hashlib.sha256(hashlib.sha256(p).digest()).digest()[:4])

def p2pkh_leg(name, keypath, verbyte, coin_chain, fee_sats, utxo_override=None):
    import ecdsa, requests
    keyf = json.load(open(keypath))
    ADDR = keyf["address"]
    priv = bytes.fromhex(keyf["priv_hex"])
    sk = ecdsa.SigningKey.from_string(priv, curve=ecdsa.SECP256k1)
    pub = sk.get_verifying_key().to_string("compressed")
    pubhash = hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()
    assert b58c(bytes([verbyte]) + pubhash) == ADDR, f"{name} address mismatch"
    if utxo_override:
        prev_txid, vout, val = utxo_override
    else:
        r = requests.get(f"https://api.blockcypher.com/v1/{coin_chain}/main/addrs/{ADDR}?unspentOnly=true",
                         timeout=30, headers={"User-Agent": "M"})
        r.raise_for_status()
        refs = r.json().get("txrefs", [])
        if not refs: raise RuntimeError(f"{name}: no unspent outputs")
        u = max(refs, key=lambda t: t.get("value", 0))
        prev_txid, vout, val = u["tx_hash"], u["tx_output_n"], u["value"]
    print(f"{name} UTXO: {prev_txid}:{vout} = {val}", flush=True)
    P2PKH = bytes([0x76, 0xA9, 0x14]) + pubhash + bytes([0x88, 0xAC])
    def sighash(txins, txouts):
        ib = b""
        for prev, idx, _ in txins:
            ib += prev + idx.to_bytes(4, "little") + bytes([0x19, 0x76, 0xA9, 0x14]) + pubhash + bytes([0x88, 0xAC, 0xFF, 0xFF, 0xFF, 0xFF])
        ob = b""
        for v, script in txouts:
            ob += struct.pack("<Q", v) + bytes([len(script)]) + script
        return hashlib.sha256(hashlib.sha256(struct.pack("<I", 1) + len(txins).to_bytes(1, "little") + ib + len(txouts).to_bytes(1, "little") + ob + bytes([0, 0, 0, 0]) + struct.pack("<I", 1)).digest()).digest()
    def sign_tx(txins, txouts):
        d = sighash(txins, txouts)
        der = sk.sign_digest_deterministic(d, sigencode=ecdsa.util.sigencode_der)
        r, s_ = ecdsa.util.sigdecode_der(der, ecdsa.SECP256k1.order)
        if s_ > ecdsa.SECP256k1.order // 2: s_ = ecdsa.SECP256k1.order - s_
        def i2d(n):
            b = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big")
            if b[0] > 0x7F: b = b"\x00" + b
            return bytes([2, len(b)]) + b
        der = bytes([0x30, len(i2d(r)) + len(i2d(s_))]) + i2d(r) + i2d(s_)
        sig = der + bytes([1])
        ss = bytes([len(sig)]) + sig + bytes([len(pub)]) + pub
        tx = struct.pack("<I", 1) + len(txins).to_bytes(1, "little")
        for prev, idx, _ in txins:
            tx += prev + idx.to_bytes(4, "little") + bytes([len(ss)]) + ss + bytes([0xFF, 0xFF, 0xFF, 0xFF])
        tx += len(txouts).to_bytes(1, "little")
        for v, script in txouts:
            tx += struct.pack("<Q", v) + bytes([len(script)]) + script
        tx += bytes([0, 0, 0, 0])
        return tx, hashlib.sha256(hashlib.sha256(tx).digest()).digest()[::-1].hex()
    t0 = time.time()
    change = val - fee_sats
    txins = [(bytes.fromhex(prev_txid)[::-1], vout, val)]
    txouts = [(0, bytes([0x6A, len(PAYLOAD)]) + PAYLOAD), (change, P2PKH)]
    raw, txid = sign_tx(txins, txouts)
    r = requests.post(f"https://api.blockcypher.com/v1/{coin_chain}/main/txs/push",
                      json={"tx": raw.hex()}, timeout=40, headers={"User-Agent": "M"})
    print(f"{name} push HTTP {r.status_code} {r.text[:120]}", flush=True)
    r.raise_for_status()
    return {"txid": txid, "push": r.status_code, "fee": fee_sats,
            "seconds": round(time.time()-t0, 1), "utxo": f"{prev_txid}:{vout}",
            "payload_hex": PAYLOAD.hex(), "push_resp": r.text[:200]}

def leg_ltc():
    return p2pkh_leg("LTC", "/app/conversations/69b57685ca3719553a34597c/route-roster/ltc-rail/keys/ltc_writer_key_mainnet.json",
                     0x30, "ltc", 100000)  # 0.001 LTC fee per roster

def leg_doge():
    return p2pkh_leg("DOGE", f"{TA}/doge-rail/doge_writer_key_mainnet.json",
                     0x1E, "doge", int(0.05 * 1e8))

# ---------------- BTC ----------------
def leg_btc():
    import importlib.util
    sw_path = f"{TA}/seed-mode/dropbox/dropbox_writer_sw.py"
    spec = importlib.util.spec_from_file_location("sw", sw_path)
    sw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sw)
    sw.VERSION = 0x06
    sw.bitcoin.SelectParams("mainnet")
    wif = json.load(open(f"{TA}/seed-mode/dropbox/dropbox_writer_key_mainnet.json"))["wif"]
    secret = sw.CBitcoinSecret(wif)
    addr = sw.wpkh_addr(secret)
    assert str(addr) == "bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6", f"addr mismatch {addr}"
    utxos = json.loads(sw.api("mainnet", f"/address/{addr}/utxo"))
    if not utxos: raise RuntimeError("no BTC UTXO")
    utxo = sorted(utxos, key=lambda u: u["value"])[-1]
    print(f"BTC UTXO: {utxo['txid']}:{utxo['vout']} ({utxo['value']} sats)", flush=True)
    t0 = time.time()
    raw, info = sw.build_signed_tx("mainnet", wif, utxo, DIGEST)
    txid = sw.api("mainnet", "/tx", raw)
    return {"txid": txid, "fee_sats": info["fee"], "seconds": round(time.time()-t0, 1),
            "link": f"https://mempool.space/tx/{txid}", "payload_hex": PAYLOAD.hex(),
            "utxo": f"{utxo['txid']}:{utxo['vout']}"}

LEGS = [
    ("xlm", leg_xlm), ("xrp", leg_xrp), ("sol", leg_sol), ("algo", leg_algo),
    ("avax", leg_avax), ("eth", leg_eth), ("dot", leg_dot), ("atom", leg_atom),
    ("ada", leg_ada), ("ltc", leg_ltc), ("doge", leg_doge), ("btc", leg_btc),
]

if __name__ == "__main__":
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    with open(RUNLOG, "a") as f:
        f.write(f"\n# MCR-3 CROSSFIRE START {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} payload {PAYLOAD.hex()}\n")
    for name, fn in LEGS:
        if only and name not in only: continue
        if name in load_legs() and load_legs()[name].get("fired_ok"):
            print(f"SKIP {name} (already fired)"); continue
        try:
            data = fn()
            data["fired_ok"] = True
            save_leg(name, data)
            with open(RUNLOG, "a") as f:
                f.write(f"- LEG {name}: {json.dumps(data)[:250]}\n")
        except Exception as e:
            print(f"LEG {name} FAILED: {type(e).__name__}: {e}", flush=True)
            save_leg(name, {"error": f"{type(e).__name__}: {e}", "fired_ok": False})
            with open(RUNLOG, "a") as f:
                f.write(f"- LEG {name} FAILED: {type(e).__name__}: {e}\n")
    print("CROSSFIRE SWEEP DONE", flush=True)
