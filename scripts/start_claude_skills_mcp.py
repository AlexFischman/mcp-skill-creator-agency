import subprocess
import sys


def start_mcp_backend() -> None:
    """
    Start the Claude Skills MCP *backend* as a standalone HTTP MCP server.

    This runs the `claude-skills-mcp-backend` package via `uvx` with Python 3.12,
    using the local `claude-skills-mcp-config.json` file for configuration.

    The backend exposes a Streamable HTTP MCP endpoint at:
        http://127.0.0.1:8765/mcp

    It is intended to be run in a dedicated terminal session, separate from
    `agency.py`, and left running while you use the agency.
    """
    cmd = [
        "uvx",
        "--python",
        "3.12",
        "claude-skills-mcp-backend",
        "--config",
        "./claude-skills-mcp-config.json",
    ]

    print(
        "Starting Claude Skills MCP backend (standalone HTTP MCP server) with command:"
    )
    print(" ", " ".join(cmd))
    print("\nLeave this process running while you use `python agency.py`.\n")

    try:
        # Start the MCP backend as a long-running process.
        # It will keep running in this terminal until interrupted (Ctrl+C).
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print(
            "\n❌ Failed to start Claude Skills MCP backend: `uvx` command not found.\n"
            "   Make sure uv is installed, for example:\n"
            "       pip install uv\n"
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(
            "\n❌ Claude Skills MCP backend exited with an error.\n"
            f"   Return code: {e.returncode}\n"
            "   Check the output above for details (Python version and dependency issues are common).\n"
        )
        sys.exit(e.returncode)


if __name__ == "__main__":
    start_mcp_backend()


