import requests

from app.config.config import config


class TiktokIntegration:
    def __init__(self, video_path, caption) -> None:
        super().__init__()
        self.video_path = video_path
        self.caption = caption
        self.url = 'https://open-api.tiktok.com/share/video/upload/'

    def post_media(self):
        status_code = requests.post(
            f'{self.url}?access_token={config.TIKTOK_ACCESS_TOKEN}&open_id={config.TIKTOK_OPEN_ID}',
            data={
                'video': self.video_path
            }
        )
        return status_code
