# Using UI Extraction Agent with ADK Web UI

This guide shows how to use the UI extraction agent through the Google ADK web interface.

## Setup for ADK Web UI

### 1. Install ADK (if not already installed)

```bash
# Activate your virtual environment
source venv/bin/activate

# Install Google ADK
pip install google-adk
```

### 2. Start the ADK Web Interface

```bash
# From the project root directory
adk start
```

This will:
- Start the ADK web server
- Open your browser to the ADK interface
- Load the agents defined in your project

### 3. Access Your Agents

The ADK web UI will automatically discover and load:
- `root_agent` - Basic conversational agent
- `ui_extractor_agent` - UI extraction specialist

---

## Using UI Extraction Agent in the Web UI

### Important Note About ADK Limitations

The current version of Google ADK doesn't support automatic function calling from the web UI chat interface. However, the agent can still help you extract UI specifications by guiding you through the process.

### Method 1: Agent-Guided Script Usage (Current Best Approach)

When you chat with the agent in the web UI, it will help you set up and run the extraction:

**Example conversation:**

```
You: "Extract the UI from https://google.com and save it as Google"

Agent: I can help you extract UI from https://google.com! Here's how to do it:

1. Edit tests/run_extraction.py and update the configuration:

   config = create_extraction_config(
       base_url="https://google.com",
       app_name="Google",
       max_pages=30
   )

2. Run the extraction:
   python3 tests/run_extraction.py

3. The output will be saved to: extraction/Google_<timestamp>/

Would you like me to provide code for authentication or custom selectors?
```

### Method 2: Get Copy-Paste Code from Agent

Ask the agent to generate ready-to-run code:

```
You: "Give me Python code to extract UI from example.com with login"

Agent: Here's the code you can run:

```python
import asyncio
from ai_pixel_parse.ui_extractor_agent import extract_ui_tool

async def main():
    result = await extract_ui_tool(
        base_url="https://example.com",
        app_name="Example",
        login_url="https://example.com/login",
        username="your-username",
        password="your-password",
        max_pages=30
    )
    print(result)

asyncio.run(main())
```

Save this to a file and run: python3 your_file.py
```

### Method 3: Use Terminal Commands (Recommended)

In the ADK web UI, you can also invoke functions directly:

The best way to use extraction is through the terminal alongside the web UI:

**Terminal workflow:**
```bash
# 1. Edit tests/run_extraction.py with your config (agent can help you write this)
# 2. Run the script
python3 tests/run_extraction.py
```

**While extraction runs**, you can:
- Chat with the agent about what's being extracted
- Ask questions about the output format
- Get help with next steps (code generation, etc.)

### What the Agent CAN Help You With

✅ **Configuration assistance**
- Generate correct config code for your use case
- Provide custom selector examples
- Help with authentication setup

✅ **Code generation**
- Provide ready-to-run Python scripts
- Create custom extraction configurations
- Generate code to parse the output

✅ **Understanding output**
- Explain the extracted specifications
- Help navigate the output files
- Guide you through using the data

✅ **Troubleshooting**
- Debug login issues
- Help with custom selectors
- Explain error messages

### Example Conversations

#### Getting Started

```
You: "I need to extract UI from my app at https://myapp.com/dashboard"

Agent: I'll help you set up the extraction! Here's what you need:

1. Edit tests/run_extraction.py:
   
   config = create_extraction_config(
       base_url="https://myapp.com/dashboard",
       app_name="MyApp",
       max_pages=30
   )

2. Run: python3 tests/run_extraction.py

Does your app require login? If so, I can add authentication to the config.
```

#### With Authentication

---

## Conversational Examples

### Example 1: Public Website

**You:** 
> Extract the UI from httpbin.org for testing. Call it HTTPBinTest.

**Agent Response:**
```
🚀 Starting UI extraction for: HTTPBinTest
   Base URL: https://httpbin.org
   Max pages: 30

Extracting: https://httpbin.org
  ✓ Extracted 5 buttons, 2 forms, 1 tables

✅ Extraction complete! Processed 8 pages
📁 Output saved to: extraction/HTTPBinTest_20250109_150245

Next steps:
1. Review the generated specifications
2. Check screenshots
3. Use JSON data for code generation
```

### Example 2: Authenticated Application

**You:**
> I need to extract UI from our admin panel:
> - URL: https://admin.company.com/dashboard
> - Login at: https://admin.company.com/login
> - Username: admin@company.com
> - Password: SecurePass123
> - Name: CompanyAdmin
> - Crawl 40 pages

**Agent Response:**
```
🚀 Starting UI extraction for: CompanyAdmin
   Base URL: https://admin.company.com/dashboard
   Login: Enabled
   Max pages: 40

✓ Logged in successfully to https://admin.company.com/login

Extracting: https://admin.company.com/dashboard
  ✓ Extracted 12 buttons, 3 forms, 2 tables

Extracting: https://admin.company.com/users
  ✓ Extracted 8 buttons, 1 forms, 1 tables

[... continues crawling ...]

✅ Extraction complete! Processed 35 pages
📁 Output saved to: extraction/CompanyAdmin_20250109_150612

Total UI Components:
  - Buttons: 287
  - Forms: 42
  - Tables: 18
  - Icons: 156
```

### Example 3: Custom Selectors

**You:**
> Extract from https://custom-app.com but the login form uses weird selectors.
> Login page: https://custom-app.com/signin
> Username field: input#email-input
> Password field: input#pass-field
> Submit button: button.submit-login
> User: test@example.com
> Pass: test123
> Name it CustomApp

**Agent Response:**
```
🚀 Starting UI extraction for: CustomApp with custom login selectors

✓ Logged in successfully using custom selectors

[Continues extraction...]
```

---

## Viewing Results in Web UI

After extraction completes, the agent will provide:

1. **Summary statistics**: Number of pages, components extracted
2. **Output location**: Path to `extraction/` folder
3. **Direct links** (if ADK supports file viewing):
   - View summary (`00_SUMMARY.txt`)
   - Browse page specifications
   - See screenshots

You can then ask follow-up questions:

**You:** "Show me the buttons from the dashboard page"

**Agent:** Will read and display button specifications

**You:** "How many forms were found across all pages?"

**Agent:** Will analyze and provide count with details

**You:** "Generate React components from the extracted specifications"

**Agent:** Can use the JSON data to help generate code

---

## Advanced Web UI Usage

### Monitoring Extraction Progress

The agent provides real-time updates in the chat:

```
🚀 Starting UI extraction...
✓ Logged in successfully
Extracting: [Page 1/30] Dashboard
  ✓ Extracted 12 buttons, 3 forms, 2 tables
Extracting: [Page 2/30] Users List
  ✓ Extracted 8 buttons, 1 forms, 1 tables
...
```

### Handling Errors

If login fails or pages can't be accessed:

```
✗ Error: Login failed
Suggestion: Check credentials or use custom selectors for the login form.
Try: input#your-username-field for the username selector
```

### Customizing Extraction

**You:** "Extract from example.com but only crawl 10 pages"

**You:** "Extract from myapp.com and find all the forms on every page"

**You:** "Extract from dashboard.app.com and focus on the data tables"

The agent understands natural language instructions and adjusts parameters accordingly.

---

## Accessing Output Files

### From the Web UI

After extraction, ask:

**You:** "Show me the summary of what was extracted"

**You:** "What buttons are on the login page?"

**You:** "Display the table structures found"

### From File System

Output is saved in timestamped app-specific subfolders within `extraction/`:

```bash
# View summary
cat extraction/YourApp_20250109_150245/00_SUMMARY.txt

# View extraction info
cat extraction/YourApp_20250109_150245/README.md

# View page specification
cat extraction/YourApp_20250109_150245/01_Dashboard.txt

# View screenshots
open extraction/YourApp_20250109_150245/screenshot_0.png

# View JSON data
cat extraction/YourApp_20250109_150245/full_extraction.json
```

**Note:** All files including screenshots and README are contained within the app-specific timestamped subfolder.

---

## Tips for Best Results

### 1. Start Small
Begin with a low `max_pages` value (10-15) to test:

**You:** "Extract from myapp.com, call it TestRun, limit to 10 pages"

### 2. Provide Clear Credentials
For authenticated apps, provide all login details:

```
URL: [base URL]
Login URL: [login page]
Username: [your username]
Password: [your password]
```

### 3. Use Custom Selectors When Needed
If login fails, inspect the form and provide selectors:

**You:** "The username field is input.email-field and password is input.pwd"

### 4. Iterate on Results
After first extraction, refine:

**You:** "Extract again but crawl 50 pages this time"

**You:** "Extract from the same URL but skip the login"

---

## Common Web UI Workflows

### Workflow 1: Quick Extraction
```
You: "Extract UI from example.com, name it Example"
[Review output in chat]
You: "Show me all the buttons found"
[Agent displays button specifications]
```

### Workflow 2: Authenticated App Extraction
```
You: "I need to extract from [URL] with login"
Agent: "Please provide login URL, username, and password"
You: [Provides credentials]
Agent: [Performs extraction]
You: "How many pages were extracted?"
Agent: [Provides statistics]
```

### Workflow 3: Code Generation
```
You: "Extract UI from myapp.com"
[Extraction completes]
You: "Now generate React components for the dashboard page"
[Agent reads specifications and generates code]
You: "Generate the user form component"
[Agent creates form based on extracted specs]
```

---

## Troubleshooting in Web UI

### Issue: "Playwright not installed"

**Solution:**
```bash
# In terminal
source venv/bin/activate
playwright install chromium
```

Then restart ADK web UI.

### Issue: "Can't access website"

**Check:**
- Is the URL correct?
- Is the site publicly accessible?
- Do you need VPN/network access?

### Issue: "Login not working"

**In chat, ask:**
**You:** "Use custom login selectors: username=input#email, password=input#pwd, submit=button.login"

---

## Configuration Options via Chat

You can specify all options in natural language:

| What You Want | What to Say |
|---------------|-------------|
| Change max pages | "Crawl only 20 pages" |
| Skip login | "Don't use authentication" |
| Custom selectors | "Username field is input#user" |
| Change output name | "Call it MyNewApp" |
| Different base URL | "Start from /dashboard instead" |

---

## Next Steps

1. **Start ADK:** `adk start`
2. **Open web UI** (browser opens automatically)
3. **Select** `ui_extractor_agent` from agent list
4. **Chat:** "Extract UI from [your URL]"
5. **Review** output in `extraction/` folder
6. **Generate code** using the specifications

---

## Advanced: Batch Extraction

**You:** "I need to extract UI from 3 different applications"

**Agent:** "Please provide the details for each application"

**You:** 
```
App 1: https://app1.com, name it App1
App 2: https://app2.com, name it App2  
App 3: https://app3.com with login at https://app3.com/login, 
       username: user@example.com, password: pass123, name it App3
```

**Agent:** [Runs extraction for each app sequentially]

---

**Ready to use the web UI!** Start ADK with `adk start` and begin extracting! 🚀
