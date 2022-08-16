from typing import List

import tweepy

from app.config.logger import Logger


logging = Logger.get_logger("Twitter")


class TwitterIntegration:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        oauth_token: str,
        oauth_secret: str,
    ) -> None:
        super().__init__()
        auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=oauth_token,
            access_token_secret=oauth_secret,
        )
        self.twitter = tweepy.API(auth)

    def search_users(self, q, page=1):
        result = self.twitter.search_users(q=f"{q}", page=page)
        return result

    def search_tweets(self, q, count=100, result_type="mixed"):
        place_id = "1b107df3ccc0aaa1"
        return self.twitter.search_tweets(
            q=f"{q} AND place:{place_id}", count=count, result_type=result_type
        )

    def send_message(self, message: str, user_id: str) -> bool:
        try:
            self.twitter.send_direct_message(user_id, message)
            return True

        except Exception:
            return False

    def post_media(self, clip_path: str, status: str) -> bool:
        try:
            upload_result = self.twitter.media_upload(filename=clip_path, chunked=True)
            self.twitter.update_status(
                status=status, media_ids=[upload_result.media_id_string]
            )
            return True
        except Exception as ex:
            logging.info(ex)
            return False

    def follow_user(self, user_id: int):
        return self.twitter.create_friendship(user_id=user_id)

    def get_followers(self):
        return self.twitter.get_follower_ids()

    def get_trending(self):
        brazil_woe_id = 23424768

        brazil_trends = self.twitter.get_place_trends(brazil_woe_id)

        return brazil_trends[0]["trends"]

    @staticmethod
    def filter_trends(trends, parameter_repo):
        trends_filtered = []
        parameters = parameter_repo.get_parameters()
        discarded_words = [
            x.value.split("|") for x in parameters if x.name == "discarded_words"
        ]
        for trend in trends:
            for discarded_word in discarded_words:
                if trend not in discarded_word:
                    trends_filtered.append(trend)

        return trends_filtered
