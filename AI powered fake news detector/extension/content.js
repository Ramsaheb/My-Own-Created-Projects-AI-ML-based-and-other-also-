// No changes needed for basic functionality
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "GET_SELECTED_TEXT") {
    sendResponse({ selectedText: window.getSelection().toString() });
  }
});