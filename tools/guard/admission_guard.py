#!/usr/bin/env python3

import os
import subprocess


REGISTER_PATH = "PRODUCT-0002_Product-Register.md"
LEDGER_HEADER = "## Admitted Products"


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr.strip()}")
    return p.stdout


def git_changed_files(base_ref: str | None) -> list[str]:
    # = Determine change set
    # -> PR context: compare base branch to HEAD.
    # -> Non-PR context: compare last commit to current.
    if base_ref:
        out = run(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    else:
        out = run(["git", "diff", "--name-only", "HEAD~1..HEAD"])
    return [line.strip() for line in out.splitlines() if line.strip()]


def detect_candidate_products(files: list[str]) -> list[str]:
    # = Candidate products
    # -> Any file whose basename starts with PRODUCT- is treated as product-bearing.
    candidates = []
    for f in files:
        base = os.path.basename(f)
        if base.startswith("PRODUCT-"):
            candidates.append(f)
    return sorted(set(candidates))


def git_show(ref: str, path: str) -> str:
    return run(["git", "show", f"{ref}:{path}"])


def read_working_tree(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_ledger(text: str) -> str:
    # = Extract append-only ledger segment
    # -> Ledger is defined as the content from "## Admitted Products" to end of file.
    idx = text.find(LEDGER_HEADER)
    if idx == -1:
        raise ValueError(f"Register ledger header not found: {LEDGER_HEADER}")
    return text[idx:]


def main() -> int:
    # = Identify base ref if running in GitHub Actions PR context
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        base_ref = f"origin/{base_ref}"

    changed_files = []
    try:
        changed_files = git_changed_files(base_ref)
    except Exception as e:
        print(f"Admission Guard ERROR: {e}")
        return 2

    candidates = detect_candidate_products(changed_files)
    register_changed = REGISTER_PATH in changed_files

    errors: list[str] = []

    print("Admission Guard: rule set v0.3")
    print(f"Changed files: {len(changed_files)}")
    print(f"Candidate product files: {len(candidates)}")

    # = Blocking Rule 1: admission implies register coupling
    if candidates and not register_changed:
        errors.append(
            "Product-bearing changes detected but Product Register was not updated. "
            f"Expected change to: {REGISTER_PATH}"
        )

    # = Blocking Rule 2: Product Register append-only ledger
    if register_changed:
        try:
            if base_ref:
                old_text = git_show(base_ref, REGISTER_PATH)
            else:
                old_text = git_show("HEAD~1", REGISTER_PATH)

            new_text = read_working_tree(REGISTER_PATH)

            old_ledger = extract_ledger(old_text)
            new_ledger = extract_ledger(new_text)

            if not new_ledger.startswith(old_ledger):
                errors.append(
                    "Product Register ledger is not append-only. "
                    "Edits to existing entries are not permitted. "
                    "Only appends at the end of the admitted-products ledger are allowed."
                )
        except Exception as e:
            errors.append(f"Could not validate Product Register append-only rule: {e}")

    if errors:
        print("COMMIT/PR REJECTED: Admission Guard violation(s)")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Admission Guard: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
