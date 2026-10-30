import http.server
import socketserver
import os

# Render កំណត់ Port ដោយស្វ័យប្រវត្តិ ដូច្នេះយើងត្រូវប្រើ os.environ.get("PORT", 8000)
PORT = int(os.environ.get("PORT", 8000))
DIRECTORY = "uploads"

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-File-Name, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        filename = self.headers.get('X-File-Name', 'video.mp4')
        file_path = os.path.join(DIRECTORY, filename)
        
        try:
            # អាននិងសរសេរទិន្នន័យម្ដង ១មេកាបៃ (1MB) ដើម្បីការពារកុំឱ្យ Server គាំង RAM
            with open(file_path, 'wb') as f:
                remaining = content_length
                chunk_size = 1024 * 1024  # 1MB
                while remaining > 0:
                    read_len = min(remaining, chunk_size)
                    chunk = self.rfile.read(read_len)
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # ส่ง URL กลับไป (ពេល Deploy នៅលើ Render វានឹងប្រើ Domain របស់ Render)
            response = f'{{"status": "success", "filename": "{filename}"}}'
            self.wfile.write(response.encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print(f"🚀 Server កំពុងរត់លើ Port {PORT}")
    httpd.serve_forever()