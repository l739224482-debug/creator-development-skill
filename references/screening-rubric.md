# Screening Rubric

Apply brief-specific numeric thresholds mechanically only when the metric and source are comparable. A keyword is a review signal, not a decision.

Contextually review:

- market and language evidence;
- predominant category, use cases, and product fit;
- recent activity and content consistency;
- sponsored-content and repeated-ad signals;
- competitor conflicts and exclusivity evidence;
- brand-safety issues and task-specific exclusions;
- public or authorized contact evidence.

Decisions:

- `recommended`: all required checks are verified and no blocking conflict remains.
- `review`: promising, but a required contextual judgment or resolvable evidence gap remains.
- `rejected`: a verified gating condition fails; name the evidence and rule.

Do not invent universal follower, engagement, view, or audience thresholds. Preserve hidden fields as `unknown`; never infer an email address or audience demographic from appearance, language, or location alone.
