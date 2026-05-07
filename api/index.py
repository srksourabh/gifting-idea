"""Legacy /api/index endpoint.

The frontend now lives in public/index.html and is served by Vercel directly
from the public/ directory. This handler exists only to redirect any stale
links pointing at /api/index back to the root.
"""

from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(301)
        self.send_header("Location", "/")
        self.end_headers()
