import shutil
import uuid
from typing import Tuple

from app.config.config import config

from googleapiclient.discovery import build
import yt_dlp
import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from app.services.clients.s3 import S3Service


class YoutubeIntegration:
    def __init__(self) -> None:
        super().__init__()

        self.youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)
        self.channel_id = config.YOUTUBE_CHANNEL_ID
        self.output_path = os.path.join(os.getcwd(), 'download')

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def youtube_search(self, next_page_token: str = None, max_results: int = 8) -> dict:
        res = self.youtube.channels().list(
            id=self.channel_id,
            part='contentDetails'
        ).execute()

        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        res = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                part='snippet',
                                                pageToken=next_page_token,
                                                maxResults=max_results).execute()

        next_page_token = res.get('nextPageToken')

        return {'videos': res['items'], 'next_token': next_page_token}

    def download_video(self, video_url) -> str:
        video_path = os.path.join(self.output_path, f'{str(uuid.uuid4())}.mp4')
        ydl_opts = {
            'outtmpl': video_path,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return video_path

    def custom_crop(self, video_path, start_time, end_time) -> Tuple[str, str]:
        output_path = os.path.join(self.output_path, f'{str(uuid.uuid4())}.mp4')
        thumbnail_path = os.path.join(self.output_path, f'{str(uuid.uuid4())}.jpeg')
        self.clip = VideoFileClip(video_path)
        self.clip.save_frame(thumbnail_path, t=5.00)
        self.clip = self.clip.subclip(t_start=start_time, t_end=end_time)
        self.clip.write_videofile(filename=output_path, audio_codec='aac')

        video_filename = video_path.split('\\')[-1]
        s3 = S3Service()
        s3_url = s3.upload_file(output_path, video_filename)
        s3_thumb_url = s3.upload_file(thumbnail_path, f'{str(uuid.uuid4())}.jpeg')

        # remover arquivos dps
        # shutil.rmtree(output_path)

        return s3_url, s3_thumb_url
