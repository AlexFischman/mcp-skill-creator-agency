from typing import Optional
from .server import call_tool


async def find_helpful_skills(
    task_description: str,
    top_k: Optional[int] = 3,
    list_documents: Optional[bool] = True,
) -> str:
    """
    Semantic search for relevant skills based on task description.

    Args:
        task_description: Description of the task you want to accomplish. Be specific about your goal, context, or problem domain for better results (e.g., 'debug Python API errors', 'process genomic data', 'build React dashboard')
        top_k: Number of skills to return (default: 3). Higher values provide more options but may include less relevant results.
        list_documents: Include a list of available documents (scripts, references, assets) for each skill (default: True)

    Returns:
        Tool result as string containing ranked skill candidates with step-by-step guidance and best practices
    """
    # Build arguments dict with required params
    arguments = {"task_description": task_description}

    # Add optional params only if provided
    if top_k is not None:
        arguments["top_k"] = top_k
    if list_documents is not None:
        arguments["list_documents"] = list_documents

    # Call the MCP tool
    return await call_tool("find_helpful_skills", arguments)


# Test - run with: python ./servers/claude_skills/find_helpful_skills.py
if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing find_helpful_skills...")
        try:
            result = await find_helpful_skills("analyze genomic data from FASTA files")
            print(f"✓ Success: {str(result)[:500]}...")
        except Exception as e:
            print(f"✗ Error: {e}")

    asyncio.run(test())
