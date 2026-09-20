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

echo "contract validation passed"
