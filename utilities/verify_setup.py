#!/usr/bin/env python3
"""
Setup verification script

Run this to check if all dependencies are installed correctly.
"""

import sys
from pathlib import Path

def check_requirement(module_name, import_name=None):
    """Check if a module can be imported."""
    import_name = import_name or module_name
    try:
        __import__(import_name)
        print(f"✓ {module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {module_name} is NOT installed")
        return False

def main():
    print("Checking AI Pixel Parse dependencies...\n")
    
    all_ok = True
    
    # Check core dependencies
    print("Core Dependencies:")
    print("-" * 40)
    
    # Note: google.adk may not be publicly available yet
    # all_ok &= check_requirement("google.adk", "google.adk.agents.llm_agent")
    
    all_ok &= check_requirement("playwright", "playwright.async_api")
    all_ok &= check_requirement("asyncio")
    all_ok &= check_requirement("json")
    
    print("\nPython Version:")
    print("-" * 40)
    print(f"Python {sys.version}")
    
    print("\nPackage Structure:")
    print("-" * 40)
    pkg_dir = Path(__file__).parent.parent / "ai_pixel_parse"
    if pkg_dir.exists():
        print(f"✓ Package directory exists: {pkg_dir}")
        print(f"  - agent.py: {'✓' if (pkg_dir / 'agent.py').exists() else '✗'}")
        print(f"  - ui_extractor_agent.py: {'✓' if (pkg_dir / 'ui_extractor_agent.py').exists() else '✗'}")
        print(f"  - __init__.py: {'✓' if (pkg_dir / '__init__.py').exists() else '✗'}")
    else:
        print(f"✗ Package directory not found: {pkg_dir}")
        all_ok = False
    
    print("\nTest Scripts:")
    print("-" * 40)
    tests_dir = Path(__file__).parent.parent / "tests"
    scripts = ["run_extraction.py", "test_agent_tool.py", "test_behavioral_extraction.py"]
    for script in scripts:
        script_path = tests_dir / script
        print(f"  - {script}: {'✓' if script_path.exists() else '✗'}")
    
    print("\nDocumentation:")
    print("-" * 40)
    docs_dir = Path(__file__).parent.parent / "docs"
    print(f"  - docs/ folder: {'✓' if docs_dir.exists() else '✗'}")
    
    print("\n" + "=" * 40)
    if all_ok:
        print("✅ Basic setup looks good!")
        print("\nNext steps:")
        print("1. Install google.adk (if not already installed)")
        print("2. Run: playwright install chromium")
        print("3. Edit tests/run_extraction.py with your app details")
        print("4. Run: python3 tests/run_extraction.py")
    else:
        print("⚠️  Some dependencies are missing")
        print("\nTo install:")
        print("1. Create venv: python3 -m venv venv")
        print("2. Activate: source venv/bin/activate")
        print("3. Install: pip install -r requirements.txt")
        print("4. Playwright: playwright install chromium")
    print("=" * 40 + "\n")

if __name__ == "__main__":
    main()
