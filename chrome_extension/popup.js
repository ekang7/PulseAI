document.getElementById("screenshot-btn").addEventListener("click", async () => {
    try {
      // 1. Get the currently active tab in the current window
      const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!activeTab) {
        console.error("No active tab found.");
        return;
      }
  
      // 2. Capture the visible area of the current active tab
      const screenshotDataUrl = await chrome.tabs.captureVisibleTab(activeTab.windowId, {
        format: "png"
      });
  
      // 3. Collect the URL and title of the current page
      const { title, url } = activeTab;
  
      // 4. Send screenshot + page info to your server
      //    Replace "https://example.com/api/upload" with your own endpoint
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          screenshot: screenshotDataUrl, // base64-encoded PNG
          pageUrl: url,
          pageTitle: title
        })
      });
  
      if (response.ok) {
        console.log("Screenshot and info successfully sent to the server.");
      } else {
        console.error("Failed to send screenshot to server. Status:", response.status);
      }
  
    } catch (error) {
      console.error("Error capturing or sending screenshot:", error);
    }
  });
  