import time

from app.db.repositories.parameters_repository import ParametersRepository
from app.db.repositories.reddit_send_message_repository import RedditSendMessageRepository
from app.db.repositories.reddit_tasks_repository import RedditTasksRepository
from app.integrations.reddit_integration import RedditIntegration, logging
from app.models.entities import RedditSendMessage

from app.tasks import tasks
from app.tasks.reddit_task.tools import get_reddit_send_message_params, get_reddit_users_to_send


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
        # tasks.reddit_send_message.apply_async(connect_timeout=10)
        reddit_repository = self.reddit_send_message_repo
        reddit_tasks_repo = self.reddit_tasks_repo
        tasks_send_message = reddit_tasks_repo.get_tasks()
        parameter_repo = self.parameter_repo

        messages_per_hour, sleep_per_send, users_per_round = get_reddit_send_message_params(
            parameter_repo
        )

        for task in tasks_send_message:
            reddit_integration = RedditIntegration(
                task.client_id, task.client_secret, task.username, task.password
            )

            stored_users = reddit_repository.get_users_by_reddit_handle(task.reddit_handle)
            stored_users_ids = [x.user_id for x in stored_users]
            sended_users = []
            logging.info(f"Reddit: {task.reddit_handle}")
            logging.info(f"Reddit: Usuários já enviados: {len(stored_users_ids)}")

            users_to_send = get_reddit_users_to_send(
                task.reddit_messages.tag.split("|"),
                reddit_integration,
                stored_users_ids,
                users_per_round
            )
            logging.info(f"Reddit: Localizado: {len(users_to_send)} usuários para o envio.")
            sended_count = 0
            not_sended_count = 0
            for user_id in users_to_send:
                if len(sended_users) == messages_per_hour:
                    break

                sended = reddit_integration.send_message(
                    user_id, task.reddit_messages.message
                )
                reddit_orm = RedditSendMessage(
                    user_id=user_id, sended=True, reddit_handle=task.reddit_handle
                )
                if sended:
                    sended_users.append(user_id)
                    time.sleep(sleep_per_send)
                    sended_count += 1
                else:
                    reddit_orm.sended = False
                    not_sended_count += 1

                reddit_repository.add(reddit_orm)

            logging.info(
                f"Reddit: Mensagens enviados: {str(sended_count)}, Mensagens não enviadas: {str(not_sended_count)}"
            )
