# PulseAI: Browser-Based Coding Assistant Tool

PulseAI is a tool that enhances your AI coding assistant experience by providing your assistant with information about your (voluntarily captured) browser activity. By providing your assistant with a better understanding of your work, you'll be able to work with an agent that provides targeted suggestions and aid.

## Features

- **Screenshot Capture**: A Chrome extension captures your browser screen and sends it to your PulseAI backend for processing.
- **Autonomous Search**: Perplexity and Mistral are used to browse the web for related topics, fetching real-time information that may be relevant.
- **Vector Search**: All of the retrieved search information is stored using ChromaDB, enabling semantic searches that retrieve relevant content quickly.
- **MCP Integration**: Seamless integration with Codeium's Windsurf/Cascade MCP framework.

## Components

### Backend (`/backend`)

The backend of PulseAI is built using FastAPI. It handles the processing of screenshots, the autonomous searches, and vector database / RAG.

### Chrome Extension (`/chrome_extension`)

The Chrome extension used to capture screenshots when allowed. It sends these to the backend.

### MCP Tool (`/mcp_tool`)

The MCP tool that is used by Cascade to retrieve relevant context in real-time.
