# Output Contract

Deduplicate by platform plus canonical public profile. Identical handles across platforms remain separate creator-platform records; multiple URLs resolving to one platform identity become one record.

Each record includes platform, public handle, canonical URL, market/language evidence, content-fit evidence, dated metrics and sources, contact status, risk signals, decision, reason, and field evidence states: `verified`, `unknown`, `pending_review`, or `skipped_by_user`.

Allowed decisions are `recommended`, `review`, and `rejected`, using the definitions in the screening rubric.

```markdown
| Platform | Creator | Evidence | Contact | Decision | Reason |
|---|---|---|---|---|---|
| YouTube | @ExampleKitchen | 8/10 recent videos match home cooking; observed 2026-09-20 | no public email found | review | audience geography unknown |
```

Report counts separately:

```yaml
discovered: 200
mechanically_screened: 120
contextually_reviewed: 45
delivered: 30
```

Counts must reconcile with record states. Candidate discovery, a running process, or a generated file is not delivery. An authorized external write is complete only after write confirmation and read-back.

For every task include coverage (`verified_fields`, `unknown_fields`, `skipped_by_user`, `blocked_items`). For Nox mode also include:

```yaml
nox_credit_usage:
  status: verified
  consumed: 12
  remaining: 88
  measurement: response_metadata
  observed_at: 2026-09-20T18:30:00-07:00
```

Allowed credit status values are `verified`, `unavailable`, and `not_applicable`. `balance_delta` is valid only for isolated same-credential snapshots. When attribution is not deterministic, use `unknown` amounts and `measurement: unavailable`, not zero.
