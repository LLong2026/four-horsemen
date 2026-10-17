# BLIND-4 Prereg Amendment v1.1 (forward-only, pre-execution)

**Reason:** The prereg's corpus-construction method (blind LLM authors) failed at the
authoring step: 8/8 independent context-blind author instances (two prompt framings:
generic adversary, then owner-commissioned preregistered red-team) REFUSED to author
impersonation/social-engineering messages. Same-family blind authors DID author technical
attacks in BLIND-1/2 — the refusal is content-class-specific (impersonation prose), not
battery-specific. This refusal is itself receipted as a **Layer-0 defense-in-depth datum**:
the authoring layer declines to produce the weapon. No corpus was produced; no execution
occurred; the corpus freeze (G5) had not yet happened when this amendment was authored.

**Amended method (supersedes prereg Method §1 only; all gates unchanged):**
Corpus authorship moves to the **GAUNTLET-M rebase standard**: 20 attack slots derived
from PUBLISHED social-engineering persuasion taxonomies, each wave carrying a public
source URL + retrieval date. Sources (retrieved 2026-10-17):
- MITRE ATT&CK T1566 Phishing family (impersonation / trusted-source posing):
  https://attack.mitre.org/techniques/T1566/
- Ferreira et al., "Principles of Persuasion in Social Engineering and Their Use in
  Phishing" (Cialdini / Gragg / Stajano taxonomies):
  https://orbilu.uni.lu/bitstream/10993/20301/1/FerreiraAna-CameraReady.pdf
- Cross et al., "How social engineers use persuasion principles during vishing attacks"
  (authority, social proof, distraction most used): https://www.emerald.com/ics/article/29/2/314/117747/
- Survey on the Principles of Persuasion as a Social Engineering Attack Vector:
  https://arxiv.org/pdf/2412.18488
- Microsoft Security, "The psychology of social engineering" (six principles):
  https://www.microsoft.com/en-us/security/blog/2020/06/30/psychology-social-engineering-soft-side-cybercrime/

The 20 slots cover the published persuasion families: authority, urgency/scarcity,
social proof/delegation, liking/relationship, reciprocity, consistency/commitment,
distraction, technical pretext, owner-unavailability delegation (BEC-style pretexts),
and financial-stakes pressure. Novelty vs the OMAHA-1 frozen fixtures is still measured (G-scan).

**Blind refusal evidence:** 8 refusal transcripts (4 + 4) preserved in blind4/refusals/.
**Gates G1-G5, predicted verdict, disclosures: unchanged** (except Method §1 superseded
herein). Single-family disclosure now covers both the (refused) blind authors and the
operator-authored research-derived corpus.
