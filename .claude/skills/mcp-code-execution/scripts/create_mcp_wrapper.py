#!/usr/bin/env python3
"""Create a new MCP wrapper script from template."""
import os
import sys

TEMPLATE = '''#!/usr/bin/env python3
"""{description}"""
import subprocess
import json
import sys


def main():
    """Execute the MCP operation and return minimal output."""
    try:
        # TODO: Replace with actual MCP operation
        result = subprocess.run(
            ["echo", "placeholder"],
            capture_output=True, text=True, timeout=30,
        )

        if result.returncode != 0:
            print(f"✗ {name} failed: {{result.stderr.strip()[:100]}}")
            sys.exit(1)

        # TODO: Process and filter the result
        data = result.stdout.strip()

        # Only this output enters agent context
        print(f"✓ {name} completed successfully")
        sys.exit(0)

    except subprocess.TimeoutExpired:
        print(f"✗ {name} timed out after 30s")
        sys.exit(1)
    except Exception as e:
        print(f"✗ {name} error: {{str(e)[:100]}}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''


def create_wrapper(name):
    filename = f"{name.replace('-', '_')}.py"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    content = TEMPLATE.format(
        name=name,
        description=f"MCP wrapper for {name} operation",
    )

    with open(filepath, "w") as f:
        f.write(content)

    print(f"✓ Created MCP wrapper: {filepath}")
    print(f"  Edit the script to add your MCP operation logic")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_mcp_wrapper.py <operation-name>")
        sys.exit(1)
    create_wrapper(sys.argv[1])
