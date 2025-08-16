// Config
// Default API URL (can be overridden in extension settings)
let API_URL = "http://localhost:8000/predict";

// Load API URL from storage or use default
chrome.storage.local.get(['apiUrl'], function(result) {
  if (result.apiUrl) {
    API_URL = result.apiUrl;
    console.log('Using API URL from settings:', API_URL);
  } else {
    // Save default URL to storage
    chrome.storage.local.set({apiUrl: API_URL});
    console.log('Using default API URL:', API_URL);
  }
});
const FALLBACK_ICON = "icon.png";

// Context Menu Setup
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "detect-fake-news",
    title: "🧠 Detect Fake News",
    contexts: ["selection", "image"],
  });
});

// Listen for settings updates
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === 'SETTINGS_UPDATED') {
    // Reload API URL from storage
    chrome.storage.local.get(['apiUrl'], function(result) {
      if (result.apiUrl) {
        API_URL = result.apiUrl;
        console.log('API URL updated:', API_URL);
      }
    });
  }
});

// Context Menu Click Handler
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "detect-fake-news") return;

  const selectedText = info.selectionText?.trim() || "";
  const imageUrl = info.srcUrl || "";

  if (!selectedText) {
    notify("❌ Missing Text", "Please highlight some text to analyze.");
    return;
  }
  
  if (!imageUrl) {
    notify("❌ Missing Image", "This feature requires an image. Please right-click on an image.");
    return;
  }

  try {
    console.log("Sending prediction request with:", { text: selectedText, image_url: imageUrl });
    
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: selectedText, image_url: imageUrl }),
    });

    if (!response.ok) throw new Error(`API Error: ${response.status}`);

    const data = await response.json();
    const label = data.label || "Unknown";
    const confidence = data.confidence ? `${(data.confidence * 100).toFixed(1)}%` : "N/A";

    notify(
      `🔍 ${label.charAt(0).toUpperCase() + label.slice(1)}`,
      `Confidence: ${confidence}`
    );

  } catch (err) {
    console.error("API Error:", err);
    notify("⚠️ Error", err.message.includes("fetch") 
      ? "Backend offline. Start the server!" 
      : "Analysis failed. Try again."
    );
  }
});

// Notification Helper
function notify(title, message) {
  chrome.notifications.create({
    type: "basic",
    iconUrl: FALLBACK_ICON,
    title,
    message,
  });
}
