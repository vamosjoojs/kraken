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
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'pt,pt_BR'})

        self.driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)

    @staticmethod
    def drag_and_drop_file(drop_target, path):
        JS_DROP_FILE = """
                var target = arguments[0],
                    offsetX = arguments[1],
                    offsetY = arguments[2],
                    document = target.ownerDocument || document,
                    window = document.defaultView || window;

                var input = document.createElement('INPUT');
                input.type = 'file';
                input.onchange = function () {
                  var rect = target.getBoundingClientRect(),
                      x = rect.left + (offsetX || (rect.width >> 1)),
                      y = rect.top + (offsetY || (rect.height >> 1)),
                      dataTransfer = { files: this.files };

                  ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                    var evt = document.createEvent('MouseEvent');
                    evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                    evt.dataTransfer = dataTransfer;
                    target.dispatchEvent(evt);
                  });

                  setTimeout(function () { document.body.removeChild(input); }, 25);
                };
                document.body.appendChild(input);
                return input;
            """

        driver = drop_target.parent
        file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
        file_input.send_keys(path)

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

            drop_target = self.driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div")
            sleep(2)

            self.drag_and_drop_file(drop_target, self.video_path)

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
