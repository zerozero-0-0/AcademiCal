from cron import start_health_check_cron
from server import create_health_server
from src.bot.client import MakeClient
from src.database.connection import DB_Connect


def main():
    health_server = create_health_server(8000)
    health_server.start()

    # ヘルスチェッククロンジョブを開始
    start_health_check_cron()

    DB_Connect()

    client = MakeClient()
    client.run_bot()

if __name__ == "__main__":
    main()
