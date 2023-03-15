import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def start_service():
    scheduler = AsyncIOScheduler() 
    scheduler.add_job(service, "interval", seconds=5, args=["Hello World!"])
    scheduler.start()

async def service(data=None):
    rows = [1,2,3,4,5,6,7,8,9,10]
    for row in rows:
        print(str(row) + f" {data}") 

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_service())
    loop.run_forever()