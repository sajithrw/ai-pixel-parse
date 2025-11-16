"""UI Extraction Agent for web applications.

This module provides functionality to crawl web applications and extract
comprehensive behavioral UI specifications including:
- Interactive behaviors and event handlers
- Form validation rules and submission methods
- Button actions and state changes
- Table interactions (sorting, filtering, pagination)
- Navigation patterns and link behaviors

The extracted specifications focus on WHAT the UI does (behaviors, validations,
interactions) rather than HOW it looks (styling, layout), making them ideal for
rebuilding applications in different tech stacks.
"""

from __future__ import annotations

import asyncio
import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.adk.agents.llm_agent import Agent
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

class UIExtractor:
    """Handles web crawling and UI behavioral specification extraction.
    
    This class orchestrates browser automation via Playwright to visit web pages,
    extract interactive component information, and generate behavioral specifications.
    
    Attributes:
        output_dir: Directory where extraction results are saved.
        browser: Playwright browser instance.
        context: Browser context for maintaining session state.
        visited_urls: Set of URLs that have been processed.
        extracted_pages: List of extracted page data dictionaries.
    """
    
    def __init__(self, output_dir: Optional[str] = None) -> None:
        """Initialize extractor with output directory configuration.

        Args:
            output_dir: Path for extraction output. If None, defaults to
                repository's "extraction" folder for workspace visibility.
        """
        # Default to repo-root/extraction for consistent output location
        if output_dir is None or str(output_dir).strip() == "":
            repo_root = Path(__file__).resolve().parents[1]
            self.output_dir = repo_root / "extraction"
        else:
            self.output_dir = Path(output_dir).expanduser().resolve()

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.visited_urls: set[str] = set()
        self.extracted_pages: List[Dict[str, Any]] = []
        
    async def initialize_browser(self, headless: bool = True) -> None:
        """Initialize Playwright browser with optimal settings.
        
        Args:
            headless: Whether to run browser in headless mode.
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
    async def close_browser(self) -> None:
        """Clean up browser resources and close connections."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def login(
        self,
        page: Page,
        login_url: str,
        username: str,
        password: str,
        username_selector: str = "input[name='username'], input[type='email'], input[id*='user'], input[id*='email']",
        password_selector: str = "input[name='password'], input[type='password'], input[id*='pass']",
        submit_selector: str = "button[type='submit'], input[type='submit'], button:has-text('Login'), button:has-text('Sign in')"
    ) -> None:
        """Handle login flow with flexible selector configuration.
        
        Args:
            page: Playwright page instance.
            login_url: URL of the login page.
            username: Username/email for authentication.
            password: Password for authentication.
            username_selector: CSS selector for username input field.
            password_selector: CSS selector for password input field.
            submit_selector: CSS selector for submit button.
            
        Raises:
            TimeoutError: If login form elements cannot be found.
        """
        await page.goto(login_url, wait_until='networkidle')
        
        # Wait for login form to be visible
        await page.wait_for_selector(username_selector, timeout=10000)
        
        # Fill credentials
        await page.fill(username_selector, username)
        await page.fill(password_selector, password)
        
        # Submit form and wait for navigation
        await page.click(submit_selector)
        await page.wait_for_load_state('networkidle')
        
        print(f"✓ Logged in successfully to {login_url}")
        
    async def extract_iframe_components(self, page: Page) -> List[Dict[str, Any]]:
        """
        Extract components from all iframes on the page.
        
        Many dashboards embed KPIs, charts, and other components in iframes.
        This method detects iframes and extracts their content.
        
        Args:
            page: Playwright Page object.
            
        Returns:
            List of iframe data with their extracted components.
        """
        iframes_data = []
        
        try:
            # Get all iframe elements
            iframe_elements = await page.query_selector_all('iframe')
            
            print(f"  → Found {len(iframe_elements)} iframe(s) on page")
            
            for idx, iframe_element in enumerate(iframe_elements):
                try:
                    # Get iframe metadata
                    iframe_info = await iframe_element.evaluate("""
                        (iframe) => ({
                            src: iframe.src,
                            id: iframe.id || `iframe_${Date.now()}`,
                            name: iframe.name,
                            title: iframe.title,
                            width: iframe.width,
                            height: iframe.height,
                            classes: iframe.className
                        })
                    """)
                    
                    print(f"    → Processing iframe #{idx + 1}: {iframe_info.get('src', 'about:blank')[:60]}")
                    
                    # Get the frame content
                    frame = await iframe_element.content_frame()
                    
                    if frame is None:
                        print(f"      ⚠ Cannot access iframe content (likely cross-origin)")
                        iframe_info['components'] = {'error': 'Cross-origin iframe - access denied'}
                        iframes_data.append(iframe_info)
                        continue
                    
                    # Wait for iframe content to load
                    try:
                        await frame.wait_for_load_state('domcontentloaded', timeout=5000)
                    except Exception as e:
                        print(f"      ⚠ Iframe load timeout: {str(e)[:50]}")
                    
                    # Extract components from iframe
                    iframe_components = {}
                    
                    # Extract KPI/metric components (common in dashboard iframes)
                    iframe_components['metrics'] = await frame.evaluate(r"""
                        () => {
                            const metrics = [];
                            
                            // Look for common KPI/metric patterns
                            const selectors = [
                                '[class*="metric"]', '[class*="kpi"]', '[class*="stat"]',
                                '[class*="count"]', '[class*="value"]', '[class*="number"]',
                                '.card', '.widget', '[class*="dashboard"]'
                            ];
                            
                            const processedElements = new Set();
                            
                            selectors.forEach(selector => {
                                try {
                                    document.querySelectorAll(selector).forEach((el, idx) => {
                                        if (processedElements.has(el)) return;
                                        processedElements.add(el);
                                        
                                        const rect = el.getBoundingClientRect();
                                        if (rect.width === 0 || rect.height === 0) return;
                                        
                                        // Extract text content
                                        const text = el.textContent.trim();
                                        if (!text) return;
                                        
                                        // Try to identify label and value
                                        const numbers = text.match(/[\d,]+\.?\d*/g);
                                        const hasNumber = numbers && numbers.length > 0;
                                        
                                        metrics.push({
                                            id: el.id || `metric_${idx}`,
                                            text: text.substring(0, 200),
                                            classes: el.className,
                                            hasNumericValue: hasNumber,
                                            values: numbers || [],
                                            selector: selector,
                                            tagName: el.tagName
                                        });
                                    });
                                } catch (e) {
                                    console.error('Error processing selector:', selector, e);
                                }
                            });
                            
                            return metrics;
                        }
                    """)
                    
                    # Extract charts/visualizations
                    iframe_components['charts'] = await frame.evaluate("""
                        () => {
                            const charts = [];
                            
                            // Common chart library elements
                            const chartSelectors = [
                                'canvas', 'svg',
                                '[class*="chart"]', '[class*="graph"]', '[class*="plot"]',
                                '[class*="visual"]', '[id*="chart"]', '[id*="graph"]'
                            ];
                            
                            chartSelectors.forEach(selector => {
                                try {
                                    document.querySelectorAll(selector).forEach((el, idx) => {
                                        const rect = el.getBoundingClientRect();
                                        if (rect.width < 50 || rect.height < 50) return;
                                        
                                        charts.push({
                                            id: el.id || `chart_${idx}`,
                                            type: el.tagName.toLowerCase(),
                                            classes: el.className,
                                            width: rect.width,
                                            height: rect.height,
                                            title: el.getAttribute('aria-label') || el.getAttribute('title') || 'Unnamed chart'
                                        });
                                    });
                                } catch (e) {
                                    console.error('Error processing chart selector:', selector, e);
                                }
                            });
                            
                            return charts;
                        }
                    """)
                    
                    # Extract buttons in iframe
                    iframe_components['buttons'] = await frame.evaluate("""
                        () => {
                            const buttons = [];
                            document.querySelectorAll('button, input[type="button"], input[type="submit"], [role="button"]').forEach((btn, idx) => {
                                const rect = btn.getBoundingClientRect();
                                if (rect.width === 0 || rect.height === 0) return;
                                
                                buttons.push({
                                    id: btn.id || `btn_${idx}`,
                                    text: btn.textContent.trim() || btn.value || '',
                                    type: btn.type || 'button',
                                    classes: btn.className,
                                    disabled: btn.disabled
                                });
                            });
                            return buttons;
                        }
                    """)
                    
                    # Extract tables in iframe
                    iframe_components['tables'] = await frame.evaluate("""
                        () => {
                            const tables = [];
                            document.querySelectorAll('table').forEach((table, idx) => {
                                const headers = Array.from(table.querySelectorAll('thead th, thead td')).map(h => h.textContent.trim());
                                const rowCount = table.querySelectorAll('tbody tr').length;
                                
                                tables.push({
                                    id: table.id || `table_${idx}`,
                                    headers: headers,
                                    rowCount: rowCount,
                                    columnCount: headers.length,
                                    classes: table.className
                                });
                            });
                            return tables;
                        }
                    """)
                    
                    # Extract forms in iframe
                    iframe_components['forms'] = await frame.evaluate("""
                        () => {
                            const forms = [];
                            document.querySelectorAll('form').forEach((form, idx) => {
                                const inputs = Array.from(form.querySelectorAll('input, select, textarea')).map(inp => ({
                                    type: inp.type || inp.tagName.toLowerCase(),
                                    name: inp.name || inp.id,
                                    placeholder: inp.placeholder || ''
                                }));
                                
                                forms.push({
                                    id: form.id || `form_${idx}`,
                                    action: form.action,
                                    method: form.method,
                                    inputs: inputs,
                                    classes: form.className
                                });
                            });
                            return forms;
                        }
                    """)
                    
                    iframe_info['components'] = iframe_components
                    
                    # Summary stats
                    metrics_count = len(iframe_components.get('metrics', []))
                    charts_count = len(iframe_components.get('charts', []))
                    buttons_count = len(iframe_components.get('buttons', []))
                    tables_count = len(iframe_components.get('tables', []))
                    forms_count = len(iframe_components.get('forms', []))
                    
                    print(f"      ✓ Extracted: {metrics_count} metrics, {charts_count} charts, "
                          f"{buttons_count} buttons, {tables_count} tables, {forms_count} forms")
                    
                    iframes_data.append(iframe_info)
                    
                except Exception as e:
                    print(f"      ⚠ Error extracting iframe #{idx + 1}: {str(e)[:100]}")
                    iframe_info['components'] = {'error': str(e)}
                    iframes_data.append(iframe_info)
                    continue
                    
        except Exception as e:
            print(f"  ⚠ Error during iframe extraction: {str(e)}")
            
        return iframes_data
    
    async def extract_page_components(self, page: Page, url: str) -> Dict[str, Any]:
        """
        Extract comprehensive UI component information from a page.
        
        Returns structured data about all UI elements, their properties,
        functions, and relationships.
        """
        # Take screenshot (saved to app-specific directory, will be moved later)
        screenshot_path = Path(f"screenshot_{len(self.extracted_pages)}.png")
        await page.screenshot(path=str(screenshot_path), full_page=True)
        
        # Extract page metadata
        page_data = {
            'url': url,
            'title': await page.title(),
            'timestamp': datetime.now().isoformat(),
            'screenshot': str(screenshot_path),
            'components': {},
            'structure': {},
            'navigation': {},
            'functions': []
        }
        
        # Extract navigation elements
        page_data['navigation'] = await page.evaluate("""
            () => {
                const navElements = [];
                const navSelectors = ['nav', '[role="navigation"]', 'header a', '.nav', '.navbar', '.menu'];
                
                navSelectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach(el => {
                        const links = el.querySelectorAll('a');
                        links.forEach(link => {
                            if (link.href && link.textContent.trim()) {
                                navElements.push({
                                    text: link.textContent.trim(),
                                    href: link.href,
                                    type: 'navigation_link'
                                });
                            }
                        });
                    });
                });
                
                return navElements;
            }
        """)
        
        # Extract buttons with their behavioral details
        page_data['components']['buttons'] = await page.evaluate("""
            () => {
                const buttons = [];
                document.querySelectorAll('button, input[type="button"], input[type="submit"], [role="button"], a[role="button"]').forEach((btn, idx) => {
                    const rect = btn.getBoundingClientRect();
                    
                    // Capture event listeners
                    const eventListeners = [];
                    const eventTypes = ['click', 'mousedown', 'mouseup', 'keydown', 'keyup', 'focus', 'blur'];
                    
                    // Extract behavior from attributes
                    const behaviors = {
                        submitsForm: btn.type === 'submit',
                        opensModal: btn.hasAttribute('data-toggle') || btn.hasAttribute('data-modal') || btn.hasAttribute('aria-haspopup'),
                        navigatesTo: btn.tagName === 'A' ? btn.href : (btn.getAttribute('data-href') || btn.getAttribute('data-url')),
                        triggersAction: btn.hasAttribute('data-action') ? btn.getAttribute('data-action') : null,
                        hasConfirmation: btn.hasAttribute('data-confirm'),
                        isAsync: btn.hasAttribute('data-remote') || btn.hasAttribute('data-async'),
                        togglesState: btn.hasAttribute('aria-pressed') || btn.hasAttribute('data-toggle'),
                        expandsCollapse: btn.hasAttribute('aria-expanded'),
                        disabled: btn.disabled || btn.getAttribute('aria-disabled') === 'true'
                    };
                    
                    // Detect parent form if submits
                    let formContext = null;
                    if (btn.type === 'submit') {
                        const form = btn.closest('form');
                        if (form) {
                            formContext = {
                                formId: form.id || 'unknown',
                                action: form.action,
                                method: form.method
                            };
                        }
                    }
                    
                    const dataAttributes = {};
                    Array.from(btn.attributes).filter(a => a.name.startsWith('data-')).forEach(a => {
                        dataAttributes[a.name] = a.value;
                    });
                    
                    buttons.push({
                        id: btn.id || `button_${idx}`,
                        text: btn.textContent.trim() || btn.value || btn.getAttribute('aria-label') || '',
                        type: btn.type || 'button',
                        tagName: btn.tagName,
                        visible: rect.width > 0 && rect.height > 0,
                        behaviors: behaviors,
                        formContext: formContext,
                        onclick: btn.onclick ? btn.onclick.toString() : null,
                        accessibilityLabel: btn.getAttribute('aria-label') || btn.getAttribute('title'),
                        keyboardAccessible: btn.tabIndex >= 0,
                        role: btn.getAttribute('role'),
                        dataAttributes: dataAttributes
                    });
                });
                return buttons;
            }
        """)
        
        # Extract forms with behavioral details
        page_data['components']['forms'] = await page.evaluate("""
            () => {
                const forms = [];
                document.querySelectorAll('form').forEach((form, idx) => {
                    const inputs = [];
                    form.querySelectorAll('input, select, textarea').forEach((input, inputIdx) => {
                        // Detect validation and behavior patterns
                        const validationRules = {
                            required: input.required || input.hasAttribute('aria-required'),
                            pattern: input.pattern || null,
                            minLength: input.minLength > 0 ? input.minLength : null,
                            maxLength: input.maxLength > 0 ? input.maxLength : null,
                            min: input.min || null,
                            max: input.max || null,
                            step: input.step || null,
                            customValidation: input.hasAttribute('data-validate') || input.hasAttribute('data-validation')
                        };
                        
                        const behaviors = {
                            autoComplete: input.autocomplete !== 'off',
                            autoFocus: input.autofocus,
                            readonly: input.readOnly,
                            disabled: input.disabled,
                            multipleSelection: input.multiple,
                            hasPlaceholder: !!input.placeholder,
                            triggersSearch: input.type === 'search' || input.hasAttribute('data-search'),
                            liveValidation: input.hasAttribute('data-live-validate') || input.oninput !== null
                        };
                        
                        const inputDataAttributes = {};
                        Array.from(input.attributes).filter(a => a.name.startsWith('data-')).forEach(a => {
                            inputDataAttributes[a.name] = a.value;
                        });
                        
                        inputs.push({
                            id: input.id || `input_${inputIdx}`,
                            name: input.name,
                            type: input.type,
                            label: input.labels && input.labels[0] ? input.labels[0].textContent.trim() : (input.getAttribute('placeholder') || input.getAttribute('aria-label') || ''),
                            required: input.required,
                            placeholder: input.placeholder,
                            defaultValue: input.defaultValue,
                            currentValue: input.value,
                            validation: validationRules,
                            behaviors: behaviors,
                            options: input.tagName === 'SELECT' ? 
                                Array.from(input.options).map(opt => ({text: opt.text, value: opt.value, selected: opt.selected})) : null,
                            dataAttributes: inputDataAttributes
                        });
                    });
                    
                    // Detect form behaviors
                    const formBehaviors = {
                        submitsViaAjax: form.hasAttribute('data-remote') || form.hasAttribute('data-ajax'),
                        hasClientSideValidation: form.noValidate === false,
                        preventsDefault: form.onsubmit ? form.onsubmit.toString().includes('preventDefault') : false,
                        hasFileUpload: form.enctype === 'multipart/form-data' || !!form.querySelector('input[type="file"]'),
                        autoSaves: form.hasAttribute('data-autosave'),
                        requiresConfirmation: form.hasAttribute('data-confirm')
                    };
                    
                    forms.push({
                        id: form.id || `form_${idx}`,
                        action: form.action,
                        method: form.method,
                        enctype: form.enctype,
                        inputs: inputs,
                        submitButtons: Array.from(form.querySelectorAll('button[type="submit"], input[type="submit"]')).map(btn => ({
                            id: btn.id,
                            text: btn.textContent.trim() || btn.value
                        })),
                        behaviors: formBehaviors,
                        onsubmit: form.onsubmit ? form.onsubmit.toString() : null
                    });
                });
                return forms;
            }
        """)
        
        # Extract tables with interaction capabilities
        page_data['components']['tables'] = await page.evaluate("""
            () => {
                const tables = [];
                document.querySelectorAll('table').forEach((table, idx) => {
                    const headers = Array.from(table.querySelectorAll('thead th, thead td')).map(h => h.textContent.trim());
                    const rows = [];
                    table.querySelectorAll('tbody tr').forEach(tr => {
                        const cells = Array.from(tr.querySelectorAll('td, th')).map(cell => cell.textContent.trim());
                        rows.push(cells);
                    });
                    
                    // Detect table behaviors
                    const behaviors = {
                        isSortable: !!table.querySelector('th[data-sort], th.sortable, th[onclick*="sort"]'),
                        isFilterable: !!table.closest('[data-filter], [class*="filter"]'),
                        hasPagination: table.closest('div') ? !!table.closest('div').querySelector('[class*="paginat"], [data-page]') : false,
                        hasRowSelection: !!table.querySelector('input[type="checkbox"], input[type="radio"]'),
                        hasRowActions: !!table.querySelector('button, a[class*="action"], .action-button'),
                        isEditable: !!table.querySelector('input:not([type="checkbox"]):not([type="radio"]), textarea, [contenteditable]'),
                        hasExpandableRows: !!table.querySelector('[class*="expand"], [data-toggle="collapse"]')
                    };
                    
                    // Detect action columns
                    const actionButtons = Array.from(table.querySelectorAll('button, a[class*="btn"]')).map(btn => {
                        let action = btn.getAttribute('data-action');
                        if (!action && btn.onclick) {
                            action = btn.onclick.toString().substring(0, 100);
                        }
                        return {
                            text: btn.textContent.trim(),
                            action: action || ''
                        };
                    });
                    
                    const tableDataAttributes = {};
                    Array.from(table.attributes).filter(a => a.name.startsWith('data-')).forEach(a => {
                        tableDataAttributes[a.name] = a.value;
                    });
                    
                    tables.push({
                        id: table.id || `table_${idx}`,
                        headers: headers,
                        rowCount: rows.length,
                        columnCount: headers.length || (rows[0] ? rows[0].length : 0),
                        sampleRows: rows.slice(0, 3),
                        behaviors: behaviors,
                        actionButtons: actionButtons.slice(0, 5),
                        dataAttributes: tableDataAttributes
                    });
                });
                return tables;
            }
        """)
        
        # Extract icons and images
        page_data['components']['icons'] = await page.evaluate("""
            () => {
                const icons = [];
                // SVG icons
                document.querySelectorAll('svg').forEach((svg, idx) => {
                    const rect = svg.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0 && rect.width < 100 && rect.height < 100) {
                        icons.push({
                            id: svg.id || `icon_svg_${idx}`,
                            type: 'svg',
                            classes: svg.className.baseVal || svg.className,
                            position: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
                            ariaLabel: svg.getAttribute('aria-label')
                        });
                    }
                });
                
                // Icon fonts (FontAwesome, Material Icons, etc.)
                document.querySelectorAll('i, .icon, [class*="icon-"], [class*="fa-"]').forEach((icon, idx) => {
                    const rect = icon.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        icons.push({
                            id: icon.id || `icon_${idx}`,
                            type: 'icon-font',
                            classes: icon.className,
                            position: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
                        });
                    }
                });
                
                return icons;
            }
        """)
        
        # Extract interactive links
        page_data['components']['links'] = await page.evaluate("""
            () => {
                const links = [];
                document.querySelectorAll('a[href]').forEach((link, idx) => {
                    const rect = link.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        const behaviors = {
                            opensInNewTab: link.target === '_blank',
                            isDownload: link.hasAttribute('download'),
                            triggersAction: link.hasAttribute('data-action'),
                            requiresAuth: link.hasAttribute('data-auth'),
                            isAjaxLink: link.hasAttribute('data-remote') || link.hasAttribute('data-ajax'),
                            hasConfirmation: link.hasAttribute('data-confirm')
                        };
                        
                        links.push({
                            id: link.id || `link_${idx}`,
                            text: link.textContent.trim(),
                            href: link.href,
                            isExternal: link.href.startsWith('http') && !link.href.includes(window.location.hostname),
                            behaviors: behaviors,
                            ariaLabel: link.getAttribute('aria-label'),
                            title: link.title
                        });
                    }
                });
                return links.slice(0, 100); // Limit to first 100
            }
        """)
        
        # Extract modals and dialogs
        page_data['components']['modals'] = await page.evaluate("""
            () => {
                const modals = [];
                document.querySelectorAll('[role="dialog"], .modal, .dialog, .popup').forEach((modal, idx) => {
                    const rect = modal.getBoundingClientRect();
                    modals.push({
                        id: modal.id || `modal_${idx}`,
                        classes: modal.className,
                        visible: window.getComputedStyle(modal).display !== 'none',
                        title: modal.querySelector('[class*="title"], h1, h2, h3')?.textContent.trim() || '',
                        position: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
                    });
                });
                return modals;
            }
        """)
        
        # Extract page structure and layout
        page_data['structure'] = await page.evaluate("""
            () => {
                return {
                    header: document.querySelector('header') ? {
                        text: document.querySelector('header').textContent.trim().substring(0, 200),
                        classes: document.querySelector('header').className
                    } : null,
                    footer: document.querySelector('footer') ? {
                        text: document.querySelector('footer').textContent.trim().substring(0, 200),
                        classes: document.querySelector('footer').className
                    } : null,
                    sidebar: document.querySelector('aside, [class*="sidebar"]') ? {
                        classes: document.querySelector('aside, [class*="sidebar"]').className
                    } : null,
                    main: document.querySelector('main, [role="main"]') ? {
                        classes: document.querySelector('main, [role="main"]').className
                    } : null
                };
            }
        """)
        
        # Identify functions/features based on components
        functions = []
        if page_data['components']['forms']:
            for form in page_data['components']['forms']:
                func_desc = f"Form submission: {form['action'] or 'client-side processing'}"
                func_desc += f"\n  Method: {form['method']}"
                func_desc += f"\n  Inputs: {len(form['inputs'])} fields"
                for inp in form['inputs']:
                    func_desc += f"\n    - {inp['label'] or inp['name']}: {inp['type']}"
                functions.append({
                    'type': 'form_submission',
                    'description': func_desc,
                    'component_id': form['id']
                })
        
        if page_data['components']['tables']:
            for table in page_data['components']['tables']:
                functions.append({
                    'type': 'data_display',
                    'description': f"Table display with {table['rowCount']} rows and {table['columnCount']} columns\n  Headers: {', '.join(table['headers'])}",
                    'component_id': table['id']
                })
        
        # Search/filter functions
        search_inputs = [inp for form in page_data['components']['forms'] for inp in form['inputs'] if 'search' in (inp.get('name', '') + inp.get('label', '')).lower()]
        if search_inputs:
            functions.append({
                'type': 'search',
                'description': f"Search functionality with {len(search_inputs)} search input(s)",
                'component_id': search_inputs[0]['id']
            })
        
        page_data['functions'] = functions
        
        # Extract iframe content
        page_data['components']['iframes'] = await self.extract_iframe_components(page)
        
        return page_data
    
    async def crawl_application(self, base_url: str, login_config: Optional[Dict[str, str]] = None, 
                               max_pages: int = 50, dynamic_content_wait: int = 0) -> List[Dict[str, Any]]:
        """
        Crawl entire application and extract UI specifications.
        
        Args:
            base_url: Starting URL of the application
            login_config: Dict with 'url', 'username', 'password' and optional selectors
            max_pages: Maximum number of pages to crawl
            dynamic_content_wait: Additional wait time in seconds for dynamic content (KPIs, charts)
        """
        await self.initialize_browser()
        page = await self.context.new_page()
        
        # Handle login if configured
        if login_config:
            await self.login(
                page, 
                login_config['url'],
                login_config['username'],
                login_config['password'],
                login_config.get('username_selector', "input[name='username'], input[type='email']"),
                login_config.get('password_selector', "input[name='password'], input[type='password']"),
                login_config.get('submit_selector', "button[type='submit'], input[type='submit']")
            )
            await asyncio.sleep(2)  # Wait for post-login redirects
        
        # Start crawling from base URL
        urls_to_visit = [base_url]
        
        while urls_to_visit and len(self.visited_urls) < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
                
            try:
                print(f"Extracting: {current_url}")
                # Try networkidle first, fallback to load if it times out
                try:
                    await page.goto(current_url, wait_until='networkidle', timeout=30000)
                except Exception as e:
                    if 'Timeout' in str(e):
                        print(f"  → Networkidle timeout, using 'load' strategy...")
                        await page.goto(current_url, wait_until='load', timeout=30000)
                        # Wait for dynamic content (default 3s, configurable)
                        if dynamic_content_wait > 0:
                            print(f"  → Waiting {dynamic_content_wait}s for dynamic content (KPIs, charts, etc.)...")
                            await page.wait_for_timeout(dynamic_content_wait * 1000)
                        else:
                            await page.wait_for_timeout(3000)
                    else:
                        raise
                print(f"  → Page loaded successfully")
                
                # Extract page data
                print(f"  → Extracting components...")
                page_data = await self.extract_page_components(page, current_url)
                print(f"  → Components extracted: {len(page_data.get('components', {}).get('buttons', []))} buttons, "
                      f"{len(page_data.get('components', {}).get('forms', []))} forms")
                
                self.extracted_pages.append(page_data)
                self.visited_urls.add(current_url)
                
                # Find more URLs to visit (same domain only)
                nav_links = page_data.get('navigation', [])
                new_links = [link['href'] for link in nav_links
                           if link.get('href', '').startswith(base_url) and link['href'] not in self.visited_urls]
                urls_to_visit.extend(new_links[:10])  # Limit new links per page
                
                print(f"  ✓ Extracted {len(page_data['components']['buttons'])} buttons, "
                      f"{len(page_data['components']['forms'])} forms, "
                      f"{len(page_data['components']['tables'])} tables")
                
            except Exception as e:
                print(f"  ✗ Error extracting {current_url}: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
        
        await self.close_browser()
        return self.extracted_pages
    
    def save_specifications(self, app_name: str):
        """Persist extracted specifications as clear text and JSON.

        Creates timestamped app-specific folder structure:
        - extraction/<AppName>_<timestamp>/00_SUMMARY.txt
        - extraction/<AppName>_<timestamp>/*.txt (per-page specs)
        - extraction/<AppName>_<timestamp>/README.md (extraction summary)
        - extraction/<AppName>_<timestamp>/screenshot_*.png (page screenshots)
        - extraction/<AppName>_<timestamp>/full_extraction.json (structured data)
        
        Note: All files are contained within the app-specific timestamped subfolder.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create app-specific directory
        app_dir = self.output_dir / f"{app_name}_{timestamp}"
        app_dir.mkdir(exist_ok=True)
        
        # Save summary
        summary_path = app_dir / "00_SUMMARY.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"UI EXTRACTION SUMMARY\n")
            f.write(f"=" * 80 + "\n\n")
            f.write(f"Application: {app_name}\n")
            f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Pages Extracted: {len(self.extracted_pages)}\n\n")
            
            # Overall statistics
            total_buttons = sum(len(page['components']['buttons']) for page in self.extracted_pages)
            total_forms = sum(len(page['components']['forms']) for page in self.extracted_pages)
            total_tables = sum(len(page['components']['tables']) for page in self.extracted_pages)
            total_icons = sum(len(page['components']['icons']) for page in self.extracted_pages)
            total_iframes = sum(len(page['components'].get('iframes', [])) for page in self.extracted_pages)
            
            f.write(f"Total UI Components:\n")
            f.write(f"  - Buttons: {total_buttons}\n")
            f.write(f"  - Forms: {total_forms}\n")
            f.write(f"  - Tables: {total_tables}\n")
            f.write(f"  - Icons: {total_icons}\n")
            f.write(f"  - Iframes: {total_iframes}\n\n")
            
            f.write(f"Pages Extracted:\n")
            for idx, page in enumerate(self.extracted_pages, 1):
                f.write(f"  {idx}. {page['title']} - {page['url']}\n")
        
        # Save detailed page specifications
        for idx, page in enumerate(self.extracted_pages, 1):
            page_file = app_dir / f"{idx:02d}_{self._sanitize_filename(page['title'])}.txt"
            
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(f"PAGE SPECIFICATION\n")
                f.write(f"=" * 80 + "\n\n")
                f.write(f"Title: {page['title']}\n")
                f.write(f"URL: {page['url']}\n")
                f.write(f"Screenshot: {page['screenshot']}\n")
                f.write(f"Extracted: {page['timestamp']}\n\n")
                
                # Page structure
                f.write(f"PAGE STRUCTURE\n")
                f.write(f"-" * 80 + "\n")
                if page['structure']['header']:
                    f.write(f"\nHeader:\n  Classes: {page['structure']['header']['classes']}\n")
                if page['structure']['main']:
                    f.write(f"\nMain Content:\n  Classes: {page['structure']['main']['classes']}\n")
                if page['structure']['sidebar']:
                    f.write(f"\nSidebar:\n  Classes: {page['structure']['sidebar']['classes']}\n")
                if page['structure']['footer']:
                    f.write(f"\nFooter:\n  Classes: {page['structure']['footer']['classes']}\n")
                
                # Functions
                f.write(f"\n\nFUNCTIONS & FEATURES\n")
                f.write(f"-" * 80 + "\n")
                for func in page['functions']:
                    f.write(f"\n[{func['type'].upper()}]\n")
                    f.write(f"{func['description']}\n")
                    f.write(f"Component ID: {func['component_id']}\n")
                
                # Buttons
                f.write(f"\n\nBUTTONS ({len(page['components']['buttons'])})\n")
                f.write(f"-" * 80 + "\n")
                for btn in page['components']['buttons']:
                    if btn['visible']:
                        f.write(f"\n[Button] {btn['text']}\n")
                        f.write(f"  ID: {btn['id']}\n")
                        f.write(f"  Type: {btn['type']}\n")
                        
                        # Behavioral details
                        f.write(f"\n  BEHAVIORS:\n")
                        behaviors = btn['behaviors']
                        if behaviors['submitsForm']:
                            f.write(f"    - Submits form\n")
                            if btn['formContext']:
                                f.write(f"      → Form: {btn['formContext']['formId']}\n")
                                f.write(f"      → Action: {btn['formContext']['action']}\n")
                                f.write(f"      → Method: {btn['formContext']['method']}\n")
                        if behaviors['navigatesTo']:
                            f.write(f"    - Navigates to: {behaviors['navigatesTo']}\n")
                        if behaviors['opensModal']:
                            f.write(f"    - Opens modal/dialog\n")
                        if behaviors['triggersAction']:
                            f.write(f"    - Triggers action: {behaviors['triggersAction']}\n")
                        if behaviors['hasConfirmation']:
                            f.write(f"    - Requires confirmation before action\n")
                        if behaviors['isAsync']:
                            f.write(f"    - Performs async/AJAX operation\n")
                        if behaviors['togglesState']:
                            f.write(f"    - Toggles state (pressed/unpressed)\n")
                        if behaviors['expandsCollapse']:
                            f.write(f"    - Expands/collapses content\n")
                        if behaviors['disabled']:
                            f.write(f"    - Currently disabled\n")
                        
                        # Accessibility
                        if btn['accessibilityLabel']:
                            f.write(f"\n  ACCESSIBILITY:\n")
                            f.write(f"    - Label: {btn['accessibilityLabel']}\n")
                        if not btn['keyboardAccessible']:
                            f.write(f"    - ⚠️ Not keyboard accessible\n")
                        
                        # Event handlers
                        if btn['onclick']:
                            f.write(f"\n  ONCLICK HANDLER:\n")
                            handler_preview = btn['onclick'][:200]
                            f.write(f"    {handler_preview}...\n")
                        
                        # Data attributes (may contain behavior info)
                        if btn['dataAttributes']:
                            f.write(f"\n  DATA ATTRIBUTES:\n")
                            for key, value in btn['dataAttributes'].items():
                                f.write(f"    - {key}: {value}\n")
                
                # Forms
                f.write(f"\n\nFORMS ({len(page['components']['forms'])})\n")
                f.write(f"-" * 80 + "\n")
                for form in page['components']['forms']:
                    f.write(f"\n[Form] {form['id']}\n")
                    f.write(f"  Action: {form['action']}\n")
                    f.write(f"  Method: {form['method']}\n")
                    if form['enctype']:
                        f.write(f"  Encoding: {form['enctype']}\n")
                    
                    # Form behaviors
                    f.write(f"\n  FORM BEHAVIORS:\n")
                    fb = form['behaviors']
                    if fb['submitsViaAjax']:
                        f.write(f"    - Submits via AJAX (no page reload)\n")
                    if fb['hasClientSideValidation']:
                        f.write(f"    - Has client-side validation\n")
                    if fb['preventsDefault']:
                        f.write(f"    - Prevents default form submission\n")
                    if fb['hasFileUpload']:
                        f.write(f"    - Supports file uploads\n")
                    if fb['autoSaves']:
                        f.write(f"    - Auto-saves form data\n")
                    if fb['requiresConfirmation']:
                        f.write(f"    - Requires confirmation before submit\n")
                    
                    # Submit buttons
                    if form['submitButtons']:
                        f.write(f"\n  SUBMIT BUTTONS:\n")
                        for sbtn in form['submitButtons']:
                            f.write(f"    - {sbtn['text']} (ID: {sbtn['id']})\n")
                    
                    f.write(f"\n  INPUTS ({len(form['inputs'])}):\n")
                    for inp in form['inputs']:
                        f.write(f"\n    [{inp['type'].upper()}] {inp['label'] or inp['name']}\n")
                        f.write(f"      ID: {inp['id']}\n")
                        f.write(f"      Name: {inp['name']}\n")
                        
                        # Validation rules
                        val = inp['validation']
                        if any([val['required'], val['pattern'], val['minLength'], val['maxLength'], val['min'], val['max']]):
                            f.write(f"\n      VALIDATION:\n")
                            if val['required']:
                                f.write(f"        - Required field\n")
                            if val['pattern']:
                                f.write(f"        - Pattern: {val['pattern']}\n")
                            if val['minLength']:
                                f.write(f"        - Min length: {val['minLength']}\n")
                            if val['maxLength']:
                                f.write(f"        - Max length: {val['maxLength']}\n")
                            if val['min']:
                                f.write(f"        - Min value: {val['min']}\n")
                            if val['max']:
                                f.write(f"        - Max value: {val['max']}\n")
                            if val['step']:
                                f.write(f"        - Step: {val['step']}\n")
                            if val['customValidation']:
                                f.write(f"        - Has custom validation logic\n")
                        
                        # Behaviors
                        behav = inp['behaviors']
                        behavior_list = []
                        if behav['autoComplete']:
                            behavior_list.append("autocomplete enabled")
                        if behav['autoFocus']:
                            behavior_list.append("auto-focus on load")
                        if behav['readonly']:
                            behavior_list.append("read-only")
                        if behav['disabled']:
                            behavior_list.append("disabled")
                        if behav['multipleSelection']:
                            behavior_list.append("multiple selection")
                        if behav['triggersSearch']:
                            behavior_list.append("triggers search")
                        if behav['liveValidation']:
                            behavior_list.append("live validation")
                        
                        if behavior_list:
                            f.write(f"\n      BEHAVIORS: {', '.join(behavior_list)}\n")
                        
                        # Placeholder and default value
                        if inp['placeholder']:
                            f.write(f"      Placeholder: {inp['placeholder']}\n")
                        if inp['defaultValue']:
                            f.write(f"      Default value: {inp['defaultValue']}\n")
                        
                        # Options for select
                        if inp['options']:
                            f.write(f"      Options ({len(inp['options'])}):\n")
                            for opt in inp['options'][:10]:  # Show first 10
                                selected = " [SELECTED]" if opt['selected'] else ""
                                f.write(f"        - {opt['text']}{selected}\n")
                            if len(inp['options']) > 10:
                                f.write(f"        ... and {len(inp['options']) - 10} more\n")
                
                # Tables
                f.write(f"\n\nTABLES ({len(page['components']['tables'])})\n")
                f.write(f"-" * 80 + "\n")
                for table in page['components']['tables']:
                    f.write(f"\n[Table] {table['id']}\n")
                    f.write(f"  Dimensions: {table['rowCount']} rows × {table['columnCount']} columns\n")
                    if table['headers']:
                        f.write(f"  Headers: {', '.join(table['headers'])}\n")
                    
                    # Table behaviors
                    behaviors = table['behaviors']
                    if any(behaviors.values()):
                        f.write(f"\n  TABLE INTERACTIONS:\n")
                        if behaviors['isSortable']:
                            f.write(f"    - Sortable columns\n")
                        if behaviors['isFilterable']:
                            f.write(f"    - Filterable data\n")
                        if behaviors['hasPagination']:
                            f.write(f"    - Paginated results\n")
                        if behaviors['hasRowSelection']:
                            f.write(f"    - Row selection (checkboxes/radio)\n")
                        if behaviors['hasRowActions']:
                            f.write(f"    - Row-level actions available\n")
                        if behaviors['isEditable']:
                            f.write(f"    - Inline editing enabled\n")
                        if behaviors['hasExpandableRows']:
                            f.write(f"    - Expandable row details\n")
                    
                    # Action buttons
                    if table['actionButtons']:
                        f.write(f"\n  ROW ACTIONS:\n")
                        for action in table['actionButtons']:
                            f.write(f"    - {action['text']}\n")
                            if action['action']:
                                f.write(f"      Action: {action['action'][:100]}\n")
                    
                    # Sample data
                    if table['sampleRows']:
                        f.write(f"\n  SAMPLE DATA:\n")
                        for row in table['sampleRows']:
                            f.write(f"    {' | '.join(row)}\n")
                
                # Icons
                f.write(f"\n\nICONS ({len(page['components']['icons'])})\n")
                f.write(f"-" * 80 + "\n")
                for icon in page['components']['icons'][:20]:  # Limit to first 20
                    f.write(f"\n[Icon] {icon['id']}\n")
                    f.write(f"  Type: {icon['type']}\n")
                    f.write(f"  Classes: {icon['classes']}\n")
                    f.write(f"  Position: x={icon['position']['x']:.0f}, y={icon['position']['y']:.0f}\n")
                
                # Navigation
                f.write(f"\n\nNAVIGATION ({len(page['navigation'])})\n")
                f.write(f"-" * 80 + "\n")
                for nav in page['navigation']:
                    f.write(f"  - {nav['text']} → {nav['href']}\n")
                
                # Interactive Links
                if 'links' in page['components']:
                    f.write(f"\n\nINTERACTIVE LINKS ({len(page['components']['links'])})\n")
                    f.write(f"-" * 80 + "\n")
                    for link in page['components']['links'][:50]:  # Show first 50
                        f.write(f"\n[Link] {link['text']}\n")
                        f.write(f"  Target: {link['href']}\n")
                        
                        behaviors = link['behaviors']
                        behavior_list = []
                        if link['isExternal']:
                            behavior_list.append("external link")
                        if behaviors['opensInNewTab']:
                            behavior_list.append("opens in new tab")
                        if behaviors['isDownload']:
                            behavior_list.append("downloads file")
                        if behaviors['triggersAction']:
                            behavior_list.append("triggers action")
                        if behaviors['requiresAuth']:
                            behavior_list.append("requires authentication")
                        if behaviors['isAjaxLink']:
                            behavior_list.append("AJAX request")
                        if behaviors['hasConfirmation']:
                            behavior_list.append("requires confirmation")
                        
                        if behavior_list:
                            f.write(f"  Behaviors: {', '.join(behavior_list)}\n")
                
                # Iframes (embedded content like KPIs, charts, dashboards)
                if 'iframes' in page['components'] and page['components']['iframes']:
                    f.write(f"\n\nIFRAMES / EMBEDDED CONTENT ({len(page['components']['iframes'])})\n")
                    f.write(f"-" * 80 + "\n")
                    f.write(f"Note: Many dashboards embed KPIs, charts, and widgets in iframes.\n\n")
                    
                    for iframe_idx, iframe in enumerate(page['components']['iframes'], 1):
                        f.write(f"\n[Iframe #{iframe_idx}] {iframe.get('id', 'unnamed')}\n")
                        if iframe.get('src'):
                            f.write(f"  Source: {iframe['src']}\n")
                        if iframe.get('title'):
                            f.write(f"  Title: {iframe['title']}\n")
                        if iframe.get('width') or iframe.get('height'):
                            f.write(f"  Dimensions: {iframe.get('width', 'auto')} × {iframe.get('height', 'auto')}\n")
                        
                        components = iframe.get('components', {})
                        
                        # Handle error cases
                        if 'error' in components:
                            f.write(f"  ⚠️ {components['error']}\n")
                            continue
                        
                        # Metrics/KPIs in iframe
                        metrics = components.get('metrics', [])
                        if metrics:
                            f.write(f"\n  METRICS/KPIs ({len(metrics)}):\n")
                            for metric in metrics:  # Show all metrics
                                f.write(f"    • {metric.get('text', 'N/A')[:100]}\n")
                                if metric.get('hasNumericValue'):
                                    f.write(f"      Values: {', '.join(metric.get('values', []))}\n")
                                f.write(f"      Classes: {metric.get('classes', 'none')}\n")
                        
                        # Charts in iframe
                        charts = components.get('charts', [])
                        if charts:
                            f.write(f"\n  CHARTS/VISUALIZATIONS ({len(charts)}):\n")
                            for chart in charts:  # Show all charts
                                chart_type = chart.get('type', 'unknown')
                                title = chart.get('title', 'Unnamed chart')
                                f.write(f"    • [{chart_type.upper()}] {title}\n")
                                f.write(f"      Size: {chart.get('width', 0):.0f} × {chart.get('height', 0):.0f}px\n")
                                if chart.get('classes'):
                                    f.write(f"      Classes: {chart['classes']}\n")
                        
                        # Buttons in iframe
                        buttons = components.get('buttons', [])
                        if buttons:
                            f.write(f"\n  BUTTONS ({len(buttons)}):\n")
                            for btn in buttons:  # Show all buttons
                                f.write(f"    • {btn.get('text', 'No text')} ({btn.get('type', 'button')})\n")
                                if btn.get('disabled'):
                                    f.write(f"      [DISABLED]\n")
                                if btn.get('classes'):
                                    f.write(f"      Classes: {btn['classes']}\n")
                        
                        # Tables in iframe
                        tables = components.get('tables', [])
                        if tables:
                            f.write(f"\n  TABLES ({len(tables)}):\n")
                            for tbl in tables:
                                f.write(f"    • {tbl.get('rowCount', 0)} rows × {tbl.get('columnCount', 0)} columns\n")
                                if tbl.get('headers'):
                                    f.write(f"      Headers: {', '.join(tbl['headers'][:5])}\n")
                        
                        # Forms in iframe
                        forms = components.get('forms', [])
                        if forms:
                            f.write(f"\n  FORMS ({len(forms)}):\n")
                            for frm in forms:
                                f.write(f"    • {frm.get('id', 'unnamed')} → {frm.get('action', 'N/A')}\n")
                                f.write(f"      Inputs: {len(frm.get('inputs', []))}\n")
        
        # Move screenshots to app-specific directory
        import glob
        for screenshot in glob.glob("screenshot_*.png"):
            screenshot_path = Path(screenshot)
            if screenshot_path.exists():
                target_path = app_dir / screenshot_path.name
                screenshot_path.rename(target_path)
                print(f"  → Moved {screenshot} to {app_dir}/")
        
        # Save JSON version for programmatic access
        json_path = app_dir / "full_extraction.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_pages, f, indent=2, ensure_ascii=False)
        
        # Create a README.md in the run directory for easy viewing
        readme_run = app_dir / "README.md"
        with open(readme_run, 'w', encoding='utf-8') as f:
            f.write(f"# UI Extraction — {app_name}\n\n")
            f.write(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"- Pages: {len(self.extracted_pages)}\n")
            f.write(f"- Buttons: {total_buttons} — Forms: {total_forms} — Tables: {total_tables} — Icons: {total_icons} — Iframes: {total_iframes}\n\n")
            f.write(f"Artifacts:\n\n")
            f.write(f"- 00_SUMMARY.txt — high-level overview\n")
            f.write(f"- full_extraction.json — structured data for programmatic use\n")
            f.write(f"- Page *.txt files — detailed specs per page\n")
            f.write(f"- screenshot_*.png — screenshots for reference\n")

        print(f"\n✓ Specifications saved to: {app_dir}")
        print(f"  - Summary: {summary_path.name}")
        print(f"  - Pages: {len(self.extracted_pages)} detailed specification files")
        print(f"  - JSON: {json_path.name}")
        
        return str(app_dir)
    
    def _sanitize_filename(self, text: str) -> str:
        """Convert text to safe filename."""
        import re
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '_', text)
        return text[:50]  # Limit length


# Google ADK Tool Function
async def extract_ui_tool(
    base_url: str,
    app_name: str,
    login_url: str = "",
    username: str = "",
    password: str = "",
    username_selector: str = "",
    password_selector: str = "",
    submit_selector: str = "",
    max_pages: int = 30,
    output_dir: str = ""
) -> str:
    """Extract behavioral UI specifications from a web application.
    
    This tool automates browser crawling to extract comprehensive behavioral
    specifications from web applications. It captures interactive elements,
    form validation rules, table interactions, and navigation patterns.
    
    Args:
        base_url: Starting URL to crawl (e.g., "https://example.com").
        app_name: Name for output folder (e.g., "ExampleApp").
        login_url: URL of login page for authenticated access.
        username: Username/email for authentication.
        password: Password for authentication.
        username_selector: CSS selector for username input field.
        password_selector: CSS selector for password input field.
        submit_selector: CSS selector for login submit button.
        max_pages: Maximum number of pages to crawl (default: 30).
        output_dir: Custom output directory path (optional).
    
    Returns:
        Status message with path to extraction output directory.
        
    Example:
        result = await extract_ui_tool(
            base_url="https://example.com",
            app_name="ExampleApp",
            max_pages=20
        )
    """
    # Build login config if credentials provided
    login_config = None
    if login_url and username and password:
        login_config = {
            'url': login_url,
            'username': username,
            'password': password
        }
        if username_selector:
            login_config['username_selector'] = username_selector
        if password_selector:
            login_config['password_selector'] = password_selector
        if submit_selector:
            login_config['submit_selector'] = submit_selector
    
    # Create extractor and run
    extractor = UIExtractor(output_dir=output_dir if output_dir else None)
    
    print(f"\n🚀 Starting UI extraction for: {app_name}")
    print(f"   Base URL: {base_url}")
    if login_config:
        print(f"   Login: Enabled")
    print(f"   Max pages: {max_pages}\n")
    
    try:
        # Perform extraction
        pages = await extractor.crawl_application(
            base_url=base_url,
            login_config=login_config,
            max_pages=max_pages
        )
        
        if not pages:
            return "Extraction ran, but no pages were processed. This could be due to an invalid URL, network issues, or the site blocking crawlers. Please check the URL and try again."

        # Save specifications
        output_path = extractor.save_specifications(app_name)
        
        print(f"\n✅ Extraction complete! Processed {len(pages)} pages")
        
        return f"Successfully extracted UI from {base_url}. Output saved to: {output_path}\n\nExtracted {len(pages)} pages with:\n- {sum(len(p['components']['buttons']) for p in pages)} buttons\n- {sum(len(p['components']['forms']) for p in pages)} forms\n- {sum(len(p['components']['tables']) for p in pages)} tables\n- {sum(len(p['components']['icons']) for p in pages)} icons\n\nYou can find detailed specifications in the output directory."
    except Exception as e:
        error_message = f"An error occurred during UI extraction: {str(e)}"
        print(f"❌ {error_message}")
        # Also check for common Playwright errors
        if "playwright install" in str(e):
            return "Error: Playwright browser dependencies are not installed. Please run 'playwright install --with-deps chromium' in your terminal and try again."
        return error_message


# Google ADK Agent Configuration
# This agent is configured with the extract_ui_tool for behavioral UI extraction
ui_extractor_agent = Agent(
    model='gemini-1.5-flash-latest',
    name='ui_extractor_agent',
    description=(
        'Specialized AI agent for extracting behavioral UI specifications '
        'from web applications using automated browser crawling.'
    ),
    instruction=(
        'You are a UI extraction specialist. Your goal is to extract '
        'behavioral specifications from web applications.\n\n'
        'When a user asks you to extract a UI:\n'
        '1. Confirm the target URL and application name\n'
        '2. Ask if authentication is required\n'
        '3. If login needed, request: login URL, username, and password\n'
        '4. Use the extract_ui_tool to perform the extraction\n'
        '5. Inform the user where the output is saved\n\n'
        'The extracted specifications focus on behaviors and interactions, '
        'not visual styling.'
    ),
    tools=[extract_ui_tool],
)


def create_extraction_config(
    base_url: str,
    app_name: str,
    login_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    username_selector: Optional[str] = None,
    password_selector: Optional[str] = None,
    submit_selector: Optional[str] = None,
    max_pages: int = 50,
    output_dir: Optional[str] = None,
    dynamic_content_wait: int = 0
) -> Dict[str, Any]:
    """Create configuration dictionary for UI extraction.
    
    This helper function constructs a configuration dictionary with all
    necessary parameters for running a UI extraction job.
    
    Args:
        base_url: Starting URL for crawl.
        app_name: Application name for output folder.
        login_url: Login page URL (optional).
        username: Authentication username (optional).
        password: Authentication password (optional).
        username_selector: CSS selector for username field (optional).
        password_selector: CSS selector for password field (optional).
        submit_selector: CSS selector for submit button (optional).
        max_pages: Maximum pages to crawl (default: 50).
        output_dir: Custom output directory (optional).
        dynamic_content_wait: Additional wait time in seconds for dynamic content
            like KPIs, charts, or async loaded components (default: 0).
    
    Returns:
        Configuration dictionary ready for extract_ui_specifications().
        
    Example:
        config = create_extraction_config(
            base_url="https://example.com/app",
            app_name="ExampleApp",
            login_url="https://example.com/login",
            username="demo@example.com",
            password="demo123",
            max_pages=30,
            dynamic_content_wait=15  # Wait 15 seconds for KPIs to load
        )
    """
    config = {
        'base_url': base_url,
        'app_name': app_name,
        'max_pages': max_pages,
        'dynamic_content_wait': dynamic_content_wait
    }
    
    if login_url:
        config['login_config'] = {
            'url': login_url,
            'username': username,
            'password': password
        }
        if username_selector:
            config['login_config']['username_selector'] = username_selector
        if password_selector:
            config['login_config']['password_selector'] = password_selector
        if submit_selector:
            config['login_config']['submit_selector'] = submit_selector
    
    if output_dir:
        config['output_dir'] = output_dir

    return config


async def extract_ui_specifications(config: Dict[str, Any]) -> str:
    """Execute UI extraction with provided configuration.
    
    This is the main entry point for running a configured extraction job.
    It orchestrates the browser automation, crawling, and specification
    generation process.
    
    Args:
        config: Configuration dictionary from create_extraction_config().
    
    Returns:
        Absolute path to extraction output directory as string.
        
    Raises:
        Exception: If extraction fails (with detailed error message).
        
    Example:
        config = create_extraction_config(
            base_url="https://example.com",
            app_name="Example",
            max_pages=10
        )
        output_path = await extract_ui_specifications(config)
        print(f"Results saved to: {output_path}")
    """
    extractor = UIExtractor(output_dir=config.get('output_dir'))
    
    print(f"\n🚀 Starting UI extraction for: {config['app_name']}")
    print(f"   Base URL: {config['base_url']}")
    if 'login_config' in config:
        print(f"   Login: Enabled")
    print(f"   Max pages: {config['max_pages']}\n")
    
    # Crawl and extract
    pages = await extractor.crawl_application(
        base_url=config['base_url'],
        login_config=config.get('login_config'),
        max_pages=config['max_pages'],
        dynamic_content_wait=config.get('dynamic_content_wait', 0)
    )
    
    # Save specifications
    output_path = extractor.save_specifications(config['app_name'])
    
    print(f"\n✅ Extraction complete! Processed {len(pages)} pages")
    return output_path
