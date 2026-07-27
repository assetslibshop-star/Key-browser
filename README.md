# 🔑 Key - Maximum Privacy Browser

A privacy-focused browser built with Python and PyQt5 that prioritizes user anonymity and security. Key operates exclusively in incognito mode, ensuring no data is ever stored locally. Inspired by Tor Browser's privacy approach.

## 🛡️ Privacy Features

### Core Privacy Protections
- **No History**: Browsing history is never saved
- **No Cookies**: All cookies are blocked by default
- **No Cache**: All caching is disabled
- **No Local Storage**: All local storage mechanisms disabled
- **No Form Data**: Form autocomplete is disabled
- **No Passwords**: Password saving is disabled
- **WebGL Disabled**: Prevents canvas fingerprinting
- **No Plugins**: All plugins and extensions disabled

### Network Privacy
- **Tor Integration**: Built-in Tor support for anonymous routing
- **DNS Leak Prevention**: DNS queries routed through Tor
- **Tracking Blocked**: Common tracking domains blocked
- **Referrer Header Stripped**: No referrer information sent
- **Popup Blocking**: All popups blocked
- **SOCKS5 Proxy**: Tor proxy configuration support

### Security Features
- **Sandboxed Architecture**: Web content isolated
- **No Clipboard Access**: JavaScript cannot access clipboard
- **No Window Opening**: JavaScript cannot open new windows
- **Auto-Fill Disabled**: Form auto-fill completely disabled
- **Session Isolation**: Each session completely isolated

## 📋 Requirements

- Python 3.8 or higher - [Download here](https://www.python.org/downloads/)
- pip (comes with Python)
- Git (for cloning the repository)
- Tor (optional, for maximum anonymity) - [Download here](https://www.torproject.org/download/)

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/assetslibshop-star/Key-browser.git
cd Key-browser
```

### Install Python (if not already installed)

1. Download Python 3.8+ from https://www.python.org/downloads/
2. Run the installer and **check "Add Python to PATH"**
3. Restart your terminal/command prompt

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Tor (Optional but Recommended)

For maximum anonymity, install Tor:
- **Windows**: Download from https://www.torproject.org/download/
- **Linux**: `sudo apt install tor`
- **macOS**: `brew install tor`

## 🎯 Running the Browser

### Standard Mode (Direct Connection)

```bash
python key_browser.py
```

### Tor Mode (Maximum Anonymity)

1. Start Tor service
2. Run with Tor enabled:

```bash
python key_browser.py --tor
```

## 🎨 Usage

1. **Launch the browser**: Run `python key_browser.py` to launch Key
2. **Navigate**: Enter a URL in the address bar and press Enter or click "Go"
3. **Search**: Type a search query directly in the address bar (uses DuckDuckGo)
4. **Navigation**: Use the back, forward, and refresh buttons
5. **Privacy Mode**: The browser always runs in private mode - no action needed
6. **Tor Mode**: Use `--tor` flag to route traffic through Tor network

### Keyboard Shortcuts

- `Ctrl/Cmd + L`: Focus the address bar
- `Ctrl/Cmd + R`: Refresh the current page
- `Escape`: Clear the address bar and lose focus

## 🔧 Configuration

Privacy settings are configured in `key_browser.py`. You can modify:

- Cookie and storage policies
- Web security settings
- Proxy settings for Tor
- User agent and headers

Tor configuration is in `tor_integration.py`. You can modify:

- Tor port and host settings
- Proxy configuration
- DNS leak prevention settings

## 🏗️ Architecture

### Main Browser (`key_browser.py`)
- Creates and manages browser window
- Configures privacy settings
- Handles navigation and UI
- Manages data clearing on exit

### Tor Integration (`tor_integration.py`)
- Manages Tor proxy connection
- Handles DNS leak prevention
- Provides Tor status checking
- Supports identity rotation

### Dependencies (`requirements.txt`)
- PyQt5: GUI framework
- PyQtWebEngine: Web browser engine
- requests: HTTP library for Tor checks
- PySocks: SOCKS proxy support

## 🔮 Future Enhancements

This is a foundation for a privacy-focused browser. Future versions could include:

- **Advanced Tor Integration**: Automatic Tor circuit rotation and bridge support
- **VPN Integration**: Built-in VPN support for IP masking
- **Additional IP Obfuscation**: Multi-hop routing and IP rotation
- **End-to-End Encryption**: Built-in encrypted messaging and file sharing
- **Cryptocurrency Integration**: Privacy-focused cryptocurrency support
- **Physical Isolation**: Integration with Tails or similar privacy OS
- **Advanced Fingerprinting Protection**: Enhanced canvas and WebGL protection
- **HTTPS Only**: Force HTTPS connections
- **Certificate Pinning**: Additional TLS security
- **Header Randomization**: Randomize headers to prevent fingerprinting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This browser provides privacy features but does not guarantee complete anonymity. Always use additional security measures (Tor, VPN, etc.) for sensitive activities. The developers are not responsible for any misuse of this software.

## 🙏 Acknowledgments

Built with [Python](https://www.python.org/) and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
Privacy inspiration from [Tor Browser](https://www.torproject.org/) and [Brave Browser](https://brave.com/)

---

**Key - Your Privacy Matters** 🔑
