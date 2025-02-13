"""
Advanced custom functions including function management
"""
import os
import json
import inspect
from datetime import datetime
from typing import Optional, Dict, Any
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from .function_registry import registry

@registry.register("Save New Function")
def save_new_function(
    function_name: str,
    parameters: Dict[str, str],
    description: str,
    code: str,
    requires_browser: bool = False,
    file_name: Optional[str] = None
) -> ActionResult:
    """
    Save a new function to the custom_functions directory
    
    Args:
        function_name: Name of the function
        parameters: Dictionary of parameter names and their types
        description: Function description
        code: Function implementation code
        requires_browser: Whether the function requires browser access
        file_name: Optional custom file name (without .py)
    
    Returns:
        ActionResult with the path to the saved function
    """
    # Generate file name if not provided
    if not file_name:
        file_name = f"custom_function_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    file_path = os.path.join(os.path.dirname(__file__), f"{file_name}.py")
    
    # Generate parameter string
    param_str = ", ".join([f"{name}: {type_}" for name, type_ in parameters.items()])
    if requires_browser:
        param_str = f"browser: BrowserContext, {param_str}"
    
    # Create function template
    function_template = f'''"""
{description}
"""
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from .function_registry import registry

@registry.register("{function_name}", requires_browser={requires_browser})
async def {function_name.lower().replace(" ", "_")}({param_str}):
    """{description}"""
    {code}
'''
    
    # Save the function
    with open(file_path, 'w') as f:
        f.write(function_template)
    
    return ActionResult(extracted_content=f"Function saved to {file_path}")

@registry.register("Extract Table Data", requires_browser=True)
async def extract_table_data(browser: BrowserContext, table_selector: str) -> ActionResult:
    """
    Extract data from a table on the webpage
    """
    page = await browser.get_current_page()
    table_data = await page.evaluate(f'''
        () => {{
            const table = document.querySelector('{table_selector}');
            if (!table) return [];
            
            const rows = Array.from(table.rows);
            return rows.map(row => 
                Array.from(row.cells).map(cell => cell.innerText)
            );
        }}
    ''')
    return ActionResult(extracted_content=json.dumps(table_data))

@registry.register("Save Page as PDF", requires_browser=True)
async def save_page_as_pdf(browser: BrowserContext, file_path: str) -> ActionResult:
    """
    Save the current page as a PDF file
    """
    page = await browser.get_current_page()
    await page.pdf(path=file_path)
    return ActionResult(extracted_content=f"PDF saved to {file_path}")

@registry.register("Get Element Styles", requires_browser=True)
async def get_element_styles(browser: BrowserContext, selector: str) -> ActionResult:
    """
    Get computed styles of an element
    """
    page = await browser.get_current_page()
    styles = await page.evaluate(f'''
        () => {{
            const element = document.querySelector('{selector}');
            if (!element) return {{}};
            return window.getComputedStyle(element);
        }}
    ''')
    return ActionResult(extracted_content=json.dumps(styles))

@registry.register("Execute Custom JavaScript", requires_browser=True)
async def execute_custom_javascript(browser: BrowserContext, script: str) -> ActionResult:
    """
    Execute custom JavaScript code on the page
    """
    page = await browser.get_current_page()
    result = await page.evaluate(script)
    return ActionResult(extracted_content=str(result))

@registry.register("Wait For Network Idle", requires_browser=True)
async def wait_for_network_idle(browser: BrowserContext, timeout: int = 5000) -> ActionResult:
    """
    Wait for network activity to be idle
    """
    page = await browser.get_current_page()
    await page.wait_for_load_state("networkidle", timeout=timeout)
    return ActionResult(extracted_content="Network is idle")

@registry.register("Get Page Performance Metrics", requires_browser=True)
async def get_page_performance_metrics(browser: BrowserContext) -> ActionResult:
    """
    Get performance metrics of the current page
    """
    page = await browser.get_current_page()
    metrics = await page.evaluate('''
        () => {
            const timing = window.performance.timing;
            const metrics = {
                loadTime: timing.loadEventEnd - timing.navigationStart,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                firstPaint: timing.responseStart - timing.navigationStart,
                dns: timing.domainLookupEnd - timing.domainLookupStart,
                tcp: timing.connectEnd - timing.connectStart,
                ttfb: timing.responseStart - timing.requestStart
            };
            return metrics;
        }
    ''')
    return ActionResult(extracted_content=json.dumps(metrics))

@registry.register("Monitor Network Requests", requires_browser=True)
async def monitor_network_requests(browser: BrowserContext, url_pattern: Optional[str] = None) -> ActionResult:
    """
    Monitor network requests matching an optional pattern
    """
    page = await browser.get_current_page()
    requests = []
    
    def handle_request(request):
        if url_pattern is None or url_pattern in request.url:
            requests.append({
                'url': request.url,
                'method': request.method,
                'headers': request.headers
            })
    
    page.on('request', handle_request)
    await page.wait_for_timeout(5000)  # Monitor for 5 seconds
    page.remove_listener('request', handle_request)
    
    return ActionResult(extracted_content=json.dumps(requests))

@registry.register("Get Form Fields", requires_browser=True)
async def get_form_fields(browser: BrowserContext, form_selector: str) -> ActionResult:
    """
    Get all form fields and their properties
    """
    page = await browser.get_current_page()
    fields = await page.evaluate(f'''
        () => {{
            const form = document.querySelector('{form_selector}');
            if (!form) return [];
            
            return Array.from(form.elements).map(element => ({{
                name: element.name,
                type: element.type,
                value: element.value,
                required: element.required,
                disabled: element.disabled
            }}));
        }}
    ''')
    return ActionResult(extracted_content=json.dumps(fields))

@registry.register("Check Accessibility", requires_browser=True)
async def check_accessibility(browser: BrowserContext) -> ActionResult:
    """
    Perform basic accessibility checks on the page
    """
    page = await browser.get_current_page()
    issues = await page.evaluate('''
        () => {
            const issues = [];
            
            // Check for images without alt text
            document.querySelectorAll('img').forEach(img => {
                if (!img.alt) {
                    issues.push(`Image missing alt text: ${img.src}`);
                }
            });
            
            // Check for empty links
            document.querySelectorAll('a').forEach(link => {
                if (!link.textContent.trim() && !link.querySelector('img')) {
                    issues.push(`Empty link found: ${link.href}`);
                }
            });
            
            // Check for proper heading structure
            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
            for (let i = 0; i < headings.length - 1; i++) {
                const current = parseInt(headings[i].tagName[1]);
                const next = parseInt(headings[i + 1].tagName[1]);
                if (next > current + 1) {
                    issues.push(`Heading level skipped from ${current} to ${next}`);
                }
            });
            
            return issues;
        }
    ''')
    return ActionResult(extracted_content=json.dumps(issues))
