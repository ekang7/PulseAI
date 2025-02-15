// This file is required for Manifest V3 to run the extension in service worker mode.
// In this particular example, we don't need to do anything special here, unless you
// want to handle extension events in the background.
// 
// If you wanted to handle the screenshot on a browser action click (without a popup),
// you could do something like:
//
// chrome.action.onClicked.addListener(async (tab) => {
//   // Same logic as in popup.js can be used here.
// });
//
// But for now, the logic remains in popup.js, so this can remain empty or for logging.

console.log("Background service worker initialized.");
