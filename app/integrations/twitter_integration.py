import tweepy
from app.config.config import config


class TwitterIntegration:
    def __init__(self) -> None:
        super().__init__()
        auth = tweepy.OAuth1UserHandler(consumer_key=config.CONSUMER_KEY,
                                        consumer_secret=config.CONSUMER_SECRET,
                                        access_token=config.OAUTH_TOKEN,
                                        access_token_secret=config.OAUTH_SECRET
            )
        self.twitter = tweepy.API(auth)

    def search_tweets(self, q, count=100, result_type="mixed"):
        place_id = '1b107df3ccc0aaa1'
        result = self.twitter.search_tweets(q=f"{q} AND place:{place_id}", count=count, result_type=result_type)
        return result

    # def get_trending_topics(self) -> str:
    #     place_brazil = self.twitter.trends.place(_id=23424768)
    #     max_tweet_volume = max([x['tweet_volume'] for x in place_brazil[0]['trends'] if x['tweet_volume'] is not None])
    #     trending_target = ''.join([x['name'] for x in place_brazil[0]['trends'] if x['tweet_volume'] == max_tweet_volume])
    #     return trending_target

    def send_message(self, message: str, user_id: str) -> bool:
        try:
            self.twitter.send_direct_message(user_id, message)
            return True

        except Exception as ex:
            print(f"mensagem não enviada: {ex}")
            return False


