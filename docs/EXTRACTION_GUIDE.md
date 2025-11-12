# AI Pixel Parse - Enhanced Behavioral Extraction

## Summary of Changes

Your UI extraction agent has been significantly enhanced to capture **behavioral and functional specifications** instead of just visual/structural information. This makes it perfect for rebuilding applications with the same functionality in any tech stack.

## What Has Been Enhanced

### 1. **Button Extraction** 
Now captures:
- ✅ Form submission behavior (which form, action, method)
- ✅ Navigation targets
- ✅ Modal/dialog triggers
- ✅ Custom action identifiers
- ✅ Confirmation requirements
- ✅ AJAX/async operations
- ✅ State toggles
- ✅ Expand/collapse behavior
- ✅ Disabled state
- ✅ Keyboard accessibility
- ✅ Event handlers (onclick)
- ✅ Data attributes for behavior

### 2. **Form & Input Extraction**
Now captures:
- ✅ **Form behaviors**: AJAX submission, client validation, file uploads, auto-save, confirmation
- ✅ **Validation rules**: Required, pattern, min/max length, min/max value, step, custom validation
- ✅ **Input behaviors**: Autocomplete, autofocus, readonly, disabled, multiple selection, live validation
- ✅ Placeholders and default values
- ✅ Select options with selected state
- ✅ Submit buttons per form

### 3. **Table Extraction**
Now captures:
- ✅ Sortable columns
- ✅ Filterable data
- ✅ Pagination
- ✅ Row selection (checkboxes/radio)
- ✅ Row-level actions (edit, delete, view)
- ✅ Inline editing capability
- ✅ Expandable rows

### 4. **Link Extraction** (NEW)
Now captures:
- ✅ External vs internal links
- ✅ Opens in new tab
- ✅ File downloads
- ✅ Custom actions
- ✅ Authentication requirements
- ✅ AJAX links
- ✅ Confirmation dialogs

### 5. **Output Format**
Enhanced text files now show:
- ✅ **BEHAVIORS** section for each component
- ✅ **VALIDATION** rules for inputs
- ✅ **TABLE INTERACTIONS** for data grids
- ✅ **ACCESSIBILITY** information
- ✅ **EVENT HANDLERS** preview
- ✅ **DATA ATTRIBUTES** that contain behavior info

## Example Output

```
[Button] Submit Application

  BEHAVIORS:
    - Submits form
      → Form: application_form
      → Action: /api/applications/submit
      → Method: POST
    - Requires confirmation before action
    - Performs async/AJAX operation

  ACCESSIBILITY:
    - Label: Submit your application for review
    - Keyboard accessible

  DATA ATTRIBUTES:
    - data-confirm: Are you sure you want to submit?
    - data-remote: true
    - data-track: submit_application


[Form] registration_form
  Action: /register
  Method: POST
  Encoding: multipart/form-data

  FORM BEHAVIORS:
    - Submits via AJAX (no page reload)
    - Has client-side validation
    - Supports file uploads
    - Auto-saves form data

  INPUTS (6):

    [EMAIL] Email Address
      ID: email_input
      Name: email

      VALIDATION:
        - Required field
        - Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
        - Max length: 255

      BEHAVIORS: autocomplete enabled, live validation
      Placeholder: Enter your email address

    [PASSWORD] Password
      ID: password_input
      Name: password

      VALIDATION:
        - Required field
        - Min length: 8
        - Max length: 128
        - Pattern: ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)

      BEHAVIORS: live validation


[Table] users_table
  Dimensions: 150 rows × 5 columns
  Headers: Name, Email, Role, Status, Actions

  TABLE INTERACTIONS:
    - Sortable columns
    - Filterable data
    - Paginated results
    - Row selection (checkboxes)
    - Row-level actions available

  ROW ACTIONS:
    - Edit
      Action: openEditModal(userId)
    - Delete
      Action: deleteUser(userId)
    - View Details
```

## Usage

### Running Extraction

```bash
python3 tests/run_extraction.py
```

Or programmatically:

```python
import asyncio
from ai_pixel_parse import create_extraction_config, extract_ui_specifications

async def main():
    config = create_extraction_config(
        base_url="https://your-app.com",
        app_name="YourApp",
        max_pages=30
    )
    
    output_path = await extract_ui_specifications(config)
    print(f"Output: {output_path}")

asyncio.run(main())
```

### With Authentication

```python
config = create_extraction_config(
    base_url="https://app.example.com/dashboard",
    app_name="SecureApp",
    login_url="https://app.example.com/login",
    username="demo@example.com",
    password="demo123",
    max_pages=50
)
```

## Output Location

All extractions are saved to: `extraction/[AppName]_[timestamp]/`

**Folder Structure:**
```
extraction/
└── AppName_20251112_143022/     # Timestamped app-specific folder
    ├── 00_SUMMARY.txt            # Statistics and overview
    ├── 01_PageName.txt           # Page 1 behavioral specs
    ├── 02_PageName.txt           # Page 2 behavioral specs
    ├── README.md                 # Quick navigation guide
    ├── screenshot_0.png          # Page 1 screenshot
    ├── screenshot_1.png          # Page 2 screenshot
    └── full_extraction.json      # Complete structured data
```

**Note:** All files (including screenshots and README) are contained within the app-specific timestamped subfolder. No files are created in the parent `extraction/` directory.

## Troubleshooting

### If extraction results are empty:

1. **Check Playwright installation**:
   ```bash
   playwright install --with-deps chromium
   ```

2. **Run with error logging**:
   The extractor now includes detailed logging. Watch for:
   - "Page loaded successfully"
   - "Components extracted: X buttons, Y forms"
   - Error stack traces if something fails

3. **Test with a simple site first**:
   ```python
   config = create_extraction_config(
       base_url="https://example.com",
       app_name="Test",
       max_pages=1
   )
   ```

4. **Check if site blocks automation**:
   Some sites block Playwright/headless browsers. Try with `headless=False` in the `UIExtractor` initialization.

## What's Different from Visual Extraction

### ❌ NOT Captured (by design):
- CSS classes (unless behavior-related)
- Pixel positions and dimensions
- Colors, fonts, styling
- Visual layout
- Decorative icons
- Spacing and margins

### ✅ Focused On:
- What users can DO
- How interactions work
- What validations apply
- What data operations are available
- How navigation flows
- What confirmations are needed
- What happens asynchronously

## Use Cases

Perfect for:
1. **Rebuilding apps** in different frameworks
2. **Creating functional clones** with your own design
3. **API requirement gathering**
4. **Test case generation**
5. **Technical documentation**
6. **Accessibility audits**

## Documentation

- `BEHAVIORAL_SPECS.md` - Complete guide to what's captured
- This file - Quick start and troubleshooting
- `ADK_WEB_UI_GUIDE.md` - Google ADK integration
- `TROUBLESHOOTING_WEB_UI.md` - Common issues

## Next Steps

1. Run an extraction on your target application
2. Review the generated specifications in `extraction/`
3. Use the behavioral specs to rebuild functionality in your chosen tech stack
4. The JSON file can be fed to code generation agents for automated implementation

---

**Note**: The extraction focuses on *behavior and function*, not *appearance and style*. This is intentional to give you freedom in how you implement the UI while preserving all interactive capabilities.
