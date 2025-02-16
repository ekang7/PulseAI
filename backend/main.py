from fastapi import FastAPI
from pydantic import BaseModel
import base64
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import os
import io
from PIL import Image
import pytesseract
from mistralai import Mistral
from db.vector_store import add_documents, query_documents
import logging
from dotenv import load_dotenv
from clients import mistral
from typing import List, Any

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "ministral-8b-latest"

client = Mistral(api_key=MISTRAL_API_KEY)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentQueryPayload(BaseModel):
    query_text : str
    n_results : int
    collection_name : str

class CollectiveSummaryPayload(BaseModel):
    sources : List[Any]

class ScreenshotPayload(BaseModel):
    screenshot: str  # data URL (e.g., "data:image/png;base64,iVBORw0KGgoAAAANS...")
    pageUrl: str
    pageTitle: str

def extract_text_from_image(image_bytes):
    """Extract text from image using OCR"""
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text.strip()

def resize_image(image_bytes, max_size=(500, 500)):
    """Resize image while maintaining aspect ratio"""
    image = Image.open(io.BytesIO(image_bytes))
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Convert back to bytes
    output_buffer = io.BytesIO()
    # Keep as PNG to maintain quality
    image.save(output_buffer, format='PNG')
    output_buffer.seek(0)
    return output_buffer.getvalue()

def describe_image_with_pixtral(image_bytes):
    """Get image description using Pixtral model"""
    # Debug original image
    original_image = Image.open(io.BytesIO(image_bytes))
    
    # Resize image if needed
    resized_image = resize_image(image_bytes)
    
    # Convert image to base64 for Pixtral
    base64_image = base64.b64encode(resized_image).decode('utf-8')

    return mistral.get_image_description(base64_image)

@app.post("/api/query_documents")
async def query_documents_endpoint(payload: DocumentQueryPayload):
    results = query_documents(payload.query_text, payload.n_results, payload.collection_name)
    return results

@app.post("/api/collective_summary")
async def collective_summary_endpoint(payload: CollectiveSummaryPayload):
    summary = mistral.get_collective_summary(payload.sources)
    return {"summary": summary}

@app.post("/api/upload")
async def upload_screenshot(payload: ScreenshotPayload):
    """
    Receives a base64-encoded PNG from the Chrome Extension, plus the page title and URL.

    Process uploaded screenshots:
    1. Save the image
    2. Extract text using OCR
    3. Get image description using Pixtral
    4. Store in vector DB
    """

    try:
        logger.info("Processing new screenshot upload")
        # The 'screenshot' is a data URL: "data:image/png;base64,<BASE64_DATA>"
        # We only want the base64 data after the comma
        # So, split the data URL to get base64 data
        header, encoded_image = payload.screenshot.split(",", 1)
        image_bytes = base64.b64decode(encoded_image)
        logger.info(f"Decoded image bytes length: {len(image_bytes)}")
        
        # Generate timestamp and filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join("screenshots", filename)
        
        logger.info(f"Saving screenshot to {filepath}")
        # Create screenshots directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        
        # Save the screenshot
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        logger.info("Extracting text using OCR")
        # Extract text using OCR
        extracted_text = extract_text_from_image(image_bytes)
        logger.info(f"Extracted text length: {len(extracted_text)}")
        
        logger.info("Getting image description from Pixtral")
        # Get image description using Pixtral
        image_description = describe_image_with_pixtral(image_bytes)
        logger.info(f"Image description length: {len(image_description)}")
        
        # Combine all information
        document_content = f"""
        Page Title: {payload.pageTitle}
        URL: {payload.pageUrl}
        
        Image Description:
        {image_description}
        
        Extracted Text:
        {extracted_text}
        """
        logger.info(f"Combined document length: {len(document_content)}")
        
        # Store in vector DB
        logger.info("Storing in vector database")
        metadata = {
            "source": "screenshot",
            "url": payload.pageUrl,
            "title": payload.pageTitle,
            "timestamp": timestamp,
            "filename": filename
        }
        
        # Generate a unique ID using timestamp
        unique_id = f"screenshot_{timestamp}"
        logger.info(f"Using unique ID: {unique_id}")
        
        add_documents(
            documents=[document_content],
            metadata=[metadata],
            ids=[unique_id],  # Pass the unique ID
            collection_name="screenshots_collection"
        )
        logger.info("Successfully stored in vector database")
        
        return {
            "status": "success",
            "message": "Screenshot processed and stored",
            "filename": filename,
            "extracted_text": extracted_text,
            "image_description": image_description
        }
        
    except Exception as e:
        logger.error(f"Error processing screenshot: {str(e)}", exc_info=True)
        return {"status": "error", "message": str(e)}