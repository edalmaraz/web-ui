"""
Example custom functions to demonstrate implementation
"""

from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from .function_registry import registry


@registry.register("Take Screenshot", requires_browser=True)
async def take_screenshot(browser: BrowserContext, filename: str):
    """
    Take a screenshot of the current page

    Args:
        browser: Browser context
        filename: Name of the file to save

    Returns:
        ActionResult with the path to the saved screenshot
    """
    page = await browser.get_current_page()
    await page.screenshot(path=filename)
    return ActionResult(extracted_content=f"Screenshot saved as {filename}")


@registry.register("Get Page Title", requires_browser=True)
async def get_page_title(browser: BrowserContext):
    """
    Get the title of the current page

    Returns:
        ActionResult with the page title
    """
    page = await browser.get_current_page()
    title = await page.title()
    return ActionResult(extracted_content=title)


@registry.register("Calculate Sum")
def calculate_sum(numbers: list[float]) -> ActionResult:
    """
    Calculate the sum of a list of numbers

    Args:
        numbers: List of numbers to sum

    Returns:
        ActionResult with the sum
    """
    total = sum(numbers)
    return ActionResult(extracted_content=str(total))
