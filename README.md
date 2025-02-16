# PulseAI: AI-Powered Screenshot Analysis Tool

PulseAI is a powerful screenshot capture and analysis system that combines OCR, image understanding, and vector search capabilities to help you organize and retrieve information from your screenshots.

## Features

- **Screenshot Capture**: Chrome extension for easy screenshot capture
- **Text Extraction**: OCR using Tesseract for extracting text from images
- **Image Understanding**: AI-powered image description using Pixtral
- **Vector Search**: Semantic search through screenshots using ChromaDB
- **MCP Integration**: Seamless integration with Codeium's MCP framework

## Components

### Backend (`/backend`)

- `main.py`: FastAPI server handling screenshot uploads and processing
- `mistral_client.py`: Mistral AI integration for text and image analysis
- `db/vector_store.py`: ChromaDB wrapper for vector storage and retrieval
- `view_screenshots.py`: Utility script to view stored screenshots

### Chrome Extension (`/chrome_extension`)

- Captures screenshots of web pages
- Sends screenshots to backend with metadata
- Endpoint: `http://127.0.0.1:8000/api/upload`

### MCP Tool (`/mcp_tool`)

- `server.py`: MCP server for context retrieval
- Implements RAG pipeline for intelligent responses

## Setup

1. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Install system dependencies:
```bash
brew install tesseract
```

3. Set environment variables:
```bash
export MISTRAL_API_KEY=your_api_key
export PYTHONPATH=/path/to/PulseAI
```

## Usage

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Install the Chrome extension:
   - Open Chrome
   - Go to `chrome://extensions`
   - Enable Developer mode
   - Load unpacked extension from `chrome_extension` directory

3. Take screenshots:
   - Click the extension icon
   - Select area to capture
   - Screenshot will be processed and stored

4. View stored screenshots:
```bash
cd backend
python view_screenshots.py
```

## Architecture

### Screenshot Processing Pipeline

1. **Capture**: Chrome extension captures screenshot and metadata
2. **Storage**: Image saved to `backend/screenshots` directory
3. **Processing**:
   - OCR extracts text using Tesseract
   - Pixtral generates detailed image description
4. **Indexing**:
   - Combined data stored in ChromaDB
   - Each screenshot gets unique timestamp-based ID
   - Metadata includes URL, title, and timestamps

### Vector Database

- Uses ChromaDB for persistent storage
- Stores combined text, descriptions, and metadata
- Enables semantic search across screenshots
- Located in `backend/chroma_db`

## Development Notes

### Current Status
- Screenshot capture and storage
- OCR text extraction
- AI image description
- Vector database integration
- Basic search functionality

## License

This project is licensed under the MIT License. See LICENSE file for details.
