from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from app.config.config import config
from app.config.logger import Logger


logging = Logger.get_logger("Twitter Selenium")


class TwitterSeleniumIntegration:
    def __init__(
        self,
        username: str,
        password: str,
    ) -> None:
        self.username = username
        self.password = password
        super().__init__()
    def post_tweet(self, video_path: str, tweet_text: str):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--kiosk-printing')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Remote(
                command_executor=config.SELENIUM_HUB_URL,
                desired_capabilities=chrome_options.to_capabilities(),
            )
            wait = WebDriverWait(driver, 10)

            driver.get("https://twitter.com/login")

            username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_field.send_keys(self.username)
            username_field.send_keys(Keys.RETURN)

            password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

            time.sleep(5)

            driver.get("https://twitter.com/compose/tweet")

            text_field = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="notranslate public-DraftEditor-content"]')))
            text_field.send_keys(tweet_text)

            media_button = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
            media_button.send_keys(video_path)

            time.sleep(50)

            tweet_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButton"]')))
            tweet_button.click()

            time.sleep(10)

            driver.quit()
            return True
        except Exception as ex:
            logging.error(ex)
            return False