#!/usr/bin/env python3
"""LTC CERT-1: BlockCypher UTXO/push, OP_RETURN envelope 6a25 53514452 06 <digest>.
STAMP BEFORE EXECUTE. Digest: DeWR-1 frozen 99e01327...b9ab6 (cross-rail comparability)."""
import json, hashlib, time, struct, sys
import ecdsa, requests

KEYF = "keys/ltc_writer_key_mainnet.json"
RUNLOG = "LTC_FIRE_RUNLOG.md"
DIGEST_HEX = "99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6"
LABEL = "LTC-CERT-1"
ADDR = json.load(open(KEYF))["address"]
priv = bytes.fromhex(json.load(open(KEYF))["priv_hex"])
ENV = bytes.fromhex("53514452") + bytes([0x06]) + bytes.fromhex(DIGEST_HEX)

# STAMP BEFORE EXECUTE
with open(RUNLOG, "a") as f:
    f.write(f"\n# {LABEL} — IN PROGRESS — {time.strftime('%Y-%m-%d %H:%M:%S %Z')} — digest {DIGEST_HEX} — envelope {ENV.hex()}\n")
print("stamp written", flush=True)

def b58(p):
    n,o=int.from_bytes(p,'big'),[]
    B58='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    while n: n,r=divmod(n,58); o.append(B58[r])
    pad=len(p)-len(p.lstrip(b'\x00')); return '1'*pad+''.join(reversed(o))
def b58c(p): return b58(p+hashlib.sha256(hashlib.sha256(p).digest()).digest()[:4])

sk=ecdsa.SigningKey.from_string(priv,curve=ecdsa.SECP256k1)
pub=sk.get_verifying_key().to_string("compressed")
pubhash=hashlib.new("ripemd160",hashlib.sha256(pub).digest()).digest()
assert b58c(bytes([0x30])+pubhash)==ADDR

def sign_tx(txins,txouts):
    ib=b""
    for prev,idx,val in txins:
        ib+=prev+idx.to_bytes(4,"little")+bytes([0x19,0x76,0xA9,0x14])+pubhash+bytes([0x88,0xAC,0xFF,0xFF,0xFF,0xFF])
    ob=b""
    for val,script in txouts:
        ob+=struct.pack("<Q",val)+bytes([len(script)])+script
    digest=hashlib.sha256(hashlib.sha256(struct.pack("<I",1)+len(txins).to_bytes(1,"little")+ib+len(txouts).to_bytes(1,"little")+ob+bytes([0,0,0,0])+struct.pack("<I",1)).digest()).digest()
    der=sk.sign_digest_deterministic(digest,sigencode=ecdsa.util.sigencode_der)
    r,s=ecdsa.util.sigdecode_der(der,ecdsa.SECP256k1.order)
    if s>ecdsa.SECP256k1.order//2: s=ecdsa.SECP256k1.order-s
    def i2d(n):
        b=n.to_bytes((n.bit_length()+7)//8,"big")
        return bytes([2,len(b)+(1 if b[0]>0x7F else 0)])+(b"\x00" if b[0]>0x7F else b"")+b
    der=bytes([0x30,len(i2d(r))+len(i2d(s))])+i2d(r)+i2d(s)
    sig=der+bytes([1]); ss=bytes([len(sig)])+sig+bytes([len(pub)])+pub
    tx=struct.pack("<I",1)+len(txins).to_bytes(1,"little")
    for prev,idx,_ in txins:
        tx+=prev+idx.to_bytes(4,"little")+bytes([len(ss)])+ss+bytes([0xFF,0xFF,0xFF,0xFF])
    tx+=len(txouts).to_bytes(1,"little")
    for val,script in txouts:
        tx+=struct.pack("<Q",val)+bytes([len(script)])+script
    tx+=bytes([0,0,0,0])
    return tx,hashlib.sha256(hashlib.sha256(tx).digest()).digest()[::-1].hex()

# UTXO via BlockCypher (Blockchair temp-blacklisted)
r=requests.get(f"https://api.blockcypher.com/v1/ltc/main/addrs/{ADDR}?unspentOnly=true",timeout=30)
utxos=r.json().get("txrefs",[])
assert utxos, f"no UTXO: {r.text[:200]}"
u=utxos[0]
prev_txid,vout,value=u["tx_hash"],u["tx_output_n"],u["value"]
print(f"spending {prev_txid}:{vout} = {value/1e8} LTC (conf {u.get('confirmations')})",flush=True)

FEE=100000  # 0.001 LTC
change=value-FEE
txins=[(bytes.fromhex(prev_txid)[::-1],vout,value)]
txouts=[(0,bytes([0x6A,len(ENV)])+ENV),(change,bytes([0x76,0xA9,0x14])+pubhash+bytes([0x88,0xAC]))]
raw,txid=sign_tx(txins,txouts)
print("canonical txid:",txid,flush=True)

r=requests.post("https://api.blockcypher.com/v1/ltc/main/txs/push",json={"tx":raw.hex()},timeout=40)
print(f"push HTTP {r.status_code} | {r.text[:200]}",flush=True)
json.dump({"label":LABEL,"txid":txid,"digest":DIGEST_HEX,"envelope_hex":ENV.hex(),"push_http":r.status_code,
           "push_resp":r.text[:300],"change_litoshi":change,"funding_utxo":f"{prev_txid}:{vout}",
           "funding_value":value,"broadcast_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())},
          open("LTC_LEGS.json","w"),indent=1)
