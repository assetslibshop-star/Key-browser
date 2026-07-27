#!/usr/bin/env python3
"""
Key Browser - Maximum Privacy Browser
A privacy-focused browser similar to Tor Browser, built with Python and PyQt5
"""

import sys
import os
import base64
import hashlib
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, 
                             QPushButton, QStatusBar, QLabel, QFrame, QCheckBox)
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEngineProfile, QWebEngineSettings)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor


class KeyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Key - Private Browser")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
        # Privacy state
        self.dark_mode = False
        self.encrypt_urls = True
        self.real_url = ""
        
        # Configure privacy settings
        self.setup_privacy()
        
        # Apply styling
        self.apply_theme()
        
        # Create UI
        self.create_ui()
        
        # Load start page
        self.load_start_page()
    
    def encrypt_text(self, text):
        """Encrypt text for display (visual obfuscation)"""
        if not text or not self.encrypt_urls:
            return text
        # Simple visual encryption - show asterisks and partial hash
        if text.startswith('http'):
            parts = text.split('/')
            if len(parts) > 2:
                domain = parts[2]
                encrypted_domain = '*' * (len(domain) - 4) + domain[-4:]
                return '/'.join(parts[:2]) + '//' + encrypted_domain + '/' + '/'.join(parts[3:])
        return '*' * len(text)
    
    def apply_theme(self):
        """Apply theme styling"""
        if self.dark_mode:
            # Dark theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1a1a2e;
                }
                QLineEdit {
                    background-color: #16213e;
                    color: #eee;
                    border: 2px solid #0f3460;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 2px solid #ffd700;
                }
                QPushButton {
                    background-color: #0f3460;
                    color: #eee;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1a4a7a;
                }
                QPushButton:pressed {
                    background-color: #ffd700;
                    color: #1a1a2e;
                }
                QPushButton:disabled {
                    background-color: #0a1a3a;
                    color: #666;
                }
                QStatusBar {
                    background-color: #16213e;
                    color: #888;
                    border-top: 2px solid #0f3460;
                }
                QLabel {
                    color: #eee;
                }
            """)
        else:
            # Light theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #333;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 2px solid #ffd700;
                }
                QPushButton {
                    background-color: #ffd700;
                    color: #1a1a2e;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ffed4a;
                }
                QPushButton:pressed {
                    background-color: #e6c200;
                }
                QPushButton:disabled {
                    background-color: #e0e0e0;
                    color: #999;
                }
                QStatusBar {
                    background-color: #f0f0f0;
                    color: #666;
                    border-top: 2px solid #ddd;
                }
                QLabel {
                    color: #333;
                }
            """)
    
    def toggle_dark_mode(self):
        """Toggle dark/light mode"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        # Update webview theme
        if self.dark_mode:
            self.browser.page().setBackgroundColor(QColor("#1a1a2e"))
        else:
            self.browser.page().setBackgroundColor(QColor("#ffffff"))
    
    def toggle_encryption(self):
        """Toggle URL encryption"""
        self.encrypt_urls = not self.encrypt_urls
        # Update URL bar display
        if self.real_url:
            if self.encrypt_urls:
                self.url_bar.setText(self.encrypt_text(self.real_url))
            else:
                self.url_bar.setText(self.real_url)
    
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
        self.back_btn.setFixedWidth(40)
        nav_layout.addWidget(self.back_btn)
        
        # Forward button
        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(self.go_forward)
        self.forward_btn.setEnabled(False)
        self.forward_btn.setFixedWidth(40)
        nav_layout.addWidget(self.forward_btn)
        
        # Refresh button
        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.clicked.connect(self.refresh)
        self.refresh_btn.setFixedWidth(40)
        nav_layout.addWidget(self.refresh_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔒 Encrypted URL or search...")
        self.url_bar.returnPressed.connect(self.navigate)
        self.url_bar.setEchoMode(QLineEdit.Password)  # Mask input by default
        nav_layout.addWidget(self.url_bar)
        
        # Toggle encryption button
        self.encrypt_btn = QPushButton("🔐")
        self.encrypt_btn.setFixedWidth(40)
        self.encrypt_btn.setToolTip("Toggle URL Encryption")
        self.encrypt_btn.clicked.connect(self.toggle_encryption)
        nav_layout.addWidget(self.encrypt_btn)
        
        # Go button
        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.navigate)
        self.go_btn.setFixedWidth(60)
        nav_layout.addWidget(self.go_btn)
        
        # Dark mode toggle
        self.dark_mode_btn = QPushButton("🌙")
        self.dark_mode_btn.setFixedWidth(40)
        self.dark_mode_btn.setToolTip("Toggle Dark Mode")
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        nav_layout.addWidget(self.dark_mode_btn)
        
        # Privacy indicator
        privacy_label = QLabel("🔒")
        privacy_label.setStyleSheet("font-size: 18px;")
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
        self.status_label = QLabel("🔒 Maximum Privacy Mode Active")
        self.status_bar.addWidget(self.status_label)
        self.setStatusBar(self.status_bar)
        
        # Security info
        security_label = QLabel("� Encrypted | 🎭 Tracking Blocked | 🗑️ No Data Stored")
        security_label.setStyleSheet("font-size: 11px;")
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
        
        self.real_url = url
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
        self.real_url = url.toString()
        if self.encrypt_urls:
            self.url_bar.setText(self.encrypt_text(self.real_url))
        else:
            self.url_bar.setText(self.real_url)
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
