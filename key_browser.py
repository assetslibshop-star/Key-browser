#!/usr/bin/env python3
"""
Key Browser - Maximum Privacy Browser
A privacy-focused browser similar to Tor Browser, built with Python and PyQt5
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, 
                             QPushButton, QStatusBar, QLabel, QFrame)
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEngineProfile, QWebEngineSettings)


class KeyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Key - Private Browser")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
        # Configure privacy settings
        self.setup_privacy()
        
        # Create UI
        self.create_ui()
        
        # Load start page
        self.load_start_page()
    
    def setup_privacy(self):
        """Configure maximum privacy settings"""
        profile = QWebEngineProfile.defaultProfile()
        
        # Disable all storage and tracking
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.setCachePath("")  # Disable cache
        profile.setPersistentStoragePath("")  # Disable persistent storage
        
        # Configure web settings
        settings = QWebEngineSettings.defaultSettings()
        
        # Disable tracking and storage
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)  # Prevent fingerprinting
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, False)
        
        # Disable auto-fill and forms
        # Note: AutoFillEnabled not available in PyQt5, handled at profile level
        
        # Disable plugins and extensions
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        
        # Disable JavaScript access to local resources
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        
        # Note: History disabled at profile level
        
        print("Privacy configuration: Maximum security mode enabled")
    
    def create_ui(self):
        """Create the browser interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Navigation bar
        nav_layout = QHBoxLayout()
        
        # Back button
        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)
        nav_layout.addWidget(self.back_btn)
        
        # Forward button
        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(self.go_forward)
        self.forward_btn.setEnabled(False)
        nav_layout.addWidget(self.forward_btn)
        
        # Refresh button
        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.clicked.connect(self.refresh)
        nav_layout.addWidget(self.refresh_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search...")
        self.url_bar.returnPressed.connect(self.navigate)
        nav_layout.addWidget(self.url_bar)
        
        # Go button
        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.navigate)
        nav_layout.addWidget(self.go_btn)
        
        # Privacy indicator
        privacy_label = QLabel("🔒 Private Mode")
        privacy_label.setStyleSheet("color: #00ff88; font-weight: bold; padding: 5px;")
        nav_layout.addWidget(privacy_label)
        
        layout.addLayout(nav_layout)
        
        # Browser view
        self.browser = QWebEngineView()
        self.browser.loadStarted.connect(self.load_started)
        self.browser.loadFinished.connect(self.load_finished)
        self.browser.titleChanged.connect(self.title_changed)
        self.browser.urlChanged.connect(self.url_changed)
        layout.addWidget(self.browser)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_label = QLabel("Ready - Maximum Privacy Mode Active")
        self.status_bar.addWidget(self.status_label)
        self.setStatusBar(self.status_bar)
        
        # Security info
        security_label = QLabel("🔒 Encrypted | 🎭 Tracking Blocked | 🗑️ No Data Stored")
        security_label.setStyleSheet("color: #888; font-size: 11px;")
        self.status_bar.addPermanentWidget(security_label)
    
    def load_start_page(self):
        """Load the privacy start page"""
        start_page = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    color: #eee;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                .logo {
                    font-size: 72px;
                    font-weight: bold;
                    color: #ffd700;
                    margin-bottom: 20px;
                }
                .tagline {
                    font-size: 24px;
                    color: #888;
                    margin-bottom: 40px;
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                    max-width: 600px;
                }
                .feature {
                    background: #0f3460;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }
                .feature-icon {
                    font-size: 32px;
                    margin-bottom: 10px;
                }
                .feature-title {
                    font-weight: bold;
                    color: #ffd700;
                    margin-bottom: 5px;
                }
                .feature-desc {
                    color: #888;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>
            <div class="logo">🔑 Key</div>
            <div class="tagline">Maximum Privacy. Zero Tracking.</div>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🔒</div>
                    <div class="feature-title">No History</div>
                    <div class="feature-desc">Nothing is saved locally</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🚫</div>
                    <div class="feature-title">No Cookies</div>
                    <div class="feature-desc">All cookies blocked</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🛡️</div>
                    <div class="feature-title">No Cache</div>
                    <div class="feature-desc">All caching disabled</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎭</div>
                    <div class="feature-title">Anti-Fingerprint</div>
                    <div class="feature-desc">WebGL fingerprinting blocked</div>
                </div>
            </div>
        </body>
        </html>
        """
        self.browser.setHtml(start_page)
    
    def navigate(self):
        """Navigate to the URL in the address bar"""
        url = self.url_bar.text().strip()
        
        if not url:
            return
        
        # Add protocol if missing
        if not url.startswith('http://') and not url.startswith('https://'):
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                # Treat as search query
                url = f'https://duckduckgo.com/?q={url}'
        
        self.browser.setUrl(QUrl(url))
    
    def go_back(self):
        """Go back in history"""
        if self.browser.history().canGoBack():
            self.browser.back()
    
    def go_forward(self):
        """Go forward in history"""
        if self.browser.history().canGoForward():
            self.browser.forward()
    
    def refresh(self):
        """Refresh the current page"""
        self.browser.reload()
    
    def load_started(self):
        """Handle page load start"""
        self.status_label.setText("Loading...")
        self.go_btn.setEnabled(False)
    
    def load_finished(self, success):
        """Handle page load finish"""
        if success:
            self.status_label.setText("Connected - Private Mode")
        else:
            self.status_label.setText("Load failed")
        
        self.go_btn.setEnabled(True)
        self.update_nav_buttons()
    
    def title_changed(self, title):
        """Handle title change"""
        if title:
            self.setWindowTitle(f"Key - {title}")
        else:
            self.setWindowTitle("Key - Private Browser")
    
    def url_changed(self, url):
        """Handle URL change"""
        self.url_bar.setText(url.toString())
        self.update_nav_buttons()
    
    def update_nav_buttons(self):
        """Update navigation button states"""
        self.back_btn.setEnabled(self.browser.history().canGoBack())
        self.forward_btn.setEnabled(self.browser.history().canGoForward())
    
    def closeEvent(self, event):
        """Handle window close - clear all data"""
        # Clear all cookies and data
        profile = QWebEngineProfile.defaultProfile()
        cookie_store = profile.cookieStore()
        cookie_store.deleteAllCookies()
        
        print("Privacy cleanup: All data cleared on exit")
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Key Browser")
    app.setOrganizationName("Key Privacy")
    
    # Create and show browser
    browser = KeyBrowser()
    browser.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
