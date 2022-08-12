import logging

from app.config.logger import Logger
from app.db.repositories.kraken_clips_repository import KrakenClipsRepository
from app.models.schemas.kraken import (TwitchClipsResponse, TwitchClipsResponsePagination, KrakenPosted)
from app.integrations.twitch_integration import TwitchIntegration


class TwitchServices:
    def __init__(self, kraken_clips_repo: KrakenClipsRepository):
        self.twitch_integration = TwitchIntegration()
        self.kraken_clips_repo = kraken_clips_repo
        self.logging = Logger.get_logger("Tasks")

    def get_clips(self, next_cursor: str = None, back_cursor: str = None) -> TwitchClipsResponsePagination:
        clips = self.twitch_integration.get_all_clips(after_cursor=next_cursor, back_cursor=back_cursor)
        list_twitch_clip_response = []
        for clip in clips['data']:
            response_model = TwitchClipsResponse(**clip)
            response_model.clip_id = clip['id']
            clip_stored = self.kraken_clips_repo.get_clips_by_clip_id(clip['id'])
            kraken_response = []
            if len(clip_stored) > 0:
                for clip in clip_stored:
                    if len(clip.kraken) > 0: # kraken e twitch clips é one-to-one
                        if clip.kraken[0].post_status != 'ERROR':
                            kraken_posted = KrakenPosted(
                                is_posted=True,
                                kraken_hand=clip.kraken[0].kraken_hand
                            )
                            kraken_response.append(kraken_posted)
            response_model.kraken_posted = kraken_response
            list_twitch_clip_response.append(response_model)

        response = TwitchClipsResponsePagination(twitch_response=list_twitch_clip_response, cursor=clips['pagination']['cursor'])
        return response
