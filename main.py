from src.database import DB_Connect
from src.bot import MakeClient
from server import run_health_server

def main(): 
    run_health_server()
    DB_Connect()
    
    client = MakeClient()
    client.run_bot()

if __name__ == "__main__":
    main()
