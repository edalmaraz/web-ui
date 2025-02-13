# Available Functions

## Quick Reference

### Basic Functions
- Calculate Sum
- Copy to Clipboard
- Get Form Fields
- Get Page Title
- Paste from Clipboard
- Take Screenshot

### Browser Navigation
- Click Element
- Go to URL
- Input Text
- Open Tab
- Send Keys
- Switch Tab
- Wait For Network Idle

### Content Extraction
- Extract Page Content
- Extract Tables from Image
- Extract Text from PDF
- Extract Text with Layout
- Get Element Styles
- Monitor Network Requests
- Perform OCR

### Media and Visual Analysis
- Check Accessibility
- Convert Speech to Text
- Extract Charts and Graphs
- Extract Color Palette
- Extract Faces
- Extract QR Codes
- Get Page Performance Metrics
- Image to Text with GPT Vision

### Development
- Execute Custom JavaScript
- Save New Function

---

## Core Browser Actions

### Navigation Actions

#### Go To URL
```python
@registry.action("Go to URL")
async def go_to_url(browser: BrowserContext, url: str):
    """Navigate to a specific URL"""
    required_params:
        - url: str (The URL to navigate to)
    returns:
        - ActionResult
```

#### Open Tab
```python
@registry.action("Open new tab")
async def open_tab(browser: BrowserContext):
    """Open a new browser tab"""
    required_params: None
    returns:
        - ActionResult
```

#### Switch Tab
```python
@registry.action("Switch tab")
async def switch_tab(browser: BrowserContext, tab_index: int):
    """Switch to a specific browser tab"""
    required_params:
        - tab_index: int (Index of the tab to switch to)
    returns:
        - ActionResult
```

### Interaction Actions

#### Click Element
```python
@registry.action("Click element")
async def click_element(browser: BrowserContext, selector: str):
    """Click an element on the page"""
    required_params:
        - selector: str (CSS or XPath selector)
    returns:
        - ActionResult
```

#### Input Text
```python
@registry.action("Input text")
async def input_text(browser: BrowserContext, selector: str, text: str):
    """Input text into a form field"""
    required_params:
        - selector: str (CSS or XPath selector)
        - text: str (Text to input)
    returns:
        - ActionResult
```

#### Send Keys
```python
@registry.action("Send keys")
async def send_keys(browser: BrowserContext, keys: str):
    """Send keyboard keys to the page"""
    required_params:
        - keys: str (Keys to send)
    returns:
        - ActionResult
```

### Content Actions

#### Extract Page Content
```python
@registry.action("Extract page content")
async def extract_page_content(browser: BrowserContext):
    """Extract content from the current page"""
    required_params: None
    returns:
        - ActionResult(extracted_content=str)
```

#### Copy to Clipboard
```python
@registry.action("Copy text to clipboard")
def copy_to_clipboard(text: str):
    """Copy text to system clipboard"""
    required_params:
        - text: str (Text to copy)
    returns:
        - ActionResult(extracted_content=str)
```

#### Paste from Clipboard
```python
@registry.action("Paste text from clipboard")
async def paste_from_clipboard(browser: BrowserContext):
    """Paste text from system clipboard"""
    required_params: None
    returns:
        - ActionResult(extracted_content=str)
```

### Page Control Actions

#### Scroll
```python
@registry.action("Scroll")
async def scroll(browser: BrowserContext, direction: str = "down"):
    """Scroll the page"""
    required_params:
        - direction: str (up/down)
    returns:
        - ActionResult
```

### Search Actions

#### Search Google
```python
@registry.action("Search Google")
async def search_google(browser: BrowserContext, query: str):
    """Perform a Google search"""
    required_params:
        - query: str (Search query)
    returns:
        - ActionResult
```

## Adding Custom Functions

### Function Template
```python
@registry.action("Your Function Name")
async def your_function_name(param1: type1, param2: type2):
    """
    Your function description
    """
    required_params:
        - param1: type1 (description)
        - param2: type2 (description)
    returns:
        - ActionResult(extracted_content=str)
```

### Implementation Requirements
1. Function must be decorated with `@registry.action`
2. Function name must be unique
3. All parameters must have type hints
4. Function must return an `ActionResult` object
5. Use `requires_browser=True` if browser access is needed
6. Make function async if it involves browser operations

### Example Custom Function
```python
@registry.action("Save Screenshot", requires_browser=True)
async def save_screenshot(browser: BrowserContext, filename: str):
    """
    Save a screenshot of the current page
    """
    required_params:
        - filename: str (Name of the file to save)
    returns:
        - ActionResult(extracted_content=f"Screenshot saved as {filename}")
