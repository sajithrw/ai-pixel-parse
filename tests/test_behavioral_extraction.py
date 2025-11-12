#!/usr/bin/env python3
"""
Test the enhanced behavioral extraction.

This script tests the UI extractor with a sample website to demonstrate
the behavioral specifications it now captures.
"""

import asyncio
import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from ai_pixel_parse import create_extraction_config, extract_ui_specifications


async def test_extraction():
    """Test extraction with a sample interactive website."""
    
    print("=" * 80)
    print("TESTING BEHAVIORAL UI EXTRACTION")
    print("=" * 80)
    print()
    print("This test extracts UI specifications with focus on:")
    print("  ✓ Interactive behaviors (clicks, hovers, submissions)")
    print("  ✓ Event handlers and dynamic actions")
    print("  ✓ Form validation rules and behaviors")
    print("  ✓ Table interactions (sorting, filtering, pagination)")
    print("  ✓ Button actions and state changes")
    print("  ✓ Link behaviors (external, downloads, AJAX)")
    print()
    
    # Test with a site that has various interactive elements
    config = create_extraction_config(
        base_url="https://google.com",
        app_name="google",
        max_pages=1
    )
    
    print("Starting extraction...")
    output_path = await extract_ui_specifications(config)
    
    print(f"\n{'=' * 80}")
    print(f"✅ EXTRACTION COMPLETE")
    print(f"{'=' * 80}")
    print(f"\n📁 Output: {output_path}")
    print("\nCheck the generated files for behavioral specifications:")
    print(f"  - Buttons with their actions and behaviors")
    print(f"  - Forms with validation rules and submission methods")
    print(f"  - Tables with sorting/filtering capabilities")
    print(f"  - Links with navigation and interaction patterns")
    print()


if __name__ == "__main__":
    asyncio.run(test_extraction())
