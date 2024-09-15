import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def sample_job(i):
    print("Hello, world, from job", i)


# start a job in 2 seconds - pass timestamp and timezone


# from apscheduler.schedulers.asyncio import AsyncIOScheduler
#
# scheduler: AsyncIOScheduler = app.scheduler.core
#
# scheduler.add_job(self.send_random_item, "interval", hours=1, kwargs={"app": app, "chat_id": chat_id})
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.start()
    import datetime

    current_time = datetime.datetime.now()

    # user time zone according to system:
    import pytz

    local_timezone = "Europe/Moscow"
    tz = pytz.timezone(local_timezone)

    target_time = "22:50"
    target_timestamp = tz.localize(datetime.datetime.strptime(target_time, "%H:%M"))
    print("Current time:", current_time)
    print("Target time:", target_timestamp)
    # scheduler.add_job(sample_job, "interval", seconds=1, args=(1,))
    # scheduler.add_job(sample_job, "interval", seconds=1, args=(2,))
    # scheduler.add_job(sample_job, "interval", seconds=1, args=(3,))
    # scheduler.add_job(sample_job, "interval", seconds=1, args=(4,))
    # scheduler.add_job(sample_job, "interval", seconds=1, args=(5,))
    # await asyncio.sleep(10)
    # scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
