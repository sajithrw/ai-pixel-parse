#!/usr/bin/env python3
"""UI Extraction Runner Script.

This script provides a simple interface for running UI extraction on web
applications. It handles Playwright dependency installation and provides
example configurations for both public and authenticated applications.

Usage:
    python run_extraction.py

Configuration:
    Edit the config section in main() to specify your target application.
"""

import asyncio
import subprocess
import sys
from pathlib import Path

# Add package to path for direct execution
sys.path.insert(0, str(Path(__file__).parent))

from ai_pixel_parse.ui_extractor_agent import (
    create_extraction_config,
    extract_ui_specifications,
)


def install_playwright_deps() -> None:
    """Install Playwright browser dependencies if not already present.
    
    This function attempts to install the Chromium browser with all OS-level
    dependencies required for headless operation. If installation fails, it
    provides instructions for manual installation.
    
    Raises:
        SystemExit: If automatic installation fails.
    """
    try:
        print("Verifying Playwright browser dependencies...")
        subprocess.run(
            ["playwright", "install", "--with-deps", "chromium"],
            check=True,
            capture_output=True,
            text=True,
            timeout=180  # 3-minute timeout
        )
        print("✓ Playwright dependencies are installed.")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print("✗ Could not automatically install Playwright dependencies.")
        print("  Please run the following command in your terminal:")
        print("\n    playwright install --with-deps chromium\n")
        if isinstance(e, subprocess.CalledProcessError):
            print(f"  Error details:\n{e.stderr}")
        sys.exit(1)


async def main() -> None:
    """Execute UI extraction with configured parameters.
    
    This function sets up and runs a UI extraction job. Customize the config
    section below to target your specific application.
    
    Configuration Examples:
        - Public site: Provide only base_url and app_name
        - Authenticated site: Include login_url, username, and password
        - Custom selectors: Add username_selector, password_selector, submit_selector
    """
    # Ensure Playwright browser dependencies are installed
    install_playwright_deps()
    
    # Configuration for extraction job
    # Example 1: Public application (no authentication)
    config = create_extraction_config(
        base_url="https://google.com",
        app_name="google",
        max_pages=20
    )
    
    # Example 2: Authenticated application
    # Uncomment and customize for applications requiring login
    # config = create_extraction_config(
    #     base_url="https://your-app.com/dashboard",
    #     app_name="YourApp",
    #     login_url="https://your-app.com/login",
    #     username="your-username",
    #     password="your-password",
    #     # Optional: Custom CSS selectors if defaults don't work
    #     # username_selector="input[name='email']",
    #     # password_selector="input[name='pass']",
    #     # submit_selector="button.login-btn",
    #     max_pages=30
    # )
    
    # Execute extraction
    output_path = await extract_ui_specifications(config)
    
    # Display results and next steps
    print(f"\n{'=' * 80}")
    print(f"📁 Output saved to: {output_path}")
    print(f"{'=' * 80}\n")
    print("Next steps:")
    print("1. Review generated specifications in the extraction/ folder")
    print("2. Check screenshots to verify component extraction accuracy")
    print("3. Use full_extraction.json for programmatic data access")
    print("4. Feed specifications to code generation agents to rebuild UI\n")


if __name__ == "__main__":
    asyncio.run(main())
