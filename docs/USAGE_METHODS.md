# UI Extraction Agent - Usage Methods

## Two Ways to Use the Agent

### 🌐 Method 1: ADK Web UI (Interactive & Conversational)

**Best for:**
- Interactive exploration
- Quick extractions
- Conversational workflow
- Iterative refinement
- Learning the tool

**How it works:**
```
┌─────────────────────────────────────────────┐
│         ADK Web UI (Browser)                │
│                                             │
│  You: "Extract UI from example.com"         │
│                                             │
│  Agent: [Performs extraction]               │
│         ✓ Logged in                         │
│         ✓ Extracted 20 pages                │
│         📁 Output: extraction/Example/      │
│                                             │
│  You: "Show me the buttons found"           │
│                                             │
│  Agent: [Displays button specifications]    │
└─────────────────────────────────────────────┘
```

**Start with:**
```bash
adk start
```

**Advantages:**
- ✅ Natural language - no coding needed
- ✅ Real-time feedback and progress
- ✅ Easy error handling and retry
- ✅ Can ask questions about results
- ✅ Perfect for exploration

**See:** [ADK_WEB_UI_GUIDE.md](ADK_WEB_UI_GUIDE.md)

---

### 💻 Method 2: Python Scripts (Programmatic & Automated)

**Best for:**
- Automated workflows
- Batch processing
- CI/CD integration
- Scheduled extractions
- Advanced customization

**How it works:**
```python
# tests/run_extraction.py or your custom script

config = create_extraction_config(
    base_url="https://your-app.com",
    app_name="YourApp",
    login_url="https://your-app.com/login",
    username="user",
    password="pass",
    max_pages=50
)

output_path = await extract_ui_specifications(config)
```

**Run with:**
```bash
python3 tests/run_extraction.py
```

**Advantages:**
- ✅ Fully automated - runs unattended
- ✅ Easy to integrate into pipelines
- ✅ Batch process multiple apps
- ✅ Scriptable and customizable
- ✅ Perfect for production use

**See:** [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)

---

## Comparison

| Feature | Web UI | Python Script |
|---------|--------|---------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ No coding | ⭐⭐⭐⭐ Basic Python |
| **Interactive** | ⭐⭐⭐⭐⭐ Conversational | ⭐ One-shot |
| **Automation** | ⭐⭐ Manual trigger | ⭐⭐⭐⭐⭐ Fully automated |
| **Learning Curve** | ⭐⭐⭐⭐⭐ Very easy | ⭐⭐⭐⭐ Easy |
| **Real-time Feedback** | ⭐⭐⭐⭐⭐ Live updates | ⭐⭐⭐ Console output |
| **Batch Processing** | ⭐⭐ One at a time | ⭐⭐⭐⭐⭐ Process many |
| **CI/CD Integration** | ⭐ Not suitable | ⭐⭐⭐⭐⭐ Perfect fit |
| **Error Recovery** | ⭐⭐⭐⭐⭐ Easy to retry | ⭐⭐⭐ Requires code |
| **Customization** | ⭐⭐⭐ Via chat | ⭐⭐⭐⭐⭐ Full control |

---

## Which Should I Use?

### Use Web UI if you:
- 🎯 Are extracting manually or occasionally
- 🎯 Want to explore what the agent can do
- 🎯 Prefer conversational interfaces
- 🎯 Need to iterate and refine extraction
- 🎯 Want immediate visual feedback
- 🎯 Are new to the tool

### Use Python Scripts if you:
- 🎯 Need to automate extractions
- 🎯 Want to process multiple apps
- 🎯 Are building a pipeline/workflow
- 🎯 Need scheduled/triggered runs
- 🎯 Require advanced customization
- 🎯 Are integrating with other tools

---

## Workflow Examples

### Web UI Workflow

```
1. Start ADK: adk start
2. Open browser (auto-opens)
3. Select ui_extractor_agent
4. Chat: "Extract from example.com as ExampleApp"
5. Review output in chat
6. Ask: "Show me the forms found"
7. Agent displays form specifications
8. Chat: "Generate React form component"
9. Agent helps generate code
```

### Script Workflow

```
1. Edit tests/run_extraction.py with config
2. Run: python3 tests/run_extraction.py
3. Wait for completion
4. Check extraction/ folder
5. Use JSON data in your pipeline
6. Generate code programmatically
```

### Hybrid Workflow

```
1. Use Web UI for initial exploration
   - Test with small max_pages
   - Verify login works
   - Check output quality

2. Once satisfied, create script:
   - Copy working config to script
   - Automate for production use
   - Schedule or trigger as needed
```

---

## Quick Start Commands

### Web UI
```bash
# One-time setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Every time
adk start
# Then chat in browser
```

### Script
```bash
# One-time setup (same as above)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Every time
python3 tests/run_extraction.py
```

---

## Output is Identical

Both methods produce the same output:

```
extraction/
└── YourApp_20250109_150245/        # App-specific timestamped folder
    ├── 00_SUMMARY.txt               # Overview & statistics
    ├── 01_Page1.txt                 # Page 1 specifications
    ├── 02_Page2.txt                 # Page 2 specifications
    ├── README.md                    # Extraction summary
    ├── screenshot_0.png             # Page 1 screenshot
    ├── screenshot_1.png             # Page 2 screenshot
    └── full_extraction.json         # Complete JSON data
```

---

## Need Help?

- **Web UI Guide:** [ADK_WEB_UI_GUIDE.md](ADK_WEB_UI_GUIDE.md)
- **Script Guide:** [README.md](../README.md) and [QUICKSTART.md](QUICKSTART.md)
- **Examples:** [tests/run_extraction.py](../tests/run_extraction.py)
- **Verification:** Run `python3 utilities/verify_setup.py`

---

**Recommendation:** Start with the **Web UI** to learn and explore, then move to **scripts** for automation! 🚀
