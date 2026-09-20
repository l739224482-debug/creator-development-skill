#!/usr/bin/env bash
set -euo pipefail

test -f SKILL.md
test -f agents/openai.yaml
grep -q '^name: creator-development$' SKILL.md
grep -q '^description: Use when ' SKILL.md
grep -qi 'source mode' SKILL.md
grep -q 'public' SKILL.md
grep -q 'nox' SKILL.md
grep -q 'skipped_by_user' SKILL.md
grep -q 'references/source-modes.md' SKILL.md
grep -q 'references/output-contract.md' SKILL.md
grep -q 'allow_implicit_invocation: true' agents/openai.yaml
test -f references/source-modes.md
test -f references/security.md
grep -q 'NOXINFLUENCER_API_KEY' references/source-modes.md
grep -q 'unknown' references/source-modes.md
grep -q 'pending_review' references/source-modes.md
grep -q 'skipped_by_user' references/source-modes.md
grep -q 'blocked_items' references/source-modes.md
grep -q 'nox_credit_usage' references/source-modes.md
grep -q 'response_metadata' references/source-modes.md
grep -q 'balance_delta' references/source-modes.md
grep -q 'unavailable' references/source-modes.md
grep -q 'Never print' references/security.md
grep -q 'wrong credential type' references/security.md
test -f references/sourcing-strategy.md
test -f references/screening-rubric.md
test -f references/platform-checks.md
test -f references/output-contract.md
grep -qi 'competitor' references/sourcing-strategy.md
grep -qi 'keyword.*review signal' references/screening-rubric.md
grep -q 'YouTube' references/platform-checks.md
grep -q 'TikTok' references/platform-checks.md
grep -q 'Instagram' references/platform-checks.md
grep -q 'recommended' references/output-contract.md
grep -q 'review' references/output-contract.md
grep -q 'rejected' references/output-contract.md
grep -qi 'platform.*canonical public profile' references/output-contract.md
grep -q 'mechanically_screened' references/output-contract.md
grep -q 'contextually_reviewed' references/output-contract.md
grep -q 'nox_credit_usage' references/output-contract.md
test -f README.md
test -f LICENSE
test -f 'nas/AI工具-README.md'
test -f 'nas/红人开发Skill/README.md'
test -f 'nas/红人开发Skill/QUICK_START.md'
grep -qi 'public' README.md
grep -qi 'nox' README.md
grep -qi 'input' README.md
grep -qi 'output' README.md
grep -qi 'limit' README.md
grep -q 'creator-development-skill' README.md
grep -q '红人开发Skill' 'nas/AI工具-README.md'
if grep -R -q 'NOXINFLUENCER_API_KEY=' nas; then
  echo 'NAS docs must not contain credential assignments' >&2
  exit 1
fi

echo "contract validation passed"
