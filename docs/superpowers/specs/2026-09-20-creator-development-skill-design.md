# Creator Development Skill Design

## 1. Purpose

Create a reusable, public Skill for creator discovery, qualification, evidence-based review, and delivery. It should let a new employee start from an explicit brief instead of rebuilding the workflow from scratch.

The Skill supports YouTube, TikTok, and Instagram in its first release. It does not automatically contact creators, send email or direct messages, write to Feishu, create sample orders, or make other external changes unless a user separately authorizes those actions.

## 2. Success Criteria

The first release is successful when:

- a user can choose either public-source research or their own Nox credential;
- public mode works without Nox installed or configured;
- no private Nox credential, response cache, proxy, account detail, or internal path is published;
- missing inputs are surfaced once with their impact and available alternatives;
- user-declined optional checks are recorded as `skipped_by_user` and are not requested again during the task;
- discovery, mechanical screening, contextual review, and final delivery remain distinct evidence stages;
- every final creator decision includes a public identity, evidence, decision, and reason;
- GitHub is the canonical source and the NAS provides a department-facing capability entry plus a verified stable release.

## 3. Source Modes

### Public mode

`public` is the default. It uses publicly accessible search results, creator profiles, recent public content, and other public evidence available to the executing agent. It must respect platform access constraints and must not pretend that inaccessible data was verified.

### Nox mode

`nox` is explicitly selected by the user. It reads `NOXINFLUENCER_API_KEY` from the user's runtime environment. The repository provides only a placeholder in `.env.example`.

If the credential is missing or rejected, the Skill explains the affected checks and offers three choices: configure a user-owned credential, switch to public mode, or stop the affected work. It does not search for an author's private credential, rotate through unknown keys, print the key, or silently spend another account's quota.

### Shared quality contract

Both modes use the same brief, screening rubric, review states, and output contract. A data-source limitation changes field status to `unknown` or `pending_review`; it does not lower a required threshold or convert missing evidence into a pass.

## 4. Workflow

1. Normalize the brief: platform, market, category, target count, thresholds, exclusions, required checks, and delivery format.
2. Run the missing-input contract before research.
3. Confirm `public` or `nox`; default to `public` if the user has not selected a mode.
4. Discover candidates and retain public profile identity, URL, platform, and discovery source.
5. Apply mechanical filters only to measurable criteria.
6. Perform contextual content review for category fit, recency, advertising signals, competitor conflicts, brand safety, and task-specific exclusions.
7. Verify contact information only from public evidence or an authorized source. Never infer an email address.
8. Deduplicate and classify candidates as `recommended`, `review`, or `rejected`.
9. Report stage-specific counts and produce the agreed deliverable.

A keyword or metadata hit is a review signal, not a verified decision. An internal search identifier is not a creator-facing identity; delivery uses the public handle and profile URL.

## 5. Missing-Input Contract

Before research, the Skill classifies missing inputs as required or optional.

For each optional missing input, it states:

- what is missing;
- which output or confidence level it affects;
- whether the user can provide it, accept a conservative default, or skip it.

When the user says an optional item is unnecessary, the Skill records it as `skipped_by_user`, stops asking about it for the current task, and describes the resulting coverage gap in the final output.

Required inputs cannot be silently skipped. Examples include a usable platform and market for targeted research, a user-owned credential for Nox mode, or an evidence source for a requested verified email. When a required input is absent, the Skill blocks only the affected scope and offers an in-scope alternative such as public mode.

The final coverage block contains:

```yaml
source_mode: public
verified_fields: []
unknown_fields: []
skipped_by_user: []
blocked_items: []
```

## 6. Decision and Delivery Contract

Each delivered creator record contains, when relevant:

- platform;
- public handle;
- public profile URL;
- market and language evidence;
- category/content-fit evidence;
- measurable metrics with source and observation date;
- contact evidence status;
- risk or exclusion signals;
- decision: `recommended`, `review`, or `rejected`;
- concise decision reason;
- field-level evidence states.

The completion summary separately reports:

- discovered candidates;
- mechanically screened candidates;
- contextually reviewed candidates;
- final delivered creators;
- unknown, skipped, and blocked checks.

Candidate count, process activity, or generated files alone do not prove final delivery. When the workflow writes to an external target under separate authorization, completion additionally requires write confirmation and read-back verification.

## 7. Repository Structure

```text
creator-development-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── .env.example
├── .gitignore
├── agents/
│   └── openai.yaml
├── references/
│   ├── source-modes.md
│   ├── sourcing-strategy.md
│   ├── screening-rubric.md
│   ├── platform-checks.md
│   ├── output-contract.md
│   └── security.md
├── tests/
│   ├── scenarios/
│   └── validate-security.sh
└── docs/
    └── superpowers/specs/
```

`SKILL.md` remains a concise router and contract. Conditional detail belongs in the referenced files. The public repository includes a README because discovery, installation, security expectations, and contributor use are part of the publishing requirement.

## 8. Security and Privacy

- The repository never stores real credentials.
- `.env*` is ignored except `.env.example`.
- Examples and tests use obvious fictitious values.
- Secrets are not passed in command arguments or printed in logs.
- Error text and fixtures are sanitized before persistence.
- Security validation scans file contents, filenames, the Git history, and the exact release archive.
- Nox account balances, quota history, private proxies, internal creator databases, and private project paths are excluded from the public artifact.
- Test execution must not read the author's real Nox environment variable.

## 9. Testing Strategy

Skill behavior follows a RED-GREEN-REFACTOR process.

Baseline scenarios run without the Skill to capture failures such as silent fallback, credential requests, repeated optional-field prompting, premature completion, guessed contact information, or loss of evidence states. The same scenarios then run with the Skill and must satisfy the contract.

Required scenarios include:

- public mode with no Nox credential;
- Nox mode with a missing credential;
- rejected or wrong-type Nox credential;
- optional input declined by the user;
- required input missing with a viable public-mode alternative;
- inaccessible metric represented as unknown;
- mechanical keyword hit requiring contextual review;
- output that distinguishes all workflow stages;
- logs and archives that contain no credential material.

The release gate includes Skill structure validation, scenario review, shell checks, link checks, secret scanning, archive inspection, and a clean Git status. Tests use fictitious credentials only.

## 10. Publishing and Versioning

The local canonical checkout is `/Users/lee/Documents/creator-development-skill`. The intended public GitHub repository is `creator-development-skill`, licensed under MIT. The first release is `v0.1.0`.

GitHub is the only editable source of truth. The current GitHub CLI session must be reauthenticated before remote repository creation or push. No publication claim is made until the remote repository and tag are verified.

## 11. NAS Department Capability Catalog

The NAS placement is not merely a backup. It is a department-facing AI capability catalog for onboarding and reuse.

Root:

```text
/TT营销部-4T/TT营销部AI工作包/AI工具/
```

Target layout:

```text
AI工具/
├── README.md
├── Liene周报半自动化/
└── 红人开发Skill/
    ├── README.md
    ├── QUICK_START.md
    ├── skill/
    └── releases/
        └── v0.1.0/
            ├── creator-development-skill-v0.1.0.zip
            ├── SHA256SUMS.txt
            └── RELEASE_NOTES.md
```

The root `README.md` acts as the department capability index. The creator Skill entry tells a new employee what it can do, the minimum inputs, public-versus-Nox choices, expected outputs, limitations, a one-line invocation example, the canonical GitHub URL, and the current stable release.

NAS content contains no `.env`, caches, private logs, or credentials. Every write is previewed with `--dry-run`; uploaded artifacts are read back or downloaded and checksum-verified. NAS copies are release artifacts and onboarding documents, not editable source.

The neighboring `CP工作流` remains separate because it contains project-isolated internal Agent rules rather than employee-facing reusable tools.

## 12. Non-Goals for v0.1.0

- automatic creator outreach;
- automatic email or direct-message sending;
- Feishu writes or sample-order creation;
- a hosted web application;
- private creator-database redistribution;
- exact parity between public data and paid provider data;
- automatic use of a fallback credential owned by the Skill author.

