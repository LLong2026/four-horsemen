#!/usr/bin/env python3
"""SQUIRREL RAILS v2 — batch-fire driver (appended per RAILS v2 doctrine; v1 frozen, untouched).
Fix locked from SPB-1 defect (v2.3): burst XRP anchors chain the account sequence via
AccountInfo(ledger_index='current') PER ANCHOR — the open-ledger view already includes
txs submitted this burst, so the next sequence is always accurate. Any tefPAST_SEQ /
tefTOO_SOON is retried with a fresh read. terQUEUED is accepted (validates later, free).
Usage: python3 squirrel_rails_v2.py (imports frozen leg constructions from squirrel_rails.py)
"""
import sys, json, time
sys.path.insert(0, "/app/tmp_push/fh_push/rails")
import squirrel_rails as v1  # frozen constructions reused, never modified

def batch_fire(payloads, fire_xlm_bundle=True):
    """payloads: list of (tag, payload_hex). Returns full measured receipt dict."""
    import xrpl
    from xrpl.clients import JsonRpcClient
    from xrpl.models.transactions import AccountSet, Memo
    from xrpl.models.requests import AccountInfo
    from xrpl.core.keypairs import derive_keypair, derive_classic_address
    from xrpl.transaction import autofill, sign, submit
    from xrpl.wallet import Wallet

    TA = v1.TA
    keyf = json.load(open(f"{TA}/xrp-rail/xrp_writer_key_mainnet_a.json"))
    public_key, private_key = derive_keypair(keyf["seed"])
    classic = derive_classic_address(public_key)
    assert classic == keyf["address"], "XRP keyfile mismatch"
    client = JsonRpcClient("https://xrplcluster.com")
    wallet = Wallet(public_key=public_key, private_key=private_key, seed=keyf["seed"])

    def one(tag, ph):
        for attempt in range(4):
            seq = client.request(AccountInfo(account=classic,
                ledger_index="current")).result["account_data"]["Sequence"]
            wallet.sequence = seq
            tx = AccountSet(account=wallet.classic_address, fee="10",
                memos=[Memo(memo_type=tag.encode().hex(), memo_data=ph)])
            r = submit(sign(autofill(tx, client, wallet), wallet), client).result
            eng = r["engine_result"]
            if eng in ("tesSUCCESS", "terQUEUED"):
                return {"tag": tag, "txid": r["tx_json"]["hash"], "engine": eng,
                        "retries": attempt}
            time.sleep(0.6)
        return {"tag": tag, "engine": eng, "error": "gave up after 4 sequence reads"}

    import threading
    t0 = time.time()
    out = {"mode": "RAILS v2 batch (current-ledger sequence chaining)", "xrp": []}

    def xlm_leg():
        # one XLM transaction, N manage_data ops (v2.2 bundle construction)
        from stellar_sdk import Keypair, Server, TransactionBuilder, Network
        keyf2 = json.load(open(f"{TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
        kp = Keypair.from_secret(keyf2["secret"])
        assert kp.public_key == keyf2["public"], "XLM keyfile mismatch"
        server = Server(horizon_url="https://horizon.stellar.org")
        acct = server.load_account(kp.public_key)
        b = TransactionBuilder(source_account=acct,
            network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE, base_fee=100)
        for tag, ph, *_ in payloads:
            b.append_manage_data_op(data_name=tag, data_value=bytes.fromhex(ph))
        b.set_timeout(30)
        tx = b.build(); tx.sign(kp)
        resp = server.submit_transaction(tx)
        out["xlm"] = {"hash": resp.get("hash"), "ledger": resp.get("ledger"),
                      "ok": bool(resp.get("successful")), "ops": len(payloads)}

    xlm_thread = threading.Thread(target=xlm_leg)
    xlm_thread.start()          # XLM bundle fires IN PARALLEL with the XRP burst
    for tag, ph in payloads:
        out["xrp"].append(one(tag, ph))
    out["xrp_burst_seconds"] = round(time.time() - t0, 2)
    xlm_thread.join()
    out["xlm_seconds"] = round(time.time() - t0, 2)
    out["total_seconds"] = round(time.time() - t0, 1)
    return out
