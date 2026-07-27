// DOM Elements
const urlInput = document.getElementById('urlInput');
const goBtn = document.getElementById('goBtn');
const backBtn = document.getElementById('backBtn');
const forwardBtn = document.getElementById('forwardBtn');
const refreshBtn = document.getElementById('refreshBtn');
const webview = document.getElementById('webview');
const newTabPage = document.getElementById('newTabPage');
const connectionStatus = document.getElementById('connectionStatus');

// Current navigation state
let currentUrl = '';
let canGoBack = false;
let canGoForward = false;

// Initialize webview
function initWebview() {
  webview.addEventListener('dom-ready', () => {
    console.log('Webview ready');
    updateNavigationState();
  });

  webview.addEventListener('did-start-loading', () => {
    connectionStatus.textContent = 'Loading...';
  });

  webview.addEventListener('did-stop-loading', () => {
    connectionStatus.textContent = 'Connected';
    updateNavigationState();
    currentUrl = webview.getURL();
    urlInput.value = currentUrl;
  });

  webview.addEventListener('did-fail-load', (event) => {
    console.error('Failed to load:', event);
    connectionStatus.textContent = 'Load failed';
  });

  webview.addEventListener('page-title-updated', (event) => {
    if (event.title) {
      document.title = `Key - ${event.title}`;
    }
  });

  // Block new windows (popups)
  webview.addEventListener('new-window', (event) => {
    event.preventDefault();
    console.log('Blocked popup:', event.url);
  });
}

// Update navigation button states
function updateNavigationState() {
  if (webview) {
    canGoBack = webview.canGoBack();
    canGoForward = webview.canGoForward();
    
    backBtn.disabled = !canGoBack;
    forwardBtn.disabled = !canGoForward;
  }
}

// Navigate to URL
function navigate(url) {
  if (!url) return;

  // Add protocol if missing
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    // Check if it looks like a URL
    if (url.includes('.') && !url.includes(' ')) {
      url = 'https://' + url;
    } else {
      // Treat as search query
      url = `https://duckduckgo.com/?q=${encodeURIComponent(url)}`;
    }
  }

  // Hide new tab page and show webview
  newTabPage.classList.add('hidden');
  webview.classList.remove('hidden');

  // Load URL
  webview.src = url;
  currentUrl = url;
  urlInput.value = url;
}

// Event Listeners
goBtn.addEventListener('click', () => {
  navigate(urlInput.value);
});

urlInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    navigate(urlInput.value);
  }
});

backBtn.addEventListener('click', () => {
  if (webview && canGoBack) {
    webview.goBack();
  }
});

forwardBtn.addEventListener('click', () => {
  if (webview && canGoForward) {
    webview.goForward();
  }
});

refreshBtn.addEventListener('click', () => {
  if (webview) {
    if (currentUrl) {
      webview.reload();
    } else {
      navigate(urlInput.value);
    }
  }
});

// Privacy: Clear data on page unload
window.addEventListener('beforeunload', () => {
  if (window.electronAPI) {
    window.electronAPI.clearData();
  }
});

// Initialize
initWebview();

// Handle keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + L to focus URL bar
  if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
    e.preventDefault();
    urlInput.focus();
    urlInput.select();
  }
  
  // Ctrl/Cmd + R to refresh
  if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
    e.preventDefault();
    refreshBtn.click();
  }
  
  // Escape to clear URL
  if (e.key === 'Escape' && document.activeElement === urlInput) {
    urlInput.value = currentUrl;
    urlInput.blur();
  }
});

// Expose functions for potential future extensions
window.KeyBrowser = {
  navigate,
  getCurrentUrl: () => currentUrl,
  clearData: async () => {
    if (window.electronAPI) {
      await window.electronAPI.clearData();
    }
  }
};
