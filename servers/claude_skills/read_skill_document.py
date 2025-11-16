from typing import Optional
from .server import call_tool


async def read_skill_document(
    skill_name: str,
    document_path: Optional[str] = None,
    include_base64: Optional[bool] = False,
) -> str:
    """
    Retrieve specific documents (scripts, references, assets) from a skill. Supports pattern matching to fetch multiple files.

    Args:
        skill_name: Name of the skill (as returned by find_helpful_skills)
        document_path: Path or pattern to match documents. Examples: 'scripts/example.py', 'scripts/*.py', 'references/*', 'assets/diagram.png'. If not provided, returns a list of all available documents.
        include_base64: For images: if True, return base64-encoded content; if False, return only URL. Default: False (URL only for efficiency)

    Returns:
        Tool result as string containing document content or URLs
    """
    # Build arguments dict with required params
    arguments = {"skill_name": skill_name}

    # Add optional params only if provided
    if document_path is not None:
        arguments["document_path"] = document_path
    if include_base64 is not None:
        arguments["include_base64"] = include_base64

    # Call the MCP tool
    return await call_tool("read_skill_document", arguments)


# Test - run with: python ./servers/claude_skills/read_skill_document.py
if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing read_skill_document...")
        try:
            # First find a skill to read from
            from .find_helpful_skills import find_helpful_skills

            skills_result = await find_helpful_skills("analyze genomic data", top_k=1)
            print(f"Found skills: {str(skills_result)[:200]}...")

            # Try to read documents from a skill (this will list available documents)
            # Note: You'll need to replace 'example_skill_name' with an actual skill name
            # result = await read_skill_document("example_skill_name")
            # print(f"✓ Success: {str(result)[:500]}...")
            print("✓ Test skipped - requires actual skill name from discovery")
        except Exception as e:
            print(f"✗ Error: {e}")

    asyncio.run(test())
