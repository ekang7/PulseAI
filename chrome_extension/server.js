const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();

app.use(express.json({ limit: "10mb" }));

app.post("/upload", (req, res) => {
    const { title, url, screenshot } = req.body;
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const filePath = path.join(__dirname, "uploads", `screenshot-${timestamp}.png`);

    fs.writeFile(filePath, Buffer.from(screenshot, "base64"), (err) => {
        if (err) {
            console.error("Failed to save image:", err);
            return res.status(500).send("Error saving image.");
        }
        console.log(`Screenshot saved: ${filePath}`);
        res.status(200).send("Screenshot received.");
    });

    console.log(`Title: ${title}`);
    console.log(`URL: ${url}`);
});

app.listen(3000, () => console.log("Server running on port 3000"));
