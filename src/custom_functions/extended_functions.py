"""
Extended functions including OCR, image processing, and advanced utilities
"""

import os
import cv2
import json
import numpy as np
import pytesseract
from PIL import Image
import requests
from io import BytesIO
from typing import Optional, List, Dict, Any, Union
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from .function_registry import registry


@registry.register("Perform OCR", requires_browser=True)
async def perform_ocr(
    browser: BrowserContext, selector: Optional[str] = None, lang: str = "eng"
) -> ActionResult:
    """
    Perform OCR on either a specific element or the entire page

    Args:
        browser: Browser context
        selector: Optional CSS selector for specific element
        lang: Language for OCR (default: eng)

    Returns:
        ActionResult with extracted text
    """
    page = await browser.get_current_page()

    if selector:
        # Capture specific element
        element = await page.query_selector(selector)
        if not element:
            return ActionResult(extracted_content="Element not found")
        screenshot = await element.screenshot()
    else:
        # Capture entire page
        screenshot = await page.screenshot()

    # Convert bytes to PIL Image
    image = Image.open(BytesIO(screenshot))

    # Perform OCR
    text = pytesseract.image_to_string(image, lang=lang)

    return ActionResult(extracted_content=text)


@registry.register("Extract Text with Layout")
async def extract_text_with_layout(image_path: str) -> ActionResult:
    """
    Extract text while preserving layout information

    Args:
        image_path: Path to the image file

    Returns:
        ActionResult with text and layout information
    """
    data = pytesseract.image_to_data(
        Image.open(image_path), output_type=pytesseract.Output.DICT
    )

    # Combine the data into a structured format
    result = []
    for i in range(len(data["text"])):
        if data["text"][i].strip():
            result.append(
                {
                    "text": data["text"][i],
                    "left": data["left"][i],
                    "top": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i],
                    "conf": data["conf"][i],
                }
            )

    return ActionResult(extracted_content=json.dumps(result))


@registry.register("Extract Tables from Image")
async def extract_tables_from_image(image_path: str) -> ActionResult:
    """
    Extract tables from an image using OpenCV

    Args:
        image_path: Path to the image file

    Returns:
        ActionResult with table data
    """
    # Read image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect lines
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10
    )

    # Process lines to find table structure
    horizontal_lines = []
    vertical_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y2 - y1) < 10:  # Horizontal line
                horizontal_lines.append((x1, y1, x2, y2))
            elif abs(x2 - x1) < 10:  # Vertical line
                vertical_lines.append((x1, y1, x2, y2))

    # Extract text from cells
    result = []
    if horizontal_lines and vertical_lines:
        # Sort lines
        horizontal_lines.sort(key=lambda x: x[1])
        vertical_lines.sort(key=lambda x: x[0])

        # Extract text from each cell
        for i in range(len(horizontal_lines) - 1):
            row = []
            for j in range(len(vertical_lines) - 1):
                top = horizontal_lines[i][1]
                bottom = horizontal_lines[i + 1][1]
                left = vertical_lines[j][0]
                right = vertical_lines[j + 1][0]

                # Extract cell image
                cell = gray[top:bottom, left:right]
                text = pytesseract.image_to_string(cell).strip()
                row.append(text)
            if row:
                result.append(row)

    return ActionResult(extracted_content=json.dumps(result))


@registry.register("Image to Text with GPT Vision", requires_browser=True)
async def image_to_text_with_gpt_vision(
    browser: BrowserContext,
    openai_api_key: str,
    selector: Optional[str] = None,
    prompt: str = "What's in this image?",
) -> ActionResult:
    """
    Use GPT-4 Vision to analyze images

    Args:
        browser: Browser context
        openai_api_key: OpenAI API key
        selector: Optional CSS selector for specific element
        prompt: Prompt for GPT-4 Vision

    Returns:
        ActionResult with GPT-4's analysis
    """
    import base64
    from openai import OpenAI

    page = await browser.get_current_page()

    if selector:
        element = await page.query_selector(selector)
        if not element:
            return ActionResult(extracted_content="Element not found")
        screenshot = await element.screenshot()
    else:
        screenshot = await page.screenshot()

    # Convert screenshot to base64
    base64_image = base64.b64encode(screenshot).decode("utf-8")

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Call GPT-4 Vision
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return ActionResult(extracted_content=response.choices[0].message.content)


@registry.register("Extract QR Codes", requires_browser=True)
async def extract_qr_codes(
    browser: BrowserContext, selector: Optional[str] = None
) -> ActionResult:
    """
    Extract QR codes from the page or specific element

    Args:
        browser: Browser context
        selector: Optional CSS selector for specific element

    Returns:
        ActionResult with QR code contents
    """
    import cv2
    from pyzbar.pyzbar import decode
    import numpy as np

    page = await browser.get_current_page()

    if selector:
        element = await page.query_selector(selector)
        if not element:
            return ActionResult(extracted_content="Element not found")
        screenshot = await element.screenshot()
    else:
        screenshot = await page.screenshot()

    # Convert bytes to numpy array
    nparr = np.frombuffer(screenshot, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Decode QR codes
    decoded_objects = decode(img)

    # Extract results
    results = []
    for obj in decoded_objects:
        results.append(
            {
                "type": obj.type,
                "data": obj.data.decode("utf-8"),
                "rect": {
                    "left": obj.rect.left,
                    "top": obj.rect.top,
                    "width": obj.rect.width,
                    "height": obj.rect.height,
                },
            }
        )

    return ActionResult(extracted_content=json.dumps(results))


@registry.register("Extract Charts and Graphs", requires_browser=True)
async def extract_charts_and_graphs(
    browser: BrowserContext, selector: Optional[str] = None
) -> ActionResult:
    """
    Detect and analyze charts and graphs in the page

    Args:
        browser: Browser context
        selector: Optional CSS selector for specific element

    Returns:
        ActionResult with chart analysis
    """
    import cv2
    import numpy as np
    from PIL import Image
    from io import BytesIO

    page = await browser.get_current_page()

    if selector:
        element = await page.query_selector(selector)
        if not element:
            return ActionResult(extracted_content="Element not found")
        screenshot = await element.screenshot()
    else:
        screenshot = await page.screenshot()

    # Convert bytes to numpy array
    nparr = np.frombuffer(screenshot, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze potential charts
    charts = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Filter small contours
            x, y, w, h = cv2.boundingRect(contour)
            roi = img[y : y + h, x : x + w]

            # Analyze colors in ROI
            unique_colors = len(np.unique(roi.reshape(-1, 3), axis=0))

            # Basic chart type detection
            if unique_colors > 10:  # Likely a chart if many colors
                charts.append(
                    {
                        "type": "unknown",
                        "position": {"x": x, "y": y, "width": w, "height": h},
                        "colors": unique_colors,
                    }
                )

    return ActionResult(extracted_content=json.dumps(charts))


@registry.register("Extract Color Palette", requires_browser=True)
async def extract_color_palette(
    browser: BrowserContext, selector: Optional[str] = None, num_colors: int = 5
) -> ActionResult:
    """
    Extract dominant colors from the page or element

    Args:
        browser: Browser context
        selector: Optional CSS selector for specific element
        num_colors: Number of colors to extract

    Returns:
        ActionResult with color palette
    """
    from sklearn.cluster import KMeans
    import numpy as np
    from PIL import Image
    from io import BytesIO

    page = await browser.get_current_page()

    if selector:
        element = await page.query_selector(selector)
        if not element:
            return ActionResult(extracted_content="Element not found")
        screenshot = await element.screenshot()
    else:
        screenshot = await page.screenshot()

    # Convert bytes to PIL Image
    image = Image.open(BytesIO(screenshot))

    # Convert image to numpy array
    img_array = np.array(image)

    # Reshape the array
    pixels = img_array.reshape(-1, 3)

    # Use k-means clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Convert colors to hex
    colors = []
    for color in kmeans.cluster_centers_:
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(color[0]), int(color[1]), int(color[2])
        )
        colors.append(hex_color)

    return ActionResult(extracted_content=json.dumps(colors))


@registry.register("Extract Faces", requires_browser=True)
async def extract_faces(
    browser: BrowserContext, selector: Optional[str] = None, min_confidence: float = 0.5
) -> ActionResult:
    """
    Detect and extract faces from the page or element

    Args:
        browser: Browser context
        selector: Optional CSS selector for specific element
        min_confidence: Minimum confidence threshold

    Returns:
        ActionResult with face detection results
    """
    import cv2
    import numpy as np

    # Load face detection model
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    page = await browser.get_current_page()

    if selector:
        element = await page.query_selector(selector)
        if not element:
            return ActionResult(extracted_content="Element not found")
        screenshot = await element.screenshot()
    else:
        screenshot = await page.screenshot()

    # Convert bytes to numpy array
    nparr = np.frombuffer(screenshot, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Process results
    results = []
    for x, y, w, h in faces:
        results.append(
            {"position": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)}}
        )

    return ActionResult(extracted_content=json.dumps(results))


@registry.register("Extract Text from PDF")
async def extract_text_from_pdf(pdf_path: str) -> ActionResult:
    """
    Extract text content from a PDF file

    Args:
        pdf_path: Path to the PDF file

    Returns:
        ActionResult with extracted text
    """
    import PyPDF2

    text = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            text.append(page.extract_text())

    return ActionResult(extracted_content="\n\n".join(text))


@registry.register("Convert Speech to Text", requires_browser=True)
async def convert_speech_to_text(
    browser: BrowserContext, audio_selector: str, language: str = "en-US"
) -> ActionResult:
    """
    Convert speech from an audio element to text

    Args:
        browser: Browser context
        audio_selector: CSS selector for audio element
        language: Language code

    Returns:
        ActionResult with transcribed text
    """
    import speech_recognition as sr
    from pydub import AudioSegment
    import tempfile

    page = await browser.get_current_page()

    # Get audio element
    audio_element = await page.query_selector(audio_selector)
    if not audio_element:
        return ActionResult(extracted_content="Audio element not found")

    # Get audio source
    src = await audio_element.get_attribute("src")
    if not src:
        return ActionResult(extracted_content="No audio source found")

    # Download audio file
    response = requests.get(src)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_path = temp_file.name

    try:
        # Convert to WAV if needed
        audio = AudioSegment.from_file(temp_path)
        audio.export(temp_path, format="wav")

        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Load audio file
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)

            # Perform speech recognition
            text = recognizer.recognize_google(audio_data, language=language)

        return ActionResult(extracted_content=text)

    finally:
        # Clean up temporary file
        os.remove(temp_path)
