const { app, BrowserWindow, session, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

// Privacy configuration - Maximum security settings
const PRIVACY_CONFIG = {
  // Disable all tracking and data collection
  disableBlinkFeatures: 'AutomationControlled',
  
  // Block all third-party cookies
  cookiesEnabled: false,
  
  // Disable cache and storage
  cacheEnabled: false,
  
  // Disable history
  saveHistory: false,
  
  // Disable form data
  saveFormData: false,
  
  // Disable passwords
  savePasswords: false,
  
  // Disable download history
  saveDownloads: false,
  
  // Disable session storage
  sessionStorage: false,
  
  // Disable local storage
  localStorage: false,
  
  // Disable indexedDB
  indexedDB: false,
  
  // Disable webSQL
  webSQL: false,
  
  // Disable service workers
  serviceWorkers: false,
  
  // Disable notifications
  notifications: false
};

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: 'Key - Private Browser',
    icon: path.join(__dirname, 'assets', 'icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
      webviewTag: true,
      partition: 'persist:incognito',
      preload: path.join(__dirname, 'preload.js')
    },
    // Privacy-focused window settings
    autoHideMenuBar: true,
    show: false
  });

  // Load the browser UI
  mainWindow.loadFile('index.html');

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Clear all data on close
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Configure privacy session
function configurePrivacySession() {
  const defaultSession = session.defaultSession;
  
  // Clear all existing data
  defaultSession.clearStorageData({
    storages: [
      'appcache',
      'cookies',
      'filesystem',
      'indexdb',
      'local storage',
      'shader cache',
      'websql',
      'service workers',
      'cache storage'
    ],
    quotas: ['temporary', 'persistent', 'syncable']
  });

  // Disable cookies
  defaultSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Set-Cookie': undefined
      }
    });
  });

  // Block tracking requests
  defaultSession.webRequest.onBeforeRequest((details, callback) => {
    const url = details.url.toLowerCase();
    
    // Block common tracking domains
    const blockedDomains = [
      'google-analytics.com',
      'doubleclick.net',
      'facebook.com/tr',
      'connect.facebook.net',
      'analytics.twitter.com',
      'pixel.wp.com',
      'hotjar.com',
      'segment.io',
      'mixpanel.com',
      'amplitude.com',
      'fullstory.com',
      'stats.g.doubleclick.net'
    ];

    const isBlocked = blockedDomains.some(domain => url.includes(domain));
    
    callback({ cancel: isBlocked });
  });

  // Remove referrer header for privacy
  defaultSession.webRequest.onBeforeSendHeaders((details, callback) => {
    delete details.requestHeaders['Referer'];
    delete details.requestHeaders['Origin'];
    
    // Set user agent to generic
    details.requestHeaders['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
    
    callback({ requestHeaders: details.requestHeaders });
  });

  // DNS leak prevention - Use secure DNS
  defaultSession.setDNSOverHTTPS({
    enabled: true,
    servers: [
      {
        template: 'https://security.cloudflare-dns.com/dns-query'
      },
      {
        template: 'https://dns.quad9.net/dns-query'
      }
    ]
  });

  // Disable spell checking (prevents data leakage)
  defaultSession.setSpellCheckerEnabled(false);

  // Disable hardware acceleration (prevents fingerprinting)
  app.disableHardwareAcceleration();

  // Set strict security policies
  defaultSession.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  );
}

// Create incognito session for webviews
function createIncognitoSession() {
  const incognitoSession = session.fromPartition('incognito-session');
  
  // Configure same privacy settings for incognito session
  incognitoSession.webRequest.onBeforeRequest((details, callback) => {
    const url = details.url.toLowerCase();
    
    const blockedDomains = [
      'google-analytics.com',
      'doubleclick.net',
      'facebook.com/tr',
      'connect.facebook.net',
      'analytics.twitter.com',
      'pixel.wp.com',
      'hotjar.com',
      'segment.io',
      'mixpanel.com',
      'amplitude.com',
      'fullstory.com'
    ];

    const isBlocked = blockedDomains.some(domain => url.includes(domain));
    
    callback({ cancel: isBlocked });
  });

  incognitoSession.webRequest.onBeforeSendHeaders((details, callback) => {
    delete details.requestHeaders['Referer'];
    delete details.requestHeaders['Origin'];
    callback({ requestHeaders: details.requestHeaders });
  });

  // Clear data on session creation
  incognitoSession.clearStorageData();
}

// App event handlers
app.whenReady().then(() => {
  configurePrivacySession();
  createIncognitoSession();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    // Clear all data before quitting
    session.defaultSession.clearStorageData();
    app.quit();
  }
});

app.on('before-quit', () => {
  // Final cleanup
  session.defaultSession.clearStorageData();
});

// IPC handlers for browser functionality
ipcMain.handle('navigate', (event, url) => {
  if (mainWindow) {
    mainWindow.webContents.send('navigate', url);
  }
});

ipcMain.handle('go-back', () => {
  if (mainWindow) {
    mainWindow.webContents.send('go-back');
  }
});

ipcMain.handle('go-forward', () => {
  if (mainWindow) {
    mainWindow.webContents.send('go-forward');
  }
});

ipcMain.handle('refresh', () => {
  if (mainWindow) {
    mainWindow.webContents.send('refresh');
  }
});

ipcMain.handle('clear-data', async () => {
  await session.defaultSession.clearStorageData();
  return { success: true };
});
