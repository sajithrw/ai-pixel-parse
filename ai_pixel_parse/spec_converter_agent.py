"""
Specification Converter Agent - Comprehensive Functional Specification Generator

Converts technical UI extractions into a single, detailed functional specification document.
Focuses on WHAT each feature does functionally (business logic, calculations, data formats),
not just UI components.
"""

from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from datetime import datetime


async def convert_to_functional_spec_tool(
    app_name: str,
    extraction_path: Optional[str] = None,
    domain: Optional[str] = None,
    target_audience: str = "AI agents and developers",
    output_dir: str = "functional_specs"
) -> str:
    """
    Convert a UI extraction to comprehensive functional specification.
    
    Generates ONE detailed document with complete functional requirements for each feature,
    including business logic, calculations, data formats, and expected behaviors.
    
    Args:
        app_name: Name of the application (matches extraction folder name)
        extraction_path: Path to specific extraction directory (auto-detects if not provided)
        domain: Application domain for context (e.g., "advertising analytics", "e-commerce")
        target_audience: Who will use these specs (default: "AI agents and developers")
        output_dir: Output directory for functional specs (default: "functional_specs/")
    
    Returns:
        Success message with output path
    """
    # Find extraction directory
    if not extraction_path:
        extraction_base = Path("extraction")
        if not extraction_base.exists():
            return f"Error: Extraction directory not found. Run UI extraction first."
        
        matching_dirs = sorted(extraction_base.glob(f"{app_name}_*"), reverse=True)
        if not matching_dirs:
            available = [d.name.split('_')[0] for d in extraction_base.glob('*_*')]
            return f"Error: No extraction found for '{app_name}'. Available: {', '.join(set(available))}"
        
        extraction_path = str(matching_dirs[0])
        print(f"📂 Found extraction: {extraction_path}")
    
    extraction_dir = Path(extraction_path)
    
    # Load extraction data from JSON
    json_file = extraction_dir / "full_extraction.json"
    
    if not json_file.exists():
        return f"Error: Extraction data not found at {json_file}"
    
    with open(json_file, 'r', encoding='utf-8') as f:
        extraction_data = json.load(f)
    
    # Load detailed specifications from text files
    page_specs = []
    for txt_file in sorted(extraction_dir.glob("*.txt")):
        if txt_file.name.startswith("00_"):  # Skip summary
            continue
        with open(txt_file, 'r', encoding='utf-8') as f:
            page_specs.append({
                'file': txt_file.name,
                'content': f.read()
            })
    
    print(f"📊 Loaded extraction data: {len(extraction_data)} pages")
    print(f"📄 Loaded detailed specifications: {len(page_specs)} files")
    
    # Create output directory
    output_base = Path(output_dir)
    output_base.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_base / f"{app_name}_spec_{timestamp}"
    output_path.mkdir(exist_ok=True)
    
    print(f"\n🔄 Generating comprehensive functional specification...")
    print(f"   Domain: {domain or 'General'}")
    print(f"   Target audience: {target_audience}")
    
    # Generate single comprehensive specification
    spec_content = _generate_comprehensive_spec(
        extraction_data,
        page_specs,
        app_name,
        domain,
        target_audience
    )
    
    # Save document
    spec_file = output_path / f"{app_name}_functional_specification.md"
    spec_file.write_text(spec_content, encoding='utf-8')
    
    print(f"\n✅ Comprehensive functional specification generated!")
    print(f"   Output: {spec_file}")
    print(f"   Size: {len(spec_content):,} characters")
    
    return f"""Successfully generated comprehensive functional specification for '{app_name}'.

Output file: {spec_file}

This document contains detailed functional requirements for every feature, including:
- Complete business logic and calculations
- Data formats and validation rules
- Expected behaviors and interactions
- Functional dependencies and relationships

Ready for developers or AI agents to implement the application."""


def _generate_comprehensive_spec(
    extraction_data: List[Dict[str, Any]],
    page_specs: List[Dict[str, Any]],
    app_name: str,
    domain: Optional[str],
    target_audience: str
) -> str:
    """Generate comprehensive functional specification with detailed requirements."""
    
    pages = extraction_data
    
    # Count all components including iframe content
    total_metrics = 0
    total_charts = 0
    total_buttons = 0
    total_forms = 0
    total_tables = 0
    
    for page in pages:
        components = page.get('components', {})
        
        # Direct page components
        total_buttons += len(components.get('buttons', []))
        total_forms += len(components.get('forms', []))
        total_tables += len(components.get('tables', []))
        
        # Iframe components
        for iframe in components.get('iframes', []):
            iframe_comps = iframe.get('components', {})
            total_metrics += len(iframe_comps.get('metrics', []))
            total_charts += len(iframe_comps.get('charts', []))
            total_buttons += len(iframe_comps.get('buttons', []))
            total_tables += len(iframe_comps.get('tables', []))
            total_forms += len(iframe_comps.get('forms', []))
    
    # Determine domain context
    domain_context = _get_domain_context(domain)
    
    doc = f"""# Comprehensive Functional Specification: {app_name}

## Document Information

- **Application**: {app_name}
- **Domain**: {domain or 'General Application'}
- **Target Audience**: {target_audience}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Pages Analyzed**: {len(pages)}

---

## Purpose

This document provides **comprehensive functional specifications** for building the {app_name} application. 
It focuses on **WHAT each feature does functionally**, including:

- Business logic and calculations
- Data formats, validation, and transformations
- Expected behaviors and user interactions
- Functional dependencies and relationships
- Data sources and destinations

This specification is **technology-agnostic** and can be implemented in any tech stack.

---

## Executive Summary

### Application Statistics

- **Pages**: {len(pages)}
- **Metrics/KPIs**: {total_metrics}
- **Charts/Visualizations**: {total_charts}
- **Interactive Actions**: {total_buttons}
- **Data Entry Forms**: {total_forms}
- **Data Tables**: {total_tables}

### Primary Purpose

{_get_app_purpose(pages, domain)}

### Key Capabilities

{_get_key_capabilities(pages, total_metrics, total_charts, total_forms, total_tables)}

---

## Authentication & Access Control

"""
    
    # Add authentication requirements
    login_forms = []
    for page in pages:
        forms = page.get('components', {}).get('forms', [])
        login_forms.extend(forms)
    
    if login_forms:
        doc += _generate_auth_requirements(pages, domain_context)
    else:
        doc += """### Authentication

**Status**: No login form detected in extraction.

If authentication is required:
- Implement secure user authentication mechanism
- Support session management
- Handle authentication tokens/cookies
- Provide logout functionality

"""
    
    # Generate detailed functional specs for each page
    doc += "\n---\n\n## Detailed Functional Specifications\n\n"
    
    for idx, page in enumerate(pages, 1):
        doc += _generate_page_functional_spec(page, idx, domain, domain_context)
    
    # Add data requirements
    doc += "\n---\n\n## Data Requirements\n\n"
    doc += _generate_data_requirements(pages, domain_context)
    
    # Add integration requirements
    doc += "\n---\n\n## Integration Requirements\n\n"
    doc += _generate_integration_requirements(pages, domain_context)
    
    # Add non-functional requirements
    doc += "\n---\n\n## Non-Functional Requirements\n\n"
    doc += _generate_nonfunctional_requirements(total_metrics, total_charts, domain)
    
    # Add glossary if domain-specific
    if domain:
        doc += "\n---\n\n## Domain Glossary\n\n"
        doc += _generate_domain_glossary(domain, pages)
    
    doc += f"""

---

## Implementation Notes

### Technology Independence

This specification deliberately avoids technology-specific details. Implementation teams should:

1. **Choose appropriate technologies** based on requirements (performance, scalability, team expertise)
2. **Design database schema** based on data requirements section
3. **Select visualization libraries** that support required chart types
4. **Implement authentication** using industry-standard security practices
5. **Build responsive UI** that works across devices

### Data Accuracy

All calculations, formats, and business rules described in this document should be:
- **Validated** with domain experts
- **Tested** with sample data
- **Documented** with edge cases and error handling
- **Maintained** as business requirements evolve

### Extensibility

Design the application to support:
- Adding new metrics/KPIs without code changes
- Configurable dashboards per user role
- Export capabilities for all data views
- API access for third-party integrations

---

## Revision History

- **v1.0** - {datetime.now().strftime('%Y-%m-%d')} - Initial comprehensive specification from UI extraction

---

*Generated by AI Pixel Parse Specification Converter*
*Source: {app_name} UI extraction*
"""
    
    return doc


def _generate_page_functional_spec(
    page: Dict[str, Any],
    page_num: int,
    domain: Optional[str],
    domain_context: Dict[str, Any]
) -> str:
    """Generate detailed functional specification for a single page."""
    
    title = page.get('title', f'Page {page_num}')
    url = page.get('url', 'N/A')
    components = page.get('components', {})
    
    doc = f"""### {page_num}. {title}

**URL**: `{url}`

**Primary Function**: {_infer_page_purpose(page, domain)}

"""
    
    # Collect all metrics from iframes
    all_metrics = []
    all_charts = []
    all_buttons = components.get('buttons', [])
    all_forms = components.get('forms', [])
    all_tables = components.get('tables', [])
    
    for iframe in components.get('iframes', []):
        iframe_comps = iframe.get('components', {})
        all_metrics.extend(iframe_comps.get('metrics', []))
        all_charts.extend(iframe_comps.get('charts', []))
        all_buttons.extend(iframe_comps.get('buttons', []))
        all_forms.extend(iframe_comps.get('forms', []))
        all_tables.extend(iframe_comps.get('tables', []))
    
    # Metrics/KPIs section with DETAILED functional specs
    if all_metrics:
        # Group metrics by label (metric-label and metric-content pairs)
        metric_groups = _group_metrics(all_metrics)
        
        doc += f"""#### Key Performance Indicators (KPIs)

This page displays **{len(metric_groups)} metrics/KPIs** for monitoring and analysis.

**Functional Requirements for Each Metric:**

"""
        for i, metric_group in enumerate(metric_groups[:30], 1):  # Detail first 30
            doc += _generate_metric_functional_spec(metric_group, i, domain, domain_context)
        
        if len(metric_groups) > 30:
            doc += f"\n*... and {len(metric_groups) - 30} additional metrics with similar functional patterns*\n"
    
    # Charts section with functional specs
    if all_charts:
        doc += f"""

#### Data Visualizations

This page includes **{len(all_charts)} charts/graphs** for visual data analysis.

**Functional Requirements for Visualizations:**

"""
        for i, chart in enumerate(all_charts[:10], 1):  # Detail first 10
            doc += _generate_chart_functional_spec(chart, i, domain, domain_context)
        
        if len(all_charts) > 10:
            doc += f"\n*... and {len(all_charts) - 10} additional visualizations*\n"
    
    # Interactive actions
    if all_buttons:
        doc += f"""

#### Interactive Actions

This page provides **{len(all_buttons)} interactive actions** for user operations.

**Functional Requirements for Actions:**

"""
        action_groups = _group_actions_by_purpose(all_buttons)
        for group_name, group_buttons in action_groups.items():
            doc += f"\n**{group_name}**\n\n"
            for i, button in enumerate(group_buttons[:5], 1):
                doc += _generate_action_functional_spec(button, i, domain, domain_context)
    
    # Data entry forms
    if all_forms:
        doc += f"""

#### Data Entry Forms

This page includes **{len(all_forms)} form(s)** for data input.

**Functional Requirements for Forms:**

"""
        for i, form in enumerate(all_forms, 1):
            doc += _generate_form_functional_spec(form, i, domain, domain_context)
    
    # Data tables
    if all_tables:
        doc += f"""

#### Data Tables

This page displays **{len(all_tables)} data table(s)** for structured data.

**Functional Requirements for Tables:**

"""
        for i, table in enumerate(all_tables, 1):
            doc += _generate_table_functional_spec(table, i, domain, domain_context)
    
    doc += "\n---\n\n"
    return doc


def _generate_metric_functional_spec(
    metric: Dict[str, Any],
    index: int,
    domain: Optional[str],
    domain_context: Dict[str, Any]
) -> str:
    """Generate detailed functional specification for a metric/KPI."""
    
    # Extract label and value from grouped metric
    label = metric.get('label', f'Metric {index}')
    value = metric.get('value', 'N/A')
    raw_text = metric.get('text', '')
    
    spec = f"""**{index}. {label}**

"""
    
    # Add specific functional requirements based on metric type
    if any(word in label.lower() for word in ['revenue', 'cost', 'profit', 'price', 'amount', 'value', 'spend']):
        spec += f"""- **Purpose**: Display {label.lower()} in monetary format
- **Data Format**: US Dollar amount with thousand separators (e.g., $1,234,567.89)
- **Calculation**: {_infer_calculation_logic(label, domain)}
- **Update Frequency**: Real-time or near-real-time (refresh every 1-5 minutes)
- **Precision**: 2 decimal places for currency
- **Data Source**: Financial transaction database / revenue tracking system
- **Validation**: Must be non-negative; validate against source data integrity
- **Display Rules**: 
  - Show "N/A" if data unavailable
  - Highlight negative values in red (if losses/negative revenue possible)
  - Show percentage change compared to previous period if applicable

"""
    elif any(word in label.lower() for word in ['count', 'total', 'number', '#']):
        spec += f"""- **Purpose**: Display count of {label.lower()}
- **Data Format**: Whole number with thousand separators (e.g., 1,234)
- **Calculation**: Count of {_infer_count_subject(label, domain)}
- **Update Frequency**: Real-time updates as items are added/removed
- **Data Source**: Database count query / aggregated statistics
- **Validation**: Must be non-negative integer
- **Display Rules**:
  - Show "0" if no items exist
  - Animate on value change to draw attention
  - Allow drill-down to see detailed list

"""
    elif any(word in label.lower() for word in ['rate', 'ratio', 'percentage', '%', 'ctr', 'cvr']):
        spec += f"""- **Purpose**: Display {label.lower()} as percentage metric
- **Data Format**: Percentage with 2 decimal places (e.g., 23.45%)
- **Calculation**: {_infer_percentage_calculation(label, domain)}
- **Update Frequency**: Recalculated every 5-15 minutes or on data change
- **Data Source**: Calculated from event tracking / conversion data
- **Validation**: Value between 0% and 100% (or up to 1000% for growth rates)
- **Display Rules**:
  - Color code: Green for positive/above target, Red for below target
  - Show trend indicator (↑ ↓) compared to previous period
  - Display confidence interval if sample size is small

"""
    elif any(word in label.lower() for word in ['date', 'time', 'duration', 'period']):
        spec += f"""- **Purpose**: Display {label.lower()} in human-readable format
- **Data Format**: {_infer_date_format(label)}
- **Data Source**: Timestamp fields / scheduling system
- **Validation**: Must be valid date/time in ISO format
- **Display Rules**:
  - Show in user's local timezone
  - Format appropriately for context (absolute vs relative time)
  - Highlight overdue/urgent dates

"""
    else:
        # Generic metric specification
        spec += f"""- **Purpose**: Display {label.lower()} for monitoring and decision-making
- **Data Format**: {_infer_data_format(value, label)}
- **Calculation**: {_infer_generic_calculation(label, domain)}
- **Update Frequency**: Refresh based on data freshness requirements (typically 1-15 minutes)
- **Data Source**: Application database / external API / analytics system
- **Validation**: Validate data type and range constraints
- **Display Rules**:
  - Clear label with tooltip explanation if needed
  - Consistent formatting across similar metrics
  - Visual indicator for stale/outdated data

"""
    
    return spec


def _generate_chart_functional_spec(
    chart: Dict[str, Any],
    index: int,
    domain: Optional[str],
    domain_context: Dict[str, Any]
) -> str:
    """Generate detailed functional specification for a chart/visualization."""
    
    classes = chart.get('classes', '') if isinstance(chart.get('classes'), str) else ''
    chart_type = _infer_chart_type(classes)
    
    spec = f"""**{index}. {chart_type}**

- **Purpose**: Visualize {_infer_chart_purpose(chart_type, domain)}
- **Chart Type**: {chart_type}
- **Data Requirements**:
  - X-axis: {_infer_x_axis_data(chart_type, domain)}
  - Y-axis: {_infer_y_axis_data(chart_type, domain)}
  - Data points: Minimum 1, Maximum 1000 (paginate/aggregate if more)
- **Interactivity**:
  - Hovering shows detailed data point values
  - Click to drill down to underlying data
  - Zoom and pan for time-series data
  - Export as image (PNG/SVG) or data (CSV/Excel)
- **Update Frequency**: Real-time or every 5 minutes (based on data volume)
- **Display Rules**:
  - Auto-scale axes based on data range
  - Show legend if multiple series
  - Display "No data available" message if empty
  - Responsive sizing for different screen sizes
- **Performance**: Render within 2 seconds even with maximum data points

"""
    
    return spec


def _generate_action_functional_spec(
    button: Dict[str, Any],
    index: int,
    domain: Optional[str],
    domain_context: Dict[str, Any]
) -> str:
    """Generate functional specification for an action/button."""
    
    text = button.get('text', f'Action {index}')
    classes = button.get('classes', '')
    
    # Infer action purpose
    purpose = _infer_action_purpose(text, classes, domain)
    
    spec = f"""**{index}. {text}**

- **Purpose**: {purpose}
- **Trigger**: User click/tap
- **Pre-conditions**: {_infer_preconditions(text, domain)}
- **Action Logic**: {_infer_action_logic(text, domain)}
- **Post-conditions**: {_infer_postconditions(text, domain)}
- **Validation**: {_infer_validation_rules(text, domain)}
- **User Feedback**: 
  - Show loading indicator during processing
  - Display success message on completion
  - Show error message with actionable guidance on failure
- **Error Handling**: Graceful degradation; allow retry on transient failures

"""
    
    return spec


def _generate_form_functional_spec(
    form: Dict[str, Any],
    index: int,
    domain: Optional[str],
    domain_context: Dict[str, Any]
) -> str:
    """Generate functional specification for a form."""
    
    fields = form.get('fields', [])
    action = form.get('action', 'N/A')
    
    spec = f"""**Form {index}**

- **Purpose**: {_infer_form_purpose(fields, domain)}
- **Submission**: {action}
- **Fields** ({len(fields)} total):

"""
    
    for field in fields:
        field_name = field.get('name', 'unnamed')
        field_type = field.get('type', 'text')
        required = field.get('required', False)
        
        spec += f"""  - **{field_name}**:
    - Type: {field_type}
    - Required: {'Yes' if required else 'No'}
    - Validation: {_infer_field_validation(field_name, field_type, domain)}
    - Format: {_infer_field_format(field_name, field_type)}
    - Error Messages: {_infer_error_messages(field_name, field_type)}

"""
    
    spec += f"""- **Submission Logic**:
  1. Validate all required fields
  2. Check field format and constraints
  3. Submit data to backend
  4. Handle success/error responses
  5. Provide user feedback

- **Success Behavior**: {_infer_success_behavior(fields, domain)}
- **Error Handling**: Display field-level errors; allow correction and resubmission

"""
    
    return spec


def _generate_table_functional_spec(
    table: Dict[str, Any],
    index: int,
    domain: Optional[str],
    domain_context: Dict[str, Any]
) -> str:
    """Generate functional specification for a data table."""
    
    headers = table.get('headers', [])
    row_count = table.get('row_count', 0)
    
    spec = f"""**Table {index}**

- **Purpose**: Display structured data in tabular format for analysis and comparison
- **Columns**: {len(headers)} columns
- **Data Volume**: {row_count} rows (current); support pagination for larger datasets
- **Column Specifications**:

"""
    
    for i, header in enumerate(headers, 1):
        spec += f"""  {i}. **{header}**:
     - Data Type: {_infer_column_data_type(header, domain)}
     - Format: {_infer_column_format(header, domain)}
     - Sortable: Yes
     - Filterable: Yes
     - Aggregation: {_infer_aggregation_support(header)}

"""
    
    spec += f"""- **Functional Capabilities**:
  - **Sorting**: Click column header to sort ascending/descending
  - **Filtering**: Filter rows based on column values
  - **Pagination**: 25/50/100 rows per page (user configurable)
  - **Search**: Full-text search across all columns
  - **Export**: Export visible/filtered data as CSV/Excel
  - **Selection**: Multi-select rows for bulk operations

- **Performance**: Load and render within 2 seconds; virtualize for >1000 rows

"""
    
    return spec


def _generate_data_requirements(
    pages: List[Dict[str, Any]],
    domain_context: Dict[str, Any]
) -> str:
    """Generate data requirements section."""
    
    doc = """### Data Storage

The application requires persistent storage for:

1. **User Data**
   - User accounts and credentials
   - User preferences and settings
   - User roles and permissions

2. **Application Data**
   - All metrics, KPIs, and calculated values
   - Historical data for trend analysis
   - Transactional data for auditing

3. **Analytics Data**
   - User interaction logs
   - Performance metrics
   - System usage statistics

### Data Integrity

- **Consistency**: All data must maintain referential integrity
- **Validation**: Validate all inputs at entry point
- **Audit Trail**: Track all data modifications with timestamp and user
- **Backup**: Daily automated backups with 30-day retention

### Data Privacy & Security

- **Encryption**: Encrypt sensitive data at rest and in transit
- **Access Control**: Role-based access to sensitive information
- **Compliance**: Follow relevant data protection regulations (GDPR, CCPA, etc.)
- **Retention**: Define data retention policies per data type

"""
    
    return doc


def _generate_integration_requirements(
    pages: List[Dict[str, Any]],
    domain_context: Dict[str, Any]
) -> str:
    """Generate integration requirements section."""
    
    doc = """### External Systems

The application likely requires integration with:

1. **Authentication Provider**
   - SSO (Single Sign-On) if enterprise deployment
   - OAuth providers (Google, Microsoft, etc.)

2. **Data Sources**
   - Primary database or data warehouse
   - Real-time event streams (if live metrics)
   - Third-party APIs for external data

3. **Analytics & Monitoring**
   - Application performance monitoring (APM)
   - Error tracking and logging
   - User analytics platform

### API Requirements

- **REST API**: Provide RESTful endpoints for data operations
- **Authentication**: API key or JWT-based authentication
- **Rate Limiting**: Prevent abuse with rate limits
- **Documentation**: OpenAPI/Swagger specification

### Data Export/Import

- **Export Formats**: CSV, Excel, JSON, PDF
- **Import Capabilities**: Bulk data import with validation
- **Scheduled Exports**: Automated daily/weekly export option

"""
    
    return doc


def _generate_nonfunctional_requirements(
    total_metrics: int,
    total_charts: int,
    domain: Optional[str]
) -> str:
    """Generate non-functional requirements."""
    
    doc = f"""### Performance

- **Page Load Time**: < 3 seconds for initial load
- **API Response Time**: < 500ms for standard queries
- **Dashboard Refresh**: Update metrics within 2 seconds
- **Chart Rendering**: Render visualizations within 2 seconds
- **Concurrent Users**: Support {_infer_concurrent_users(domain)} simultaneous users

### Scalability

- **Data Volume**: Handle {_infer_data_volume(domain)} records efficiently
- **Metrics Processing**: Process and aggregate {total_metrics} metrics in < 1 second
- **Chart Data**: Support up to 1000 data points per visualization
- **Horizontal Scaling**: Support load balancing across multiple servers

### Availability

- **Uptime**: 99.9% availability (< 8.7 hours downtime per year)
- **Maintenance Windows**: Scheduled maintenance during off-peak hours
- **Disaster Recovery**: RPO < 1 hour, RTO < 4 hours

### Security

- **Authentication**: Industry-standard authentication (OAuth 2.0, SAML)
- **Authorization**: Role-based access control (RBAC)
- **Session Management**: Secure session tokens with expiration
- **Data Encryption**: TLS 1.3 for data in transit, AES-256 for data at rest
- **Audit Logging**: Log all security-relevant events

### Usability

- **Responsive Design**: Work on desktop, tablet, and mobile devices
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Accessibility**: WCAG 2.1 Level AA compliance
- **Internationalization**: Support multiple languages and locales
- **Help & Documentation**: Contextual help and user guide

### Maintainability

- **Code Quality**: Follow industry best practices and coding standards
- **Testing**: Minimum 80% code coverage
- **Documentation**: Comprehensive technical and user documentation
- **Monitoring**: Real-time monitoring and alerting
- **Logging**: Structured logging for debugging and analysis

"""
    
    return doc


def _generate_domain_glossary(domain: Optional[str], pages: List[Dict[str, Any]]) -> str:
    """Generate domain-specific glossary."""
    
    if not domain:
        return ""
    
    glossary_terms = {
        'advertising': {
            'Impression': 'A single instance of an ad being displayed to a user',
            'Click': 'User interaction with an ad (clicking on it)',
            'CTR (Click-Through Rate)': 'Percentage of impressions that result in clicks (Clicks / Impressions × 100%)',
            'Conversion': 'Desired user action after clicking ad (purchase, signup, etc.)',
            'CVR (Conversion Rate)': 'Percentage of clicks that result in conversions (Conversions / Clicks × 100%)',
            'CPC (Cost Per Click)': 'Average cost paid for each click on an ad',
            'CPM (Cost Per Mille)': 'Cost per 1000 impressions',
            'Revenue': 'Money earned from advertising campaigns',
            'ROI (Return on Investment)': 'Profit from campaign relative to cost ((Revenue - Cost) / Cost × 100%)',
            'Campaign': 'Organized advertising effort with specific goals and budget',
            'Creative': 'The actual ad content (image, video, text) shown to users'
        },
        'e-commerce': {
            'SKU (Stock Keeping Unit)': 'Unique identifier for each product variant',
            'Cart': 'Collection of products user intends to purchase',
            'Checkout': 'Process of completing a purchase',
            'Conversion Rate': 'Percentage of visitors who complete a purchase',
            'AOV (Average Order Value)': 'Average amount spent per order',
            'Inventory': 'Stock of products available for sale',
            'Fulfillment': 'Process of picking, packing, and shipping orders'
        },
        'finance': {
            'Transaction': 'A financial exchange or transfer of funds',
            'Balance': 'Current amount of money in an account',
            'Credit': 'Amount owed or borrowed',
            'Debit': 'Amount withdrawn or spent',
            'Reconciliation': 'Process of matching records to ensure accuracy',
            'Ledger': 'Complete record of financial transactions'
        },
        'analytics': {
            'KPI (Key Performance Indicator)': 'Measurable value that indicates business performance',
            'Metric': 'Quantifiable measurement used to track performance',
            'Dashboard': 'Visual interface displaying multiple metrics and charts',
            'Dimension': 'Categorical attribute for segmenting data (e.g., date, region)',
            'Measure': 'Numerical value that can be aggregated (e.g., revenue, count)',
            'Drill-down': 'Navigate from summary to detailed data',
            'Filter': 'Restrict data to specific criteria'
        }
    }
    
    # Find matching domain
    domain_lower = domain.lower()
    matching_glossary = {}
    
    for key, terms in glossary_terms.items():
        if key in domain_lower:
            matching_glossary.update(terms)
    
    if not matching_glossary:
        return ""
    
    doc = f"### Domain-Specific Terms ({domain})\n\n"
    
    for term, definition in sorted(matching_glossary.items()):
        doc += f"**{term}**  \n{definition}\n\n"
    
    return doc


# Helper functions for inference

def _group_metrics(metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Group metrics by pairing labels with their values."""
    grouped = []
    i = 0
    
    while i < len(metrics):
        metric = metrics[i]
        text = metric.get('text', '')
        classes = metric.get('classes', '')
        values = metric.get('values', [])
        
        # Check if this is a label (metric-label class or no numeric values)
        if 'label' in classes.lower() or not values:
            label = text
            value = 'N/A'
            
            # Look ahead for corresponding value
            if i + 1 < len(metrics):
                next_metric = metrics[i + 1]
                next_values = next_metric.get('values', [])
                if next_values and ('content' in next_metric.get('classes', '').lower() or 'metric' in next_metric.get('classes', '').lower()):
                    value = next_values[0] if next_values else 'N/A'
                    i += 1  # Skip the value metric since we've processed it
            
            grouped.append({
                'label': label,
                'value': value,
                'text': text
            })
        else:
            # This is a standalone metric with value
            # Try to extract label from text
            label = text
            # Remove numeric values from label
            for val in values:
                label = label.replace(str(val), '').replace('$', '').replace('K', '').replace('M', '').strip()
            
            grouped.append({
                'label': label,
                'value': values[0] if values else 'N/A',
                'text': text
            })
        
        i += 1
    
    return grouped


def _get_domain_context(domain: Optional[str]) -> Dict[str, Any]:
    """Get context information for the domain."""
    if not domain:
        return {}
    
    domain_lower = domain.lower()
    
    contexts = {
        'advertising': {
            'primary_metrics': ['impressions', 'clicks', 'conversions', 'revenue', 'ctr', 'cvr', 'cpc', 'roi'],
            'data_sources': ['ad server', 'tracking pixels', 'conversion API'],
            'update_frequency': 'real-time or 1-5 minutes'
        },
        'e-commerce': {
            'primary_metrics': ['orders', 'revenue', 'products', 'customers', 'conversion rate', 'cart abandonment'],
            'data_sources': ['order database', 'inventory system', 'payment gateway'],
            'update_frequency': 'real-time on transactions'
        },
        'finance': {
            'primary_metrics': ['transactions', 'balances', 'revenue', 'expenses', 'profit', 'cash flow'],
            'data_sources': ['transaction database', 'accounting system', 'bank feeds'],
            'update_frequency': 'real-time or daily batch'
        },
        'analytics': {
            'primary_metrics': ['pageviews', 'users', 'sessions', 'bounce rate', 'time on site'],
            'data_sources': ['analytics platform', 'event tracking', 'user database'],
            'update_frequency': 'real-time or 5-15 minutes'
        }
    }
    
    for key, context in contexts.items():
        if key in domain_lower:
            return context
    
    return {}


def _get_app_purpose(pages: List[Dict[str, Any]], domain: Optional[str]) -> str:
    """Infer the primary purpose of the application."""
    
    total_metrics = sum(len(p.get('iframe_metrics', [])) for p in pages)
    total_charts = sum(len(p.get('iframe_charts', [])) for p in pages)
    total_forms = sum(len(p.get('forms', [])) for p in pages)
    
    if total_metrics > 20 or total_charts > 10:
        return f"Analytics and reporting platform for monitoring business metrics, KPIs, and performance indicators{' in the ' + domain + ' domain' if domain else ''}."
    elif total_forms > 3:
        return "Data entry and management system for collecting, processing, and managing information."
    elif total_charts > 5:
        return "Data visualization platform for analyzing trends and patterns in business data."
    else:
        return "Business application for managing operations and workflows."


def _get_key_capabilities(pages, total_metrics, total_charts, total_forms, total_tables):
    """Generate key capabilities list."""
    
    capabilities = []
    
    if total_metrics > 10:
        capabilities.append(f"- Monitor {total_metrics} key performance indicators (KPIs) in real-time")
    if total_charts > 5:
        capabilities.append(f"- Visualize data through {total_charts} interactive charts and graphs")
    if total_forms > 0:
        capabilities.append(f"- Capture user input through {total_forms} data entry form(s)")
    if total_tables > 0:
        capabilities.append(f"- Display structured data in {total_tables} tabular view(s)")
    
    capabilities.extend([
        "- Provide role-based access to features and data",
        "- Export data and reports for offline analysis",
        "- Support filtering and date range selection"
    ])
    
    return "\n".join(capabilities)


def _generate_auth_requirements(pages: List[Dict[str, Any]], domain_context: Dict[str, Any]) -> str:
    """Generate authentication requirements based on detected forms."""
    
    return """### Authentication

**Functional Requirements**:

1. **User Login**:
   - Users must provide valid credentials (username/email and password)
   - System validates credentials against user database
   - Upon successful authentication, create secure session token
   - Redirect authenticated user to main dashboard/home page
   - Display error message for invalid credentials

2. **Session Management**:
   - Maintain user session across page navigation
   - Session timeout after 30 minutes of inactivity (configurable)
   - Provide "Remember Me" option for extended session (7 days)
   - Secure session tokens (HTTP-only, secure cookies)

3. **Password Requirements**:
   - Minimum 8 characters
   - At least one uppercase letter, one lowercase letter, one number
   - Special characters recommended but not required
   - Password strength indicator during registration/reset

4. **Password Reset**:
   - "Forgot Password" link on login page
   - Send reset link to registered email
   - Reset link valid for 24 hours
   - Require confirmation of new password

5. **Account Lockout**:
   - Lock account after 5 failed login attempts
   - Unlock automatically after 15 minutes or via email
   - Log all authentication attempts for security monitoring

6. **Multi-Factor Authentication (MFA)** (Optional but recommended):
   - Support 2FA via email or authenticator app
   - Required for admin/privileged accounts
   - Option for users to enable on their accounts

"""


def _infer_page_purpose(page: Dict[str, Any], domain: Optional[str]) -> str:
    """Infer the purpose of a page based on its content."""
    
    title = page.get('title', '').lower()
    metrics_count = len(page.get('iframe_metrics', []))
    charts_count = len(page.get('iframe_charts', []))
    forms_count = len(page.get('forms', []))
    
    if 'dashboard' in title or (metrics_count > 5 and charts_count > 3):
        return "Main analytics dashboard displaying key metrics and visualizations"
    elif 'login' in title or forms_count > 0:
        return "User authentication and access control"
    elif 'report' in title:
        return "Detailed reporting and data analysis"
    elif 'settings' in title or 'config' in title:
        return "Application configuration and user preferences"
    else:
        return "Data display and user interaction"


def _infer_calculation_logic(label: str, domain: Optional[str]) -> str:
    """Infer how a metric should be calculated."""
    
    label_lower = label.lower()
    
    if 'gross' in label_lower and 'revenue' in label_lower:
        if domain and 'advertising' in domain.lower():
            return "Sum of all advertising revenue across all campaigns and ad types"
        else:
            return "Sum of all revenue streams without deductions"
    elif 'net' in label_lower and 'revenue' in label_lower:
        return "Gross revenue minus refunds, discounts, and adjustments"
    elif 'cost' in label_lower:
        return "Sum of all costs/expenses for the period"
    elif 'profit' in label_lower:
        return "Revenue minus costs (Profit = Revenue - Cost)"
    elif 'roi' in label_lower:
        return "Return on investment calculated as ((Revenue - Cost) / Cost) × 100%"
    else:
        return f"Aggregate/calculate {label_lower} based on underlying data sources"


def _infer_count_subject(label: str, domain: Optional[str]) -> str:
    """Infer what is being counted."""
    
    label_lower = label.lower()
    
    if 'campaign' in label_lower:
        return "active campaigns in the system"
    elif 'user' in label_lower or 'customer' in label_lower:
        return "registered users/customers"
    elif 'order' in label_lower:
        return "completed orders"
    elif 'product' in label_lower:
        return "products in catalog"
    elif 'impression' in label_lower:
        return "ad impressions served"
    elif 'click' in label_lower:
        return "ad clicks registered"
    elif 'conversion' in label_lower:
        return "completed conversions/goals"
    else:
        return f"items matching {label_lower} criteria"


def _infer_percentage_calculation(label: str, domain: Optional[str]) -> str:
    """Infer how a percentage/rate is calculated."""
    
    label_lower = label.lower()
    
    if 'ctr' in label_lower or 'click-through' in label_lower:
        return "(Clicks / Impressions) × 100%"
    elif 'cvr' in label_lower or 'conversion rate' in label_lower:
        return "(Conversions / Clicks) × 100%"
    elif 'bounce' in label_lower:
        return "(Single-page sessions / Total sessions) × 100%"
    elif 'growth' in label_lower:
        return "((Current period - Previous period) / Previous period) × 100%"
    elif 'margin' in label_lower:
        return "((Revenue - Cost) / Revenue) × 100%"
    else:
        return f"Percentage calculation based on {label_lower} formula"


def _infer_date_format(label: str) -> str:
    """Infer appropriate date/time format."""
    
    label_lower = label.lower()
    
    if 'time' in label_lower and 'date' not in label_lower:
        return "HH:MM:SS (24-hour format) or HH:MM AM/PM (12-hour format)"
    elif 'duration' in label_lower:
        return "HH:MM:SS for durations or human-readable format (e.g., '2 hours 30 minutes')"
    else:
        return "YYYY-MM-DD or localized format (e.g., MM/DD/YYYY for US, DD/MM/YYYY for EU)"


def _infer_data_format(value: str, label: str) -> str:
    """Infer data format from value and label."""
    
    if value and value.replace(',', '').replace('.', '').replace('$', '').replace('%', '').isdigit():
        if '$' in value:
            return "Currency with thousand separators (e.g., $1,234.56)"
        elif '%' in value:
            return "Percentage with decimal places (e.g., 23.45%)"
        elif ',' in value:
            return "Number with thousand separators (e.g., 1,234,567)"
        else:
            return "Numeric value"
    else:
        return "Text/string value"


def _infer_generic_calculation(label: str, domain: Optional[str]) -> str:
    """Generic calculation inference."""
    return f"Retrieve and aggregate {label.lower()} data from source systems"


def _infer_chart_type(classes: str) -> str:
    """Infer chart type from CSS classes."""
    
    classes_lower = classes.lower()
    
    if 'line' in classes_lower:
        return "Line Chart"
    elif 'bar' in classes_lower:
        return "Bar Chart"
    elif 'pie' in classes_lower:
        return "Pie Chart"
    elif 'scatter' in classes_lower:
        return "Scatter Plot"
    elif 'area' in classes_lower:
        return "Area Chart"
    elif 'heatmap' in classes_lower:
        return "Heatmap"
    else:
        return "Data Visualization Chart"


def _infer_chart_purpose(chart_type: str, domain: Optional[str]) -> str:
    """Infer what the chart is meant to show."""
    
    if 'line' in chart_type.lower():
        return "trends over time (time-series data)"
    elif 'bar' in chart_type.lower():
        return "comparisons between categories"
    elif 'pie' in chart_type.lower():
        return "proportional distribution of categories"
    elif 'scatter' in chart_type.lower():
        return "correlation between two variables"
    elif 'area' in chart_type.lower():
        return "cumulative totals over time"
    else:
        return "data patterns and insights"


def _infer_x_axis_data(chart_type: str, domain: Optional[str]) -> str:
    """Infer X-axis data type."""
    
    if 'line' in chart_type.lower() or 'area' in chart_type.lower():
        return "Time periods (dates, hours, months)"
    elif 'bar' in chart_type.lower():
        return "Categories or groups"
    elif 'scatter' in chart_type.lower():
        return "Independent variable (numeric)"
    else:
        return "Categorical or temporal data"


def _infer_y_axis_data(chart_type: str, domain: Optional[str]) -> str:
    """Infer Y-axis data type."""
    
    if 'pie' in chart_type.lower():
        return "N/A (pie charts show proportions)"
    else:
        return "Numeric values (counts, revenue, percentages, etc.)"


def _infer_action_purpose(text: str, classes: str, domain: Optional[str]) -> str:
    """Infer what an action/button does."""
    
    text_lower = text.lower()
    
    if 'export' in text_lower or 'download' in text_lower:
        return "Export/download data or reports"
    elif 'filter' in text_lower:
        return "Apply filters to refine displayed data"
    elif 'refresh' in text_lower or 'reload' in text_lower:
        return "Refresh data to show latest values"
    elif 'save' in text_lower:
        return "Save changes or data"
    elif 'cancel' in text_lower:
        return "Cancel current operation and revert changes"
    elif 'submit' in text_lower:
        return "Submit form data for processing"
    elif 'search' in text_lower:
        return "Search for specific data or records"
    elif 'create' in text_lower or 'new' in text_lower or 'add' in text_lower:
        return "Create new record or item"
    elif 'edit' in text_lower or 'update' in text_lower:
        return "Edit/update existing record"
    elif 'delete' in text_lower or 'remove' in text_lower:
        return "Delete/remove record or item"
    else:
        return f"Perform action: {text}"


def _infer_preconditions(text: str, domain: Optional[str]) -> str:
    """Infer preconditions for an action."""
    
    text_lower = text.lower()
    
    if 'export' in text_lower or 'download' in text_lower:
        return "Data must be loaded and available"
    elif 'save' in text_lower:
        return "Changes must be made to form/data"
    elif 'submit' in text_lower:
        return "All required fields must be filled and valid"
    elif 'delete' in text_lower:
        return "Item must be selected; user must have delete permissions"
    elif 'edit' in text_lower:
        return "Item must be selected; user must have edit permissions"
    else:
        return "User must be authenticated and authorized"


def _infer_action_logic(text: str, domain: Optional[str]) -> str:
    """Infer the logic behind an action."""
    
    text_lower = text.lower()
    
    if 'export' in text_lower:
        return "Collect filtered/visible data, format according to export type (CSV/Excel/PDF), generate file, trigger download"
    elif 'filter' in text_lower:
        return "Read filter criteria from UI, apply to dataset, refresh displayed data with filtered results"
    elif 'refresh' in text_lower:
        return "Re-fetch data from backend, update all metrics and visualizations with latest values"
    elif 'save' in text_lower:
        return "Validate changes, submit to backend API, update database, confirm success"
    elif 'submit' in text_lower:
        return "Validate form fields, submit data to backend, process according to business rules, return result"
    elif 'delete' in text_lower:
        return "Confirm deletion with user, send delete request to backend, remove from database, refresh UI"
    else:
        return "Execute corresponding business logic on backend, update UI based on result"


def _infer_postconditions(text: str, domain: Optional[str]) -> str:
    """Infer expected state after action."""
    
    text_lower = text.lower()
    
    if 'export' in text_lower:
        return "File downloaded to user's device"
    elif 'filter' in text_lower:
        return "Display updated with filtered data only"
    elif 'refresh' in text_lower:
        return "All data displays show current values"
    elif 'save' in text_lower:
        return "Changes persisted to database; UI shows success message"
    elif 'submit' in text_lower:
        return "Form cleared or user redirected; data processed successfully"
    elif 'delete' in text_lower:
        return "Item removed from system; no longer appears in lists/views"
    else:
        return "System state updated according to action"


def _infer_validation_rules(text: str, domain: Optional[str]) -> str:
    """Infer validation rules for action."""
    
    text_lower = text.lower()
    
    if 'export' in text_lower:
        return "Ensure data exists to export; check user has export permissions"
    elif 'save' in text_lower or 'submit' in text_lower:
        return "Validate all required fields; check data format and constraints"
    elif 'delete' in text_lower:
        return "Confirm user intent; check for dependencies that would be affected"
    else:
        return "Validate user permissions; ensure action is allowed in current context"


def _group_actions_by_purpose(buttons: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group buttons by their likely purpose."""
    
    groups = {
        'Data Actions': [],
        'Navigation': [],
        'Filters & Search': [],
        'Settings & Configuration': [],
        'Other Actions': []
    }
    
    for button in buttons:
        text = button.get('text', '').lower()
        
        if any(word in text for word in ['export', 'download', 'save', 'delete', 'create', 'edit', 'update']):
            groups['Data Actions'].append(button)
        elif any(word in text for word in ['next', 'previous', 'back', 'home', 'dashboard']):
            groups['Navigation'].append(button)
        elif any(word in text for word in ['filter', 'search', 'sort', 'refresh']):
            groups['Filters & Search'].append(button)
        elif any(word in text for word in ['settings', 'config', 'preferences']):
            groups['Settings & Configuration'].append(button)
        else:
            groups['Other Actions'].append(button)
    
    # Remove empty groups
    return {k: v for k, v in groups.items() if v}


def _infer_form_purpose(fields: List[Dict[str, Any]], domain: Optional[str]) -> str:
    """Infer the purpose of a form based on its fields."""
    
    field_names = [f.get('name', '').lower() for f in fields]
    
    if any('email' in name or 'username' in name for name in field_names) and any('password' in name for name in field_names):
        return "User authentication (login)"
    elif any('search' in name or 'query' in name for name in field_names):
        return "Search functionality"
    elif len(fields) > 5:
        return "Comprehensive data entry for creating/updating records"
    else:
        return "Data input for specific operation"


def _infer_field_validation(field_name: str, field_type: str, domain: Optional[str]) -> str:
    """Infer validation rules for a form field."""
    
    name_lower = field_name.lower()
    
    if 'email' in name_lower:
        return "Valid email format (RFC 5322)"
    elif 'password' in name_lower:
        return "Minimum 8 characters; at least one uppercase, lowercase, and number"
    elif 'phone' in name_lower:
        return "Valid phone number format (with country code)"
    elif 'zip' in name_lower or 'postal' in name_lower:
        return "Valid postal code format for region"
    elif 'url' in name_lower or 'website' in name_lower:
        return "Valid URL format (http:// or https://)"
    elif 'date' in name_lower:
        return "Valid date in YYYY-MM-DD format"
    elif field_type == 'number':
        return "Numeric value within acceptable range"
    elif field_type == 'email':
        return "Valid email format"
    else:
        return "Non-empty value; appropriate length (1-255 characters)"


def _infer_field_format(field_name: str, field_type: str) -> str:
    """Infer display format for field."""
    
    name_lower = field_name.lower()
    
    if 'email' in name_lower:
        return "user@example.com"
    elif 'phone' in name_lower:
        return "+1 (555) 123-4567"
    elif 'date' in name_lower:
        return "YYYY-MM-DD or MM/DD/YYYY based on locale"
    elif 'currency' in name_lower or 'price' in name_lower or 'amount' in name_lower:
        return "$1,234.56"
    elif 'percentage' in name_lower or 'rate' in name_lower:
        return "23.45%"
    else:
        return "Plain text"


def _infer_error_messages(field_name: str, field_type: str) -> str:
    """Infer error messages for field validation."""
    
    name_lower = field_name.lower()
    
    if 'email' in name_lower:
        return "Please enter a valid email address"
    elif 'password' in name_lower:
        return "Password must be at least 8 characters with uppercase, lowercase, and number"
    elif 'phone' in name_lower:
        return "Please enter a valid phone number"
    elif 'required' in name_lower or field_type == 'required':
        return "This field is required"
    else:
        return f"Please enter a valid {field_name}"


def _infer_success_behavior(fields: List[Dict[str, Any]], domain: Optional[str]) -> str:
    """Infer what happens after successful form submission."""
    
    field_names = [f.get('name', '').lower() for f in fields]
    
    if any('email' in name or 'username' in name for name in field_names) and any('password' in name for name in field_names):
        return "Redirect to dashboard/home page; create user session"
    elif any('search' in name for name in field_names):
        return "Display search results below form"
    else:
        return "Show success message; clear form or redirect to relevant page"


def _infer_column_data_type(header: str, domain: Optional[str]) -> str:
    """Infer data type for table column."""
    
    header_lower = header.lower()
    
    if any(word in header_lower for word in ['date', 'time', 'created', 'updated']):
        return "Date/Time"
    elif any(word in header_lower for word in ['id', '#', 'number', 'count']):
        return "Number/Integer"
    elif any(word in header_lower for word in ['revenue', 'cost', 'price', 'amount', '$']):
        return "Currency"
    elif any(word in header_lower for word in ['rate', 'percentage', '%', 'ctr', 'cvr']):
        return "Percentage"
    elif any(word in header_lower for word in ['status', 'state', 'type', 'category']):
        return "Categorical/Enum"
    else:
        return "Text/String"


def _infer_column_format(header: str, domain: Optional[str]) -> str:
    """Infer display format for table column."""
    
    header_lower = header.lower()
    
    if any(word in header_lower for word in ['date', 'created', 'updated']):
        return "YYYY-MM-DD HH:MM:SS or localized format"
    elif any(word in header_lower for word in ['revenue', 'cost', 'price', 'amount', '$']):
        return "$1,234.56 with thousand separators"
    elif any(word in header_lower for word in ['rate', 'percentage', '%', 'ctr', 'cvr']):
        return "23.45%"
    elif any(word in header_lower for word in ['count', 'number']):
        return "1,234 with thousand separators"
    else:
        return "Plain text"


def _infer_aggregation_support(header: str) -> str:
    """Infer if column supports aggregation."""
    
    header_lower = header.lower()
    
    if any(word in header_lower for word in ['revenue', 'cost', 'amount', 'count', 'total']):
        return "Sum, Average, Min, Max"
    elif any(word in header_lower for word in ['rate', 'percentage']):
        return "Average, Min, Max"
    elif any(word in header_lower for word in ['id', 'name', 'title']):
        return "Count (distinct)"
    else:
        return "Count"


def _infer_concurrent_users(domain: Optional[str]) -> str:
    """Infer expected concurrent users."""
    
    if domain and 'enterprise' in domain.lower():
        return "1,000+"
    elif domain and any(word in domain.lower() for word in ['small', 'startup']):
        return "100-500"
    else:
        return "500-1,000"


def _infer_data_volume(domain: Optional[str]) -> str:
    """Infer expected data volume."""
    
    if domain and 'enterprise' in domain.lower():
        return "millions of"
    elif domain and any(word in domain.lower() for word in ['small', 'startup']):
        return "tens of thousands of"
    else:
        return "hundreds of thousands of"


# Agent configuration
spec_converter_agent = Agent(
    model='gemini-2.0-flash-exp',
    name='spec_converter_agent',
    description='Converts technical UI extractions to comprehensive functional specifications',
    instruction="""You are a business analyst and technical writer specialized in creating comprehensive functional specifications.

Your role is to convert technical UI extraction data into detailed functional specifications that focus on:
- WHAT each feature does (business logic, calculations, data formats)
- Expected behaviors and interactions
- Data requirements and validation rules
- Business rules and workflows

When asked to convert specifications:
1. Ask about the application domain (advertising, e-commerce, finance, etc.) if not provided
2. Ask about target audience (developers, AI agents, product managers) if not provided
3. Use the convert_to_functional_spec_tool to generate comprehensive specification
4. Focus on functional details, not technical implementation

Important:
- Generate ONE comprehensive document with all functional requirements
- Describe calculations, formats, and business logic in detail
- Example: "Gross Revenue: Display platform revenue in USD with thousand separators, calculated by summing revenue across all categories"
- Avoid generic UI component descriptions
- Be specific about data formats, calculations, and expected behaviors
- Include validation rules, error handling, and edge cases

Ask clarifying questions about:
- Domain context (advertising, finance, e-commerce, etc.)
- Business rules and logic
- Data sources and calculations
- User roles and permissions""",
    tools=[convert_to_functional_spec_tool]
)
