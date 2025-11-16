#!/usr/bin/env python3
"""
Test the enhanced behavioral extraction.

This script tests the UI extractor with a sample website to demonstrate
the behavioral specifications it now captures.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

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


async def test_dashboard_login():
    """Test extraction of dashboard with login authentication."""
    
    print("=" * 80)
    print("TESTING DASHBOARD WITH LOGIN")
    print("=" * 80)
    print()
    print("Target: https://ui.rtb-adingenious.com/dashboard")
    print("Authentication: Required (login flow)")
    print()
    
    # Configure extraction with login
    # After login, it will navigate to dashboard and extract from there
    config = create_extraction_config(
        base_url="https://ui.rtb-adingenious.com/dashboard",  # Target dashboard after login
        app_name="dashboard",
        login_url="https://ui.rtb-adingenious.com/login",
        username="Sajit",
        password="Sajit@pll",
        username_selector="#name",
        password_selector="#password",
        submit_selector="button",  # Login button selector
        max_pages=10,
        dynamic_content_wait=15  # Wait 15s for KPIs and dynamic charts to load
    )
    
    print("Starting extraction with login flow...")
    print("  1. Navigate to login page")
    print("  2. Enter credentials")
    print("  3. Submit login form")
    print("  4. Wait for redirect and page load")
    print("  5. Extract dashboard pages")
    print()
    
    try:
        output_path = await extract_ui_specifications(config)
        
        print(f"\n{'=' * 80}")
        print(f"✅ EXTRACTION COMPLETE")
        print(f"{'=' * 80}")
        print(f"\n📁 Output: {output_path}")
        print("\nExtracted specifications include:")
        print(f"  - Login page structure and form")
        print(f"  - Dashboard pages (after authentication)")
        print(f"  - All interactive elements and behaviors")
        print(f"  - Form validations and submissions")
        print()
    except Exception as e:
        print(f"\n{'=' * 80}")
        print(f"❌ EXTRACTION FAILED")
        print(f"{'=' * 80}")
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Verify credentials are correct")
        print("  2. Check if selectors match the actual form fields")
        print("  3. Ensure the website is accessible")
        print("  4. Check if there are any CAPTCHA or 2FA requirements")
        print("  5. The page might be a SPA with continuous network activity")
        print("     - Try accessing dashboard directly in browser after login")
        print()
        raise


if __name__ == "__main__":
    # Run the test you want
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        # Run dashboard login test
        asyncio.run(test_dashboard_login())
    else:
        # Run default test
        asyncio.run(test_extraction())
