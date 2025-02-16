import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: "#388e3c", // Darker green
        boxShadow: "0 3px 5px 2px rgba(56, 142, 60, 0.3)",
      }}
    >
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: "bold" }}>
          PulseAI Database and Log Viewer
        </Typography>
        <Button
          color="inherit"
          component={Link}
          to="/"
          sx={{ fontWeight: "bold" }}
        >
          Database
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/logs"
          sx={{ fontWeight: "bold" }}
        >
          Logs
        </Button>
      </Toolbar>
    </AppBar>
  );
}
