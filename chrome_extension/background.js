chrome.action.onClicked.addListener(async (tab) => {
    try {
      // Execute our function in the active tab (the user’s current page).
      const results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: getReadableText
      });
  
      // Results is an array (one item per frame). 
      // We'll just take the .result of the first item.
      const pageText = results[0].result;
  
      // Send the text to your server via a POST request.
      await fetch("https://yourserver.com/api/collectText", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ pageText })
      });
      
      console.log("Successfully sent page text");
    } catch (error) {
      console.error("Error sending page text:", error);
    }
  });
  
  /**
   * This function is injected into the page.
   * By default, it just returns the entire text from document.body.
   * This works on most static or React-based pages, as React’s output
   * is eventually rendered into the DOM as normal HTML.
   */
  function getReadableText() {
    return document.body.innerText;
  }
  