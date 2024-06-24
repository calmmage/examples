from bot_lib.utils import setup_bot
from calmapp import App
from dev.unsorted.apscheduler_async_tgbot.lib import MyHandler

# bot = create_bot()
handlers = [MyHandler()]
app = App(enable_scheduler=True)
dp, bot = setup_bot(app, handlers=handlers)

if __name__ == "__main__":
    app.run(dp, bot)
