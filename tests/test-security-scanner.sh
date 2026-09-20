#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
scanner="$repo_root/tests/validate-security.sh"

test -x "$scanner"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$tmp_dir/repo/tests"
cp "$scanner" "$tmp_dir/repo/tests/validate-security.sh"
printf '%s\n' 'NOXINFLUENCER_API_KEY=nox_FAKE_TEST_SECRET_1234567890' > "$tmp_dir/repo/.env"

if (cd "$tmp_dir/repo" && bash tests/validate-security.sh >/dev/null 2>&1); then
  echo "scanner accepted a forbidden .env secret" >&2
  exit 1
fi

rm "$tmp_dir/repo/.env"
printf '%s\n' 'NOXINFLUENCER_API_KEY=your_key_here' > "$tmp_dir/repo/.env.example"
(cd "$tmp_dir/repo" && bash tests/validate-security.sh)
