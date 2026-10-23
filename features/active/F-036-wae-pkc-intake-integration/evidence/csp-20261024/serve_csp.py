from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os, sys
ROOT=sys.argv[1]; PORT=int(sys.argv[2]); CSP=sys.argv[3]
class H(SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def end_headers(self):
        self.send_header('Content-Security-Policy', CSP)
        super().end_headers()
    def log_message(self,*a): pass
ThreadingHTTPServer(('127.0.0.1',PORT),H).serve_forever()
