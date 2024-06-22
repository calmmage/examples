from bot_lib import Handler
from calmapp import App


class MyHandler(Handler):
    commands = {
        "setup_scheduled_reminders": "setup_reminders",
        "stop_reminders": "stop_reminders",
    }

    async def setup_scheduled_reminders(self, message, app: App):
        # use app scheduler to schedule reminders - send a message evey second
        chat_id = message.chat.id

        assert app.scheduler is not None
        # todo: store jobs in db for persistence
        job_id = chat_id  # generate id?

        app.scheduler.core.add_job(
            self.send_safe,
            "interval",
            seconds=1,
            kwargs=dict(text="Reminder!", chat_id=chat_id),
            id=job_id,
        )

    async def stop_reminders(self, message, app: App):
        # stop reminders
        chat_id = message.chat.id
        assert app.scheduler is not None
        job_id = chat_id
        app.scheduler.core.remove_job(job_id)
        await self.answer_safe(message, "Reminders stopped")
