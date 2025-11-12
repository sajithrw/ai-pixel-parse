# Documentation Index

Complete guide to all documentation files in the `docs/` folder.

## Getting Started

### [QUICKSTART.md](QUICKSTART.md)
**Purpose:** Get up and running in 5 minutes  
**Contents:**
- Quick installation steps
- First extraction walkthrough
- Basic usage examples
- Common next steps

**Best for:** New users who want to start immediately

---

### [USAGE_METHODS.md](USAGE_METHODS.md)
**Purpose:** Compare different ways to use AI Pixel Parse  
**Contents:**
- Web UI method (using Google ADK)
- Script method (direct Python)
- Comparison table
- When to use each method

**Best for:** Understanding your workflow options

---

## Detailed Guides

### [EXTRACTION_GUIDE.md](EXTRACTION_GUIDE.md)
**Purpose:** Complete reference for extraction features  
**Contents:**
- Configuration options explained
- Component types extracted
- Behavioral specifications
- Output file formats
- Advanced customization

**Best for:** Understanding what gets extracted and how

---

### [BEHAVIORAL_SPECS.md](BEHAVIORAL_SPECS.md)
**Purpose:** Understanding behavioral focus vs visual extraction  
**Contents:**
- What behavioral specs mean
- Difference from visual specs
- Component behaviors captured
- Use cases for rebuilding UIs

**Best for:** Understanding the extraction philosophy

---

### [ADK_WEB_UI_GUIDE.md](ADK_WEB_UI_GUIDE.md)
**Purpose:** Using AI Pixel Parse through Google ADK Web UI  
**Contents:**
- ADK setup instructions
- Conversational extraction workflow
- Example conversations
- Tips for best results

**Best for:** Users preferring the conversational interface

---

## Reference Documentation

### [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md)
**Purpose:** Complete repository organization reference  
**Contents:**
- Directory structure diagram
- File purposes
- Output organization
- Example extractions
- Command reference

**Best for:** Understanding project layout and finding files

---

### [TROUBLESHOOTING_WEB_UI.md](TROUBLESHOOTING_WEB_UI.md)
**Purpose:** Solving common problems  
**Contents:**
- Installation issues
- Authentication problems
- Empty extraction results
- Browser automation errors
- Setup verification checklist

**Best for:** Debugging issues and error resolution

---

## Special Documents

### [REORGANIZATION_SUMMARY.md](../REORGANIZATION_SUMMARY.md)
**Purpose:** Guide to the new folder structure (Nov 2024)  
**Contents:**
- What changed
- Migration guide
- Updated commands
- Benefits of new structure

**Best for:** Users upgrading from old structure

---

## Quick Reference

| Document | Primary Use Case | Read Time |
|----------|-----------------|-----------|
| QUICKSTART.md | First-time setup | 5 min |
| USAGE_METHODS.md | Choose your workflow | 5 min |
| EXTRACTION_GUIDE.md | Understand extraction | 15 min |
| BEHAVIORAL_SPECS.md | Understand output | 10 min |
| ADK_WEB_UI_GUIDE.md | Use conversational UI | 15 min |
| FOLDER_STRUCTURE.md | Navigate repository | 5 min |
| TROUBLESHOOTING_WEB_UI.md | Fix problems | As needed |

## Suggested Reading Order

### For New Users:
1. **QUICKSTART.md** - Get it working
2. **USAGE_METHODS.md** - Choose your method
3. **BEHAVIORAL_SPECS.md** - Understand output
4. **EXTRACTION_GUIDE.md** - Learn details

### For Troubleshooting:
1. **TROUBLESHOOTING_WEB_UI.md** - Common issues
2. **FOLDER_STRUCTURE.md** - Verify structure
3. Run `python3 utilities/verify_setup.py`

### For Advanced Usage:
1. **EXTRACTION_GUIDE.md** - All options
2. **BEHAVIORAL_SPECS.md** - Output format
3. **FOLDER_STRUCTURE.md** - Output organization
4. Review `tests/run_extraction.py` for examples

## Documentation Standards

All documentation follows these conventions:

- **Code blocks:** Clearly marked with language
- **Commands:** Include full paths (e.g., `tests/run_extraction.py`)
- **Links:** Relative paths from document location
- **Examples:** Real-world, runnable examples
- **Updates:** Reflect latest folder structure

## Contributing to Documentation

When updating docs:

1. Use correct paths: `tests/`, `utilities/`, `docs/`
2. Keep Quick Links in README.md updated
3. Update this index if adding new docs
4. Test all code examples
5. Use consistent formatting

## Getting Help

If documentation doesn't answer your question:

1. Check [TROUBLESHOOTING_WEB_UI.md](TROUBLESHOOTING_WEB_UI.md)
2. Run `python3 utilities/verify_setup.py`
3. Review extraction output in `extraction/`
4. Check `.github/copilot-instructions.md` for technical details

## Documentation Locations

All documentation is now centralized:

```
docs/
├── ADK_WEB_UI_GUIDE.md
├── BEHAVIORAL_SPECS.md
├── EXTRACTION_GUIDE.md
├── FOLDER_STRUCTURE.md
├── QUICKSTART.md
├── TROUBLESHOOTING_WEB_UI.md
└── USAGE_METHODS.md
```

Main README remains in root: `README.md`

## Version History

- **v1.0** (Nov 2024): Initial documentation
- **v1.1** (Nov 2024): Added behavioral specs guide
- **v1.2** (Nov 2024): Reorganized into docs/ folder
- **v1.3** (Nov 2024): Added this index file
