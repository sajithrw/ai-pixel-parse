# AI Pixel Parse - UI Extraction Agent

An AI agent that automatically crawls web applications, handles authentication, and extracts comprehensive UI specifications for rebuilding applications with any tech stack.

## Features

✨ **Complete UI Extraction**
- Buttons, forms, tables, icons, modals, and all interactive elements
- Component properties, positions, styling, and relationships
- Functional analysis (what each component does)
- Page structure, navigation, and hierarchy

🔐 **Authentication Support**
- Handles login pages with configurable selectors
- Maintains session across crawled pages
- Works with most common authentication patterns

📸 **Visual Documentation**
- Full-page screenshots for every page
- Component position mapping
- Visual hierarchy analysis

📄 **Multiple Output Formats**
- Clear text specifications (human-readable)
- JSON data (programmatic access)
- Organized by page with summary

## Quick Links

📁 **Repository Structure:**
- `ai_pixel_parse/` - Main package code
- `tests/` - Test scripts and extraction runner
- `utilities/` - Setup verification and utility scripts
- `docs/` - Comprehensive documentation
- `extraction/` - Output directory (created on first run)

📚 **Documentation:**
- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- [Usage Methods](docs/USAGE_METHODS.md) - Web UI vs Script comparison
- [Extraction Guide](docs/EXTRACTION_GUIDE.md) - Detailed extraction info
- [Troubleshooting](docs/TROUBLESHOOTING_WEB_UI.md) - Common issues & solutions

🔧 **Common Commands:**
```bash
python3 utilities/verify_setup.py           # Verify installation
python3 tests/run_extraction.py             # Run extraction
python3 tests/test_agent_tool.py            # Test agent/tool
```

## Installation

1. **Clone and setup environment:**

```bash
cd ai-pixel-parse
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers:**

```bash
playwright install chromium
```

## Quick Start

### Option 1: Use the ADK Web UI (Recommended) 🌐

Start the interactive web interface:

```bash
# Activate environment
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Start ADK web UI
adk start
```

Then chat with the agent:
```
"Extract UI from https://your-app.com and name it YourApp"
```

**See [ADK_WEB_UI_GUIDE.md](ADK_WEB_UI_GUIDE.md) for complete instructions.**

### Option 2: Use the runner script

Edit `tests/run_extraction.py` and configure your target application:

```python
config = create_extraction_config(
    base_url="https://your-app.com/dashboard",
    app_name="YourApp",
    login_url="https://your-app.com/login",
    username="your-username",
    password="your-password",
    max_pages=30
)
```

Then run:

```bash
python tests/run_extraction.py
```

### Option 2: Use as a Python module

```python
import asyncio
from ai_pixel_parse.ui_extractor_agent import create_extraction_config, extract_ui_specifications

async def main():
    # Public app (no login)
    config = create_extraction_config(
        base_url="https://example.com",
        app_name="ExampleApp",
        max_pages=20
    )
    
    output_path = await extract_ui_specifications(config)
    print(f"Specifications saved to: {output_path}")

asyncio.run(main())
```

### Option 3: With login authentication

```python
config = create_extraction_config(
    base_url="https://app.example.com/dashboard",
    app_name="MyApp",
    login_url="https://app.example.com/login",
    username="demo@example.com",
    password="demo123",
    # Optional custom selectors if defaults don't work:
    username_selector="input[name='email']",
    password_selector="input[id='password']",
    submit_selector="button.submit-btn",
    max_pages=50
)

output_path = await extract_ui_specifications(config)
```

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `base_url` | Starting URL to crawl | Required |
| `app_name` | Name for output folder | Required |
| `login_url` | Login page URL | `None` |
| `username` | Login username | `None` |
| `password` | Login password | `None` |
| `username_selector` | CSS selector for username field | `"input[name='username'], input[type='email']"` |
| `password_selector` | CSS selector for password field | `"input[name='password'], input[type='password']"` |
| `submit_selector` | CSS selector for submit button | `"button[type='submit'], input[type='submit']"` |
| `max_pages` | Maximum pages to crawl | `50` |

## Output Structure

After extraction, you'll find organized specifications in `extraction/<app_name>_<timestamp>/`:

```
extraction/
└── YourApp_20250109_143022/        # App-specific timestamped folder
    ├── 00_SUMMARY.txt               # Overview & statistics
    ├── 01_Dashboard.txt             # Page 1 specification
    ├── 02_User_Profile.txt          # Page 2 specification
    ├── README.md                    # Extraction summary
    ├── screenshot_0.png             # Page 1 screenshot
    ├── screenshot_1.png             # Page 2 screenshot
    └── full_extraction.json         # Complete data in JSON
```

### Specification File Format

Each page specification includes:

1. **Page Metadata**: Title, URL, timestamp, screenshot reference
2. **Page Structure**: Header, main content, sidebar, footer layout
3. **Functions & Features**: What the page does, user workflows
4. **Buttons**: All clickable buttons with text, IDs, classes, positions
5. **Forms**: Input fields, validation, submission endpoints
6. **Tables**: Headers, data structure, sample rows
7. **Icons**: SVG and icon fonts with positions
8. **Navigation**: Links and menu structure

## Example Output

```
PAGE SPECIFICATION
================================================================================

Title: User Dashboard
URL: https://app.example.com/dashboard
Screenshot: screenshot_0.png
Extracted: 2025-11-09T14:30:22

FUNCTIONS & FEATURES
--------------------------------------------------------------------------------

[FORM_SUBMISSION]
Form submission: /api/users/search
  Method: GET
  Inputs: 2 fields
    - Search Query: text
    - Filter By: select

[DATA_DISPLAY]
Table display with 15 rows and 5 columns
  Headers: Name, Email, Role, Status, Actions

BUTTONS (8)
--------------------------------------------------------------------------------

[Button] Create New User
  ID: btn-create-user
  Type: button
  Classes: btn btn-primary
  Position: x=1200, y=80, w=150, h=40
  Aria Label: Create new user account

[Button] Export CSV
  ID: btn-export
  Type: button
  Classes: btn btn-secondary
  Position: x=1360, y=80, w=120, h=40
...
```

## Use Cases

1. **UI Migration**: Extract existing app UI to rebuild in new tech stack
2. **Documentation**: Generate comprehensive UI documentation automatically
3. **Design System**: Identify reusable components and patterns
4. **Quality Assurance**: Catalog all UI elements for testing
5. **AI Training**: Feed specifications to another agent to generate code

## Integration with Code Generation

The output specifications are designed to be consumed by code generation agents:

```python
# Read specifications
import json

with open('extraction/MyApp_20250109/full_extraction.json') as f:
    specs = json.load(f)

# Feed to code generation agent
for page in specs:
    # Agent can now generate React/Vue/Angular components
    # based on buttons, forms, tables, etc.
    pass
```

## Advanced Usage

### Custom Component Extraction

Extend `UIExtractor.extract_page_components()` to extract custom component types:

```python
# In ui_extractor_agent.py, add to extract_page_components():
page_data['components']['custom_widgets'] = await page.evaluate("""
    () => {
        const widgets = [];
        document.querySelectorAll('.custom-widget').forEach((widget, idx) => {
            widgets.push({
                id: widget.id || `widget_${idx}`,
                type: widget.dataset.type,
                config: JSON.parse(widget.dataset.config || '{}')
            });
        });
        return widgets;
    }
""")
```

### Vision-Based Analysis

The agent captures screenshots. You can enhance it with vision models:

```python
# Use Gemini Vision to analyze screenshots
from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content([
    "Describe the visual hierarchy and design patterns in this UI",
    {"mime_type": "image/png", "data": screenshot_data}
])
```

## Troubleshooting

**Login not working?**
- Inspect the login page and update selectors in config
- Check for CAPTCHA or MFA (may need manual handling)
- Verify credentials are correct

**Missing components?**
- Some components may load via JavaScript after page load
- Increase wait time: modify `wait_until='networkidle'` timeout
- Check browser console for errors

**Too many/too few pages?**
- Adjust `max_pages` parameter
- Check that navigation links are being detected correctly
- Verify `base_url` matches the domain structure

**ADK Web UI not working?**
- See [TROUBLESHOOTING_WEB_UI.md](TROUBLESHOOTING_WEB_UI.md) for detailed ADK-specific troubleshooting
- Run `python3 test_agent_tool.py` to verify the tool works
- Make sure agent has `functions=[extract_ui_tool]` registered

## Architecture

- **UIExtractor**: Core class handling browser automation and extraction
- **ui_extractor_agent**: Google ADK Agent with extraction instructions
- **Playwright**: Headless browser for page interaction
- **Output**: Structured text files + JSON + screenshots

## Contributing

To add new extraction features:

1. Add extraction logic to `UIExtractor.extract_page_components()`
2. Update output formatting in `save_specifications()`
3. Document the new capability in this README

## License

[Add your license here]

## Support

For issues or questions:
- Check the troubleshooting section above
- Review example configurations in `tests/run_extraction.py`
- Run setup verification with `python utilities/verify_setup.py`
- Examine output specifications to verify extraction quality
