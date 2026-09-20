# Source Modes and Missing Inputs

| Mode | Select when | Evidence boundary |
|---|---|---|
| `public` | Default, or user chooses public research | Use accessible public pages and search results; hidden provider metrics remain `unknown`. |
| `nox` | User explicitly chooses Nox and configures their own runtime credential | Use only fields whose semantics the authorized Nox tool exposes; do not assume a CLI credential is a REST credential. |

## Nox activation

Read `NOXINFLUENCER_API_KEY` from the runtime without displaying its value. If it is missing, rejected, or the wrong credential type, offer exactly these paths: configure a user-owned compatible credential, switch the affected work to `public`, or stop that scope. Do not silently switch modes after billable work starts.

## Missing inputs

Classify each consequential gap as required or optional. For an optional gap, notify once with its effect and offer provide/default/skip. Record a clear refusal as `skipped_by_user`; do not ask again. If “skip” could name more than one field, ask one scope question. Put unresolved gates in `blocked_items`. Publicly inaccessible data is `unknown`; evidence needing human context is `pending_review`.

```yaml
source_mode: public
verified_fields: []
unknown_fields: []
skipped_by_user: []
blocked_items: []
```

## Nox credit settlement

Settle credits after every Nox task, including partial failures:

1. Use `response_metadata` only when provider documentation or the authorized tool defines the field as this task's usage.
2. Otherwise use `balance_delta` only when before/after balances use the same credential and no concurrent consumer can affect them.
3. When semantics, snapshots, or isolation are missing, use `unavailable`; never infer zero.
4. Public mode uses `not_applicable`.

```yaml
nox_credit_usage:
  status: verified
  consumed: 12
  remaining: 88
  measurement: response_metadata
  observed_at: 2026-09-20T18:30:00-07:00
```

For an unavailable settlement, set `consumed` and `remaining` to `unknown`, set `measurement: unavailable`, and explain the evidence gap without exposing account identity.
