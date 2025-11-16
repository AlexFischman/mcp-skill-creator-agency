from dotenv import load_dotenv
from agency_swarm import Agency
from skill_creator import skill_creator

import asyncio
import psutil
from typing import List


load_dotenv()


def _is_mcp_process(proc_cmdline: List[str]) -> bool:
    """
    Best-effort detection of the Claude Skills MCP backend process.

    We look for either the 'claude-skills-mcp-backend' entry point or the Python
    module being invoked via uvx or python.
    """
    if not proc_cmdline:
        return False

    joined = " ".join(proc_cmdline)
    return "claude-skills-mcp-backend" in joined


def is_mcp_server_running() -> bool:
    """
    Check if a Claude Skills MCP backend server is already running.

    This is a defensive check only – it does NOT attempt to start the server.
    """
    try:
        for proc in psutil.process_iter(["cmdline"]):
            cmd = proc.info.get("cmdline") or []
            if _is_mcp_process(cmd):
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        # Ignore transient process issues; fall back to "not detected"
        pass
    return False


# do not remove this method, it is used in the main.py file to deploy the agency (it has to be a method)
def create_agency(load_threads_callback=None):
    agency = Agency(
        skill_creator,
        communication_flows=[],
        name="SkillCreatorAgency",
        shared_instructions="shared_instructions.md",
        load_threads_callback=load_threads_callback,
    )

    return agency


if __name__ == "__main__":
    # Before spinning up the agency, ensure the external MCP server is already running.
    # We do NOT start it from here – we only check and give guidance.
    if not is_mcp_server_running():
        print("\n⚠️  Claude Skills MCP backend does not appear to be running.")
        print("   To start it, open a separate terminal and run:")
        print("       source venv/bin/activate")
        print("       python start_claude_skills_mcp.py")
        print("\n   Once the MCP server is up, re-run:")
        print("       python agency.py\n")
        raise SystemExit(1)

    agency = create_agency()

    # Test with a single message (uncomment to test programmatically)
    # async def main():
    #     response = await agency.get_response(\"Hello, how are you?\")
    #     print(response)
    # asyncio.run(main())

    # Run in interactive terminal (requires interactive shell)
    # Note: Use 'python agency.py' in a real terminal, not through IDE
    try:
        agency.terminal_demo()
    except (OSError, KeyError):
        print("\n⚠️  Terminal demo requires an interactive terminal.")
        print("   Run 'python agency.py' directly in your terminal instead.")
        print("   Or use the async get_response() method for programmatic access.\n")
