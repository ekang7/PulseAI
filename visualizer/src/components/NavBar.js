import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          PulseAI Database and Log Viewer
        </Typography>
        <Button color="inherit" component={Link} to="/">
          Database
        </Button>
        <Button color="inherit" component={Link} to="/logs">
          Logs
        </Button>
      </Toolbar>
    </AppBar>
  );
}
