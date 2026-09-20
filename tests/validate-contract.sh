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

echo "contract validation passed"
