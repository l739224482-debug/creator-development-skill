---
name: creator-development
description: Use when sourcing, screening, qualifying, shortlisting, or reviewing creators, influencers, or KOLs for YouTube, TikTok, or Instagram, especially when a brief includes market, category, audience, contact, competitor, brand-safety, or evidence requirements.
---

# Creator Development

Build evidence-backed creator shortlists without confusing discovery, automated checks, contextual review, and delivered results.

## Intake

Establish the platform, market, category or product fit, target count, exclusions, required checks, and delivery format. Treat thresholds, audience details, contact requirements, competitor rules, and other fields as required only when the brief makes them gating conditions.

Notify the user once about each consequential missing input and explain its impact. Offer: provide it, accept a conservative default, or skip it when optional. Record an explicit skip as `skipped_by_user` and do not ask again during the task. If “skip” is ambiguous, ask one concise scope question. A required gap blocks only the affected scope; offer any valid alternative.

## Source mode

Use `public` when no mode is selected. Use `nox` only when the user explicitly selects it and supplies their own runtime credential. Read [source modes](references/source-modes.md) before any Nox call or when inputs are missing. Never treat unavailable paid-provider evidence as verified public evidence.

For every Nox-mode task, settle credit usage even after a partial failure. Report verified task consumption and remaining credits only when field semantics or isolated same-credential balance snapshots support attribution; otherwise report `unavailable`, never zero.

## Evidence stages

1. Discover candidates and retain the public handle, canonical profile, platform, source, and observation date.
2. Apply mechanical checks only to measurable requirements.
3. Contextually review content fit, recency, advertising signals, conflicts, brand safety, and exclusions. A keyword is a review signal, not a decision.
4. Classify each record as `recommended`, `review`, or `rejected` with evidence and a reason.
5. Report discovered, mechanically screened, contextually reviewed, and delivered counts separately.

Do not infer emails or hidden metrics. Do not send outreach, write external systems, or create orders without separate authorization. If authorized to write, verify the target by read-back before reporting delivery.

## References

- For discovery methods, read [sourcing strategy](references/sourcing-strategy.md).
- For review decisions, read [screening rubric](references/screening-rubric.md).
- For platform evidence, read [platform checks](references/platform-checks.md).
- For records, counts, coverage, and credits, read [output contract](references/output-contract.md).
- For credential and publication rules, read [security](references/security.md).

## Completion checklist

- Public identity and evidence accompany every decision.
- Unknown, pending, skipped, and blocked checks remain visible.
- Stage counts close against the delivered records.
- Nox credit status is included when applicable.
- External delivery is claimed only after write and read-back evidence.
