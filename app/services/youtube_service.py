from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.integrations.youtube_integration import YoutubeIntegration
from app.models.schemas.kraken import (YoutubeClipsResponsePagination, YoutubeClipsResponse, KrakenPosted)
from app.tasks import tasks


class YoutubeServices:
    def __init__(self, kraken_clips_repo: KrakenClipsRepository):
        self.youtube_integration = YoutubeIntegration()
        self.kraken_clips_repo = kraken_clips_repo

    def get_videos(self, page_token: str) -> YoutubeClipsResponsePagination:
        videos_dict = self.youtube_integration.youtube_search(next_page_token=page_token)
        list_youtube_clip_response = []
        for clip in videos_dict['videos']:
            response_model = YoutubeClipsResponse(
                url=f"https://www.youtube.com/watch?v={clip['snippet']['resourceId']['videoId']}",
                thumbnail_url=clip['snippet']['thumbnails']['default']['url'],
                title=clip['snippet']['title'],
                clip_id=clip['id'],
                video_id=clip['snippet']['resourceId']['videoId']
            )
            list_youtube_clip_response.append(response_model)

        response = YoutubeClipsResponsePagination(youtube_response=list_youtube_clip_response,
                                                  cursor=videos_dict['next_token'])
        return response

    @staticmethod
    def crop_videos(video_url: str, start: int, end: int, caption: str, youtube_id: str):
        payload = {
            'video_url': video_url,
            'start': start,
            'end': end,
            'caption': caption,
            'youtube_id': youtube_id
        }

        tasks.cut_youtube_video.apply_async(
            args=[dict(payload)], connect_timeout=10
        )

    def get_clips(self, youtube_id: str):
        clips = self.kraken_clips_repo.get_clips(youtube_id)
        list_clip_response = []
        for clip in clips:
            response_model = YoutubeClipsResponse(
                url=clip.clip_url,
                title=clip.clip_name,
                clip_id=clip.id,
                video_id=clip.clip_id
            )
            kraken_response = []
            if len(clip.kraken) > 0:
                for kraken in clip.kraken:
                    if kraken.post_status != 'ERROR':
                        kraken_posted = KrakenPosted(
                            is_posted=True,
                            kraken_hand=kraken.kraken_hand
                        )
                        kraken_response.append(kraken_posted)
            response_model.kraken_posted = kraken_response
            list_clip_response.append(response_model)

        response = YoutubeClipsResponsePagination(youtube_response=list_clip_response)
        return response
