"""Quick test script for the SkillCreatorAgency"""

import asyncio
from agency import create_agency


async def main():
    print("=" * 70)
    print("Testing SkillCreatorAgency")
    print("=" * 70)

    # Create the agency
    agency = create_agency()
    print(f"✓ Agency created: {agency.name}")
    print(f"✓ Entry agent: {agency.entry_agent.name}")
    print(f"✓ Available tools: {[tool.__name__ for tool in agency.entry_agent.tools]}")

    # Test with a simple query
    print("\n" + "-" * 70)
    print("Sending test message...")
    print("-" * 70)

    response = await agency.get_response(
        "Hello! Can you explain what you can help me with?"
    )

    print("\n" + "=" * 70)
    print("Response:")
    print("=" * 70)
    print(response)
    print("\n" + "=" * 70)
    print("✓ Test completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())


