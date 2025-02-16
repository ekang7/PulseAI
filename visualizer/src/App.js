import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/NavBar";
import DatabaseView from "./components/DatabaseView";
import LogsView from "./components/LogsView";
import DocumentEditor from "./components/DocumentEditor";
import { Container } from "@mui/material";

function App() {
  return (
    <Router>
      <Navbar />
      <Container maxWidth="lg" style={{ marginTop: "2rem" }}>
        <Routes>
          <Route path="/" element={<DatabaseView />} />
          <Route path="/logs" element={<LogsView />} />
          <Route path="/edit/:docId" element={<DocumentEditor />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
