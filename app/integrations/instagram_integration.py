from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from app.config.config import config
from selenium.webdriver.chrome.options import Options


class InstagramIntegration:
    def __init__(self, video_path, caption) -> None:
        super().__init__()

        PATH = config.CHROME_DRIVER_PATH
        self.username = config.INSTA_USERNAME
        self.password = config.INSTA_PASSWORD
        self.video_path = video_path
        self.caption = caption
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)

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
            sleep(4)

            drop_target = self.driver.find_element(By.XPATH, "/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div")
            sleep(4)

            self.drag_and_drop_file(drop_target, self.video_path)

            sleep(4)
            self.driver.find_element(By.CSS_SELECTOR,
                                     'body > div.RnEpo.gpWnf.Yx5HN > div.pbNvD > div > div > div > div.uYzeu > div._C8iK > div > div > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.soMvl.JI_ht.DhRcB.O1flK.D8xaz.fm1AK > div > div:nth-child(2) > div > button').click()
            sleep(4)
            self.driver.find_element(By.XPATH,
                                '/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[1]').click()

            sleep(4)
            self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button').click()
            sleep(4)
            self.driver.find_element(By.XPATH,'/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button').click()
            sleep(4)
            caption_field = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea")
            sleep(4)
            caption_field.send_keys(self.caption)
            self.driver.find_element(By.XPATH,"//button[contains(text(),'Share')]").click()
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
            sleep(4)
            not_now_btn = self.driver.find_element(By.XPATH,"//a[contains(text(),'Not Now')]")
            not_now_btn.click()
        except:
            pass

    def close_notification(self):
        try:
            sleep(4)
            close_noti_btn = self.driver.find_element(By.XPATH,"//button[contains(text(),'Not Now')]")
            close_noti_btn.click()
            sleep(4)
        except:
            pass

    def close_add_to_home(self):
        sleep(4)
        close_addHome_btn = self.driver.find_element(By.XPATH,"//button[contains(text(),'Not Now')]")
        close_addHome_btn.click()
        sleep(4)
