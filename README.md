# 🔑 Key - Maximum Privacy Browser

A privacy-focused browser built with Electron that prioritizes user anonymity and security. Key operates exclusively in incognito mode, ensuring no data is ever stored locally.

## 🛡️ Privacy Features

### Core Privacy Protections
- **No History**: Browsing history is never saved
- **No Cookies**: All cookies are blocked by default
- **No Cache**: All caching is disabled
- **No Local Storage**: localStorage, sessionStorage, IndexedDB, WebSQL all disabled
- **No Form Data**: Form autocomplete is disabled
- **No Passwords**: Password saving is disabled
- **No Downloads History**: Download history is not tracked
- **No Service Workers**: Service workers are disabled

### Network Privacy
- **DNS over HTTPS**: All DNS queries are encrypted using Cloudflare and Quad9 secure DNS
- **Tracking Blocked**: Common tracking domains and analytics services are blocked
- **Referrer Header Stripped**: No referrer information is sent to websites
- **Origin Header Stripped**: Origin information is removed from requests
- **Generic User Agent**: Uses a generic user agent string to reduce fingerprinting
- **Popup Blocking**: All popups and new windows are blocked

### Security Features
- **Sandboxed Webviews**: All web content runs in sandboxed processes
- **Context Isolation**: Renderer processes are isolated from main process
- **No Node Integration**: Node.js integration is disabled in renderer
- **Spell Check Disabled**: Prevents potential data leakage through spell checking
- **Hardware Acceleration Disabled**: Reduces fingerprinting surface

## 📋 Requirements

- Node.js (v16 or higher)
- npm (comes with Node.js)
- Git (for cloning the repository)

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/Key-browser.git
cd Key-browser
```

### Install Dependencies

```bash
npm install
```

## 🎯 Running the Browser

### Development Mode

```bash
npm start
```

### Build for Production

```bash
npm run build
```

The built application will be in the `dist` directory.

## 🎨 Usage

1. **Launch the browser**: Run `npm start` to launch Key
2. **Navigate**: Enter a URL in the address bar and press Enter or click "Go"
3. **Search**: Type a search query directly in the address bar (uses DuckDuckGo)
4. **Navigation**: Use the back, forward, and refresh buttons
5. **Privacy Mode**: The browser always runs in private mode - no action needed

### Keyboard Shortcuts

- `Ctrl/Cmd + L`: Focus the address bar
- `Ctrl/Cmd + R`: Refresh the current page
- `Escape`: Clear the address bar and lose focus

## 🔧 Configuration

Privacy settings are configured in `main.js`. You can modify:

- Blocked tracking domains
- DNS over HTTPS servers
- User agent string
- Session partition settings
- Web request interceptors

## 🏗️ Architecture

### Main Process (`main.js`)
- Creates and manages browser windows
- Configures privacy sessions
- Handles web request interception
- Manages data clearing

### Renderer Process (`renderer.js`)
- Handles UI interactions
- Manages webview navigation
- Updates navigation state
- Handles keyboard shortcuts

### Preload Script (`preload.js`)
- Provides secure IPC bridge
- Exposes safe APIs to renderer
- Maintains context isolation

### UI (`index.html`)
- Browser interface with navigation controls
- Privacy status indicators
- New tab page with feature overview

## 🔮 Future Enhancements

This is a foundation for a privacy-focused browser. Future versions could include:

- **Tor Integration**: Route traffic through Tor network for multi-relay routing
- **VPN Integration**: Built-in VPN support for IP masking
- **Additional IP Obfuscation**: Multi-hop routing and IP rotation
- **End-to-End Encryption**: Built-in encrypted messaging and file sharing
- **Cryptocurrency Integration**: Privacy-focused cryptocurrency support
- **Physical Isolation**: Integration with Tails or similar privacy OS
- **Advanced Fingerprinting Protection**: Canvas and WebGL fingerprinting protection
- **HTTPS Only**: Force HTTPS connections
- **Certificate Pinning**: Additional TLS security

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This browser provides privacy features but does not guarantee complete anonymity. Always use additional security measures (Tor, VPN, etc.) for sensitive activities. The developers are not responsible for any misuse of this software.

## 🙏 Acknowledgments

Built with [Electron](https://www.electronjs.org/)
Privacy inspiration from [Tor Browser](https://www.torproject.org/) and [Brave Browser](https://brave.com/)

---

**Key - Your Privacy Matters** 🔑
