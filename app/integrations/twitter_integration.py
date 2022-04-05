import tweepy


class TwitterIntegration:
    def __init__(self, consumer_key: str, consumer_secret: str, oauth_token: str, oauth_secret: str) -> None:
        super().__init__()
        auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key,
                                        consumer_secret=consumer_secret,
                                        access_token=oauth_token,
                                        access_token_secret=oauth_secret
            )
        self.twitter = tweepy.API(auth)

    def search_users(self, q, page=1):
        result = self.twitter.search_users(q=f"{q}", page=page)
        return result
    
    def search_tweets(self, q, count=100, result_type="mixed"):

        place_id = '1b107df3ccc0aaa1'

        result = self.twitter.search_tweets(q=f"{q} AND place:{place_id}", count=count, result_type=result_type)
        
    def send_message(self, message: str, user_id: str) -> bool:
        try:
            self.twitter.send_direct_message(user_id, message)
            return True

        except Exception as ex:
            print(f"mensagem não enviada: {ex}")
            return False


