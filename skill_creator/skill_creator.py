from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import IPythonInterpreter, PersistentShellTool
from agents.mcp import MCPServerStreamableHttp
from openai.types.shared import Reasoning


# Configure Claude Skills MCP Server (standalone backend over HTTP)
# Backend docs: https://pypi.org/project/claude-skills-mcp-backend/
# The backend is expected to be running separately, started via:
#   python start_claude_skills_mcp.py
# which exposes a Streamable HTTP MCP endpoint at http://127.0.0.1:8765/mcp
claude_skills_mcp = MCPServerStreamableHttp(
    params={
        "url": "http://127.0.0.1:8765/mcp",
        "timeout": 10,
        "sse_read_timeout": 60 * 5,
        # We are connecting to a shared, standalone backend, so do not
        # terminate the server when the client session is closed.
        "terminate_on_close": False,
    },
    cache_tools_list=True,
    name="Claude_Skills_HTTP",
    client_session_timeout_seconds=120,  # Allow time for backend initialization on first run
)

skill_creator = Agent(
    name="skill_creator",
    description="Creates and manages skills and tools for agents",
    instructions="./instructions.md",
    files_folder="./files",
    tools_folder="./tools",
    tools=[IPythonInterpreter, PersistentShellTool],
    mcp_servers=[claude_skills_mcp],
    model="gpt-5-mini",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium", summary="auto"),
    ),
)


# Test MCP server integration
if __name__ == "__main__":
    import asyncio

    async def test_agent():
        print("=" * 70)
        print("Testing Claude Skills MCP Server Integration")
        print("=" * 70)

        # List available tools from MCP server
        print("\nConnecting to Claude Skills MCP server...")
        await claude_skills_mcp.connect()

        tools = await claude_skills_mcp.list_tools()
        print(f"\nFound {len(tools)} tools from Claude Skills MCP:\n")
        for tool in tools:
            print(f"  • {tool.name}")
            print(f"    {tool.description}\n")

        print("=" * 70)
        print("✓ MCP Server Integration Successful!")
        print("=" * 70)

    asyncio.run(test_agent())
