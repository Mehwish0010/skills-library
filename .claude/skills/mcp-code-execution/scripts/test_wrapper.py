#!/usr/bin/env python3
"""Test an MCP wrapper script for token efficiency."""
import subprocess
import sys
import os


def test_wrapper(script_name):
    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"{script_name.replace('-', '_')}.py",
    )

    if not os.path.exists(script_path):
        print(f"✗ Script not found: {script_path}")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True, timeout=60,
    )

    output = result.stdout.strip()
    output_lines = output.split("\n") if output else []
    output_tokens = len(output.split())

    print(f"Script: {script_path}")
    print(f"Exit code: {result.returncode}")
    print(f"Output lines: {len(output_lines)}")
    print(f"Estimated tokens: ~{output_tokens}")
    print(f"Output:\n{output}")

    if output_tokens > 200:
        print(f"\n⚠ Warning: Output exceeds 200 tokens. Consider filtering more aggressively.")
    elif result.returncode == 0:
        print(f"\n✓ Wrapper is token-efficient ({output_tokens} tokens)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_wrapper.py <script-name>")
        sys.exit(1)
    test_wrapper(sys.argv[1])
