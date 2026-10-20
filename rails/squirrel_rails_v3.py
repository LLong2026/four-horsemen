#!/usr/bin/env python3
"""SQUIRREL RAILS v3 — PARALLEL batch-fire driver (appended per RAILS v2 doctrine; v1/v2 preserved).
v3 (receipted SPB-3): one fresh AccountInfo(ledger_index='current') sequence read at burst
start, deterministic sequence slots (seq+i), 10 CONCURRENT submit threads. Per-thread
self-healing: any tef* -> fresh current-read + retry (max 5). terQUEUED accepted.
XLM bundle fires in a parallel thread. Deterministic, no LLM anywhere.
"""
import sys, json, time, threading
sys.path.insert(0, "/app/tmp_push/fh_push/rails")

def batch_fire_parallel(payloads):
    import xrpl
    from xrpl.clients import JsonRpcClient
    from xrpl.models.transactions import AccountSet, Memo
    from xrpl.models.requests import AccountInfo
    from xrpl.core.keypairs import derive_keypair, derive_classic_address
    from xrpl.transaction import autofill, sign, submit
    from xrpl.wallet import Wallet

    TA = "/app/tmp_push/fh_push/tokenization-adoption"
    keyf = json.load(open(f"{TA}/xrp-rail/xrp_writer_key_mainnet_a.json"))
    public_key, private_key = derive_keypair(keyf["seed"])
    classic = derive_classic_address(public_key)
    assert classic == keyf["address"], "XRP keyfile mismatch"

    def read_seq(client):
        return client.request(AccountInfo(account=classic,
            ledger_index="current")).result["account_data"]["Sequence"]

    results = [None] * len(payloads)

    def worker(i, tag, ph):
        client = JsonRpcClient("https://xrplcluster.com")  # thread-local client
        wallet = Wallet(public_key=public_key, private_key=private_key, seed=keyf["seed"])
        seq_block = read_seq(client) + i  # deterministic slot on first attempt
        for attempt in range(5):
            wallet.sequence = seq_block if attempt == 0 else read_seq(client)
            tx = AccountSet(account=wallet.classic_address, fee="10",
                memos=[Memo(memo_type=tag.encode().hex(), memo_data=ph)])
            r = submit(sign(autofill(tx, client, wallet), wallet), client).result
            eng = r["engine_result"]
            if eng in ("tesSUCCESS", "terQUEUED"):
                results[i] = {"tag": tag, "txid": r["tx_json"]["hash"],
                              "engine": eng, "retries": attempt}
                return
            time.sleep(0.4)
        results[i] = {"tag": tag, "engine": eng, "error": "gave up after 5"}

    def xlm_bundle():
        from stellar_sdk import Keypair, Server, TransactionBuilder, Network
        keyf2 = json.load(open(f"{TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
        kp = Keypair.from_secret(keyf2["secret"])
        assert kp.public_key == keyf2["public"], "XLM keyfile mismatch"
        server = Server(horizon_url="https://horizon.stellar.org")
        acct = server.load_account(kp.public_key)
        b = TransactionBuilder(source_account=acct,
            network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE, base_fee=100)
        for tag, ph in payloads:
            b.append_manage_data_op(data_name=tag, data_value=bytes.fromhex(ph))
        b.set_timeout(30)
        tx = b.build(); tx.sign(kp)
        resp = server.submit_transaction(tx)
        out["xlm"] = {"hash": resp.get("hash"), "ledger": resp.get("ledger"),
                      "ok": bool(resp.get("successful")), "ops": len(payloads),
                      "submitted_seconds": round(time.time() - t0, 2)}

    t0 = time.time()
    out = {"mode": "RAILS v3 parallel batch (deterministic slots + self-healing)",
           "t0_utc_epoch": t0}
    threads = [threading.Thread(target=worker, args=(i, tag, ph))
               for i, (tag, ph) in enumerate(payloads)]
    txlm = threading.Thread(target=xlm_bundle)
    for t in threads + [txlm]:
        t.start()
    for t in threads:
        t.join()
    out["xrp_submit_window_seconds"] = round(time.time() - t0, 2)
    out["xrp"] = list(results)
    txlm.join()
    out["total_seconds"] = round(time.time() - t0, 2)
    return out
