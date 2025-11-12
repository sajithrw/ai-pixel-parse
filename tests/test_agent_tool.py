#!/usr/bin/env python3
"""
Test the UI extraction agent tool function.

This verifies that the agent's extract_ui_tool function works correctly
before running it in the ADK web UI.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ai_pixel_parse.ui_extractor_agent import extract_ui_tool


async def test_simple_extraction():
    """Test extraction from a simple public website."""
    print("=" * 80)
    print("Testing UI Extraction Tool")
    print("=" * 80)
    print()
    print("This will extract UI from httpbin.org (a simple test site)")
    print("with limited pages to verify the tool works correctly.")
    print()
    
    try:
        result = await extract_ui_tool(
            base_url="https://httpbin.org",
            app_name="HTTPBin_Test",
            max_pages=5  # Limit for testing
        )
        
        print("\n" + "=" * 80)
        print("✅ TEST PASSED!")
        print("=" * 80)
        print()
        print("Result:")
        print(result)
        print()
        print("The agent tool is working correctly!")
        print("You can now use it in the ADK web UI with commands like:")
        print('  "Extract UI from google.com, call it google"')
        print()
        
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ TEST FAILED!")
        print("=" * 80)
        print()
        print(f"Error: {e}")
        print()
        print("This might be due to missing dependencies.")
        print("Make sure you have installed:")
        print("  pip install -r requirements.txt")
        print("  playwright install chromium")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🧪 Starting Agent Tool Test...\n")
    asyncio.run(test_simple_extraction())
