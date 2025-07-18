from cron import start_health_check_cron
from server import create_health_server
from src.bot import MakeClient
from src.database import DB_Connect
from src.utils.scheduler import scheduler


def main():
    health_server = create_health_server(8000)
    health_server.start()

    # ヘルスチェッククロンジョブを開始
    start_health_check_cron()

    DB_Connect()

    client = MakeClient()
    client.run_bot()
    s = scheduler()
    print(s)


if __name__ == "__main__":
    main()
