# AI Pixel Parse - Folder Structure

## Repository Structure

```
ai-pixel-parse/
├── ai_pixel_parse/                  # Main package
│   ├── __init__.py                  # Package exports
│   ├── agent.py                     # Root agent configuration
│   └── ui_extractor_agent.py        # UI extraction agent & tool
│
├── tests/                           # Test and runner scripts
│   ├── run_extraction.py            # Main runner script
│   ├── test_agent_tool.py           # Agent/tool testing utilities
│   └── test_behavioral_extraction.py # Behavioral extraction tests
│
├── utilities/                       # Utility scripts
│   └── verify_setup.py              # Setup verification
│
├── docs/                            # Documentation
│   ├── ADK_WEB_UI_GUIDE.md          # Web UI usage guide
│   ├── BEHAVIORAL_SPECS.md          # Behavioral specs guide
│   ├── EXTRACTION_GUIDE.md          # Extraction details
│   ├── FOLDER_STRUCTURE.md          # This file
│   ├── QUICKSTART.md                # Quick start guide
│   ├── TROUBLESHOOTING_WEB_UI.md    # Troubleshooting tips
│   └── USAGE_METHODS.md             # Methods comparison
│
├── extraction/                      # Output directory (created on first run)
│   └── <AppName>_<timestamp>/       # Timestamped app-specific folder
│       ├── 00_SUMMARY.txt           # Overview & statistics
│       ├── 01_PageName.txt          # Page 1 behavioral specifications
│       ├── 02_PageName.txt          # Page 2 behavioral specifications
│       ├── ...                      # Additional page specs
│       ├── README.md                # Extraction summary & navigation
│       ├── screenshot_0.png         # Page 1 screenshot
│       ├── screenshot_1.png         # Page 2 screenshot
│       ├── ...                      # Additional screenshots
│       └── full_extraction.json     # Complete structured data
│
├── .github/
│   └── copilot-instructions.md      # AI agent guidance
│
├── adk_config.py                    # ADK configuration
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # Main documentation
```

## Output Directory Details

### Key Features

✅ **Self-contained**: Each extraction run is in its own timestamped subfolder
✅ **No clutter**: Parent `extraction/` directory contains only app subfolders
✅ **Complete**: All artifacts (specs, screenshots, README, JSON) in one place
✅ **Timestamped**: Easy to identify and compare different extraction runs
✅ **Organized**: Consistent naming and structure across all extractions

### Folder Naming Convention

```
extraction/
├── GoogleTest_20251112_143022/      # Format: <AppName>_<YYYYMMDD>_<HHMMSS>
├── ExampleApp_20251112_150245/
└── MyApp_20251113_091530/
```

### File Types in Each Extraction

| File Type | Pattern | Purpose |
|-----------|---------|---------|
| Summary | `00_SUMMARY.txt` | High-level statistics and overview |
| Page Specs | `01_PageName.txt`, `02_PageName.txt`, ... | Detailed behavioral specifications per page |
| README | `README.md` | Quick navigation and extraction info |
| Screenshots | `screenshot_0.png`, `screenshot_1.png`, ... | Visual reference for each page |
| JSON Data | `full_extraction.json` | Complete structured data for programmatic use |

## Example: Complete Extraction Output

```
extraction/
└── MyApp_20251112_143022/
    ├── 00_SUMMARY.txt               # 156 lines
    │   ├── Application name
    │   ├── Extraction date
    │   ├── Total pages
    │   ├── Component counts
    │   └── Page list
    │
    ├── 01_Dashboard.txt             # 450 lines
    │   ├── Page metadata
    │   ├── Functions & features
    │   ├── Button specifications
    │   ├── Form specifications
    │   ├── Table specifications
    │   └── Navigation links
    │
    ├── 02_User_Profile.txt          # 320 lines
    │   └── ... (same structure)
    │
    ├── 03_Settings.txt              # 280 lines
    │   └── ... (same structure)
    │
    ├── README.md                    # 25 lines
    │   ├── Extraction summary
    │   ├── Statistics
    │   └── Artifact descriptions
    │
    ├── screenshot_0.png             # Dashboard screenshot
    ├── screenshot_1.png             # User Profile screenshot
    ├── screenshot_2.png             # Settings screenshot
    │
    └── full_extraction.json         # 8,450 lines
        └── Complete structured data for all pages
```

## Migration from Old Structure

### Old Structure (Deprecated)
```
extraction/
├── README.md                        # ❌ Top-level README (removed)
├── screenshot_0.png                 # ❌ Loose screenshots (moved)
├── screenshot_1.png                 # ❌ Loose screenshots (moved)
└── AppName_timestamp/
    ├── 00_SUMMARY.txt
    ├── *.txt
    └── full_extraction.json
```

### New Structure (Current)
```
extraction/
└── AppName_timestamp/               # ✅ Everything in app folder
    ├── 00_SUMMARY.txt
    ├── *.txt
    ├── README.md                    # ✅ README inside app folder
    ├── screenshot_*.png             # ✅ Screenshots inside app folder
    └── full_extraction.json
```

## Accessing Output Files

### Command Line

```bash
# List all extractions
ls -la extraction/

# View latest extraction
ls -la extraction/$(ls -t extraction/ | head -1)

# Read summary
cat extraction/MyApp_20251112_143022/00_SUMMARY.txt

# View README
cat extraction/MyApp_20251112_143022/README.md

# Open screenshot
open extraction/MyApp_20251112_143022/screenshot_0.png

# Process JSON
jq '.[] | .title' extraction/MyApp_20251112_143022/full_extraction.json
```

### Python

```python
from pathlib import Path
import json

# Find latest extraction
extraction_dir = Path("extraction")
latest = max(extraction_dir.glob("*/"), key=lambda p: p.stat().st_mtime)

# Read summary
summary = (latest / "00_SUMMARY.txt").read_text()

# Read JSON
with open(latest / "full_extraction.json") as f:
    data = json.load(f)

# List all page specs
page_specs = sorted(latest.glob("*.txt"))
for spec in page_specs:
    print(spec.name)
```

## Benefits of This Structure

1. **Clean workspace**: Parent directory stays clean with only app subfolders
2. **Easy cleanup**: Delete entire app folder to remove all related artifacts
3. **Version comparison**: Keep multiple extractions and compare changes over time
4. **Portable**: Copy entire app folder to share complete extraction results
5. **Organized**: All related files grouped logically by extraction run
6. **Timestamped**: Automatic chronological ordering and identification

## Notes

- The `extraction/` directory is created automatically on first run
- Each extraction creates a new timestamped subfolder
- No files are created in the parent `extraction/` directory
- Old extractions are preserved (manual cleanup required if needed)
- Screenshots are automatically moved from workspace root to app folder
- All file paths in specifications reference files within the same subfolder
