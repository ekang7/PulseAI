from fastapi import FastAPI, Request
from pydantic import BaseModel
import base64
import re
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your extension's ID/origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ScreenshotPayload(BaseModel):
    screenshot: str  # data URL (e.g., "data:image/png;base64,iVBORw0KGgoAAAANS...")
    pageUrl: str
    pageTitle: str

@app.post("/api/upload")
async def upload_screenshot(payload: ScreenshotPayload):
    """
    Receives a base64-encoded PNG from the Chrome Extension, plus the page title and URL.
    Decodes and saves the image locally, and returns a success response.
    """

    # The 'screenshot' is a data URL: "data:image/png;base64,<BASE64_DATA>"
    # We only want the base64 data after the comma
    try:
        # Split on the first comma to separate "data:image/png;base64" from the actual base64
        header, encoded = payload.screenshot.split(",", 1)
    except ValueError:
        return {"error": "Invalid screenshot data format"}

    # Decode the base64 data into raw bytes
    try:
        image_bytes = base64.b64decode(encoded)
    except Exception as e:
        return {"error": f"Failed to decode base64: {str(e)}"}

    # Generate a timestamped filename for the screenshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    
    # Save the screenshot to the screenshots directory
    filepath = os.path.join("screenshots", filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # Log or otherwise process the page URL/title as needed
    print(f"Received screenshot from page: {payload.pageUrl}")
    print(f"Page title: {payload.pageTitle}")
    print(f"Saved file: {filepath}")

    return {"message": "Screenshot received successfully", "filename": filename}
