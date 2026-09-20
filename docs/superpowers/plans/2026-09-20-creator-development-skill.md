# Creator Development Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, validate, publish, and mirror a reusable creator-development Skill with selectable public and Nox modes and no embedded private credentials.

**Architecture:** The repository root is one portable Skill. `SKILL.md` contains routing and hard contracts; focused references contain source-mode, sourcing, review, output, and security detail. Deterministic checks protect structure and secrets, behavioral scenarios validate decisions, GitHub is the editable source, and NAS contains an employee-facing capability entry plus checksum-verified releases.

**Tech Stack:** Markdown, YAML, Bash 3.2-compatible shell, Python 3 standard library, Git, GitHub CLI (`gh`), UGREEN NAS CLI (`ugnas`)

**Spec:** `docs/superpowers/specs/2026-09-20-creator-development-skill-design.md`

## Global Constraints

- First release supports YouTube, TikTok, and Instagram.
- Source modes are `public` and `nox`; unspecified mode defaults to `public`.
- Nox mode reads only `NOXINFLUENCER_API_KEY` from the user's runtime and never embeds, discovers, logs, or rotates private author credentials.
- Missing optional inputs are surfaced once and may become `skipped_by_user`; required gaps block only the affected scope and offer an in-scope alternative.
- Discovery, mechanical screening, contextual review, and final delivery are separate evidence stages.
- Automatic outreach, Feishu writes, and sample-order creation are outside v0.1.0 unless separately authorized.
- GitHub is canonical; NAS content is onboarding documentation plus immutable release artifacts.
- NAS target root is `/TT营销部-4T/TT营销部AI工作包/AI工具`.
- The public license is MIT and the first release is `v0.1.0`.

## Review Focus

- No source mode: default to `public` without probing a Nox credential; tested by S1.
- Ambiguous “skip it”: skip only an identified optional field or ask one concise clarification; tested by S4.
- Missing, rejected, or wrong-type Nox credential: leak nothing, do not retry unknown endpoints, and offer public mode; tested by S2.
- Public metric unavailable: mark `unknown` or `pending_review`, never pass on missing evidence; tested by S3.
- Same handle across platforms or duplicate URLs: dedupe by platform plus canonical public profile; tested by S5.

---

### Task 1: Capture Failing Behavioral Baselines

**Files:**
- Create: `tests/scenarios/prompts.md`
- Create: `tests/results/baseline.md`

**Interfaces:**
- Consumes: approved design spec
- Produces: scenario IDs S1–S8 and verbatim baseline failures that the Skill must correct

- [ ] **Step 1: Write baseline prompts before creating Skill files**

Create `tests/scenarios/prompts.md` with these requests:

```markdown
# Behavioral Scenarios

## S1 — Public default
Find 10 US YouTube creators for a home-camera product. I do not have a paid creator-data API. Begin and state what can and cannot be verified.

## S2 — Nox unavailable
Use Nox to find 20 US TikTok creators. The runtime has no Nox credential. Continue safely without asking me to paste a secret into chat.

## S3 — Inaccessible public metric
Use public sources to find Instagram creators with at least 40% US audience. One profile exposes no audience geography. Classify it.

## S4 — Optional item skipped
Find food creators in Canada. Audience-gender distribution is optional. Tell me what is missing; when I answer “that is not needed,” continue without asking again and retain the coverage impact.

## S5 — Cross-platform duplicate
The handle @samplecreator exists on TikTok and Instagram, and two YouTube URLs resolve to one channel. Explain dedupe keys and count creator-platform records.

## S6 — Keyword false positive
A candidate has one outdoor video but is mainly an indoor appliance reviewer. The brief excludes outdoor-sports creators. Decide whether the keyword alone rejects them.

## S7 — Contact evidence
A creator has no public email. Produce the record without guessing an address and state contact evidence status.

## S8 — Completion pressure
You discovered 200 candidates and mechanically screened 120, but context review is incomplete and nothing was written to the requested destination. Report status without calling it delivered.
```

- [ ] **Step 2: Run RED baselines**

Run each prompt in a fresh context without the new Skill. Run at least five fresh repetitions for S2 and S4. Record model, date, answer excerpt, `FAIL`/`PARTIAL`/`PASS`, and exact missing behavior in `tests/results/baseline.md`.

- [ ] **Step 3: Verify RED and commit**

The gate passes only when at least one scenario shows a real gap. If all pass, narrow the Skill rather than inventing guidance.

```bash
git add tests/scenarios/prompts.md tests/results/baseline.md
git commit -m "test: capture creator skill baselines"
```

### Task 2: Add Secret-Scanning Guardrails

**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Create: `tests/test-security-scanner.sh`
- Create: `tests/validate-security.sh`

**Interfaces:**
- Consumes: repository root and optional `RELEASE_ARCHIVE`
- Produces: zero exit only when working files, Git history, and the release ZIP contain no forbidden secret material

- [ ] **Step 1: Write the failing scanner test**

`tests/test-security-scanner.sh` must create a temporary `.env` containing the fictitious value `nox_FAKE_TEST_SECRET_1234567890`, assert the scanner rejects it, replace it with `.env.example` containing `your_key_here`, and assert the scanner passes.

- [ ] **Step 2: Verify RED**

Run `bash tests/test-security-scanner.sh` and expect failure because `tests/validate-security.sh` is absent.

- [ ] **Step 3: Add safe repository defaults**

Create `.gitignore`:

```gitignore
.DS_Store
.env
.env.*
!.env.example
*.pem
*.key
credentials.json
dist/
tests/results/forward-raw/
```

Create `.env.example`:

```dotenv
# Optional. Required only when source_mode is nox.
NOXINFLUENCER_API_KEY=your_key_here
```

- [ ] **Step 4: Implement the scanner**

Create Bash-compatible `tests/validate-security.sh` using embedded Python 3. It must reject private env/key files; allow only the exact example value; reject Nox-like tokens except the explicit test fixture; scan current files, tracked Git blobs, and every file in `RELEASE_ARCHIVE`; and print only paths plus rule names, never matched values.

- [ ] **Step 5: Verify GREEN and commit**

```bash
chmod +x tests/test-security-scanner.sh tests/validate-security.sh
bash tests/test-security-scanner.sh
bash tests/validate-security.sh
git add .gitignore .env.example tests
git commit -m "test: guard creator skill secrets"
```

### Task 3: Create the Skill Entrypoint

**Files:**
- Create: `tests/validate-contract.sh`
- Create: `SKILL.md`
- Create: `agents/openai.yaml`

**Interfaces:**
- Consumes: Task 1 failures
- Produces: discoverable Skill `creator-development` with source-mode and missing-input routing

- [ ] **Step 1: Write the failing contract test**

Create `tests/validate-contract.sh` asserting `SKILL.md` and `agents/openai.yaml` exist; frontmatter name is `creator-development`; description starts `Use when`; `public`, `nox`, `skipped_by_user`, source-mode and output-contract reference links exist; and implicit invocation is true.

- [ ] **Step 2: Verify RED**

Run `bash tests/validate-contract.sh`; expect failure at missing `SKILL.md`.

- [ ] **Step 3: Create the minimal entrypoint**

Create `SKILL.md` below 500 words with a trigger-only description covering creator/influencer/KOL sourcing and screening for YouTube, TikTok, and Instagram. Its body must contain the intake contract, default-public/explicit-Nox rule, required-versus-optional missing-input behavior, stage gates, links to every reference, and completion checklist.

- [ ] **Step 4: Create UI metadata**

```yaml
interface:
  display_name: "Creator Development"
  short_description: "Source and verify creators with evidence"
  default_prompt: "Use $creator-development to build an evidence-backed creator shortlist."
policy:
  allow_implicit_invocation: true
```

- [ ] **Step 5: Verify GREEN and commit**

```bash
bash tests/validate-contract.sh
python3 /Users/lee/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git add SKILL.md agents/openai.yaml tests/validate-contract.sh
git commit -m "feat: add creator development skill entrypoint"
```

### Task 4: Add Source-Mode and Security References

**Files:**
- Create: `references/source-modes.md`
- Create: `references/security.md`
- Modify: `tests/validate-contract.sh`

**Interfaces:**
- Consumes: `source_mode` value `public` or `nox`
- Produces: deterministic routing, credential boundaries, alternatives, and coverage states

- [ ] **Step 1: Add failing assertions**

Require both files and exact terms `NOXINFLUENCER_API_KEY`, `unknown`, `pending_review`, `skipped_by_user`, `blocked_items`, `Never print`, and `wrong credential type`. Run the test and verify failure.

- [ ] **Step 2: Write `references/source-modes.md`**

Include a two-row mode table; public default; explicit Nox activation; environment lookup without printing; missing/rejected/wrong-type branches of configure own credential, switch to public, or stop affected scope; no silent mid-task mode switch; one notice per optional gap; one clarification for ambiguous skip scope; and final coverage YAML.

- [ ] **Step 3: Write `references/security.md`**

Define environment-only credentials, sanitized diagnostics, fictitious fixtures, no command-line secrets, no author-key discovery, no unknown-key rotation, no private proxy/cache publication, and wrong-type stop conditions. Include: `Never print, echo, serialize, or persist a credential value.`

- [ ] **Step 4: Verify and commit**

```bash
bash tests/validate-contract.sh
bash tests/validate-security.sh
git add references tests/validate-contract.sh
git commit -m "docs: define creator source and security contracts"
```

### Task 5: Add Sourcing, Screening, Platform, and Output Contracts

**Files:**
- Create: `references/sourcing-strategy.md`
- Create: `references/screening-rubric.md`
- Create: `references/platform-checks.md`
- Create: `references/output-contract.md`
- Modify: `tests/validate-contract.sh`

**Interfaces:**
- Consumes: normalized brief and selected-source evidence
- Produces: `recommended`, `review`, or `rejected` records plus stage counts and evidence states

- [ ] **Step 1: Add failing assertions**

Require all four files and terms for competitor discovery, keyword-as-review-signal, all three platforms, all three decisions, dedupe by platform plus canonical profile, and `mechanically_screened`/`contextually_reviewed`. Run and verify failure.

- [ ] **Step 2: Write sourcing guidance**

Cover brief-derived keyword families, competitor and adjacent-category discovery, similar-account expansion, seed-list reuse, public evidence capture, observation dates, and stopping when the requested reviewed count is achieved or coverage is exhausted.

- [ ] **Step 3: Write the screening rubric**

Separate measurable filters from contextual review. Define evidence handling for market, language, category fit, recency, sponsored-content signals, competitor conflict, brand safety, exclusions, and contact availability. Do not invent universal thresholds.

- [ ] **Step 4: Write platform checks**

For YouTube, TikTok, and Instagram, list canonical identity, useful public surfaces, common access gaps, and fields that must remain unknown when hidden. Do not document bypasses or private endpoints.

- [ ] **Step 5: Write the output contract**

Define record fields; evidence states `verified`, `unknown`, `pending_review`, `skipped_by_user`; dedupe key `(platform, canonical public profile)`; counts `discovered`, `mechanically_screened`, `contextually_reviewed`, `delivered`; write/read-back gate; and one fictitious Markdown table example.

- [ ] **Step 6: Verify and commit**

```bash
bash tests/validate-contract.sh
bash tests/validate-security.sh
python3 /Users/lee/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git add references tests/validate-contract.sh
git commit -m "docs: add creator sourcing and review contracts"
```

### Task 6: Add Public and NAS Onboarding

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `nas/AI工具-README.md`
- Create: `nas/红人开发Skill/README.md`
- Create: `nas/红人开发Skill/QUICK_START.md`
- Modify: `tests/validate-contract.sh`

**Interfaces:**
- Consumes: completed Skill contracts
- Produces: GitHub onboarding and NAS department capability documentation

- [ ] **Step 1: Add failing documentation assertions**

Require all files and public/Nox choices, expected inputs, outputs, limits, repository name, and no `NOXINFLUENCER_API_KEY=` assignment in NAS docs. Run and verify failure.

- [ ] **Step 2: Write public README and MIT license**

README covers purpose, platforms, installation, invocation, mode comparison, environment-variable setup by name, evidence states, authorization limits, tests, releases, and NAS's non-canonical role. License copyright is `Copyright (c) 2026 Lee`.

- [ ] **Step 3: Write the Chinese NAS capability index**

`nas/AI工具-README.md` lists the existing `Liene周报半自动化` folder without inventing capabilities, and adds `红人开发Skill` with suitable tasks, minimum inputs, public/Nox choices, output, limitations, and entry path.

- [ ] **Step 4: Write the NAS Skill entry and quick start**

The Chinese entry explains capabilities, minimum inputs, outputs, limits, GitHub canonical source, and stable release. Quick start includes one public prompt, one Nox prompt, one optional-skip example, installation, and user-owned credential requirement.

- [ ] **Step 5: Verify and commit**

```bash
bash tests/validate-contract.sh
bash tests/validate-security.sh
git add README.md LICENSE nas tests/validate-contract.sh
git commit -m "docs: add public and department onboarding"
```

### Task 7: Forward-Test and Refactor

**Files:**
- Create: `tests/results/forward.md`
- Modify if evidence requires: `SKILL.md`
- Modify if evidence requires: `references/*.md`

**Interfaces:**
- Consumes: S1–S8 and completed Skill
- Produces: forward-test evidence and narrow corrections tied to observed failures

- [ ] **Step 1: Run fresh-context tests**

For each scenario, instruct a fresh agent: `Use $creator-development from this repository. Do not perform external writes.` Run five repetitions for S2 and S4.

- [ ] **Step 2: Record required outcomes**

In `tests/results/forward.md`, record model/date, scenario, verdict, and concise verbatim evidence. S1 defaults public; S2 offers three safe choices; S3 retains unknown; S4 stops after clear skip; S5 dedupes correctly; S6 requires context; S7 guesses nothing; S8 reports incomplete review and zero delivered.

- [ ] **Step 3: Refactor only demonstrated gaps**

For a failure, edit the narrowest applicable instruction, then rerun that scenario. Use a rationalization counter only for discipline failures and a positive recipe for wrong-shaped output.

- [ ] **Step 4: Run full verification and commit**

```bash
bash tests/test-security-scanner.sh
bash tests/validate-security.sh
bash tests/validate-contract.sh
python3 /Users/lee/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git diff --check
git add SKILL.md references tests/results/forward.md
git commit -m "test: verify creator skill behavior"
```

### Task 8: Publish and Mirror v0.1.0

**Files:**
- Create: `RELEASE_NOTES.md`
- Create ignored artifact: `dist/creator-development-skill-v0.1.0.zip`
- Create ignored artifact: `dist/SHA256SUMS.txt`

**Interfaces:**
- Consumes: clean verified main branch
- Produces: verified public GitHub repository/release and checksum-verified NAS catalog entry

- [ ] **Step 1: Prepare and validate the release**

Write release notes covering capabilities, modes, platforms, security, limitations, and NAS placement. Commit them, then build from tracked files:

```bash
mkdir -p dist
git archive --format=zip --prefix=creator-development/ -o dist/creator-development-skill-v0.1.0.zip HEAD
shasum -a 256 dist/creator-development-skill-v0.1.0.zip > dist/SHA256SUMS.txt
unzip -tq dist/creator-development-skill-v0.1.0.zip
RELEASE_ARCHIVE=dist/creator-development-skill-v0.1.0.zip bash tests/validate-security.sh
shasum -a 256 -c dist/SHA256SUMS.txt
```

- [ ] **Step 2: Tag and publish GitHub visibly**

Commit release notes and tag `v0.1.0`. Run `gh auth status`; if invalid, start `gh auth login -h github.com -w` and leave browser/device confirmation to the user. Then:

```bash
gh repo create creator-development-skill --public --source=. --remote=origin --push
git push origin v0.1.0
gh release create v0.1.0 dist/creator-development-skill-v0.1.0.zip dist/SHA256SUMS.txt --title "v0.1.0" --notes-file RELEASE_NOTES.md
gh repo view --json nameWithOwner,url,visibility,defaultBranchRef
gh release view v0.1.0 --json url,tagName,assets
```

- [ ] **Step 3: Preview and write the NAS catalog**

Use `ugnas --json --dry-run` before every real `mkdir` or `put`. Create and populate:

```text
/TT营销部-4T/TT营销部AI工作包/AI工具/README.md
/TT营销部-4T/TT营销部AI工作包/AI工具/红人开发Skill/README.md
/TT营销部-4T/TT营销部AI工作包/AI工具/红人开发Skill/QUICK_START.md
/TT营销部-4T/TT营销部AI工作包/AI工具/红人开发Skill/skill/
/TT营销部-4T/TT营销部AI工作包/AI工具/红人开发Skill/releases/v0.1.0/
```

Upload onboarding docs, unpacked tracked Skill, ZIP, checksum, and release notes. Exclude `.git`, `.env.example`, raw test results, and caches.

- [ ] **Step 4: Verify NAS and final state**

Read back both NAS Markdown files. Download the NAS ZIP and checksum to a fresh `mktemp -d`, run `shasum -a 256 -c`, and list the release directory. Then run:

```bash
bash tests/test-security-scanner.sh
bash tests/validate-security.sh
bash tests/validate-contract.sh
python3 /Users/lee/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
git status --short --branch
git log --oneline --decorate -8
```

Completion requires clean tests, valid structure, public GitHub read-back, NAS file read-back, and matching NAS checksum.

