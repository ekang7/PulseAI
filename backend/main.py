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
from fastapi.responses import StreamingResponse
import asyncio
import queue
from pydantic import BaseModel
from fastapi import Request


import utils

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

@app.get("/api/list_all_documents")
async def list_all_documents_endpoint():
    from db.vector_store import list_all_documents
    return list_all_documents("screenshots_collection")



class UpdateDocumentPayload(BaseModel):
    id: str
    content: str
    metadata: dict = {}

@app.post("/api/update_document")
async def update_document_endpoint(payload: UpdateDocumentPayload):
    """
    Receives an ID, new content, and metadata to update a document
    in the 'screenshots_collection' (or any other collection).
    """
    from db.vector_store import update_document 

    try:
        update_document(
            id=payload.id,
            new_content=payload.content,
            new_metadata=payload.metadata,
            collection_name="screenshots_collection"  
        )
        return {
            "status": "success",
            "message": f"Document {payload.id} updated."
        }
    except Exception as e:
        logger.error(f"Error updating document {payload.id}: {e}")
        return {
            "status": "error",
            "message": str(e)
        }



@app.post("/api/collective_summary")
async def collective_summary_endpoint(payload: CollectiveSummaryPayload):
    summary = mistral.get_collective_summary(payload.sources)
    return {"summary": summary}

def call_passive_perplexity(browser_info):
    related_topics_info = utils.browser_info_to_related_topics(browser_info)
    documents = [topic.topic_information for topic in related_topics_info.topics]
    metadata = [{"topic" : topic.name} for topic in related_topics_info.topics]
    add_documents(documents, metadata)

def call_active_perplexity(question):
    pass
    
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
    
        call_passive_perplexity(browser_info)
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





# A thread-safe queue to store log messages
log_queue = queue.Queue()

# Custom logging handler that pushes logs to our queue
class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_queue.put(log_entry)

# Add the queue handler to the root logger
queue_handler = QueueHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
queue_handler.setFormatter(formatter)
logging.getLogger().addHandler(queue_handler)

@app.get("/api/logs/stream")
async def stream_logs(request: Request):
    async def event_generator():
        while True:
            # If the client closes the connection, break
            if await request.is_disconnected():
                break

            try:
                # Try to get a log message from the queue
                message = log_queue.get(timeout=1)
                # Format it as SSE
                yield f"data: {message}\n\n"
            except queue.Empty:
                # If no message, just sleep briefly and continue
                await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

