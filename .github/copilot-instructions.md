## Purpose

This file helps AI coding agents become productive in this repository quickly by describing the minimal architecture, important files, and concrete patterns to change safely.

## Quick project summary

- Repository layout (relevant files):
  - `ai_pixel_parse/agent.py` — core module with the basic LLM agent instance (`root_agent`).
  - `ai_pixel_parse/ui_extractor_agent.py` — specialized agent for web UI extraction with Playwright automation.
  - `ai_pixel_parse/__init__.py` — package entry that exposes agents.
  - `tests/run_extraction.py` — runner script to execute UI extraction on target web apps.
  - `tests/test_agent_tool.py` — testing utilities for agent and tool validation.
  - `utilities/verify_setup.py` — setup verification script.
  - `docs/` — comprehensive documentation files.
  - `extraction/` — output folder for generated UI specifications (created on first run).

- Big picture: this repo provides AI agents built with `google.adk` for extracting comprehensive UI specifications from web applications. The primary agent (`ui_extractor_agent`) automates browser interaction, handles authentication, crawls pages, and generates detailed component specifications that can be used by code generation agents to rebuild UIs in any tech stack.

## What to change and how (high-value, low-risk edits)

### Basic Agent Configuration

- To change the basic assistant behavior, edit `ai-pixel-parse/agent.py` where `root_agent` is created. Example fields to update:
  - `model`: the model id string (currently `gemini-2.5-flash`).
  - `name`, `description`, `instruction`: high-level prompts that control agent behavior.

### UI Extraction Agent

- To modify extraction behavior, edit `ai-pixel-parse/ui_extractor_agent.py`:
  - `UIExtractor.extract_page_components()`: Add new component types or modify extraction logic for buttons, forms, tables, icons, etc.
  - `UIExtractor.save_specifications()`: Change output format or add new specification sections.
  - `ui_extractor_agent` Agent instance: Update extraction instructions and behavior prompts.

- To run extraction on a new application:
  - Edit `tests/run_extraction.py` and configure `create_extraction_config()` with your target app details.
  - Review test configurations in `tests/test_behavioral_extraction.py` for different scenarios (public site, login required, SPA).

- Example pattern used in this repo (follow this shape when adding agents):

```python
from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```

Create additional agents by following the same pattern and exporting them from the package.

## Important integration points & dependencies

- External dependency: `google.adk` (imported as `google.adk.agents.llm_agent`). Any change that affects how the Agent is instantiated or invoked should assume that library's API and authentication are required but are managed outside this repo.
- **Playwright**: Used by `ui_extractor_agent` for browser automation. Install with `playwright install chromium` after pip install.
- **Async/await**: UI extraction runs asynchronously using `asyncio`. All extraction functions are `async def` and must be awaited.
- **Output directory**: Extraction results are saved to `extraction/` folder (created automatically). Each run creates a timestamped app-specific subdirectory (e.g., `extraction/AppName_20251112_143022/`) containing specifications, screenshots, README, and JSON data. All files are self-contained within each run's subfolder.
- There are no tests or CI configuration in this repo; changes that touch runtime behavior should be validated locally with the target `google.adk` environment.

## Developer workflows and quick commands

- There is no build system present. Typical local validation flow:
  1. Create a Python virtualenv and install required runtime packages:
  
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

  2. Verify setup:

```bash
python utilities/verify_setup.py
```

  3. Run extraction script:

```bash
# Edit tests/run_extraction.py with your app config first
python tests/run_extraction.py
```

  4. Check output in `extraction/AppName_timestamp/` subfolder for generated specifications, screenshots, README, and JSON data.

  5. Quick REPL check to import agents:

```python
python -c "import sys; sys.path.insert(0, '.'); from ai_pixel_parse import agent, ui_extractor_agent; print(agent.root_agent); print(ui_extractor_agent.ui_extractor_agent)"
```

Note: The package directory uses hyphens (`ai-pixel-parse`) but imports as underscores (`ai_pixel_parse`).

## Patterns, conventions and gotchas discovered here

- The repository is intentionally minimal: configuration is encoded directly as module-level variables (the Agent instance). Avoid adding complex runtime side-effects at import time.
- Keep agent configuration (prompts, model names) in `agent.py`. If you need stronger separation later, extract a small config module, but keep the same shape (constructor args to `Agent`).
- Do not embed secrets or credentials in repository files — the `google.adk` client will require authentication handled by environment or external config.

## Examples to reference

- See `ai_pixel_parse/agent.py` for the canonical agent instantiation. Use that file as the authoritative example when creating new agent instances.
- See `ai_pixel_parse/ui_extractor_agent.py` for a complete example of:
  - Building a specialized agent with Playwright browser automation
  - Async workflows with `asyncio` 
  - Structured data extraction from web pages
  - Output generation in multiple formats (text, JSON, screenshots)
- See `tests/run_extraction.py` for configuration patterns:
  - Public applications without authentication
  - Login flows with custom selectors
  - Single Page Applications (SPAs)
- See `tests/test_behavioral_extraction.py` for test examples

## When to ask a human

- If you need to change how the `google.adk` client is initialized (authentication, session, custom transports), ask a human — this repo only configures agent instances.
- If you want to add persistent storage, a server, or a test harness, propose a small design first (folder layout + dependencies) before implementing.

## Final notes

- This guidance is intentionally concise and factual — it documents only patterns discoverable in the code. If you'd like, I can expand this with a small local-run README or a simple test harness to exercise the `root_agent`.
