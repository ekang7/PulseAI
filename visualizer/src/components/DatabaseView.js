import React, { useEffect, useState } from "react";
import { getAllDocuments } from "../services/dbService";
import {
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Stack,
} from "@mui/material";
import { Link } from "react-router-dom";

export default function DatabaseView() {
  const [docs, setDocs] = useState([]);

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

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Database View
      </Typography>

      <Grid container spacing={2}>
        {docs?.ids?.map((id, idx) => (
          <Grid item xs={12} md={6} lg={4} key={id}>
            <Card>
              <CardContent>
                <Typography variant="h6">ID: {id}</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {docs.documents[idx]?.slice(0, 100)}...
                </Typography>
                <Stack direction="row" spacing={2}>
                  <Button
                    variant="contained"
                    component={Link}
                    to={`/edit/${id}`}
                  >
                    Edit
                  </Button>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  );
}
