import time
import schedule
import threading
from module import crawl_data
from fastapi import FastAPI

app = FastAPI()


def run_schedule():
    schedule.every(5).minutes.do(crawl_data)

    while True:
        schedule.run_pending()
        time.sleep(1)


@app.on_event("startup")
async def startup():
    # first run
    crawl_data()

    threading.Thread(target=run_schedule).start()


@app.post("/crawl")
async def read_item():
    crawl_data()
    return {"status": "success"}
