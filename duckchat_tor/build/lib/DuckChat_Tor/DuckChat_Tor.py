import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class DuckChat_Tor:
    def __init__(self, tor_browser_path, headless, url):
        self.firefox_options = Options()
        self.tor_browser_path = tor_browser_path  #"D:/Tor Browser/Browser/"
        self.firefox_options.binary_location = f"{tor_browser_path}/firefox.exe"
        if ( headless ):
            self.firefox_options.add_argument("--headless")
        self.firefox_options.add_argument("--profile")
        self.firefox_options.add_argument(f"{tor_browser_path}/TorBrowser/Data/Browser/profile.default")
        self.driver = webdriver.Firefox(options=self.firefox_options)
        try:
            # Ждём, пока не исчезнут все элементы на странице
            WebDriverWait(self.driver, 20).until(
                lambda d: len(d.find_elements(By.XPATH, "//*")) == 0
            )

            # print("Страница загрузилась полностью и является пустой.")

        except Exception as e:
            pass
            # print("Произошла ошибка ожидания:", e)
        # Открываем сайт
        self.driver.get(url)
        self.__waiting()

    def __agree(self):
        try:
            # Локатор кнопки (например, по атрибуту aria-label)
            button_locator = (By.CSS_SELECTOR, 'button[type="button"]')

            # Ждём, пока кнопка станет включённой (атрибут 'disabled' исчезнет)
            buttons = WebDriverWait(self.driver, 20).until(
                lambda d: [btn for btn in d.find_elements(*button_locator) if
                           btn.get_attribute("tabindex") == "1" or "I Agree" in btn.text]
            )

            if buttons:
                for button in buttons:
                    button.click()  # Нажимаем на каждую доступную кнопку
                    # print("Кнопка нажата.")
            else:
                pass
                # print("Кнопка не найдена или не доступна для нажатия.")

        except Exception as e:
            print("Произошла ошибка в согласии:", e)

    def __waiting(self):
        try:
            # Устанавливаем время ожидания
            wait_time = 10
            start_time = time.time()

            while True:
                # Проверяем, появился ли элемент
                try:
                    element = WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located((By.NAME, "user-prompt"))
                    )
                    # print("Элемент 'user-prompt' появился.")
                    break  # Выходим из цикла, если элемент найден
                except:
                    # Если элемент не найден, выполняем нужные действия
                    # print("Элемент 'user-prompt' не найден. Выполняем действия...")
                    self.__agree()
                    time.sleep(1)

                # Проверяем, не истекло ли время ожидания
                if time.time() - start_time > wait_time:
                    # print("Время ожидания истекло.")
                    break
        except Exception as e:
            pass
            # print("Произошла ошибка в user-prompt:", e)

    def GetPrompt(self, text):
        self.driver.find_element(By.NAME, "user-prompt").send_keys(text)
        try:
            # Локатор кнопки (например, по атрибуту aria-label)
            button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')

            # Ждём, пока кнопка станет включённой (атрибут 'disabled' исчезнет)
            if (WebDriverWait(self.driver, 20).until(
                    lambda d: d.find_element(*button_locator).get_attribute("disabled") is None
            )):
                self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        except Exception as e:
            pass

        while True:
            wait_time = 10
            start_time = time.time()
            try:
                # Ждем, пока элементы с атрибутом heading появятся на странице
                elements = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@heading="GPT-4o mini"]'))
                )

                for element in elements:
                    # Находим все кнопки внутри текущего элемента
                    buttons = element.find_elements(By.TAG_NAME, "button")

                    # Проверяем, что количество кнопок равно 2

                    if len(buttons) == 4:
                        start_time1 = time.time()
                        while True:
                            try:
                                # driver.find_element(By.XPATH,"/html/body/div[2]/div[6]/div[4]/div/div[2]/main/div/section[2]/div/div[2]/form/div[1]/div[2]/button").click()
                                buff_element = element.find_element(By.CSS_SELECTOR,
                                                                    'p[class="_7Umba5sjAq6KV8_X26Kg wZ4JdaHxSAhGy1HoNVja yPVtygfW3yi77pB7G6Se"]')
                                #asdas = buff_element.text
                                if (buff_element.text == "GPT-4o mini"):
                                    break

                            except Exception as e:
                                pass
                                # print("Не то: ", e)
                            if time.time() - start_time1 > wait_time:
                                # print("Время ожидания истекло.")
                                break
                        # Извлекаем текст из указанного XPath
                        text_element = element.find_element(By.CSS_SELECTOR, 'div[class="JXNYs5FNOplxLlVAOswQ"]')
                        return text_element.text
            except Exception as e:
                pass
                # print("Произошла ошибка в поисках ответа нейронки:", e)
            if time.time() - start_time > wait_time:
                # print("Время ожидания истекло.")
                break
        return self.GetPrompt(text)

    def __del__(self):
        self.driver.quit()