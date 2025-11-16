#!/usr/bin/env python3
"""
Test the specification converter agent.

This script tests converting a UI extraction to functional specifications.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_pixel_parse import convert_to_functional_spec_tool


async def test_spec_conversion():
    """Test converting dashboard extraction to functional spec."""
    
    print("=" * 80)
    print("TESTING SPECIFICATION CONVERTER")
    print("=" * 80)
    print()
    print("This test converts a technical UI extraction into functional specifications")
    print("that developers or AI agents can use to build the application.")
    print()
    
    # Test with dashboard extraction
    result = await convert_to_functional_spec_tool(
        app_name="dashboard",
        domain="advertising analytics",
        target_audience="AI agents and developers",
        include_user_stories=True,
        include_workflows=True
    )
    
    print(f"\n{'=' * 80}")
    print(f"✅ CONVERSION COMPLETE")
    print(f"{'=' * 80}")
    print(f"\n{result}")
    print()


if __name__ == "__main__":
    asyncio.run(test_spec_conversion())
