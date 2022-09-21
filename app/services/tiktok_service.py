from app.config.logger import Logger
from app.db.repositories.tiktok_tasks_repository import TiktokTasksRepository
from app.integrations.tiktok_integration import TiktokIntegration

logging = Logger.get_logger("Tiktok")


class TiktokServices:
    def __init__(
        self,
        tiktok_repo: TiktokTasksRepository,

    ):
        self.tiktok_repo = tiktok_repo

    def post_clip(self, caption, video_path) -> bool:
        logging.info(f'video path {video_path}')
        tiktok_integration = TiktokIntegration(video_path=video_path, caption=caption, tiktok_repo=self.tiktok_repo)
        logging.info('Começando integração com o tiktik')
        status_code = tiktok_integration.post_media()
        logging.info(status_code)
        if status_code != 200:
            return True
        return False

    def refresh_token(self):
        tiktok_integration = TiktokIntegration(tiktok_repo=self.tiktok_repo)
        refresh_data = tiktok_integration.refresh_token()
        if refresh_data:
            old_data = self.tiktok_repo.get_task_by_tiktok_handle("vamos_joojar")

            self.tiktok_repo.update_message_task(
                id=old_data.id,
                access_token=refresh_data["access_token"],
                refresh_token=refresh_data["refresh_token"],
                expires_in=refresh_data["expires_in"]
            )
