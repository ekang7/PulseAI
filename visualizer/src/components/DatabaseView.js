import React, { useEffect, useState } from "react";
import {
  Typography,
  Card,
  CardContent,
  Grid,
  IconButton,
  Stack,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Button,
} from "@mui/material";
import { Link } from "react-router-dom";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { getAllDocuments, deleteDocument } from "../services/dbService";

export default function DatabaseView() {
  const [docs, setDocs] = useState({ ids: [], documents: [], metadatas: [] });
  const [openModal, setOpenModal] = useState(false);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await getAllDocuments();
      setDocs(response);
    } catch (err) {
      console.error("Error fetching documents:", err);
    }
  };

  const handleDeleteClick = (id) => {
    setSelectedId(id);
    setOpenModal(true);
  };

  const handleModalClose = () => {
    setOpenModal(false);
    setSelectedId(null);
  };

  const handleConfirmDelete = async () => {
    try {
      await deleteDocument(selectedId);
      handleModalClose();
      fetchDocuments();
    } catch (err) {
      console.error("Error deleting document:", err);
    }
  };

  return (
    <div>
      <Typography
        variant="h4"
        gutterBottom
        sx={{ textAlign: "center", marginTop: "20px" }}
      >
        Database View
      </Typography>
      <Grid container spacing={3}>
        {docs?.ids?.map((id, idx) => (
          <Grid item xs={12} sm={6} md={4} key={id}>
            <Card
              sx={{
                boxShadow: 3,
                borderRadius: 2,
                transition: "transform 0.2s",
                "&:hover": { transform: "scale(1.02)" },
              }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                  {docs.metadatas[idx]?.title || "Untitled Document"}
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ my: 1 }}
                >
                  {docs.documents[idx]?.slice(0, 100)}...
                </Typography>
                <Stack direction="row" spacing={1} justifyContent="flex-end">
                  <IconButton
                    component={Link}
                    to={`/edit/${id}`}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    color="error"
                    onClick={() => handleDeleteClick(id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Confirm Delete Modal */}
      <Dialog open={openModal} onClose={handleModalClose}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the document{" "}
            <strong>{docs.metadatas[docs.ids.indexOf(selectedId)]?.title || selectedId}</strong>? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleModalClose} variant="outlined">
            Cancel
          </Button>
          <Button
            onClick={handleConfirmDelete}
            variant="contained"
            color="error"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
