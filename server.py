import json
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthCheckHandler(BaseHTTPRequestHandler):
    """ヘルスチェック用のHTTPリクエストハンドラー"""

    def do_GET(self):
        """GETリクエストの処理"""
        if self.path == "/":
            self.send_health_response()
        else:
            self.send_error(404, "Not Found")

    def send_health_response(self):
        """ヘルスチェックレスポンスを送信（Honoスタイル）"""
        try:
            # Honoのレスポンスと同じ形式
            response_data = {
                "status": "ok",
                "message": "Discord Bot is running",
                "python_version": sys.version.split()[0],  # "3.11.0" 形式
                "timestamp": datetime.now().isoformat(),
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode("utf-8"))

        except Exception as e:
            error_response = {
                "status": "error",
                "message": f"Health check failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            }
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error_response, indent=2).encode("utf-8"))

    def log_message(self, format, *args):
        """ログメッセージの出力をカスタマイズ（簡潔にする）"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] HTTP: {format % args}")


class HealthCheckServer:
    """ヘルスチェック用HTTPサーバー"""

    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        """サーバーを開始"""
        try:
            self.server = HTTPServer(("0.0.0.0", self.port), HealthCheckHandler)
            self.thread = threading.Thread(
                target=self.server.serve_forever, daemon=True
            )
            self.thread.start()
            print(f"ヘルスチェックサーバーがポート {self.port} で開始されました")
            print(f"ヘルスチェック: http://localhost:{self.port}/")
        except Exception as e:
            print(f"ヘルスチェックサーバーの開始に失敗しました: {e}")

    def stop(self):
        """サーバーを停止"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("ヘルスチェックサーバーを停止しました")


def create_health_server(port=8080):
    """ヘルスチェックサーバーを作成して返す"""
    return HealthCheckServer(port)


# 単体実行時のテスト
if __name__ == "__main__":
    print("ヘルスチェックサーバーをテスト実行中...")
    health_server = create_health_server(8080)
    health_server.start()

    try:
        print("サーバーが実行中です。Ctrl+Cで停止できます。")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止シグナルを受信しました")
        health_server.stop()
        print("サーバーを停止しました")
