#!/usr/bin/env python3
"""
Server HTTP semplice per servire il sito di test.
Supporta range requests per i PDF e routing dinamico.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8001
DIRECTORY = Path(__file__).parent

class TestSiteHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # CORS headers per permettere richieste da qualsiasi origine
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Routing dinamico per URL clean (senza .html)
        path = self.path
        
        # Mappa URL clean ai file HTML
        routes = {
            '/': '/index.html',
            '/pricing': '/company/pricing.html',
            '/careers': '/company/careers.html',
            '/case-studies': '/company/case-studies.html',
            '/tech/stack': '/tech/stack.html',
            '/tech/api': '/tech/api.html',
            '/resources/blog': '/resources/blog.html',
            '/resources/webinars': '/resources/webinars.html',
        }
        
        if path in routes:
            self.path = routes[path]
            print(f"[ROUTE] {path} → {self.path}")
        
        print(f"[REQUEST] {self.command} {self.path}")
        super().do_GET()

    def log_message(self, format, *args):
        # Log colorato
        print(f"\033[94m[SERVER]\033[0m {format % args}")

if __name__ == "__main__":
    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), TestSiteHandler) as httpd:
        print(f"\n🚀 TestSite Pro in esecuzione su http://localhost:{PORT}")
        print(f"📁 Directory: {DIRECTORY}")
        print("\nPagine disponibili:")
        print(f"  - http://localhost:{PORT}/                    (Homepage)")
        print(f"  - http://localhost:{PORT}/pricing             (Pricing dinamico)")
        print(f"  - http://localhost:{PORT}/careers             (Offerte lavoro)")
        print(f"  - http://localhost:{PORT}/case-studies        (Casi di successo)")
        print(f"  - http://localhost:{PORT}/tech/stack          (Stack tecnologico)")
        print(f"  - http://localhost:{PORT}/tech/api            (Documentazione API)")
        print(f"  - http://localhost:{PORT}/resources/blog      (Blog tecnico)")
        print(f"  - http://localhost:{PORT}/resources/webinars  (Webinar passati)")
        print(f"\n📄 PDF disponibili in /docs/")
        print("\nPremi Ctrl+C per fermare\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server fermato.")