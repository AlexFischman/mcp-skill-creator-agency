"""Test script for Claude Skills MCP tools"""

import asyncio
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from servers.claude_skills import find_helpful_skills, list_skills


async def test_list_skills():
    print("Testing list_skills...")
    try:
        result = await list_skills()
        print(f"✓ Success: {str(result)[:500]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_find_helpful_skills():
    print("\nTesting find_helpful_skills...")
    try:
        result = await find_helpful_skills(
            "analyze genomic data from FASTA files", top_k=2
        )
        print(f"✓ Success: {str(result)[:500]}...")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    print("=" * 60)
    print("Claude Skills MCP Server Tests")
    print("=" * 60)

    # Test list_skills first (simpler, no arguments)
    success1 = await test_list_skills()

    # Test find_helpful_skills
    success2 = await test_find_helpful_skills()

    print("\n" + "=" * 60)
    if success1 and success2:
        print("All tests passed!")
    else:
        print("Some tests failed.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


