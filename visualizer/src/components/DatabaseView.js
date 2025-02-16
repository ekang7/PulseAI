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
  TextField,
  Box,
} from "@mui/material";
import { Link } from "react-router-dom";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import SearchIcon from "@mui/icons-material/Search";
import {
  getAllDocuments,
  deleteDocument,
  queryDocuments as queryDocsService,
} from "../services/dbService";

export default function DatabaseView() {
  const [docs, setDocs] = useState({ ids: [], documents: [], metadatas: [] });
  const [searchResults, setSearchResults] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [openModal, setOpenModal] = useState(false);
  const [selectedId, setSelectedId] = useState(null);
  const [openClearModal, setOpenClearModal] = useState(false);

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
      if (searchResults) {
        // Remove the deleted document from the search results
        const index = searchResults.ids.indexOf(selectedId);
        if (index !== -1) {
          const newResults = {
            ids: [...searchResults.ids],
            documents: [...searchResults.documents],
            metadatas: [...searchResults.metadatas],
          };
          newResults.ids.splice(index, 1);
          newResults.documents.splice(index, 1);
          newResults.metadatas.splice(index, 1);
          setSearchResults(newResults);
        }
      } else {
        fetchDocuments();
      }
    } catch (err) {
      console.error("Error deleting document:", err);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    try {
      const response = await queryDocsService(searchQuery);
      setSearchResults(response);
    } catch (err) {
      console.error("Error searching documents:", err);
    }
  };

  const handleClearSearch = () => {
    setSearchQuery("");
    setSearchResults(null);
    fetchDocuments();
  };

  // Handler to open the clear database confirmation modal
  const handleOpenClearModal = () => {
    setOpenClearModal(true);
  };

  const handleCloseClearModal = () => {
    setOpenClearModal(false);
  };

  // Handler to clear the entire database
  const handleConfirmClearDatabase = async () => {
    try {
      // Loop over all document IDs in the main docs state
      for (const id of docs.ids) {
        await deleteDocument(id);
      }
      handleCloseClearModal();
      // Clear searchResults as well if they exist, then re-fetch the documents.
      setSearchResults(null);
      fetchDocuments();
    } catch (err) {
      console.error("Error clearing the database:", err);
    }
  };

  // Use search results if available; otherwise, use all documents.
  const documentsToDisplay = searchResults || docs;

  return (
    <div>
      <Typography
        variant="h4"
        gutterBottom
        sx={{
          textAlign: "center",
          marginTop: "20px",
          fontFamily: "Arial",
          fontSize: "5rem",
          fontWeight: "bold",
        }}
      >
        ChromaDB View
      </Typography>

      {/* Search Bar */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          my: 2,
        }}
      >
        <TextField
          label="Search Documents"
          variant="outlined"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSearch();
            }
          }}
          sx={{ width: "60%", mr: 2 }}
        />
        <Button
          variant="contained"
          onClick={handleSearch}
          startIcon={<SearchIcon />}
        >
          Search
        </Button>
        {searchResults && (
          <Button
            variant="outlined"
            onClick={handleClearSearch}
            sx={{ ml: 2 }}
          >
            Clear Search
          </Button>
        )}
      </Box>

      {/* Clear Database Button */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          my: 2,
        }}
      >
        <Button
          variant="outlined"
          color="error"
          onClick={handleOpenClearModal}
        >
          Clear Database
        </Button>
      </Box>

      {searchResults && (
        <Typography variant="h5" gutterBottom sx={{ textAlign: "center", mt: 2 }}>
          Search Results
        </Typography>
      )}

      <Grid container spacing={3}>
        {documentsToDisplay?.ids?.map((id, idx) => (
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
                  {documentsToDisplay.metadatas[idx]?.title ||
                    documentsToDisplay.metadatas[idx]?.topic ||
                    "Untitled Document"}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ my: 1 }}>
                  {documentsToDisplay.documents[idx]?.slice(0, 100)}...
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

      {/* Confirm Delete Modal for Individual Document */}
      <Dialog open={openModal} onClose={handleModalClose}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the document{" "}
            <strong>
              {
                documentsToDisplay.metadatas[
                  documentsToDisplay.ids.indexOf(selectedId)
                ]?.title || selectedId
              }
            </strong>
            ? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleModalClose} variant="outlined">
            Cancel
          </Button>
          <Button onClick={handleConfirmDelete} variant="contained" color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Confirm Clear Database Modal */}
      <Dialog open={openClearModal} onClose={handleCloseClearModal}>
        <DialogTitle>Confirm Clear Database</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to clear the entire database? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseClearModal} variant="outlined">
            Cancel
          </Button>
          <Button onClick={handleConfirmClearDatabase} variant="contained" color="error">
            Clear Database
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
