from .server import call_tool


async def list_skills() -> str:
    """
    View the complete inventory of all loaded skills for exploration or debugging.

    Returns names, descriptions, sources, and document counts for all skills.
    For task-driven work, prefer calling 'find_helpful_skills' first to locate
    the most relevant option before reading documents.

    Returns:
        Tool result as string containing the full inventory of loaded skills
    """
    # Call the MCP tool with no arguments
    return await call_tool("list_skills", {})


# Test - run with: python ./servers/claude_skills/list_skills.py
if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing list_skills...")
        try:
            result = await list_skills()
            print(f"✓ Success: {str(result)[:500]}...")
        except Exception as e:
            print(f"✗ Error: {e}")

    asyncio.run(test())
