document.getElementById("screenshot-btn").addEventListener("click", async () => {
    try {
      // Query the currently active tab in the current window
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab) {
        console.error("No active tab found.");
        return;
      }
  
      // Capture visible area of the current active tab
      const screenshotDataUrl = await chrome.tabs.captureVisibleTab(
        tab.windowId,
        { format: "png" }
      );
  
      // Title and URL of the current tab
      const { title, url } = tab;
  
      // Download the screenshot to "pulse" folder in the user's downloads
      // (Chrome will automatically create the 'pulse' subfolder if it doesn't exist)
      const timestamp = new Date().getTime();
      await chrome.downloads.download({
        url: screenshotDataUrl,
        filename: `pulse/screenshot-${timestamp}.png` // Will appear under Downloads/pulse/
      });
  
      // Send the data to the server
      // Typically you'd replace "https://example.com/api/upload" with your own endpoint
      const response = await fetch("https://example.com/api/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          screenshot: screenshotDataUrl, // base64-encoded PNG
          title: title,
          url: url
        })
      });
  
      if (!response.ok) {
        console.error("Failed to send screenshot to server");
      } else {
        console.log("Screenshot data successfully sent to the server.");
      }
  
    } catch (error) {
      console.error("Error capturing or sending screenshot:", error);
    }
  });
  