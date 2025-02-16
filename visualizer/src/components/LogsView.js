import React, { useEffect, useState } from "react";
import { Typography, Box } from "@mui/material";

// Define custom styles for different log levels
const levelStyles = {
  INFO: { color: "#4caf50" },
  ERROR: { color: "#f44336" },
  WARN: { color: "#ff9800" },
  DEBUG: { color: "#9e9e9e" },
};

export default function LogsView() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/api/logs/stream");

    eventSource.onmessage = (event) => {
      // Append each new log message
      setLogs((prevLogs) => [...prevLogs, event.data]);
    };

    eventSource.onerror = (error) => {
      console.error("EventSource failed:", error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  // Helper to parse and render a log line
  const renderLog = (log, idx) => {
    // Regex to match: timestamp - logger - level - message
    const regex = /^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d+)\s-\s(\S+)\s-\s(\S+)\s-\s(.*)$/;
    const match = log.match(regex);

    if (match) {
      const [, timestamp, logger, level, message] = match;
      const levelStyle = levelStyles[level] || { color: "#fff" };

      return (
        <Box key={idx} sx={{ marginBottom: "0.5rem", fontFamily: "monospace" }}>
          <Typography component="span" variant="body2" sx={{ color: "#aaa", marginRight: "0.5rem" }}>
            {timestamp}
          </Typography>
          <Typography component="span" variant="body2" sx={{ color: "#fff", marginRight: "0.5rem" }}>
            {logger}
          </Typography>
          <Typography
            component="span"
            variant="body2"
            sx={{ ...levelStyle, marginRight: "0.5rem", fontWeight: "bold" }}
          >
            {level}
          </Typography>
          <Typography component="span" variant="body2">
            {message}
          </Typography>
        </Box>
      );
    }

    // Fallback: if log doesn't match the expected format, show as-is
    return (
      <Box key={idx} sx={{ marginBottom: "0.5rem", fontFamily: "monospace" }}>
        {log}
      </Box>
    );
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Real-Time Logs
      </Typography>
      <Box
        sx={{
          backgroundColor: "#333",
          color: "#fff",
          padding: "1rem",
          height: "60vh",
          overflowY: "scroll",
          borderRadius: "4px",
        }}
      >
        {logs.map((log, idx) => renderLog(log, idx))}
      </Box>
    </Box>
  );
}
