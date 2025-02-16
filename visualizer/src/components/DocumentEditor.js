import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getAllDocuments, updateDocument } from "../services/dbService";
import {
  Typography,
  TextField,
  Button,
  Stack,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from "@mui/material";

export default function DocumentEditor() {
  const { docId } = useParams();
  const navigate = useNavigate();
  const [content, setContent] = useState("");
  const [metadata, setMetadata] = useState({});
  const [originalData, setOriginalData] = useState(null);
  const [openSuccessModal, setOpenSuccessModal] = useState(false);

  useEffect(() => {
    fetchDocument();
  }, []);

  const fetchDocument = async () => {
    try {
      // We'll fetch all docs and then find the one we need
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
      setOpenSuccessModal(true);
    } catch (err) {
      console.error("Error updating document:", err);
      // Optionally, handle errors with a modal or message here.
    }
  };

  const handleCancel = () => {
    navigate(-1); // Go back to the previous page
  };

  const handleSuccessModalClose = () => {
    setOpenSuccessModal(false);
    navigate("/"); // Navigate back to the main database view (or adjust as needed)
  };

  if (!originalData) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box sx={{ mt: 4 }}>
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
              // Ignore JSON parse errors while editing.
            }
          }}
        />
        <Stack direction="row" spacing={2}>
          <Button variant="contained" onClick={handleSave}>
            Save
          </Button>
          <Button variant="outlined" onClick={handleCancel}>
            Cancel
          </Button>
        </Stack>
      </Stack>

      {/* Custom success modal */}
      <Dialog open={openSuccessModal} onClose={handleSuccessModalClose}>
        <DialogTitle>Success</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Document updated successfully!
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSuccessModalClose} variant="contained">
            OK
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
