import autoit
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from app.config.config import config


class InstagramIntegration:
    def __init__(self, video_path, caption) -> None:
        super().__init__()

        PATH = config.CHROME_DRIVER_PATH
        self.username = config.INSTA_USERNAME
        self.password = config.INSTA_PASSWORD
        self.video_path = video_path
        self.caption = caption

        self.driver = webdriver.Chrome(executable_path=PATH)

    def post_video(self) -> bool:
        try:
            main_url = "https://www.instagram.com"
            self.driver.get(main_url)
            sleep(4)
            self.login()
            sleep(4)
            self.close_reactivated()
            sleep(4)
            self.close_add_to_home()
            sleep(4)
            self.close_notification()
            sleep(4)
            self.driver.find_element(By.XPATH,
                                '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button').click()
            sleep(2)
            self.driver.find_element(By.XPATH,
                                '/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/button').click()
            sleep(2)
            autoit.win_active("Abrir")
            sleep(2)
            autoit.control_send("Abrir", "Edit1", self.video_path)
            sleep(2)
            autoit.control_send("Abrir", "Edit1", "{ENTER}")
            sleep(2)
            self.driver.find_element(By.XPATH,
                                '/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button').click()
            sleep(2)
            self.driver.find_element(By.XPATH,
                                '/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[1]').click()
            sleep(2)
            self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button').click()
            sleep(2)
            self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button').click()
            sleep(2)
            caption_field = self.driver.find_element(By.XPATH,"//textarea[@aria-label='Escreva uma legenda...']")
            sleep(1.5)
            caption_field.send_keys(self.caption)
            self.driver.find_element(By.XPATH,"//button[contains(text(),'Compartilhar')]").click()
            sleep(30)
            self.driver.close()
            return True
        except Exception as ex:
            print(ex)
            return False

    def login(self):
        username_input = self.driver.find_element(By.XPATH,"//input[@name='username']")
        username_input.send_keys(self.username)
        password_input = self.driver.find_element(By.XPATH,"//input[@name='password']")
        password_input.send_keys(self.password)
        password_input.submit()

    def close_reactivated(self):
        try:
            sleep(2)
            not_now_btn = self.driver.find_element(By.XPATH,"//a[contains(text(),'Agora não')]")
            not_now_btn.click()
        except:
            pass

    def close_notification(self):
        try:
            sleep(2)
            close_noti_btn = self.driver.find_element(By.XPATH,"//button[contains(text(),'Agora não')]")
            close_noti_btn.click()
            sleep(2)
        except:
            pass

    def close_add_to_home(self):
        sleep(3)
        close_addHome_btn = self.driver.find_element(By.XPATH,"//button[contains(text(),'Agora não')]")
        close_addHome_btn.click()
        sleep(1)
