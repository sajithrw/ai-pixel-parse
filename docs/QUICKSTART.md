# UI Extraction Agent - Quick Start Guide

## What This Project Does

This AI agent **automatically extracts complete UI specifications** from any web application, including:

- 🔐 **Handles authentication** (login flows)
- 🕷️ **Crawls entire applications** (discovers all pages)
- 📋 **Catalogs all UI components**:
  - Buttons (with functions/actions)
  - Forms (inputs, validation, submission)
  - Tables (data structures, headers)
  - Icons (SVG, icon fonts)
  - Modals, navigation, layout structure
- 📸 **Captures screenshots** for visual reference
- 📝 **Generates clear specifications** in text + JSON format

**Purpose**: These specifications can be fed to another AI agent to **rebuild the UI in any tech stack** (React, Vue, Angular, etc.)

---

## Installation (5 minutes)

### 1. Clone and setup Python environment

```bash
cd ai-pixel-parse

# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Verify setup

```bash
python3 verify_setup.py
```

---

## Quick Usage

### Option 1: ADK Web UI (Recommended for Interactive Use) 🌐

Start the ADK web interface for conversational extraction:

```bash
adk start
```

Then in the web UI, simply chat with the agent:

```
"Extract UI from https://example.com and call it ExampleApp"
```

See **[ADK_WEB_UI_GUIDE.md](ADK_WEB_UI_GUIDE.md)** for complete web UI instructions.

### Option 2: Run Example (Public Website)

```bash
python3 examples.py
```

This will extract UI from `httpbin.org` as a demo.

### Option 3: Extract Your Own App (Script)

Edit `run_extraction.py` and update the configuration:

```python
config = create_extraction_config(
    base_url="https://your-app.com/dashboard",
    app_name="YourApp",
    login_url="https://your-app.com/login",  # Optional
    username="your-user",                     # Optional
    password="your-pass",                     # Optional
    max_pages=30
)
```

Then run:

```bash
python3 run_extraction.py
```

### Output Location

Check `extraction/YourApp_<timestamp>/` for:
- `00_SUMMARY.txt` - Overview & statistics
- `01_PageName.txt` - Detailed page specifications
- `screenshot_0.png` - Page screenshots
- `full_extraction.json` - Complete data in JSON

---

## Configuration Examples

### Public Website (No Login)

```python
config = create_extraction_config(
    base_url="https://example.com",
    app_name="ExampleApp",
    max_pages=20
)
```

### With Login

```python
config = create_extraction_config(
    base_url="https://app.example.com/home",
    app_name="MyApp",
    login_url="https://app.example.com/login",
    username="demo@example.com",
    password="demo123",
    max_pages=50
)
```

### Custom Login Selectors

```python
config = create_extraction_config(
    base_url="https://custom-app.com",
    app_name="CustomApp",
    login_url="https://custom-app.com/signin",
    username="user",
    password="pass",
    username_selector="input#email-field",      # Custom!
    password_selector="input#pwd",              # Custom!
    submit_selector="button#login-submit",      # Custom!
    max_pages=30
)
```

**Tip**: Use browser DevTools to find correct CSS selectors for your login form.

---

## Output Format

Each page specification includes:

### 1. Page Metadata
- Title, URL, timestamp
- Screenshot reference

### 2. Functions & Features
- What the page does
- User workflows
- Business logic

### 3. Components
- **Buttons**: Text, ID, classes, position, function
- **Forms**: Inputs, validation, submission endpoints
- **Tables**: Headers, data structure, sample rows
- **Icons**: Type, classes, positions
- **Navigation**: Links, menu structure

### Example Output

```
PAGE SPECIFICATION
================================================================================

Title: User Dashboard
URL: https://app.example.com/dashboard

FUNCTIONS & FEATURES
--------------------------------------------------------------------------------

[FORM_SUBMISSION]
Form submission: /api/users/search
  Method: GET
  Inputs: 2 fields
    - Search Query: text
    - Filter By: select

BUTTONS (8)
--------------------------------------------------------------------------------

[Button] Create New User
  ID: btn-create-user
  Type: button
  Classes: btn btn-primary
  Position: x=1200, y=80, w=150, h=40
  Function: Opens user creation modal
```

---

## Use With Code Generation

Feed the specifications to another AI agent:

```python
import json

# Load extracted specifications
with open('extraction/MyApp_20250109/full_extraction.json') as f:
    specs = json.load(f)

# Use in your code generation workflow
for page in specs:
    print(f"Generating components for: {page['title']}")
    # Feed to React/Vue/Angular code generator
    # Generate components from buttons, forms, tables, etc.
```

---

## Troubleshooting

### Login Not Working?

1. Inspect the login page in your browser
2. Find the correct CSS selectors using DevTools
3. Update `username_selector`, `password_selector`, `submit_selector`

### Missing Components?

- Increase timeout: Components may load via JavaScript
- Check `wait_until='networkidle'` in code
- Verify page has fully loaded before extraction

### Too Many/Few Pages?

- Adjust `max_pages` parameter
- Check navigation link detection
- Verify `base_url` matches domain structure

---

## Project Structure

```
ai-pixel-parse/
├── ai-pixel-parse/
│   ├── agent.py                 # Basic agent
│   ├── ui_extractor_agent.py    # UI extraction agent ⭐
│   └── __init__.py              # Package exports
├── run_extraction.py            # Main runner script
├── examples.py                  # Example configurations
├── verify_setup.py              # Setup verification
├── requirements.txt             # Python dependencies
├── README.md                    # Full documentation
├── QUICKSTART.md                # This file
└── extraction/                  # Output folder (created on first run)
    └── AppName_timestamp/       # Each extraction in its own subfolder
        ├── 00_SUMMARY.txt       # Overview
        ├── *.txt                # Page specifications
        ├── README.md            # Extraction summary
        ├── screenshot_*.png     # Screenshots
        └── full_extraction.json # JSON data
```

---

## Next Steps

1. ✅ Install dependencies (`pip install -r requirements.txt`)
2. ✅ Install Playwright (`playwright install chromium`)
3. ✅ Run example (`python3 examples.py`)
4. ✅ Configure your app in `run_extraction.py`
5. ✅ Extract UI (`python3 run_extraction.py`)
6. ✅ Review output in `extraction/` folder
7. ✅ Use specifications with code generation agents

---

## Key Features

- ✅ **Automatic crawling** - Discovers all pages automatically
- ✅ **Authentication** - Handles login flows with custom selectors
- ✅ **Comprehensive extraction** - All UI components with properties
- ✅ **Function analysis** - Documents what each component does
- ✅ **Multiple formats** - Text (human) + JSON (programmatic)
- ✅ **Visual reference** - Screenshots for every page
- ✅ **Tech-agnostic output** - Use with any framework

---

## Support

- 📖 Full docs: See `README.md`
- 🔧 Setup issues: Run `python3 verify_setup.py`
- 💡 Examples: Check `examples.py` for templates
- 🤖 AI guidance: See `.github/copilot-instructions.md`

---

**Ready to extract?** Start with `python3 examples.py` 🚀
