from app.config.logger import Logger
from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.db.repositories.kraken_repository import KrakenRepository
from app.models.schemas.common.paginated import Paginated
from app.models.schemas.kraken import (TwitchClipsResponse, TwitchClipsResponsePagination, KrakenPosted)
from app.integrations.twitch_integration import TwitchIntegration


class TwitchServices:
    def __init__(self, kraken_clips_repo: KrakenClipsRepository, kraken_repo: KrakenRepository):
        self.twitch_integration = TwitchIntegration()
        self.kraken_clips_repo = kraken_clips_repo
        self.kraken_repo = kraken_repo
        self.logging = Logger.get_logger("Tasks")

    def get_clips(self, page: int) -> Paginated[TwitchClipsResponse]:
        clips = self.kraken_clips_repo.get_clips_by_kraken_head(page=page, page_size=8, kraken_head='TWITCH')
        list_clip_response = []
        for clip in clips.items:
            response_model = TwitchClipsResponse(
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

