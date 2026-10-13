// DR-1 entity export: snapshot a single entity for the transparency-repo backup.
// Token-gated (BASE44_API_KEY in body) — the public function URL alone yields nothing.
// Strips created_by / created_by_id server-side; returns records + count + has_more.
Deno.serve(async (req) => {
  try {
    const { createClientFromRequest } = await import("npm:@base44/sdk@0.8.31");
    const base44 = createClientFromRequest(req);
    const body = await req.json().catch(() => ({}));
    const token = Deno.env.get("BASE44_API_KEY");
    if (!token || body.token !== token) {
      return Response.json({ error: "forbidden" }, { status: 403 });
    }
    const entityName = String(body.entity || "");
    if (!/^[A-Za-z]+$/.test(entityName)) {
      return Response.json({ error: "invalid_entity_name" }, { status: 400 });
    }
    const max = Math.min(Number(body.limit) || 2000, 5000);
    const records = [];
    let skip = 0;
    let hasMore = true;
    const pageSize = 500;
    while (hasMore && records.length < max) {
      const batch = await base44.asServiceRole.entities[entityName].list({
        limit: pageSize,
        skip,
        sort: "-created_date",
      });
      for (const r of batch.items ?? batch ?? []) {
        const rec = { ...r };
        delete rec.created_by;
        delete rec.created_by_id;
        records.push(rec);
      }
      const got = (batch.items ?? batch ?? []).length;
      hasMore = got === pageSize;
      skip += got;
      if (got === 0) break;
    }
    return Response.json({
      entity: entityName,
      exported_at: new Date().toISOString(),
      count: records.length,
      has_more: hasMore,
      records,
    });
  } catch (e) {
    return Response.json({ error: String(e?.message || e) }, { status: 500 });
  }
});
