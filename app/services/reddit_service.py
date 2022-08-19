from app.db.repositories.parameters_repository import ParametersRepository
from app.db.repositories.reddit_send_message_repository import RedditSendMessageRepository
from app.db.repositories.reddit_tasks_repository import RedditTasksRepository

from app.tasks import tasks


class RedditServices:
    def __init__(
        self,
        reddit_tasks_repo: RedditTasksRepository,
        reddit_send_message_repo: RedditSendMessageRepository,
        parameter_repo: ParametersRepository
    ):
        self.reddit_tasks_repo = reddit_tasks_repo
        self.reddit_send_message_repo = reddit_send_message_repo
        self.parameter_repo = parameter_repo

    def trigger_send_message(
        self,
    ):
        tasks.reddit_send_message.apply_async(connect_timeout=10)
