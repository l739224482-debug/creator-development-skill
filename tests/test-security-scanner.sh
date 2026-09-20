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
printf '%s\n' 'NOXINFLUENCER_API_KEY="SYNTHETIC_REVIEW_VALUE_1234567890"' > "$tmp_dir/repo/.env.example"
if (cd "$tmp_dir/repo" && bash tests/validate-security.sh >/dev/null 2>&1); then
  echo "scanner accepted a quoted credential assignment" >&2
  exit 1
fi

printf '%s\n' 'NOXINFLUENCER_API_KEY=your_key_here' > "$tmp_dir/repo/.env.example"
(cd "$tmp_dir/repo" && bash tests/validate-security.sh)

python3 - "$tmp_dir/quoted-secret.zip" <<'PY'
import sys
import zipfile

with zipfile.ZipFile(sys.argv[1], "w") as bundle:
    bundle.writestr(
        "creator-development/.env.example",
        'NOXINFLUENCER_API_KEY="SYNTHETIC_ARCHIVE_VALUE_1234567890"\n',
    )
PY

if (cd "$tmp_dir/repo" && RELEASE_ARCHIVE="$tmp_dir/quoted-secret.zip" bash tests/validate-security.sh >/dev/null 2>&1); then
  echo "scanner accepted a quoted credential inside a release archive" >&2
  exit 1
fi
