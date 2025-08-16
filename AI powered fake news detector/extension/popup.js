// Popup script to handle API URL settings

document.addEventListener('DOMContentLoaded', function() {
  // Load current API URL from storage
  chrome.storage.local.get(['apiUrl'], function(result) {
    const apiUrlInput = document.getElementById('apiUrl');
    if (result.apiUrl) {
      apiUrlInput.value = result.apiUrl;
    } else {
      // Default value
      apiUrlInput.value = 'http://localhost:8000/predict';
    }
  });

  // Save settings button click handler
  document.getElementById('saveSettings').addEventListener('click', function() {
    const apiUrl = document.getElementById('apiUrl').value.trim();
    
    // Validate URL format
    if (!apiUrl) {
      updateStatus('Please enter a valid URL', 'error');
      return;
    }

    try {
      new URL(apiUrl); // Will throw if invalid URL
      
      // Save to storage
      chrome.storage.local.set({apiUrl: apiUrl}, function() {
        updateStatus('Settings saved successfully!', 'success');
        
        // Optional: Notify background script that settings changed
        chrome.runtime.sendMessage({action: 'SETTINGS_UPDATED'});
      });
    } catch (e) {
      updateStatus('Invalid URL format', 'error');
    }
  });

  // Helper function to update status message
  function updateStatus(message, type) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.style.color = type === 'error' ? '#d93025' : '#188038';
    
    // Clear status after 3 seconds
    setTimeout(() => {
      status.textContent = '';
    }, 3000);
  }
});