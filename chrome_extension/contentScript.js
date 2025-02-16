let scrollTimeout = null;

// Listen for scroll events
window.addEventListener('scroll', () => {
  // Clear any pending timer whenever a new scroll event fires
  clearTimeout(scrollTimeout);

  // Set a new timer; if no more scrolls happen in next 3 seconds, send message
  scrollTimeout = setTimeout(() => {
    chrome.runtime.sendMessage({ type: 'scrollStopped' });
  }, 3000);
});
