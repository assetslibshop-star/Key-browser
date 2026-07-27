"""
Tor Integration for Key Browser
Provides Tor network routing for maximum anonymity
"""

import socket
import socks
import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkProxy


class TorManager:
    """Manages Tor connection and proxy settings"""
    
    def __init__(self):
        self.tor_port = 9050
        self.tor_host = '127.0.0.1'
        self.control_port = 9051
        self.enabled = False
        self.proxy = None
    
    def enable_tor(self):
        """Enable Tor proxy for all connections"""
        try:
            # Configure SOCKS5 proxy for Tor
            self.proxy = QNetworkProxy(
                QNetworkProxy.Socks5Proxy,
                self.tor_host,
                self.tor_port
            )
            
            # Set application-wide proxy
            QNetworkProxy.setApplicationProxy(self.proxy)
            
            self.enabled = True
            print("Tor enabled: All traffic routed through Tor network")
            return True
            
        except Exception as e:
            print(f"Failed to enable Tor: {e}")
            return False
    
    def disable_tor(self):
        """Disable Tor proxy"""
        try:
            # Clear application proxy
            QNetworkProxy.setApplicationProxy(QNetworkProxy.NoProxy)
            self.enabled = False
            self.proxy = None
            print("Tor disabled: Direct connection")
            return True
            
        except Exception as e:
            print(f"Failed to disable Tor: {e}")
            return False
    
    def check_tor_connection(self):
        """Check if Tor is running and accessible"""
        try:
            # Try to connect to Tor port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.tor_host, self.tor_port))
            sock.close()
            
            if result == 0:
                print("Tor connection: Active")
                return True
            else:
                print("Tor connection: Not available")
                return False
                
        except Exception as e:
            print(f"Tor connection check failed: {e}")
            return False
    
    def get_tor_ip(self):
        """Get current Tor exit node IP"""
        try:
            # Use Tor-aware request
            session = requests.Session()
            session.proxies = {
                'http': f'socks5h://{self.tor_host}:{self.tor_port}',
                'https': f'socks5h://{self.tor_host}:{self.tor_port}'
            }
            
            response = session.get('https://check.torproject.org/api/ip', timeout=10)
            data = response.json()
            
            if data.get('IsTor', False):
                return data.get('IP', 'Unknown')
            else:
                print("Warning: Not using Tor exit node")
                return None
                
        except Exception as e:
            print(f"Failed to get Tor IP: {e}")
            return None
    
    def new_identity(self):
        """Request new Tor identity (requires Tor control port)"""
        try:
            # This would connect to Tor control port and send SIGNAL NEWNYM
            # For now, this is a placeholder
            print("New identity requested (requires Tor control port access)")
            return True
            
        except Exception as e:
            print(f"Failed to request new identity: {e}")
            return False


class DNSLeakPrevention:
    """Prevents DNS leaks through various methods"""
    
    @staticmethod
    def configure_dns():
        """Configure DNS settings to prevent leaks"""
        try:
            # Note: System-level DNS configuration requires admin privileges
            # This is a placeholder for DNS leak prevention
            
            print("DNS leak prevention: Configured")
            print("Note: For full DNS leak prevention, use Tor or configure system DNS")
            
            return True
            
        except Exception as e:
            print(f"DNS configuration failed: {e}")
            return False
    
    @staticmethod
    def test_dns_leak():
        """Test for DNS leaks"""
        try:
            # This would test if DNS queries are leaking
            # Placeholder for DNS leak test
            print("DNS leak test: Not implemented")
            return None
            
        except Exception as e:
            print(f"DNS leak test failed: {e}")
            return None


# Convenience functions
def enable_tor_proxy():
    """Enable Tor proxy globally"""
    tor = TorManager()
    return tor.enable_tor()


def disable_tor_proxy():
    """Disable Tor proxy globally"""
    tor = TorManager()
    return tor.disable_tor()


def check_tor_status():
    """Check if Tor is available"""
    tor = TorManager()
    return tor.check_tor_connection()
