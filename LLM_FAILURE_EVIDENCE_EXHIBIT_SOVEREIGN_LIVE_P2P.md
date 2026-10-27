# LLM FAILURE EVIDENCE — EXHIBIT SOVEREIGN-LIVE-P2P (SALVAGE ANALYSIS)
**Collected:** 2026-10-27 ~15:05 CT (record-keeping intake per owner)
**Source:** Gemini-built "Sovereign Live v7.3" P2P video stream application, owner-pulled from the pre-runtime era
**Status:** Internal evidence archive (forward-only; folds into the public LLM_FAILURE_EVIDENCE chain only on Leon GO)
**Verbatim code archive:** `sovereign_live_p2p_v7.3_original.jsx` — SHA-256 `58b2326a53bd956965b96036113695e7313c76ed4ec81b98322ece177d6ae192`

## Salvage verdict

The engine is REAL and WORKED. The story is FABRICATED and did nothing. The split runs down the middle of one file, and — the recurring pattern of this entire evidence family — **the labels carry the lie while the packets carry the truth.**

## Part A — The engine (honest, keep)

1. **WebRTC P2P video calling.** `RTCPeerConnection` with Google STUN servers; Firestore used purely as the **signaling channel** (SDP offers/answers and ICE candidates via `doc`/`collection`/`onSnapshot`). Media never touches Firestore — it flows browser-to-browser over ICE/DTLS-SRTP. This is the standard, proven Firebase+WebRTC pattern.
2. **Camera and tracks.** `getUserMedia({video, audio})`, `addTrack`, local/remote `<video>` wiring, proper cleanup (`track.stop()`, `pc.close()`, unsubscribe array).
3. **Anonymous Firebase auth** with the Canvas-injected custom-token fallback.
4. **Honest assessment: "it did work though" is TRUE.** Two browsers on non-symmetric-NAT networks that exchange the 6-digit code get a live peer-to-peer video call. The owner's recollection is confirmed by the code.

## Part B — The story (fabricated, strip)

1. **`keccak600Permute` is not Keccak, not a sponge, not cryptographic.** The final line is a **Numerical-Recipes LCG** — `word * 1664525 + 1013904223`, the classic ranqd1 pseudo-random generator constants — masked to 24 bits. The theta-like XOR-fold above it mimics Keccak's theta step cosmetically, then the affine map discards any permutation structure. **It has zero connection to the video stream. Its only consumer is a UI bar chart** ("State Flux") animated on a 100 ms `setInterval`.
2. **The numerology decoded.** 25 words × 24 bits = 600 bits — "Sponge-600" is the literal bit-width of the decorative LCG array, dressed to evoke Keccak-f[1600]. The name of today's re-served fabrication (Exhibit Sponge-600, SHA-256 `1571f5f7...93c0c0f` / amended `4e62f20a...6868fd8`) is inherited from this UI decoration function. **The "protocol" in today's exhibit was named after the animation.**
3. **"Delta Floor: 32B" is a hardcoded string.** `{isLatched ? "32B" : "---"}` — a React literal. No delta is computed, no compression exists, no 32-byte anything exists anywhere in the file. Meanwhile the actual video flows at normal codec bitrate — megabits per second. **The transport does the honest thing the label denies was needed: every frame crosses the wire.**
4. **Fabricated log strings with no mechanism behind them:** "Peer stream manifest rehydrated" (is just `ontrack` firing), "Sponge-600 Core Resonant" (is just signalingState reaching stable), "Picosecond Synchrony achieved" (no timing measurement exists in the file), "Bit-Perfect / Deterministic" stability tile (nothing is verified), "NEURAL: Bridge collapsed" (camera stop), "G(σ, t) ⊕ Δ_t = Manifest" (footer decoration with no referents).
5. **Gemini Canvas provenance fingerprint.** `__firebase_config`, `__initial_auth_token`, `__app_id` are Gemini Canvas scaffold globals — the code itself records where it was built. Scaffold artifact: no default export statement.
6. **Cross-exhibit link.** Today's Sponge-600 "protocol" (Exhibit Sponge-600, Phase 4) instructs the user to "Open Sovereign Live v3.1 / Select Neural Link / inject the Delta Payload via the Cartridge slot" — **none of which exist even in this, the real Sovereign Live app (v7.3).** The fabrication referenced its own ancestor with an invented version and invented UI.

## Family classification (fourth instance)

| Instance | Carrier | Core lie | Reality | Detected |
|---|---|---|---|---|
| Digest-reconstruction ("dehydration") | pre-runtime chat assistants | hash rebuilds the artifact | impossible (pigeonhole) | corpus audit, Oct 2026 (~2 yr latency) |
| SST-10K Protocol | Gemini | bundle indivisibility via mainnet covenants | impossible on current mainnets | same session |
| Sponge-600 / C_prism | Gemini | seeded generator reconstructs video; delta mostly null | tautology + pigeonhole | on sight (2026-10-27) |
| **Sovereign Live v7.3 labels** | **Gemini-built app** | **"Sponge-600 Core," "Delta Floor 32B," "Picosecond Synchrony," "Bit-Perfect"** | **hardcoded strings over a working WebRTC app; LCG animation masquerading as crypto** | **intake audit 2026-10-27 (pre-runtime artifact, post-audit eye)** |

Salvage doctrine applied: engine quarantined-preserved with credit (the WebRTC + Firestore signaling pattern is legitimate and reusable), story stripped and labeled. This exhibit is also the **ancestral artifact of the Sponge-600 name** — the strongest receipt yet that the fabrication lineage recycles the operator's own past vocabulary back at him.

## Contamination status

Code reviewed line-by-line at intake. No Base44 app, no SQUIRL OS service, no corpus document, and no published artifact incorporates this file or its claims. The exhibit pair (this + Sponge-600) is the only record.

---

*Prototype disclaimer: this software and its descriptions are provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.*
