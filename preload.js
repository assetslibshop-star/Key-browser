const { contextBridge, ipcRenderer } = require('electron');

// Expose secure IPC methods to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Navigation methods
  navigate: (url) => ipcRenderer.invoke('navigate', url),
  goBack: () => ipcRenderer.invoke('go-back'),
  goForward: () => ipcRenderer.invoke('go-forward'),
  refresh: () => ipcRenderer.invoke('refresh'),
  
  // Privacy methods
  clearData: () => ipcRenderer.invoke('clear-data'),
  
  // Listen for navigation events from main process
  onNavigate: (callback) => ipcRenderer.on('navigate', (event, url) => callback(url)),
  onGoBack: (callback) => ipcRenderer.on('go-back', () => callback()),
  onGoForward: (callback) => ipcRenderer.on('go-forward', () => callback()),
  onRefresh: (callback) => ipcRenderer.on('refresh', () => callback()),
  
  // Remove listeners
  removeAllListeners: () => ipcRenderer.removeAllListeners()
});
