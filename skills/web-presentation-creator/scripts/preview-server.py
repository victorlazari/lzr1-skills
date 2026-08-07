#!/usr/bin/env python3
# A simple local server to preview the generated landing page before delivery.

import http.server
import socketserver
import sys
import os

PORT = 8000

if len(sys.argv) > 1:
    directory = sys.argv[1]
    if os.path.isdir(directory):
        os.chdir(directory)
    else:
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
