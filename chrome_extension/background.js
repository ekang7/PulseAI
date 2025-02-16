console.log("Background service worker initialized.");

// Helper function to capture and send a screenshot for a given tab object
async function captureScreenshot(tab) {
  if (!tab || !tab.id) {
    console.error("No active tab found or invalid tab.");
    return;
  }

  try {
    // 1. Capture the visible area of the current active tab
    const screenshotDataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, {
      format: "png"
    });

    // 2. Collect the URL and title of the current page
    const { title, url } = tab;

    // 3. Send screenshot + page info to your server
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
}

// 1) When the user switches tabs (onActivated), wait 3 seconds, then capture screenshot
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  setTimeout(async () => {
    try {
      const tab = await chrome.tabs.get(activeInfo.tabId);
      await captureScreenshot(tab);
    } catch (err) {
      console.error("Error after tab switch:", err);
    }
  }, 3000);
});

// 2) Listen for messages from contentScript.js indicating scrolling has stopped for 3 seconds
chrome.runtime.onMessage.addListener((message, sender) => {
  if (message.type === "scrollStopped") {
    // The tab that sent the message is sender.tab
    captureScreenshot(sender.tab);
  }
});
