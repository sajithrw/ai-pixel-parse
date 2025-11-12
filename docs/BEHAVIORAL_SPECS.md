# Behavioral UI Specifications

This document describes the behavioral and functional information extracted by the UI extraction agent.

## Overview

The extraction focuses on **interactive behaviors** and **functional specifications** rather than visual styling. This makes the output ideal for rebuilding applications with different tech stacks while preserving the same user interactions and features.

## What Is Captured

### 1. **Buttons & Interactive Elements**

For each button/clickable element, the extraction captures:

#### Behaviors:
- **submitsForm**: Whether the button submits a form
  - If yes, includes form context (form ID, action URL, method)
- **navigatesTo**: Navigation target (URL or route)
- **opensModal**: Opens a modal/dialog
- **triggersAction**: Custom action identifier
- **hasConfirmation**: Requires user confirmation before action
- **isAsync**: Performs AJAX/async operation
- **togglesState**: Toggles pressed/unpressed state
- **expandsCollapse**: Expands/collapses content
- **disabled**: Current disabled state

#### Accessibility:
- Keyboard accessible (tab index)
- ARIA labels and roles
- Screen reader support

#### Event Handlers:
- onclick handlers (function code)
- Data attributes that may contain behavior info

**Example Output:**
```
[Button] Submit Application

  BEHAVIORS:
    - Submits form
      → Form: application_form
      → Action: /api/submit
      → Method: POST
    - Requires confirmation before action
    - Performs async/AJAX operation

  ACCESSIBILITY:
    - Label: Submit your application
    - Keyboard accessible

  DATA ATTRIBUTES:
    - data-confirm: Are you sure?
    - data-remote: true
```

---

### 2. **Forms & Inputs**

For each form, the extraction captures:

#### Form Behaviors:
- **submitsViaAjax**: Submits without page reload
- **hasClientSideValidation**: Client-side validation enabled
- **preventsDefault**: Custom submission handling
- **hasFileUpload**: Supports file uploads
- **autoSaves**: Automatically saves form data
- **requiresConfirmation**: Requires confirmation before submit

#### For Each Input Field:

**Validation Rules:**
- Required field
- Pattern (regex)
- Min/max length
- Min/max value
- Step (for numbers)
- Custom validation logic

**Input Behaviors:**
- Autocomplete enabled/disabled
- Auto-focus on load
- Read-only state
- Disabled state
- Multiple selection (for selects)
- Triggers search
- Live validation

**Example Output:**
```
[Form] registration_form
  Action: /register
  Method: POST

  FORM BEHAVIORS:
    - Submits via AJAX (no page reload)
    - Has client-side validation
    - Requires confirmation before submit

  INPUTS (5):

    [EMAIL] Email Address
      ID: email_input
      Name: email

      VALIDATION:
        - Required field
        - Pattern: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
        - Max length: 255

      BEHAVIORS: autocomplete enabled, live validation
      Placeholder: Enter your email

    [PASSWORD] Password
      ID: password_input
      Name: password

      VALIDATION:
        - Required field
        - Min length: 8
        - Max length: 128

      BEHAVIORS: live validation
```

---

### 3. **Tables & Data Grids**

For each table, the extraction captures:

#### Table Interactions:
- **isSortable**: Columns can be sorted
- **isFilterable**: Data can be filtered
- **hasPagination**: Results are paginated
- **hasRowSelection**: Rows can be selected (checkboxes/radio)
- **hasRowActions**: Actions available per row
- **isEditable**: Inline editing enabled
- **hasExpandableRows**: Rows can be expanded for details

#### Row Actions:
- Action buttons with their functions
- Edit, delete, view operations
- Custom actions

**Example Output:**
```
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
      Action: navigate('/users/{id}')
```

---

### 4. **Interactive Links**

For each link, the extraction captures:

#### Link Behaviors:
- **isExternal**: Links to external site
- **opensInNewTab**: Opens in new window/tab
- **isDownload**: Downloads a file
- **triggersAction**: Triggers custom action
- **requiresAuth**: Requires authentication
- **isAjaxLink**: Makes AJAX request
- **hasConfirmation**: Requires confirmation

**Example Output:**
```
[Link] Download Report
  Target: /api/reports/monthly.pdf
  Behaviors: downloads file, requires authentication

[Link] External Documentation
  Target: https://docs.example.com
  Behaviors: external link, opens in new tab
```

---

### 5. **Navigation**

All navigation elements with their:
- Link text
- Target URLs
- Navigation structure

---

### 6. **Page Functions & Features**

High-level summary of page capabilities:
- Form submission workflows
- Data display and management
- Search functionality
- Filter and sort operations
- CRUD operations

**Example:**
```
FUNCTIONS & FEATURES

[FORM_SUBMISSION]
Form submission: /api/create-account
  Method: POST
  Inputs: 8 fields
    - username: text
    - email: email
    - password: password
    - confirm_password: password
    ...

[DATA_DISPLAY]
Table display with 200 rows and 6 columns
  Headers: ID, Name, Email, Created, Status, Actions
  
[SEARCH]
Search functionality with 1 search input(s)
```

---

## What Is NOT Captured

To keep specifications focused on behavior, the following are **minimized or excluded**:

- ❌ CSS classes (unless they indicate behavior)
- ❌ Exact pixel positions and dimensions
- ❌ Colors, fonts, styling
- ❌ Visual layout details
- ❌ Icons (unless functional)
- ❌ Decorative elements

---

## Use Cases

### ✅ Perfect For:

1. **Rebuilding applications** in different frameworks (React → Vue, Angular → Svelte, etc.)
2. **Creating functional clones** with your own design system
3. **Documenting application features** for technical specs
4. **API requirement gathering** (understand what endpoints are needed)
5. **Test case generation** (know what interactions to test)
6. **Accessibility audits** (understand required keyboard/screen reader support)

### ❌ Not Suitable For:

1. Pixel-perfect visual reproduction
2. Design system documentation
3. Brand/style guide creation
4. Layout recreation

---

## Output Format

Extraction generates:

### 1. Text Files (Human-Readable)
- `00_SUMMARY.txt` - Overview statistics
- `01_PageName.txt`, `02_PageName.txt` - Detailed behavioral specs per page
- Clear, hierarchical format focusing on actions and interactions

### 2. JSON Files (Machine-Readable)
- `full_extraction.json` - Complete structured data for programmatic use

### 3. Screenshots
- Visual reference for each page
- Useful for understanding context

### 4. README Files
- Quick navigation and summary
- Latest run information

---

## Example: Rebuilding from Specs

Given this extracted spec:

```
[Button] Add to Cart
  BEHAVIORS:
    - Triggers action: addToCart
    - Performs async/AJAX operation
    - Requires confirmation before action
  DATA ATTRIBUTES:
    - data-product-id: 12345
    - data-confirm: Add this item to cart?
```

You can implement in any framework:

**React:**
```jsx
<Button
  onClick={async () => {
    if (confirm("Add this item to cart?")) {
      await addToCart(12345);
    }
  }}
>
  Add to Cart
</Button>
```

**Vue:**
```vue
<button @click="handleAddToCart(12345)">
  Add to Cart
</button>

<script>
methods: {
  async handleAddToCart(productId) {
    if (confirm("Add this item to cart?")) {
      await this.addToCart(productId);
    }
  }
}
</script>
```

The behavioral spec tells you **what** needs to happen, you decide **how** to implement it in your chosen tech stack.

---

## Summary

The behavioral extraction gives you a **functional blueprint** of the application:
- What actions users can take
- How forms validate and submit
- What data operations are available
- How navigation flows
- What confirmations are needed
- What happens asynchronously

This is everything needed to rebuild the **functionality** without being constrained by the original **styling**.
