#!/usr/bin/env python
"""Run all pre-commit checks in parallel and show summary at the end."""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class CheckResult:
    name: str
    passed: bool
    output: str


def run_check(name: str, command: list[str]) -> CheckResult:
    """Run a single check and capture its result."""
    result = subprocess.run(command, capture_output=True, text=True, cwd=".")  # noqa: S603
    output = result.stdout + result.stderr

    return CheckResult(
        name=name,
        passed=result.returncode == 0,
        output=output,
    )


def main():
    checks = [
        ("Ruff Lint", ["uv", "run", "ruff", "check", "--diff", "."]),
        ("Ruff Format", ["uv", "run", "ruff", "format", "--check", "."]),
        ("Pytest", ["uv", "run", "pytest"]),
        # ("Safety", ["uv", "run", "safety", "scan"]),
    ]

    print("🚀 Running pre-commit checks...\n")

    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_check, name, cmd): name for name, cmd in checks}

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "✅" if result.passed else "❌"
            print(f"{result.name} {'.' * (100 - len(result.name))} {status}")

    # Sort results by name for consistent output
    results.sort(key=lambda r: r.name)
    # Show summary
    print("\n" + "=" * 100)
    text = "SUMMARY"
    print(f"{text: ^100}")
    print("=" * 100 + "\n")

    failed_checks = [r for r in results if not r.passed]

    if not failed_checks:
        print("✅ All checks passed!\n")
        return 0

    print(f"❌ {len(failed_checks)} check(s) failed:\n")

    for result in failed_checks:
        print(f"\n{'=' * 100}")
        text = f"❌ {result.name}"
        print(f"{text: ^100}")
        print(f"{'=' * 100}")
        print(result.output)

    return 1


if __name__ == "__main__":
    sys.exit(main())
