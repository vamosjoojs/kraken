import requests
import os
from app.db.repositories.tiktok_tasks_repository import TiktokTasksRepository


class TiktokIntegration:
    def __init__(self, tiktok_repo: TiktokTasksRepository, video_path: str = None, caption: str = None) -> None:
        super().__init__()
        self.tiktok_repo = tiktok_repo
        self.video_path = video_path
        self.caption = caption
        self.url = 'https://open.tiktokapis.com/v2/'

    def post_media(self):
        connection_params = self.tiktok_repo.get_task_by_tiktok_handle("vamos_joojar")
        file_stats = os.stat(self.video_path)
        source = {'source_info':
            {
                "source": "FILE_UPLOAD",
                "video_size": file_stats.st_size,
                "chunk_size": file_stats.st_size,
                "total_chunk_count": 1
            }
        }

        headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {connection_params.access_token}',
        }

        response = requests.post(
            f'{self.url}post/publish/inbox/video/init/',
            json=source,
            headers=headers
        )

        if response.json()['error']['code'] == 'ok':
            headers = {
                'Content-Range': f'bytes 0-{file_stats.st_size-1}/{file_stats.st_size}',
                'Content-Type': 'video/mp4',
            }
            upload_url = response.json()['data']['upload_url']
            response = requests.put(url=upload_url,
                                    headers=headers,
                                    data=open(self.video_path, 'rb'))

        return response.status_code

    def refresh_token(self):
        connection_params = self.tiktok_repo.get_task_by_tiktok_handle("vamos_joojar")
        response = requests.get(
            f'{self.url}oauth/refresh_token/?client_key={connection_params.client_key}&grant_type=refresh_token&refresh_token={connection_params.refresh_token}')
        return response.json().get('data')
