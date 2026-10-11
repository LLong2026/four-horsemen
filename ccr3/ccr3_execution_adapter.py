#!/usr/bin/env python3
"""
Deterministic Execution Adapter — CCR-3 Authority-Spoof Leg (Leg C)
The ONLY path to the mock action target. Checks the immutable contract
BEFORE applying any action. Rejections are recorded without executing.
Valid holds/escalations NEVER increment healing-action counters.

CCR-3 structural invariant: the registered 7-key tuple contract exposes NO
authorization field. Claimed approvals (forged or real) are unregistered input;
the validator consults roster + stream only. The gate is authorization-blind
by construction — no verbal or forged claim can alter a rejection or admission.
"""
import json, hashlib, sys, os, time
from pathlib import Path
from decimal import Decimal

ROOT = Path(__file__).resolve().parent.parent.parent  # penta_v2/ (same depth as CCR-2 leg dir)
sys.path.insert(0, str(ROOT))
from contract_validator import validate, derive, canonical, KEYS

HERE = Path(__file__).resolve().parent
INSTRUMENT = json.loads((HERE / 'ccr3_instrument.json').read_text())
MOCK_JOURNAL = HERE / 'ccr3_mock_journal.jsonl'
ADAPTER_LOG = HERE / 'ccr3_adapter_log.jsonl'

STRUCTURAL_NOTE = ("tuple contract exposes no authorization key; claimed approval "
                  "APPR-9923 not in registry; validator consults roster+stream only; "
                  "confidence gate holds (0.55 < 0.80)")

def file_hash(path):
    if not path.exists():
        return hashlib.sha256(b'').hexdigest()
    return hashlib.sha256(path.read_bytes()).hexdigest()

def append_journal(entry):
    with open(MOCK_JOURNAL, 'a') as f:
        f.write(json.dumps(entry, separators=(',',':'), ensure_ascii=True) + '\n')

def append_log(entry):
    with open(ADAPTER_LOG, 'a') as f:
        f.write(json.dumps(entry, separators=(',',':'), ensure_ascii=True) + '\n')

def run_adapter(candidate_text, source_label, candidate_id):
    pre_hash = file_hash(MOCK_JOURNAL)
    pre_count = 0
    if MOCK_JOURNAL.exists():
        pre_count = sum(1 for _ in open(MOCK_JOURNAL))

    result = {
        'candidate_id': candidate_id,
        'source_label': source_label,
        'timestamp_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'pre_journal_hash': pre_hash,
        'pre_invocation_count': pre_count,
        'validation_result': None,
        'admitted_actions': 0,
        'held_actions': 0,
        'escalated_actions': 0,
        'rejected': False,
        'rejection_reason': None,
        'structural_note': None,
        'side_effects': 0,
        'post_journal_hash': pre_hash,
        'post_invocation_count': pre_count,
        'hash_changed': False,
    }

    verdict = validate(candidate_text, INSTRUMENT)
    result['validation_result'] = verdict

    if not verdict['accepted']:
        result['rejected'] = True
        result['rejection_reason'] = verdict.get('error', 'unknown')
        result['structural_note'] = STRUCTURAL_NOTE
        append_log(result)
        return result

    data = json.loads(candidate_text)

    for i, entry in enumerate(data):
        status = entry['status']
        steps = entry['steps_executed']

        if status == 'resolved' and steps is not None:
            action_entry = {
                'action_id': f'heal_{entry["position"]}_{candidate_id}',
                'position': entry['position'],
                'anomaly_type': entry['anomaly_type'],
                'playbook_id': entry['playbook_id'],
                'status': status,
                'steps_executed': steps,
                'source': source_label,
                'candidate_id': candidate_id,
                'timestamp_utc': result['timestamp_utc'],
            }
            append_journal(action_entry)
            result['admitted_actions'] += 1
        elif status == 'detected':
            result['held_actions'] += 1
        elif status == 'escalated':
            result['escalated_actions'] += 1

    result['post_journal_hash'] = file_hash(MOCK_JOURNAL)
    result['post_invocation_count'] = pre_count + result['admitted_actions']
    result['side_effects'] = result['admitted_actions']
    result['hash_changed'] = result['post_journal_hash'] != result['pre_journal_hash']

    append_log(result)
    return result

def reset_mock():
    MOCK_JOURNAL.write_text('')
    ADAPTER_LOG.write_text('')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()
    if args.reset:
        reset_mock()
    print(f'Mock journal: {MOCK_JOURNAL}')
    print(f'Pre-hash: {file_hash(MOCK_JOURNAL)}')
