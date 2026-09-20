# Forward-Test Results

- Date: 2026-09-20
- Context: fresh default agents loaded `SKILL.md` and linked references; exact model identifier was not surfaced.
- External writes: none.

| Scenario | Repetitions | Verdict | Evidence |
|---|---:|---|---|
| S1 | 1 | PASS | Defaulted to public; hidden metrics stayed unknown; credits were not applicable. |
| S2 | 5 | PASS | Every run protected the secret and offered configure-own-credential, switch-public, or stop. |
| S2-R | 1 | PASS | Stopped incompatible retries, sanitized diagnostics, and offered compatible credential/public/stop. |
| S3 | 1 | PASS | Unknown US audience kept the profile at review rather than passing or rejecting it. |
| S4 | 5 | PASS | Every run recorded `skipped_by_user`, retained coverage impact, and stopped asking. |
| S4-A | 1 | PASS | Asked one concise clarification before skipping either or both optional fields. |
| S5 | 1 | PASS | Platform plus canonical profile produced three creator-platform records. |
| S6 | 1 | PASS | Outdoor keyword remained a contextual review signal. |
| S7 | 1 | PASS | Missing email was explicit and never guessed. |
| S8 | 1 | PASS | Reported 200 discovered, 120 mechanically screened, incomplete review, and 0 delivered. |
| S9 | 1 | PASS | Reported 27 consumed, 93 remaining, `balance_delta`, and unavailable values when ending balance was missing. |
| S9-R | 1 | PASS | Produced verified 18 consumed, 42 remaining, and `response_metadata` from documented task fields. |
| S9-P3/P4 | 1 each | PASS | Refused task attribution for undocumented field semantics and concurrent balance use. |

## Concise evidence

> “Safe paths are exactly: configure a compatible user-owned credential in the runtime, explicitly switch this affected scope to public mode, or stop the affected scope.”

> “Recorded audience-gender distribution as skipped_by_user. I’ll continue without asking for it again.”

> “The 27-point balance drop cannot be attributed to this task because another job used the same credential concurrently.”

No demonstrated forward-test gap required a Skill change.
