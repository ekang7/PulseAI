const button = document.getElementById("screenshot-btn");

button.addEventListener("click", async () => {
  // Disable the button and show an immediate "Sending..." state
  button.disabled = true;
  button.textContent = "Sending...";

  try {
    // 1. Get the currently active tab in the current window
    const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!activeTab) {
      console.error("No active tab found.");
      button.textContent = "Send to PulseAI";
      button.disabled = false;
      return;
    }

    // 2. Capture the visible area of the active tab
    const screenshotDataUrl = await chrome.tabs.captureVisibleTab(activeTab.windowId, {
      format: "png"
    });

    // 3. Collect the URL and title of the current page
    const { title, url } = activeTab;

    // 4. Start sending screenshot + page info to your server without waiting for response
    fetch("http://127.0.0.1:8000/api/upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        screenshot: screenshotDataUrl, // base64-encoded PNG
        pageUrl: url,
        pageTitle: title
      })
    }).catch(error => console.error("Error sending screenshot:", error));

    // Immediately update the button to "Sent!" regardless of the response.
    button.textContent = "Sent!";

    // After 1 second, revert the button back to its original state.
    setTimeout(() => {
      button.textContent = "Send to PulseAI";
      button.disabled = false;
    }, 1000);
  } catch (error) {
    console.error("Error capturing screenshot:", error);
    // On error, show an error message briefly before reverting.
    button.textContent = "Error! Try Again";
    setTimeout(() => {
      button.textContent = "Send to PulseAI";
      button.disabled = false;
    }, 1000);
  }
});
