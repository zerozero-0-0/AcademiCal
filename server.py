from threading import Thread
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
async def health():
    return "OK"

def start():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
    
def run_health_server():
    t = Thread(target=start,daemon=True)
    t.start()

