// CCR-P pre-write gate: deterministic validator in front of a LIVE Base44 entity write path.
// Series signature: containment_gap_closure_20261011. Fail-closed. Audit on every decision.
// Frozen references (parity): penta_v2/contract_validator.py sha256 b1cdbac7...8afa; instrument per prereg.
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.31';
const INSTRUMENT = {"version":"PENTA-CONTRACT-V2-LOCAL","roster":[{"anomaly_type":"latency_spike","record_id":"6a5d29cb54e45d7e8bad47c5","playbook":"PB-003: Latency Spike Resolver","confidence_threshold":0.8},{"anomaly_type":"latency_spike","record_id":"6a6671df0ad58ac5d8179da4","playbook":"PB-003: Latency Spike Resolver","confidence_threshold":0.8},{"anomaly_type":"latency_spike","record_id":"6a669671d21d94c236bcfab7","playbook":"PB-003: Latency Spike Resolver","confidence_threshold":0.8},{"anomaly_type":"latency_spike","record_id":"6ac128339004bb8bd5785432","playbook":"Latency Spike Resource Contention Recovery (SIP-015 consolidated)","confidence_threshold":0.8},{"anomaly_type":"heartbeat_miss","record_id":"6a5d29cb54e45d7e8bad47ca","playbook":"PB-008: Heartbeat Re-igniter","confidence_threshold":0.85},{"anomaly_type":"heartbeat_miss","record_id":"6a6672030ad58ac5d8179e0d","playbook":"PB-008: Heartbeat Re-igniter","confidence_threshold":0.85},{"anomaly_type":"heartbeat_miss","record_id":"6a669671d21d94c236bcfabc","playbook":"PB-008: Heartbeat Re-igniter","confidence_threshold":0.9},{"anomaly_type":"quantum_vulnerability_detected","record_id":"6a5d29cb54e45d7e8bad47cb","playbook":"PB-009: Quantum Vulnerability Migrator","confidence_threshold":0.8},{"anomaly_type":"quantum_vulnerability_detected","record_id":"6a6671df0ad58ac5d8179db1","playbook":"PB-009: Quantum Vulnerability Migrator","confidence_threshold":0.8},{"anomaly_type":"quantum_vulnerability_detected","record_id":"6a669671d21d94c236bcfabd","playbook":"PB-009: Quantum Vulnerability Migrator","confidence_threshold":0.8},{"anomaly_type":"quantum_vulnerable_algorithm_detected","record_id":"6abf3acad1a10b9555bff95c","playbook":"PB-PQC-ALGO-MIGRATION-001","confidence_threshold":0.95}],"stream":[{"position":0,"anomaly_type":"latency_spike","component":"synthetic_rail_02","description":"SDR-D seeded batch position 000: synthetic sign op anomaly on synthetic_rail_02","confidence_score":0.9,"severity":"low","synthetic":true,"source":"sdr-d-harness","op_result_hash":"00db3c32fe61ff2aa13ada8da4307d3ec9397a1128988e308edce105cc6f38f3"},{"position":40,"anomaly_type":"heartbeat_miss","component":"synthetic_rail_00","description":"SDR-D seeded batch position 040: synthetic anchor op anomaly on synthetic_rail_00","confidence_score":0.9,"severity":"low","synthetic":true,"source":"sdr-d-harness","op_result_hash":"643a8f3ca6b2f2700b36e94145e476976a8e0aabee2a6ae29bd011fc89275f50"},{"position":80,"anomaly_type":"quantum_vulnerability_detected","component":"synthetic_rail_04","description":"SDR-D seeded batch position 080: synthetic keygen op anomaly on synthetic_rail_04","confidence_score":0.9,"severity":"low","synthetic":true,"source":"sdr-d-harness","op_result_hash":"63c3f1b641224fe6f4516826cdc56235b17b16cbd5017213618103f0687c9419"},{"position":120,"anomaly_type":"latency_spike","component":"synthetic_rail_01","description":"SDR-D seeded batch position 120: synthetic sign op anomaly on synthetic_rail_01","confidence_score":0.9,"severity":"low","synthetic":true,"source":"sdr-d-harness","op_result_hash":"68c4ce56c410caac7fea9c3a2c2faebac4fd696924f856adc8f791a1c24a7a2e"},{"position":160,"anomaly_type":"quantum_vulnerability_detected","component":"synthetic_rail_07","description":"SDR-D seeded batch position 160: synthetic keygen op anomaly on synthetic_rail_07","confidence_score":0.9,"severity":"low","synthetic":true,"source":"sdr-d-harness","op_result_hash":"2dba3656faa95559b93c505974926c48f4d5c11f7e306de4f965288556d1d4ef"},{"position":200,"anomaly_type":"quantum_vulnerability_detected","component":"synthetic_rail_05","description":"SDR-D seeded batch position 200: synthetic keygen op anomaly on synthetic_rail_05","confidence_score":0.9,"severity":"low","synthetic":true,"source":"sdr-d-harness","op_result_hash":"956a7435f953b9b53aab9a58e9e8730109543922c1a33afa6111f28779dadb5b"},{"position":240,"anomaly_type":"latency_spike","component":"synthetic_contract_boundary","description":"V2 synthetic boundary probe; no operation executes","confidence_score":0.799999,"severity":"low","synthetic":true,"source":"penta-v2-local-instrument"},{"position":280,"anomaly_type":"latency_spike","component":"synthetic_contract_boundary","description":"V2 synthetic boundary probe; no operation executes","confidence_score":0.8,"severity":"low","synthetic":true,"source":"penta-v2-local-instrument"},{"position":320,"anomaly_type":"heartbeat_miss","component":"synthetic_contract_boundary","description":"V2 synthetic boundary probe; no operation executes","confidence_score":0.849999,"severity":"low","synthetic":true,"source":"penta-v2-local-instrument"},{"position":360,"anomaly_type":"heartbeat_miss","component":"synthetic_contract_boundary","description":"V2 synthetic boundary probe; no operation executes","confidence_score":0.85,"severity":"low","synthetic":true,"source":"penta-v2-local-instrument"},{"position":400,"anomaly_type":"LATENCY_SPIKE","component":"synthetic_contract_boundary","description":"V2 synthetic boundary probe; no operation executes","confidence_score":0.9,"severity":"low","synthetic":true,"source":"penta-v2-local-instrument"},{"position":440,"anomaly_type":"unregistered_synthetic_fault","component":"synthetic_contract_boundary","description":"V2 synthetic boundary probe; no operation executes","confidence_score":0.9,"severity":"low","synthetic":true,"source":"penta-v2-local-instrument"}]};
const KEYS = ['position','anomaly_type','playbook','playbook_id','match_type','steps_executed','status'];
const STEPS = 'isolation,healing,verification';

// Strict JSON scanner: rejects duplicate keys, non-finite values, trailing garbage.
function strictParse(text) {
  let i = 0;
  function ws() { while (i < text.length && ' \t\n\r'.includes(text[i])) i++; }
  function fail(msg) { throw new Error(msg + ' at char ' + i); }
  function parseValue() {
    ws();
    const c = text[i];
    if (c === '{') return parseObj();
    if (c === '[') return parseArr();
    if (c === '"') return parseString();
    if (text.startsWith('true', i)) { i += 4; return true; }
    if (text.startsWith('false', i)) { i += 5; return false; }
    if (text.startsWith('null', i)) { i += 4; return null; }
    return parseNumber();
  }
  function parseObj() {
    i++; ws();
    const obj = {}; const seen = new Set(); let first = true;
    while (text[i] !== '}') {
      if (!first) { if (text[i] !== ',') fail('Expected comma'); i++; ws(); }
      first = false;
      if (text[i] !== '"') fail('Expected key');
      const key = parseString();
      if (seen.has(key)) throw new Error('Duplicate JSON key: ' + key);
      seen.add(key);
      ws(); if (text[i] !== ':') fail('Expected colon'); i++; ws();
      obj[key] = parseValue(); ws();
    }
    i++; return obj;
  }
  function parseArr() {
    i++; ws();
    const arr = []; let first = true;
    while (text[i] !== ']') {
      if (!first) { if (text[i] !== ',') fail('Expected comma'); i++; ws(); }
      first = false;
      arr.push(parseValue()); ws();
    }
    i++; return arr;
  }
  function parseString() {
    i++; let out = '';
    while (text[i] !== '"') {
      if (text[i] === '\\') {
        const n = text[i+1];
        const map = {'"':'"','\\':'\\','/':'/','b':'\b','f':'\f','n':'\n','r':'\r','t':'\t'};
        if (map[n] !== undefined) { out += map[n]; i += 2; continue; }
        if (n === 'u') {
          const hex = text.slice(i+2, i+6);
          if (!/^[0-9a-fA-F]{4}$/.test(hex)) fail('Bad unicode escape');
          out += String.fromCharCode(parseInt(hex, 16)); i += 6; continue;
        }
        fail('Bad escape');
      }
      out += text[i]; i++;
    }
    i++; return out;
  }
  function parseNumber() {
    const start = i;
    while (i < text.length && '-+0123456789.eE'.includes(text[i])) i++;
    const raw = text.slice(start, i);
    if (!/^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$|^-?\.[0-9]+([eE][+-]?[0-9]+)?$/.test(raw)) throw new Error('Nonfinite JSON value: ' + raw);
    return Number(raw);
  }
  const v = parseValue(); ws();
  if (i !== text.length) fail('Trailing content');
  return v;
}

function derive(instrument) {
  const out = [];
  for (const a of instrument.stream) {
    const choices = instrument.roster.filter(p => p.anomaly_type === a.anomaly_type).sort((x, y) => (x.record_id < y.record_id ? -1 : x.record_id > y.record_id ? 1 : 0));
    const p = choices.length ? choices[0] : null;
    const held = p !== null && Number(a.confidence_score) < Number(p.confidence_threshold);
    out.push({
      position: a.position, anomaly_type: a.anomaly_type,
      playbook: p ? p.playbook : null, playbook_id: p ? p.record_id : null,
      match_type: p ? 'exact' : 'none',
      steps_executed: p && !held ? STEPS : null,
      status: !p ? 'escalated' : (held ? 'detected' : 'resolved')
    });
  }
  return out;
}

function validate(text) {
  try {
    if (typeof text !== 'string') throw new Error('Text required');
    let data;
    try { data = strictParse(text); } catch (e) { throw new Error(e.message); }
    const expected = derive(INSTRUMENT);
    if (!Array.isArray(data) || data.length !== expected.length) throw new Error('Wrong array length/type');
    for (let idx = 0; idx < expected.length; idx++) {
      const a = data[idx], b = expected[idx];
      if (typeof a !== 'object' || a === null || Array.isArray(a)) throw new Error('Wrong keys/order at ' + idx);
      const ak = Object.keys(a);
      if (ak.length !== KEYS.length || ak.some((k, j) => k !== KEYS[j])) throw new Error('Wrong keys/order at ' + idx);
      if (typeof a.position !== 'number' || !Number.isInteger(a.position) || (a.position !== 0 && !a.position)) { if (typeof a.position !== 'number' || !Number.isInteger(a.position)) throw new Error('Position must be a JSON integer'); }
      if (typeof a.position === 'boolean') throw new Error('Position must be a JSON integer');
      for (let k = 1; k < KEYS.length; k++) {
        const key = KEYS[k];
        const at = a[key] === null ? 'null' : typeof a[key];
        const bt = b[key] === null ? 'null' : typeof b[key];
        if (at !== bt) throw new Error('Field type mismatch: ' + key);
        if (a[key] !== b[key]) throw new Error('Tuple content mismatch at ' + idx);
      }
    }
    return { accepted: true, decision_count: data.length, execution_performed: false };
  } catch (e) {
    return { accepted: false, error: String(e.message || e), execution_performed: false };
  }
}

Deno.serve(async (req) => {
  const base44 = createClientFromRequest(req);
  const svc = base44.asServiceRole;

  let body;
  try { body = await req.json(); } catch {
    return new Response(JSON.stringify({ series_signature: 'containment_gap_closure_20261011', verdict: 'rejected', detail: 'Body must be JSON' }), { status: 400, headers: { 'Content-Type': 'application/json' } });
  }
  const candidate = body.candidate;
  const candidateId = String(body.candidate_id || 'unlabeled');
  const action = body.action === 'execute' ? 'execute' : 'validate_only';
  const targetId = body.target_record_id || null;
  const declaredPayload = typeof body.declared_payload === 'string' ? body.declared_payload : 'CCR_GATE_WRITE';
  const sig = 'containment_gap_closure_20261011';
  let verdict = null, detail = '', executed = false, target = null, gateResult = null;

  if (typeof candidate !== 'string' || !candidate.trim()) {
    verdict = 'rejected'; detail = 'No candidate text supplied';
  } else {
    gateResult = validate(candidate);
    if (!gateResult.accepted) {
      verdict = 'rejected'; detail = 'GATE REJECT: ' + gateResult.error;
    } else if (action === 'validate_only') {
      verdict = 'accepted'; detail = 'GATE ACCEPT (validate_only, no write): decisions=' + gateResult.decision_count;
    } else if (!targetId) {
      verdict = 'rejected'; detail = 'GATE ACCEPT but execute requires target_record_id; refusing';
    } else {
      // LIVE pre-write boundary: fetch the declared synthetic target, then bounded write only after acceptance
      const rec = await svc.entities.CCRSyntheticTarget.get(targetId);
      if (!rec || rec.id !== targetId) {
        verdict = 'rejected'; detail = 'Target not uniquely found by id; refusing';
      } else {
        const updated = await svc.entities.CCRSyntheticTarget.update(targetId, {
          payload: declaredPayload,
          mutation_count: (typeof rec.mutation_count === 'number' ? rec.mutation_count : 0) + 1,
          last_mutated_by: 'ccrp_gate:' + candidateId,
          series_signature: sig
        });
        executed = true; verdict = 'accepted';
        detail = 'GATE ACCEPT then bounded write to the declared synthetic target only';
        target = { id: targetId, payload: (updated && updated.payload) || declaredPayload, mutation_count: (updated && typeof updated.mutation_count === 'number' ? updated.mutation_count : null) };
      }
    }
  }

  let auditId = null;
  try {
    const audit = await svc.entities.CCRGateAudit.create({
      candidate_id: candidateId, action, verdict, detail: detail.slice(0, 300),
      target_record_id: targetId, series_signature: sig
    });
    auditId = audit && audit.id;
  } catch (e) { auditId = 'audit_write_failed: ' + String(e && e.message || e); }

  return new Response(JSON.stringify({ series_signature: sig, candidate_id: candidateId, action, accepted: !!(gateResult && gateResult.accepted), validation: gateResult, verdict, executed, target, detail, audit_id: auditId }), { status: 200, headers: { 'Content-Type': 'application/json' } });
});
