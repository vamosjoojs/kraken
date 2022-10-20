import requests
import json

from app.config.config import config
from app.config.logger import Logger

logging = Logger.get_logger("graph api")


class InstagramGraphIntegration:
    def __init__(self, video_path, caption) -> None:
        super().__init__()
        self.video_path = video_path
        self.caption = caption

    def create_container_instagram_graph_api(self) -> str:
        post_url = f"https://graph.facebook.com/v14.0/{config.INSTA_USERID}/media"
        payload = {
            "media_type": "REELS",
            "video_url": self.video_path,
            "caption": self.caption,
            "access_token": config.INSTA_ACCESS_TOKEN,
        }
        r = requests.post(post_url, data=payload)
        logging.info(r.status_code)
        logging.info(r.text)
        return json.loads(r.text)['id']

    def verify_container_id(self, container_id: str):
        verify_url = f"https://graph.facebook.com/{container_id}?fields=status_code&access_token={config.INSTA_ACCESS_TOKEN}"
        r = requests.get(verify_url)
        return json.loads(r.text)['status_code']

    def post_media(self, container_id: str):
        second_url = "https://graph.facebook.com/v14.0/{}/media_publish".format(
            config.INSTA_USERID
        )
        second_payload = {
            "creation_id": container_id,
            "access_token": config.INSTA_ACCESS_TOKEN,
        }
        r = requests.post(second_url, data=second_payload)