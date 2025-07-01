"""
Shared HTTP Server Utilities
============================

Common HTTP server functionality extracted from facebook-ads-intelligence
to eliminate duplication and provide reusable server components.
"""

import http.server
import socketserver
import time
import threading
import webbrowser
from typing import Optional, Callable


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Enhanced HTTP request handler with CORS support and better logging."""
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(204)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging format with timestamps."""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timestamp} - {self.address_string()} - {format % args}")


class CustomHTTPServer:
    """Reusable HTTP server with common configuration."""
    
    def __init__(self, 
                 host: str = '0.0.0.0',
                 port: int = 8000,
                 handler_class: Optional[Callable] = None,
                 auto_open_browser: bool = True):
        """
        Initialize HTTP server.
        
        Args:
            host: Host address to bind to
            port: Port number to use
            handler_class: Custom request handler class
            auto_open_browser: Whether to auto-open browser
        """
        self.host = host
        self.port = port
        self.handler_class = handler_class or CustomHTTPRequestHandler
        self.auto_open_browser = auto_open_browser
        self.httpd = None
    
    def start(self, 
             working_directory: Optional[str] = None,
             service_name: str = "HTTP Server") -> bool:
        """
        Start the HTTP server.
        
        Args:
            working_directory: Directory to serve files from
            service_name: Name of service for logging
            
        Returns:
            True if server started successfully
        """
        try:
            # Change working directory if specified
            if working_directory:
                import os
                os.chdir(working_directory)
            
            # Create server
            self.httpd = socketserver.TCPServer((self.host, self.port), self.handler_class)
            
            print(f'\n🚀 {service_name}')
            print('=' * (len(service_name) + 3))
            print(f'✅ Server running at: http://localhost:{self.port}')
            if working_directory:
                print(f'📂 Serving files from: {working_directory}')
            print('\n💡 Press Ctrl+C to stop the server\n')
            
            # Open browser in separate thread
            if self.auto_open_browser:
                browser_thread = threading.Thread(target=self._open_browser)
                browser_thread.daemon = True
                browser_thread.start()
            
            # Start serving
            self.httpd.serve_forever()
            return True
            
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f'❌ Port {self.port} is already in use.')
                print(f'   Try a different port or stop the existing server.')
                return False
            else:
                print(f'❌ Server error: {e}')
                return False
        except KeyboardInterrupt:
            self.stop()
            return True
    
    def stop(self):
        """Stop the HTTP server gracefully."""
        if self.httpd:
            print('\n👋 Shutting down server...')
            self.httpd.shutdown()
            self.httpd.server_close()
            print('✅ Server stopped.')
    
    def _open_browser(self):
        """Open default browser after short delay."""
        time.sleep(1)
        webbrowser.open(f'http://localhost:{self.port}')
    
    @classmethod
    def quick_serve(cls, 
                   port: int = 8000,
                   directory: Optional[str] = None,
                   service_name: str = "Quick HTTP Server") -> bool:
        """
        Quick way to start a simple HTTP server.
        
        Args:
            port: Port to use
            directory: Directory to serve
            service_name: Service name for logging
            
        Returns:
            True if server started successfully
        """
        server = cls(port=port)
        return server.start(working_directory=directory, service_name=service_name)


def create_cors_handler(base_handler_class: Optional[Callable] = None) -> type:
    """
    Create a CORS-enabled HTTP request handler.
    
    Args:
        base_handler_class: Base handler class to extend
        
    Returns:
        CORS-enabled handler class
    """
    if base_handler_class is None:
        base_handler_class = http.server.SimpleHTTPRequestHandler
    
    class CORSHandler(base_handler_class):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def do_OPTIONS(self):
            self.send_response(204)
            self.end_headers()
    
    return CORSHandler