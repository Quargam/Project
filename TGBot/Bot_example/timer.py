import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def send_channel():
    await bot.send_message(chat_id=-1001529216403, text= str(datetime.datetime.now()))

def timer():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_channel, 'interval', seconds=60)
    scheduler.start()