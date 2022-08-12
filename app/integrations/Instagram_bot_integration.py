from app.integrations.InstagramAPI import InstagramAPI


class InstagramBotIntegration:
    def __init__(self, username: str, password: str) -> None:
        super().__init__()
        self.client = InstagramAPI(username, password)
        self.client.login()

    def get_users_by_tag(self, tag) -> dict:
        self.client.tagFeed(tag)
        users = self.client.LastJson
        return users['items']

    def follow_user(self, user_id):
        return self.client.follow(user_id)

    def get_followers(self):
        users = self.client.getTotalSelfFollowers()
        return [int(x['pk']) for x in users]
