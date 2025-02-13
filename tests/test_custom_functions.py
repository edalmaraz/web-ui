"""
Test suite for custom functions
"""
import os
import json
import pytest
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from src.custom_functions.function_registry import registry
from src.custom_functions.example_functions import *
from src.custom_functions.advanced_functions import *

# Setup test HTML content
TEST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Test Page</h1>
    <table id="test-table">
        <tr><td>1</td><td>2</td></tr>
        <tr><td>3</td><td>4</td></tr>
    </table>
    <form id="test-form">
        <input type="text" name="username" required>
        <input type="password" name="password">
    </form>
    <img src="test.jpg">
    <a href="#"></a>
</body>
</html>
"""

@pytest.fixture
async def browser_context():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_content(TEST_HTML)
        yield BrowserContext(context=context, page=page)
        await browser.close()

@pytest.mark.asyncio
async def test_save_new_function():
    """Test saving a new function"""
    result = await registry.get_function("Save New Function")(
        function_name="Test Function",
        parameters={"param1": "str", "param2": "int"},
        description="Test function description",
        code="return ActionResult(extracted_content='test')",
        requires_browser=False
    )
    
    # Check if file was created
    assert "Function saved to" in result.extracted_content
    
    # Check if file exists and has correct content
    file_path = result.extracted_content.split("saved to ")[-1]
    assert os.path.exists(file_path)
    
    # Clean up
    os.remove(file_path)

@pytest.mark.asyncio
async def test_extract_table_data(browser_context):
    """Test table data extraction"""
    result = await registry.get_function("Extract Table Data")(
        browser_context,
        "#test-table"
    )
    data = json.loads(result.extracted_content)
    assert len(data) == 2
    assert data[0][0] == "1"

@pytest.mark.asyncio
async def test_get_form_fields(browser_context):
    """Test form fields extraction"""
    result = await registry.get_function("Get Form Fields")(
        browser_context,
        "#test-form"
    )
    fields = json.loads(result.extracted_content)
    assert len(fields) == 2
    assert fields[0]["name"] == "username"
    assert fields[0]["required"] == True

@pytest.mark.asyncio
async def test_check_accessibility(browser_context):
    """Test accessibility checks"""
    result = await registry.get_function("Check Accessibility")(browser_context)
    issues = json.loads(result.extracted_content)
    assert len(issues) > 0  # Should find issues in our test HTML

@pytest.mark.asyncio
async def test_get_page_title(browser_context):
    """Test getting page title"""
    result = await registry.get_function("Get Page Title")(browser_context)
    assert result.extracted_content == "Test Page"

@pytest.mark.asyncio
async def test_calculate_sum():
    """Test sum calculation"""
    result = await registry.get_function("Calculate Sum")([1, 2, 3, 4, 5])
    assert result.extracted_content == "15"

def test_function_registry():
    """Test function registry functionality"""
    functions = registry.list_functions()
    assert len(functions) > 0
    assert "Save New Function" in functions
    assert "Calculate Sum" in functions

class TestNewFunctionValidator:
    """Validator for new functions added to the custom_functions directory"""
    
    @staticmethod
    def validate_function(func_name: str, func) -> list[str]:
        """Validate a single function"""
        errors = []
        
        # Check if function has docstring
        if not func.__doc__:
            errors.append(f"Function {func_name} missing docstring")
        
        # Check if function returns ActionResult
        if 'return ActionResult' not in inspect.getsource(func):
            errors.append(f"Function {func_name} must return ActionResult")
        
        # Check if parameters have type hints
        sig = inspect.signature(func)
        for param_name, param in sig.parameters.items():
            if param.annotation == inspect.Parameter.empty:
                errors.append(f"Parameter {param_name} in {func_name} missing type hint")
        
        return errors

    @staticmethod
    def validate_all_functions() -> dict:
        """Validate all functions in the registry"""
        validation_results = {}
        for func_name, func in registry.functions.items():
            errors = TestNewFunctionValidator.validate_function(func_name, func)
            if errors:
                validation_results[func_name] = errors
        return validation_results

def test_validate_all_functions():
    """Test that all functions meet the requirements"""
    validation_results = TestNewFunctionValidator.validate_all_functions()
    assert len(validation_results) == 0, f"Function validation failed: {json.dumps(validation_results, indent=2)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
