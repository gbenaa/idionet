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
    # -> In push/manual context, compare HEAD~1..HEAD as a best-effort default.
    if base_ref:
        out = run(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    else:
        out = run(["git", "diff", "--name-only", "HEAD~1..HEAD"])

    files = [line.strip() for line in out.splitlines() if line.strip()]
    return files


def detect_candidate_products(files: list[str]) -> list[str]:
    # = Candidate products
    # -> Any file whose basename starts with PRODUCT- is treated as product-bearing.
    candidates = []
    for f in files:
        base = os.path.basename(f)
        if base.startswith("PRODUCT-"):
            candidates.append(f)
    return sorted(set(candidates))


def main() -> int:
    # = Identify base ref if running in GitHub Actions PR context
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        base_ref = f"origin/{base_ref}"

    try:
        changed_files = git_changed_files(base_ref)
    except Exception as e:
        print(f"Admission Guard ERROR: {e}")
        return 2

    candidates = detect_candidate_products(changed_files)
    register_path = "PRODUCT-0002_Product-Register.md"
    register_changed = register_path in changed_files

    errors: list[str] = []

    print("Admission Guard: rule set v0.2")
    print(f"Changed files: {len(changed_files)}")
    print(f"Candidate product files: {len(candidates)}")

    if candidates:
        print("Candidate product-bearing changes detected:")
        for f in candidates:
            print(f" - {f}")

        # = Blocking Rule 1: admission implies register coupling
        # -> If any PRODUCT-* file changes, the canonical Product Register must change too.
        if not register_changed:
            errors.append(
                "Product-bearing changes detected but Product Register was not updated. "
                f"Expected change to: {register_path}"
            )

    if errors:
        print("COMMIT/PR REJECTED: Admission Guard violation(s)")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Admission Guard: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
