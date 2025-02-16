import React, { useEffect, useState } from "react";
import { Typography, Box } from "@mui/material";

export default function LogsView() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/api/logs/stream");

    eventSource.onmessage = (event) => {
      // Each SSE message could be a log line
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
        {logs.map((log, idx) => (
          <div key={idx}>{log}</div>
        ))}
      </Box>
    </Box>
  );
}
