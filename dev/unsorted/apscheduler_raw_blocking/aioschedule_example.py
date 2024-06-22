from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# The "apscheduler." prefix is hard coded
# scheduler = BackgroundScheduler({
#     # 'apscheduler.jobstores.mongo': {
#     #      'type': 'mongodb'
#     # },
#     # 'apscheduler.jobstores.default': {
#     #     'type': 'sqlalchemy',
#     #     'url': 'sqlite:///jobs.sqlite'
#     # },
#     # 'apscheduler.executors.default': {
#     #     'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
#     #     'max_workers': '20'
#     # },
#     # 'apscheduler.executors.processpool': {
#     #     'type': 'processpool',
#     #     'max_workers': '5'
#     # },
#     # 'apscheduler.job_defaults.coalesce': 'false',
#     # 'apscheduler.job_defaults.max_instances': '3',
#     # 'apscheduler.timezone': 'UTC',
# })

scheduler = BlockingScheduler()
i = 0


def myfunc():
    global i
    i += 1
    print("Hello world", i)


if __name__ == "__main__":

    scheduler.add_job(myfunc, "interval", seconds=2, id="my_job_id")
    scheduler.start()
