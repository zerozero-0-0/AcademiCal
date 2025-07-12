from http.server import HTTPServer, BaseHTTPRequestHandler
import threading


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")


def start_health_server():
    server = HTTPServer(("0.0.0.0", 8000), HealthHandler)
    server.serve_forever()


# Discordボット起動前に実行
threading.Thread(target=start_health_server, daemon=True).start()
