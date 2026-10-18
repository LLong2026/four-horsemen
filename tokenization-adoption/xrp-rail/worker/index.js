const RPC_UPSTREAM = "https://s.altnet.rippletest.net";
const FAUCET_UPSTREAM = "https://faucet.altnet.rippletest.net/accounts";
export default {
  async fetch(request) {
    const url = new URL(request.url);
    let upstream;
    if (url.pathname === "/faucet") {
      upstream = FAUCET_UPSTREAM;
    } else {
      upstream = RPC_UPSTREAM;
    }
    const resp = await fetch(upstream, {
      method: request.method,
      headers: { "Content-Type": "application/json" },
      body: request.method === "GET" ? undefined : await request.text(),
    });
    return new Response(resp.body, { status: resp.status,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
  }
};
