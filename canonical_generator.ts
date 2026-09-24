export default async function generateSyntheticTelemetry(req: any) {
  const { batch_id, seed, event_count = 12, tenant = "SIMZ", chaos = false } = req || {};
  if (!batch_id || !seed) { return { error: "batch_id and seed are required" }; }

  // ---- CANONICAL DETERMINISTIC PRNG (H-Line standard, identical on all arms) ----
  function xmur3(str: string) {
    let h = 1779033703 ^ str.length;
    for (let i = 0; i < str.length; i++) {
      h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
      h = (h << 13) | (h >>> 19);
    }
    return function () {
      h = Math.imul(h ^ (h >>> 16), 2246822507);
      h = Math.imul(h ^ (h >>> 13), 3266489909);
      return (h ^= h >>> 16) >>> 0;
    };
  }
  function mulberry32(a: number) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const seedFn = xmur3(`${batch_id}::${seed}::${tenant}`);
  const rand = mulberry32(seedFn());

  // ---- CANONICAL EVENT MENU (identical on all arms) ----
  const MENU = [
    { event_type: "sign_in_failure_storm", category: "Identity", component: "entra-signin" },
    { event_type: "mailbox_latency_spike", category: "Exchange", component: "exchange-mailbox" },
    { event_type: "device_compliance_drift", category: "Intune", component: "intune-device" },
    { event_type: "storage_quota_pressure", category: "SharePoint", component: "sharepoint-storage" },
    { event_type: "license_anomaly", category: "Entra", component: "entra-license" },
    { event_type: "agent_heartbeat_miss", category: "Platform", component: "orchestrator-heartbeat" },
    { event_type: "service_unreachable", category: "Platform", component: "service-endpoint" },
    { event_type: "rate_limit_abuse_burst", category: "Platform", component: "gateway-throttle" },
  ];
  function severityFor(r: number): string {
    if (r < 0.5) return "low";
    if (r < 0.82) return "medium";
    if (r < 0.95) return "high";
    return "critical";
  }
  function pick(arr: any[], r: number) { return arr[Math.floor(r * arr.length) % arr.length]; }

  // ---- GENERATE THE SEQUENCE ----
  const events: any[] = [];
  const n = Math.max(1, Math.min(500, Math.floor(event_count)));
  for (let i = 0; i < n; i++) {
    const item = pick(MENU, rand());
    const severity = severityFor(rand());
    const component = `${item.component}-${String(Math.floor(rand() * 500)).padStart(3, "0")}`;
    events.push({
      tenant,
      event_type: item.event_type,
      category: item.category,
      component,
      severity,
      batch_id,
      seed,
      source: "synthetic_generator",
      payload: { index: i, synthetic: true },
      processed: false,
      timestamp: Date.now(),
    });
  }
  // Chaos mode (War/Death contention arms): deterministic cascade + burst suffix
  if (chaos === true) {
    const base = events[events.length - 1];
    for (let i = 0; i < 4; i++) {
      const item = pick(MENU, rand());
      events.push({
        tenant,
        event_type: i < 2 ? "cascading_failure" : "rate_limit_abuse_burst",
        category: item.category,
        component: `${base.component}-chaos${i}`,
        severity: i < 2 ? "high" : "critical",
        batch_id,
        seed,
        source: "synthetic_generator_chaos",
        payload: { index: n + i, synthetic: true, chaos: true },
        processed: false,
        timestamp: Date.now(),
      });
    }
  }

  // ---- CANONICAL CHECKSUM: FNV-1a 32-bit over type|component|severity sequence ----
  let h = 0x811c9dc5;
  for (const e of events) {
    const s = `${e.event_type}|${e.component}|${e.severity}`;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 0x01000193);
    }
  }
  const checksum = `0x${(h >>> 0).toString(16).padStart(8, "0")}`;

  // ---- PERSIST ----
  const created = await base44.entities.SimTelemetryEvent.create(events);
  await base44.entities.BenchmarkBatch.create({
    batch_id, seed, tenant,
    event_count: events.length,
    generated_at: new Date().toISOString(),
    status: "generated",
    notes: chaos ? "chaos-injected canonical batch" : "canonical batch",
  });

  return { batch_id, generated: created ? events.length : 0, event_count: events.length, checksum, tenant, chaos: chaos === true };
}
