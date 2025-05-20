// Config
const API_URL = "http://127.0.0.1:8000/predict";
const FALLBACK_ICON = "icon.png";

// Context Menu Setup
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "detect-fake-news",
    title: "🧠 Detect Fake News",
    contexts: ["selection", "image"],
  });
});

// Context Menu Click Handler
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "detect-fake-news") return;

  const selectedText = info.selectionText?.trim() || "";
  const imageUrl = info.srcUrl || "";

  if (!selectedText && !imageUrl) {
    notify("❌ No Input", "Highlight text or right-click an image.");
    return;
  }

  try {
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