#!/usr/bin/env python3

import os
import subprocess
import sys


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr.strip()}")
    return p.stdout


def git_changed_files(base_ref: str | None) -> list[str]:
    # = Determine change set
    # -> In PR context, compare base branch to current HEAD.
    # -> In push/manual context, fall back to working tree diff against HEAD.
    if base_ref:
        out = run(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    else:
        out = run(["git", "diff", "--name-only", "HEAD"])

    files = [line.strip() for line in out.splitlines() if line.strip()]
    return files


def detect_candidate_products(files: list[str]) -> list[str]:
    # = Candidate products
    # -> Any file whose basename starts with PRODUCT- is treated as a product-bearing artefact.
    candidates = []
    for f in files:
        base = os.path.basename(f)
        if base.startswith("PRODUCT-"):
            candidates.append(f)
    return sorted(set(candidates))


def main() -> int:
    # = Identify base ref if running in GitHub Actions PR context
    # -> GITHUB_BASE_REF is set for pull_request events.
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        base_ref = f"origin/{base_ref}"

    try:
        changed_files = git_changed_files(base_ref)
    except Exception as e:
        print(f"Admission Guard ERROR: {e}")
        return 2

    candidates = detect_candidate_products(changed_files)

    print("Admission Guard: rule set v0.1")
    print(f"Changed files: {len(changed_files)}")
    print(f"Candidate product files: {len(candidates)}")

    if candidates:
        print("NOTICE: Candidate product-bearing changes detected:")
        for f in candidates:
            print(f" - {f}")

    # = No enforcement yet
    # -> Always pass at this stage
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
