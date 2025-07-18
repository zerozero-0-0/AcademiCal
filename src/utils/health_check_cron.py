import schedule
import time
import requests
import threading
from datetime import datetime
import os

# ヘルスチェックURL（環境変数または既定値）
HEALTH_CHECK_URL = os.getenv("HEALTH_CHECK_URL", "http://localhost:8000")

def health_check():
    """ヘルスチェックを実行する関数"""
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"🔍 [{now}] ヘルスチェック実行中... ({HEALTH_CHECK_URL})")
        
        # HTTPリクエストを送信（タイムアウト設定）
        response = requests.get(HEALTH_CHECK_URL, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ [{now}] ヘルスチェック成功: {response.status_code}")
        else:
            print(f"⚠️ [{now}] ヘルスチェック失敗: {response.status_code}")
            
    except requests.exceptions.Timeout:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"⏰ [{now}] ヘルスチェックタイムアウト")
    except requests.exceptions.ConnectionError:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"🔌 [{now}] ヘルスチェック接続エラー")
    except Exception as error:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"❌ [{now}] ヘルスチェックエラー: {error}")

def start_health_check_cron():
    """1時間ごとにヘルスチェックの定期実行を開始"""
    # 1時間ごとにヘルスチェックを実行
    schedule.every().hour.do(health_check)
    
    print("🕐 ヘルスチェックの定期実行を開始しました (1時間間隔)")
    
    def run_scheduler():
        """スケジューラーを実行する関数"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにスケジュールをチェック
    
    # バックグラウンドスレッドでスケジューラーを実行
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    return scheduler_thread

def start_health_check_cron_10min():
    """10分ごとにヘルスチェックの定期実行を開始（元のコードと同じ間隔）"""
    # 10分ごとにヘルスチェックを実行
    schedule.every(10).minutes.do(health_check)
    
    print("🕐 ヘルスチェックの定期実行を開始しました (10分間隔)")
    
    def run_scheduler():
        """スケジューラーを実行する関数"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1分ごとにスケジュールをチェック
    
    # バックグラウンドスレッドでスケジューラーを実行
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    return scheduler_thread

# テスト実行用
if __name__ == "__main__":
    print("ヘルスチェッククロンジョブをテスト実行中...")
    
    # 1時間ごとのテスト
    start_health_check_cron()
    
    # または10分ごとのテスト
    # start_health_check_cron_10min()
    
    try:
        print("クロンジョブが実行中です。Ctrl+Cで停止できます。")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止シグナルを受信しました")
        print("クロンジョブを停止しました")
