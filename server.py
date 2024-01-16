import http.server
import socketserver
import os

PORT = 8080


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        file_path = "." + self.path.split("?")[0]
        if self.headers.get("HX-Request") == "true":
            file_path += "_partial"
        file_path += ".html"

        print(file_path)

        if os.path.isfile(file_path):
            # Open and read the file
            with open(file_path, "rb") as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
