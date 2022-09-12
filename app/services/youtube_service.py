from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.integrations.youtube_integration import YoutubeIntegration
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import (YoutubeClipsResponsePagination, YoutubeClipsResponse, KrakenPosted)
from app.tasks import tasks


class YoutubeServices:
    def __init__(self, kraken_clips_repo: KrakenClipsRepository, kraken_repo: KrakenRepository):
        self.youtube_integration = YoutubeIntegration()
        self.kraken_clips_repo = kraken_clips_repo
        self.kraken_repo = kraken_repo

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

    def get_all_clips(self, page) -> Paginated[YoutubeClipsResponse]:
        clips = self.kraken_clips_repo.get_clips_by_kraken_head(page=page, page_size=8, kraken_head='YOUTUBE')
        list_clip_response = []
        for clip in clips.items:
            response_model = YoutubeClipsResponse(
                id=clip.id,
                url=clip.clip_url,
                title=clip.clip_name,
                clip_id=clip.id,
                video_id=clip.clip_id
            )
            clip_stored = self.kraken_repo.get_by_clip_id(clip.id)
            kraken_response = []
            if len(clip_stored) > 0:
                for clip in clip_stored:
                    if clip.post_status != 'ERROR':
                        kraken_posted = KrakenPosted(
                            is_posted=True,
                            kraken_hand=clip.kraken_hand
                        )
                        kraken_response.append(kraken_posted)
            response_model.kraken_posted = kraken_response
            list_clip_response.append(response_model)

        return Paginated(
            total_items=clips.total_items,
            total_pages=clips.total_pages,
            current_page=clips.current_page,
            items=list_clip_response
        )
