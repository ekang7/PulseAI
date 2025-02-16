import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getAllDocuments, updateDocument } from "../services/dbService";
import {
  Typography,
  TextField,
  Button,
  Stack,
  Box,
} from "@mui/material";

export default function DocumentEditor() {
  const { docId } = useParams();
  const [content, setContent] = useState("");
  const [metadata, setMetadata] = useState({});
  const [originalData, setOriginalData] = useState(null);

  useEffect(() => {
    fetchDocument();
  }, []);

  const fetchDocument = async () => {
    try {
      // We'll fetch *all* docs, then find the one we need
      const response = await getAllDocuments();
      if (!response || !response.ids) return;

      const idx = response.ids.findIndex((id) => id === docId);
      if (idx !== -1) {
        setContent(response.documents[idx]);
        setMetadata(response.metadatas[idx] || {});
        setOriginalData({
          content: response.documents[idx],
          metadata: response.metadatas[idx],
        });
      }
    } catch (err) {
      console.error("Error fetching document:", err);
    }
  };

  const handleSave = async () => {
    try {
      await updateDocument(docId, content, metadata);
      alert("Document updated successfully!");
    } catch (err) {
      console.error("Error updating document:", err);
      alert("Error updating document!");
    }
  };

  if (!originalData) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Editing Document: {docId}
      </Typography>
      <Stack spacing={2}>
        <TextField
          label="Document Content"
          multiline
          rows={10}
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <TextField
          label="Metadata (JSON)"
          multiline
          rows={6}
          value={JSON.stringify(metadata, null, 2)}
          onChange={(e) => {
            try {
              setMetadata(JSON.parse(e.target.value));
            } catch (err) {
              // ignore parse errors
            }
          }}
        />
        <Button variant="contained" onClick={handleSave}>
          Save
        </Button>
      </Stack>
    </Box>
  );
}
