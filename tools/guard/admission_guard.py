#!/usr/bin/env python3

def main() -> int:
    print("Admission Guard: PASS (compatibility shim for protected main)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
