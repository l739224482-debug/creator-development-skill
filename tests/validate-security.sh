#!/usr/bin/env bash
set -euo pipefail

python3 - "${RELEASE_ARCHIVE:-}" <<'PY'
from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile

root = Path.cwd()
archive_arg = sys.argv[1]
failures: list[tuple[str, str]] = []

SKIP_DIRS = {".git", ".superpowers", ".worktrees", "__pycache__"}
FORBIDDEN_NAMES = {"credentials.json"}
FORBIDDEN_SUFFIXES = {".pem", ".key"}
SAFE_ENV_EXAMPLE = "your_key_here"
SAFE_FAKE_TOKENS = {"nox_FAKE_TEST_SECRET_1234567890"}

assignment = re.compile(r"NOXINFLUENCER_API_KEY\s*=\s*([A-Za-z0-9_.<>-]+)")
nox_token = re.compile(r"nox_[A-Za-z0-9_-]{16,}")
generic_tokens = [
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github-token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("openai-token", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
]


def path_rule(name: str) -> str | None:
    path = Path(name)
    base = path.name
    if base.startswith(".env") and base != ".env.example":
        return "private-env-file"
    if base in FORBIDDEN_NAMES:
        return "credential-file"
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        return "private-key-file"
    return None


def scan_text(name: str, raw: bytes) -> None:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return

    for match in assignment.finditer(text):
        if match.group(1) != SAFE_ENV_EXAMPLE and match.group(1) not in SAFE_FAKE_TOKENS:
            failures.append((name, "nox-env-assignment"))
            break

    for match in nox_token.finditer(text):
        if match.group(0) not in SAFE_FAKE_TOKENS:
            failures.append((name, "nox-token-pattern"))
            break

    for rule, pattern in generic_tokens:
        if pattern.search(text):
            failures.append((name, rule))


def scan_worktree() -> None:
    for current, dirs, files in os.walk(root):
        dirs[:] = [item for item in dirs if item not in SKIP_DIRS]
        for filename in files:
            path = Path(current) / filename
            rel = path.relative_to(root).as_posix()
            rule = path_rule(rel)
            if rule:
                failures.append((rel, rule))
                continue
            scan_text(rel, path.read_bytes())


def scan_history() -> None:
    check = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if check.returncode != 0:
        return

    objects = subprocess.run(
        ["git", "rev-list", "--objects", "--all"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    for line in objects:
        object_id, _, name = line.partition(" ")
        if not name:
            continue
        object_type = subprocess.run(
            ["git", "cat-file", "-t", object_id],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        if object_type != "blob":
            continue
        rule = path_rule(name)
        if rule:
            failures.append((f"git:{name}", rule))
            continue
        raw = subprocess.run(
            ["git", "cat-file", "-p", object_id],
            cwd=root,
            capture_output=True,
            check=True,
        ).stdout
        scan_text(name, raw)


def scan_archive(archive_path: str) -> None:
    if not archive_path:
        return
    archive = Path(archive_path)
    if not archive.is_file():
        failures.append((archive_path, "release-archive-missing"))
        return
    with zipfile.ZipFile(archive) as bundle:
        for info in bundle.infolist():
            if info.is_dir():
                continue
            name = info.filename
            rule = path_rule(name)
            if rule:
                failures.append((f"zip:{name}", rule))
                continue
            scan_text(name, bundle.read(info))


scan_worktree()
scan_history()
scan_archive(archive_arg)

unique_failures = sorted(set(failures))
if unique_failures:
    for path, rule in unique_failures:
        print(f"{path}: {rule}", file=sys.stderr)
    raise SystemExit(1)

print("security scan passed")
PY
