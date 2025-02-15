document.getElementById("scrapeBtn").addEventListener("click", async () => {
    const messageEl = document.getElementById("message");
  
    try {
      // 1. Get the active tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab) {
        messageEl.textContent = "No active tab found.";
        return;
      }
  
      // 2. Inject a function into the page to scrape the content
      const results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          // This function runs in the context of the web page
          // Return the entire text content from the <body>
          return document.body.innerText;
        },
      });
  
      // 3. Retrieve the scraped data (if any)
      if (!results || !results.length) {
        messageEl.textContent = "Failed to scrape page.";
        return;
      }
  
      const scrapedContent = results[0].result;
      
      // 4. Send the scraped data to your server
      // Replace 'https://example.com/api/upload' with your actual endpoint
      const response = await fetch("https://example.com/api/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: scrapedContent }),
      });
  
      if (response.ok) {
        messageEl.textContent = "Page content successfully sent to server.";
      } else {
        messageEl.textContent = "Error sending data to server.";
      }
    } catch (error) {
      messageEl.textContent = "Error: " + error.toString();
    }
  });
  