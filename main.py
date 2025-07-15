from src.bot import MakeClient
from src.database import DB_Connect
from src.utils.scheduler import scheduler


def main():
    DB_Connect()

    client = MakeClient()
    client.run_bot()
    s = scheduler()
    print(s)


if __name__ == "__main__":
    main()
