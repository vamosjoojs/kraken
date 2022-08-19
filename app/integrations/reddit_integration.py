import time
from datetime import datetime
import praw
from app.config.logger import Logger

logging = Logger.get_logger("Reddit")


class RedditIntegration:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str

    ) -> None:
        super().__init__()
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="automations",
            username=username,
            password=password,
        )

    @staticmethod
    def iso_timestamp_from_unix_time(unix_time):
        dt = datetime.fromtimestamp(unix_time)
        return dt.isoformat()

    def scrape_subreddit(self, query, subreddit_name):
        try:
            sr = self.reddit.subreddit(display_name=subreddit_name)
            users = []
            for comment in sr.comments(limit=600):
                if comment.author:
                    if comment.author.name not in users:
                        users.append(comment.author.name)
            return users
        except Exception as ex:
            logging.error(ex)

    def get_users(self, query: str, subreddit_names: str):
        return self.scrape_subreddit(query, subreddit_names)

    def try_posting(self, username, subject, message):
        try:
            self.reddit.redditor(username).message(message=message, subject=subject)
        except praw.exceptions.RedditAPIException as e:
            for subexception in e.items:
                if subexception.error_type == "RATELIMIT":
                    error_str = str(subexception)
                    logging.info(error_str)

                    if 'minute' in error_str:
                        delay = error_str.split('for ')[-1].split(' minute')[0]
                        delay = int(delay) * 60.0
                    else:
                        delay = error_str.split('for ')[-1].split(' second')[0]
                        delay = int(delay)

                    time.sleep(delay)
                elif subexception.error_type == 'INVALID_USER':
                    return True

            return False
        except Exception as e:
            logging.error(e)
            return False

        return True

    def send_message(self, username: str, message: str) -> bool:
        is_sended = self.try_posting(username, 'Sea_Dragonfly5535', message)

        logging.info(self.reddit.auth.limits)

        if self.reddit.auth.limits['remaining'] == 0:
            timeout = self.reddit.auth.limits['reset_timestamp'] - time.time()
            logging.info("Used up requests in current time window - sleeping for {} seconds".format(timeout))
            time.sleep(timeout)

        return is_sended
