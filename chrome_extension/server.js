const express = require("express");
const app = express();
const port = 3000;

app.use(express.json());

let collectedData = [];

app.post("/collect", (req, res) => {
  collectedData = req.body.tabs;
  console.log("Received tab data:", collectedData);
  res.sendStatus(200);
});

app.get("/data", (req, res) => {
  res.json(collectedData);
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
