import os
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime

# ヘルスチェックURL（環境変数または既定値）
PORT = os.getenv("PORT", "8000")
HEALTH_CHECK_URL = os.getenv("HEALTH_CHECK_URL", f"http://localhost:{PORT}")


def health_check():
    """ヘルスチェックを実行する関数"""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔍 [{now}] ヘルスチェック実行中... ({HEALTH_CHECK_URL})")

        # HTTPリクエストを送信（urllib使用でライブラリ依存なし）
        req = urllib.request.Request(HEALTH_CHECK_URL)
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()

            if status_code == 200:
                print(f"✅ [{now}] ヘルスチェック成功: {status_code}")
            else:
                print(f"⚠️ [{now}] ヘルスチェック失敗: {status_code}")

    except urllib.error.HTTPError as error:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"⚠️ [{now}] ヘルスチェック失敗: {error.code}")
    except urllib.error.URLError as error:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔌 [{now}] ヘルスチェック接続エラー: {error.reason}")
    except Exception as error:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"❌ [{now}] ヘルスチェックエラー: {error}")


def start_health_check_cron():
    """1時間ごとにヘルスチェックの定期実行を開始"""
    print("🕐 ヘルスチェックの定期実行を開始しました (1時間間隔)")

    def run_cron():
        """クロンジョブを実行する関数"""
        while True:
            health_check()
            # 1時間（3600秒）待機
            time.sleep(3600)

    # バックグラウンドスレッドでクロンジョブを実行
    cron_thread = threading.Thread(target=run_cron, daemon=True)
    cron_thread.start()

    return cron_thread


def start_health_check_cron_10min():
    """10分ごとにヘルスチェックの定期実行を開始（元のコードと同じ間隔）"""
    print("🕐 ヘルスチェックの定期実行を開始しました (10分間隔)")

    def run_cron():
        """クロンジョブを実行する関数"""
        while True:
            health_check()
            # 10分（600秒）待機
            time.sleep(600)

    # バックグラウンドスレッドでクロンジョブを実行
    cron_thread = threading.Thread(target=run_cron, daemon=True)
    cron_thread.start()

    return cron_thread


# テスト実行用
if __name__ == "__main__":
    print("ヘルスチェッククロンジョブをテスト実行中...")

    # 1時間ごとのテスト（テスト用に短縮）
    print("テストモード: 30秒間隔でヘルスチェックを実行します")

    def test_cron():
        while True:
            health_check()
            time.sleep(30)  # テスト用に30秒間隔

    test_thread = threading.Thread(target=test_cron, daemon=True)
    test_thread.start()

    try:
        print("クロンジョブが実行中です。Ctrl+Cで停止できます。")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止シグナルを受信しました")
        print("クロンジョブを停止しました")
