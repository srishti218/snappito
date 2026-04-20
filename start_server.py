import http.server
import os

class SmartHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Split off query string before file resolution
        path_only = self.path.split('?')[0]
        base, ext = os.path.splitext(path_only)
        if not ext and not path_only.endswith('/'):
            if os.path.exists(path_only.strip('/') + '.html'):
                self.path = path_only + '.html' + (
                    ('?' + self.path.split('?', 1)[1]) if '?' in self.path else ''
                )
        return super().do_GET()

if __name__ == "__main__":
    # Ensure we are serving the directory where this script is located
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Starting frontend server on port 8000 from {os.getcwd()}...")
    http.server.test(HandlerClass=SmartHandler, port=8000)
