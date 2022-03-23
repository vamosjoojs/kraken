from twitchAPI.twitch import Twitch
from app.config.config import config
import os
import uuid
from urllib import request


class TwitchIntegration:
    def __init__(self) -> None:
        super().__init__()
        self.twitch = Twitch(config.TWITCH_APP_ID, config.TWITCH_APP_SECRET)

    def get_all_clips(self, after_cursor=None, back_cursor=None):
        clips = self.twitch.get_clips(broadcaster_id='736977657', first=8, after=after_cursor, before=back_cursor)
        return clips

    @staticmethod
    def download_clip(thumbnail) -> str:
        clip_url = thumbnail.split("-preview", 1)[0] + ".mp4"
        clip_name = f'{str(uuid.uuid4())}.mp4'
        output_path = os.path.join(os.getcwd(), 'downloads')

        if not os.path.exists(output_path):
            os.mkdir(output_path)
        request.urlretrieve(clip_url, os.path.join(output_path, clip_name))
        return os.path.join(output_path, clip_name)
