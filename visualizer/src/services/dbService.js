import axios from "axios";

// Adjust the base URL to your actual backend (localhost:8000 or your deployed URL)
const BASE_URL = "http://127.0.0.1:8000/api";

export async function getAllDocuments() {
  const response = await axios.get(`${BASE_URL}/list_all_documents`);
  return response.data;
}

export async function updateDocument(docId, content, metadata) {
  return axios.post(`${BASE_URL}/update_document`, {
    id: docId,
    content,
    metadata,
  });
}

export async function deleteDocument(id) {
  return axios.post(`${BASE_URL}/delete_document`, { id });
}

export async function queryDocuments(query_text) {
  const response = await axios.post(`${BASE_URL}/query_documents`, {
    query_text,
    n_results: 5,
    collection_name: "screenshots_collection",
  });
  return response.data;
}
