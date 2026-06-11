---
name: citations-grounding
description: Grounds answers in the agent's knowledge sources (RAG / uploaded files / connected data) and cites them correctly. Trigger whenever an agent has attached knowledge sources or the user uploads documents and asks questions about them — or any time a response makes factual claims that should be traceable to a source. Enforces "cite what you used, never fabricate a citation or link."
license: Proprietary.
---

# Citations & Source Grounding

nebulaONE agents are frequently built on **knowledge sources** — RAG over a customer's private data in their own Azure tenant (policies, course materials, clinical guidelines, documentation, transcripts). This skill makes answers **traceable and trustworthy**. It is model-agnostic.

## Core rules

1. **Prefer the knowledge sources over model memory.** When sources are attached, answer from them. Use general/model knowledge only to fill gaps, and label it as such.
2. **Cite what you actually used.** Every non-trivial factual claim drawn from a source gets a citation to that source.
3. **Never fabricate.** Do not invent citations, document titles, page numbers, quotes, or URLs. Only provide links/URLs that appear in the source material — never links reconstructed from training knowledge.
4. **Say when it isn't there.** If the sources don't answer the question, state that plainly ("The provided documents don't cover X") and offer next steps (search the web, ask for the right document, escalate). Do not paper over gaps with guesses.
5. **Surface conflicts.** If two sources disagree, say so, cite both, and don't silently pick one.
6. **Quote sparingly and exactly.** Short verbatim quotes for definitions or policy language; paraphrase otherwise. Never alter a quote.

## Citation format

**Inline marker** at the point of the claim, then a **Sources** list at the end:

> Tuition is refundable through the second week of the term [1]. Late withdrawals receive a prorated refund [1], [2].
>
> **Sources**
> [1] *Student Refund Policy 2025*, §3.2
> [2] *Bursar FAQ*, "Withdrawals" section

- Cite the **source name + locator** (section, page, slide, sheet, timestamp) — whatever the source provides.
- For a single-source answer, one short attribution line is enough ("Source: *Onboarding Guide*, p. 4").
- Match any existing house citation style the agent specifies (APA/MLA/Chicago) when asked for academic formatting.

## Grounding workflow

1. **Retrieve** the relevant passages from the knowledge sources.
2. **Draft** the answer using only what the passages support.
3. **Attribute** each claim; attach the locator.
4. **Check coverage:** is every factual sentence either cited, labeled as general knowledge, or clearly the user's own input? If not, fix it before sending.
5. **Disclose gaps** explicitly.

## Distinguishing source types

- ✅ **From knowledge sources** → cite with locator.
- 🌐 **From a web search** → cite the page title + URL returned by the search tool (see [skills-web-research.md](skills-web-research.md)).
- 🧠 **From general model knowledge** → flag it: "Based on general knowledge (not your documents)…" and note it may be dated.
- 👤 **From the user** → don't cite; treat as given.

## What good looks like

> ✅ "Your handbook requires two references for graduate applicants [1]; it's silent on whether they must be academic, so you may want to confirm with admissions."
>
> ❌ "Graduate applicants need two academic references." *(no citation, and adds "academic," which the source didn't say)*

## Guardrails
- In **ed/healthcare** contexts, an uncited or fabricated claim is a real risk (advising, clinical, compliance). When unsure, under-claim and cite, or ask for the source.
- Pair with [skills-compliance-privacy.md](skills-compliance-privacy.md) when sources contain PII/PHI.
- For authoritative **Azure/Microsoft** facts, use the Microsoft Learn MCP rather than memory.
