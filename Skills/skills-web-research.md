---
name: web-research
description: Uses internet search to ground answers in current, external information. Trigger when a user asks about current events, recent developments, prices, people, products, "look up / search / find / latest," or anything likely to have changed since training — and whenever a factual answer should be verified against live sources. Covers query construction, source quality, recency, and citing results.
license: Proprietary.
---

# Web Research

A quick web search should be a **default reflex**, not a last resort, for anything time-sensitive or verifiable. This skill governs how to search well and report honestly. Model-agnostic. (For answering from the customer's *private* data, use [skills-citations-grounding.md](skills-citations-grounding.md) instead.)

## When to search
- Current events, news, "latest," recent releases, schedules, prices, weather, sports.
- People, places, organizations, products — especially anything that changes over time.
- Any claim where being wrong matters and you're not certain.
- To verify or update something that might be stale in model memory.

## When *not* to search
- Stable general knowledge, definitions, math, or reasoning you can do directly.
- Looking up a **person or record from the user's private/uploaded data** — that's a privacy violation, not research (see [skills-compliance-privacy.md](skills-compliance-privacy.md)).

## Searching well
- **Keep queries tight** (≤ ~400 characters). Use specific terms, names, and dates.
- **Fan out** for multi-part or comparative questions — run several focused searches rather than one broad one.
- **Add recency cues** ("2026", "latest", a month/quarter) when freshness matters.
- **Triangulate:** confirm important facts across 2+ reputable, independent sources before stating them.
- **Prefer authoritative sources:** primary documents, official sites, established outlets, peer-reviewed work. Note when a source is a vendor, opinion, or low-reputation page.
- Pull **images** from results when the topic is visual (people, places, products) and the source provides them.

## Reporting results
- **Attribute** every searched fact to the page it came from, and end with a **Sources** list of titles + URLs you actually used.
- **Timestamp** volatile info ("As of June 2026…").
- **Flag conflicts** between sources instead of silently choosing one.
- **Don't fabricate** URLs, publication dates, or quotes. If results are thin or contradictory, say so and state your confidence.
- Separate **fact** (sourced) from **interpretation** (your analysis).

## Example pattern
> **Q:** "What's the latest on X's pricing?"
> 1. Search official site → current price.
> 2. Search a recent independent article → cross-check + context.
> 3. Answer with the figure, "as of <date>," and both sources listed.

## Tooling note
For authoritative **Microsoft/Azure** documentation, prefer the **Microsoft Learn MCP** over open web search — it returns current, canonical docs. Use Context7 for library/framework/API documentation. Use general web search for everything else.
