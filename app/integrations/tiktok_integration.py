import requests
from app.db.repositories.tiktok_tasks_repository import TiktokTasksRepository


class TiktokIntegration:
    def __init__(self, tiktok_repo: TiktokTasksRepository, video_path: str = None, caption: str = None) -> None:
        super().__init__()
        self.tiktok_repo = tiktok_repo
        self.video_path = video_path
        self.caption = caption
        self.url = 'https://open-api.tiktok.com/'

    def post_media(self):
        connection_params = self.tiktok_repo.get_task_by_tiktok_handle("vamos_joojar")
        files = {'video': open(self.video_path, 'rb')}

        response = requests.post(
            f'{self.url}share/video/upload/?access_token={connection_params.access_token}&open_id={connection_params.open_id}',
            files=files
        )
        return response

    def refresh_token(self):
        connection_params = self.tiktok_repo.get_task_by_tiktok_handle("vamos_joojar")
        response = requests.get(f'{self.url}oauth/refresh_token/?client_key={connection_params.client_key}&grant_type=refresh_token&refresh_token={connection_params.refresh_token}')
        return response.json().get('data')
