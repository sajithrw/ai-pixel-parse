# Troubleshooting: ADK Web UI Usage

## Current ADK Limitation

**Issue**: The Google ADK doesn't support automatic function calling via the `functions` parameter in the Agent constructor.

**Error you might see**:
```
ValidationError: 1 validation error for LlmAgent
functions
  Extra inputs are not permitted
```

## Solution: Agent-Guided Workflow

The agent can't execute extraction automatically, but it CAN guide you through the process by providing:
- ✅ Exact configuration code
- ✅ Ready-to-run Python scripts  
- ✅ Step-by-step instructions
- ✅ Troubleshooting help

## How to Use the Agent Now

### Approach 1: Ask for Configuration

**You:** "Extract UI from google.com, call it google"

**Agent responds with:**
```
I'll help you extract UI from google.com! Here's how:

1. Edit tests/run_extraction.py with this config:

config = create_extraction_config(
    base_url="https://google.com",
    app_name="google",
    max_pages=30
)

2. Run: python3 tests/run_extraction.py
```

### Approach 2: Ask for Direct Code

**You:** "Give me Python code to extract from example.com"

**Agent provides:**
```python
import asyncio
from ai_pixel_parse.ui_extractor_agent import extract_ui_tool

async def main():
    result = await extract_ui_tool(
        base_url="https://example.com",
        app_name="Example",
        max_pages=30
    )
    print(result)

asyncio.run(main())
```

### Approach 3: Use Terminal Directly (Recommended)

Don't rely on ADK web UI for execution. Instead:

1. **Edit** `tests/run_extraction.py` with your config
2. **Run** in terminal: `python3 tests/run_extraction.py`
3. **Chat with agent** for help, questions, or next steps

---

## What the Agent CAN Help With

✅ Generate configuration code  
✅ Provide authentication examples  
✅ Create custom selector configs  
✅ Explain output format  
✅ Help with troubleshooting  
✅ Guide code generation from results  

❌ Cannot automatically execute extraction from chat  

---

## Recommended Workflow

```
Terminal                          ADK Web UI
--------                          ----------
                              1. "I need to extract from myapp.com"
                              ← Agent provides config code
                                 
2. Edit tests/run_extraction.py    
   (paste agent's config)
   
3. python3 tests/run_extraction.py
   [Extraction runs...]
   
4. Check extraction/ folder
                              5. "Extraction done! Show me the output"
                              ← Agent explains the files
                              
                              6. "Generate React components from this"
                              ← Agent helps with code generation
```

---

## Quick Reference

| What You Want | What to Ask Agent |
|---------------|-------------------|
| Configuration code | "Give me config for extracting from [URL]" |
| Python script | "Provide Python code to extract [URL]" |
| With login | "Include authentication for [URL]" |
| Custom selectors | "Login form uses input#email for username" |
| Help with output | "Explain the extraction output format" |
| Code generation | "Generate React form from extracted specs" |

---

**Bottom Line**: Use the ADK web UI as a helpful assistant that provides code and guidance, then run the actual extraction in your terminal. This gives you the best of both worlds! 🚀

### ✅ Correct Behavior

**You:** "Extract UI from google.com, call it google"

**Agent:** 
```
🚀 Starting UI extraction for: google
   Base URL: https://google.com
   Max pages: 30

Extracting: https://google.com
  ✓ Extracted 5 buttons, 1 forms, 0 tables

✅ Extraction complete! Processed 3 pages

Successfully extracted UI from https://google.com. 
Output saved to: extraction/google_20250109_150245

Extracted 3 pages with:
- 5 buttons
- 1 forms
- 0 tables
- 12 icons

You can find detailed specifications in the output directory.
```

## Testing the Fix

### Option 1: Test the tool directly

```bash
python3 tests/test_agent_tool.py
```

This will verify the extraction tool works before using it in ADK.

### Option 2: Start ADK and try again

```bash
# Make sure dependencies are installed
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Start ADK
adk start
```

Then in the web UI:
```
"Extract UI from google.com, call it google"
```

## Supported Command Patterns

The agent now recognizes these patterns:

| What You Say | What Happens |
|--------------|--------------|
| "Extract UI from google.com, call it google" | Extracts with app_name="google" |
| "Extract from https://example.com" | Extracts with auto-generated name |
| "Get UI specs from myapp.com" | Extracts from myapp.com |
| "Crawl example.com for UI components" | Extracts from example.com |
| "Extract example.com with max 20 pages" | Limits to 20 pages |

### With Authentication

| What You Say | What Happens |
|--------------|--------------|
| "Extract from myapp.com with login at myapp.com/login, user: demo@example.com, password: demo123" | Handles login automatically |
| "Extract myapp.com, login required, user: demo, pass: pass123, login page: myapp.com/signin" | Parses auth details |

## Verification Checklist

Before using in ADK web UI:

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Playwright installed: `playwright install chromium`
- [ ] Test tool works: `python3 tests/test_agent_tool.py`
- [ ] Agent imported correctly: Check `adk_config.py` loads without errors

## Still Not Working?

### Check 1: Verify agent has the function

```python
# In Python REPL
from ai_pixel_parse.ui_extractor_agent import ui_extractor_agent
print(ui_extractor_agent.functions)
# Should show: [<function extract_ui_tool at ...>]
```

### Check 2: Verify ADK is loading the agent

When you run `adk start`, check the console output:
- Should see "ui_extractor_agent" loaded
- Should see function "extract_ui_tool" registered

### Check 3: Test extraction manually

```python
import asyncio
from ai_pixel_parse.ui_extractor_agent import extract_ui_tool

async def test():
    result = await extract_ui_tool(
        base_url="https://httpbin.org",
        app_name="Test",
        max_pages=3
    )
    print(result)

asyncio.run(test())
```

## Additional Notes

### URL Formats Accepted

The agent is flexible with URL formats:
- ✅ `google.com` → Auto-adds `https://`
- ✅ `https://google.com` → Uses as-is
- ✅ `http://example.com` → Uses as-is
- ✅ `www.example.com` → Auto-adds `https://`

### App Name Generation

If you don't provide a name:
- `"Extract from google.com"` → Creates name "Google"
- `"Extract https://my-app.com"` → Creates name "MyApp"

### Default Values

- **max_pages**: 30 (if not specified)
- **login**: Disabled (unless credentials provided)
- **selectors**: Uses sensible defaults (can be overridden)

## Quick Reference

### Minimal Command
```
"Extract UI from example.com"
```

### With Name
```
"Extract UI from example.com, call it Example"
```

### With Page Limit
```
"Extract UI from example.com, max 20 pages, call it Example"
```

### With Login
```
"Extract from example.com/dashboard with login at example.com/login, 
user: demo@example.com, password: demo123, call it Example"
```

### With Custom Selectors
```
"Extract from example.com with login, username field is input#email, 
password field is input#pwd, submit button is button.submit"
```

---

**Updated:** The agent now has proper tool integration. Try your command again in the ADK web UI!
