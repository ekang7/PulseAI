import axios from "axios";

// Adjust the base URL to your actual backend (localhost:8000 or your deployed URL)
const BASE_URL = "http://127.0.0.1:8000/api";

export async function getAllDocuments() {
  const response = await axios.get(`${BASE_URL}/list_all_documents`);
  return response.data; 
}

// If you want to store an "update document" feature, you'll need a dedicated endpoint in your backend:
export async function updateDocument(docId, content, metadata) {
  // This is a custom endpoint you might create, e.g. /api/update_document
  // Not provided in your original code, so you'd have to implement it in main.py
  return axios.post(`${BASE_URL}/update_document`, {
    id: docId,
    content,
    metadata
  });
}
