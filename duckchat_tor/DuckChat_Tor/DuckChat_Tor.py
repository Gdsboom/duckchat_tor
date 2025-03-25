import random
import time
import psutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService

import pyautogui
import os

class DuckChat_Tor:
    """
    Класс для работы с браузером.

    Параметры:
    ----------
    tor_browser_path : str
        Путь к исполняемому файлу браузера.
    headless : bool
        Режим работы браузера (без графического интерфейса, если True).
    url : str, optional
        URL-адрес для открытия (например, "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1").
    browser : str
        Название браузера (например, "firefox").
    service : str, optional
        Путь к драйверу браузера (например, "D:/geckodriver.exe").
    """
    def __init__(self, tor_browser_path, headless, url, browser, service, model="GPT-4o"):

        self.browser = browser
        self.model = model
        try:
            self.__close_tor_browser()
        except:
            pass
        try:
            self.__close_tor_browser()
        except:
            pass

        self.tor_browser_path = tor_browser_path  # "D:/Tor Browser/Browser/"
        profile_dir = tor_browser_path+"TorBrowser/Data/Browser/profile.default"

        self.firefox_options = Options()

        self.firefox_options.profile = profile_dir

        self.firefox_options.set_preference("dom.webdriver.enabled", False)
        self.firefox_options.set_preference("useAutomationExtension", False)
        self.firefox_options.set_preference("webgl.disabled", True)  # Отключаем WebGL
        self.firefox_options.set_preference("permissions.default.image", 2)  # Блокируем изображения
        self.firefox_options.binary_location = f"{tor_browser_path}/{browser}"

        # 2. Критические настройки для скрытия WebDriver
        self.firefox_options.set_preference("dom.webdriver.enabled", False)
        self.firefox_options.set_preference("useAutomationExtension", False)
        self.firefox_options.set_preference("webgl.disabled", True)  # Отключаем WebGL
        self.firefox_options.set_preference("permissions.default.image", 2)  # Блокируем изображения

        # 3. Настройки User-Agent (должен совпадать с обычным Tor Browser)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
        self.firefox_options.set_preference("general.useragent.override", user_agent)

        # 4. Параметры приватности
        self.firefox_options.set_preference("privacy.resistFingerprinting", True)
        self.firefox_options.set_preference("privacy.trackingprotection.enabled", True)
        self.firefox_options.set_preference("browser.privatebrowsing.autostart", True)

        if ( headless ):
            self.firefox_options.add_argument("--headless")
        #self.firefox_options.add_argument("--profile")
        #self.firefox_options.add_argument(f"{tor_browser_path}/TorBrowser/Data/Browser/profile.default")
        self.driver = webdriver.Firefox(service=FirefoxService(service), options=self.firefox_options)
        """
        try:
            # Ждём, пока не исчезнут все элементы на странице
            WebDriverWait(self.driver, 20).until(
                lambda d: len(d.find_elements(By.XPATH, "//*")) == 0
            )

            # print("Страница загрузилась полностью и является пустой.")

        except Exception as e:
            pass
        """
        while True:
            # Ожидание появления элемента <head>
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "head"))
                )
                # Проверка, что <head> пустой
                head_content = self.driver.execute_script("return document.head.innerHTML;")
                if not head_content.strip():  # Проверяем, что содержимое пустое
                    break
                else:
                    pass
                    #print("<head> элемент не пуст:", head_content)
            except Exception as e:
                pass
                #print(f"Ошибка при ожидании <head>: {e}")

            # Ожидание появления элемента <body>
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                # Проверка, что <body> пустой
                body_content = self.driver.execute_script("return document.body.innerHTML;")
                if not body_content.strip():  # Проверяем, что содержимое пустое
                    break
                else:
                    pass
                    #print("<body> элемент не пуст:", body_content)
            except Exception as e:
                pass
                #print(f"Ошибка при ожидании <body>: {e}")

        # print("Произошла ошибка ожидания:", e)
        # Ожидание полной загрузки страницы
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        # Открываем сайт
        self.driver.get(url)
        self.__waiting()
        self.change_model()



    def change_model(self):
        #nrcWY09Dfq7ESacde0NN wZ4JdaHxSAhGy1HoNVja d26Geqs1C__RaCO7MUs2 - model
        #
        #buff_element = element.find_element(By.CSS_SELECTOR,'p[class="nrcWY09Dfq7ESacde0NN wZ4JdaHxSAhGy1HoNVja d26Geqs1C__RaCO7MUs2"]')

        # нахождение используемой модели
        buff_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'span[class="nrcWY09Dfq7ESacde0NN wZ4JdaHxSAhGy1HoNVja d26Geqs1C__RaCO7MUs2"]')))

        spans = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'span'))
        )
        # print("2!")
        # Извлекаем текст из всех label
        if not(any(1 for span in spans if self.model in span.text )) : #not (buff_element.text in self.model) or
            buff_element.click()
            try:
                # Ждем, пока элементы label будут загружены
                #print("1!")
                labels = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'label'))
                )
                #print("2!")
                # Извлекаем текст из всех label
                for label in labels:
                    label_text = label.text

                    # Проверяем, содержит ли текст нужный фрагмент
                    if self.model in label_text:
                        #print("3!", label_text)
                        # Находим кнопку, связанную с этим label
                        #button = self.driver.find_element(By.XPATH,f"//label[text()='{label_text}']")
                        label.click()
                        #print("4!")
                        #button.click()  # Нажимаем на кнопку
                        #print("5!")
                        break  # Выходим из цикла, если нашли и нажали на кнопку
            except:
                print("Ошибка!")
                time.sleep(5)  # Ждем немного, чтобы увидеть результат
                self.driver.quit()  # Закрываем браузер

            self.wait_page()
            try:
                # Локатор кнопки (например, по атрибуту aria-label)
                button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')

                # Ждём, пока кнопка станет включённой (атрибут 'disabled' исчезнет)
                buttons = WebDriverWait(self.driver, 20).until(
                    lambda d: [btn for btn in d.find_elements(*button_locator) if
                               "Start New Chat" in btn.text]
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



    def __close_tor_browser(self):
        """Закрывает все экземпляры Tor Browser."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.browser:  # Убедитесь, что имя процесса соответствует вашему Tor Browser
                try:
                    # Завершаем дочерние процессы
                    children = proc.children(recursive=True)
                    for child in children:
                        child.kill()  # или child.kill() для принудительного завершения

                    # Завершаем родительский процесс
                    proc.kill()  # или proc.kill() для принудительного завершения
                    # print(f"Процесс {proc.info['pid']} и его дочерние процессы успешно завершены.")
                except psutil.NoSuchProcess:
                    pass
                    # print(f"Процесс {proc.info['pid']} не найден.")
                except psutil.AccessDenied:
                    pass
                    # print(f"Нет доступа к процессу {proc.info['pid']}.")
                except Exception as e:
                    pass
                    # print(f"Ошибка при завершении процесса {proc.info['pid']}: {e}")
    """
    def __close_tor_browser(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'firefox1.exe':  # Убедитесь, что имя процесса соответствует вашему Tor Browser
                # Завершаем дочерние процессы
                children = proc.children(recursive=True)
                for child in children:
                    child.kill()  # или child.kill() для принудительного завершения

                # Завершаем родительский процесс
                proc.kill()  # или proc.kill() для принудительного завершения
                #print(f"Процесс {proc.info['pid']} и его дочерние процессы успешно завершены.")
        '''
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'geckodriver.exe':  # Убедитесь, что имя процесса соответствует вашему Tor Browser
                # Завершаем дочерние процессы
                try:
                    children = proc.children(recursive=True)
                    for child in children:
                        child.kill()  # или child.kill() для принудительного завершения
                except:
                    pass
                # Завершаем родительский процесс
                proc.kill()  # или proc.kill() для принудительного завершения
                #print(f"Процесс {proc.info['pid']} и его дочерние процессы успешно завершены.")
        '''
    """
    def wait_page(self):
        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                return
            except:
                pass
    def __agree(self):
        self.wait_page()
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
        self.wait_page()
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
                    #time.sleep(1)

                # Проверяем, не истекло ли время ожидания
                if time.time() - start_time > wait_time:
                    # print("Время ожидания истекло.")
                    break
        except Exception as e:
            pass
            # print("Произошла ошибка в user-prompt:", e)

    def GetPrompt(self, text):
        self.wait_page()
        self.driver.find_element(By.NAME, "user-prompt").click()
        bufelement = self.driver.find_element(By.NAME, "user-prompt").send_keys(text)
        #for char in text:
            #bufelement.send_keys(char)
            #time.sleep(0.01)  # Задержка между вводом каждого символа
        try:
            pass
        except Exception as e:
            print("Ошибка!", e)
            pass

        # print("1!")
        # Локатор кнопки (например, по атрибуту aria-label)
        button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')
        # print("2!")
        # Ждём, пока кнопка станет включённой (атрибут 'disabled' исчезнет)
        if (WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(*button_locator).get_attribute("disabled") is None
        )):
            # print("3!")

            buttons = WebDriverWait(self.driver, 10).until(
                lambda d: [button for button in d.find_elements(*button_locator) if
                           button.find_elements(By.TAG_NAME, 'svg') and button.get_attribute('type') == 'submit']
            )

            for button in buttons:
                try:
                    # Используем JavaScript для клика по кнопке
                    self.driver.execute_script("arguments[0].click();", button)
                    break  # Выходим из цикла, если клик успешен
                except Exception as e:
                    print(f"Не удалось кликнуть по кнопке: {e}")
            # self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            # print("4!")

        wait_time = 5
        start_time = time.time()


        while True:
                try:
                    # Явное ожидание, чтобы убедиться, что элемент загружен
                    wait = WebDriverWait(self.driver, 10)
                    #print("1!")
                    # Используйте XPath для поиска элемента <p> внутри нужного <div>
                    p_element = wait.until(EC.presence_of_element_located(
                        (By.XPATH, f"//div[starts-with(@heading, '{self.model}')]//p[not(@class)]")
                    ))
                    #print("2!")
                    # Извлеките текст из элемента <p>
                    p_text = p_element.text
                    print(p_text)
                    return p_text
                    """
                    # Ждем, пока элементы с атрибутом heading появятся на странице
                    # elements = WebDriverWait(self.driver, 2).until(
                    #    EC.presence_of_all_elements_located((By.XPATH, '//*[@heading="GPT-4o mini"]'))
                    # )
                    # Ждем, пока все div с заголовками загрузятся
                    # Ожидаем, пока все div элементы загрузятся
                    elements = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, 'div')))
                    print(f'Найдено {len(elements)} элементов div.')
                    for element in elements:
                        # print("1!")
                        try:
                            pass
                        except:
                            pass
                        # Проверяем, содержится ли нужное слово в тексте div
                        if self.model in element.text and "You are chatting with" not in element.text:
                            # print(element.text, self.model in element.text)
                            ps = element.find_elements(By.TAG_NAME, "p")
                            print( "ps:",len(ps) )
                            for p in ps:
                                # print("1!   ", p.text)
                                if not (self.model in p.text) and p.text != text:
                                    # print("2!")
                                    # Извлекаем текст из указанного XPath
                                    # Получаем путь к текущему скрипту
                                    current_directory = os.path.dirname(os.path.abspath(__file__))

                                    # Указываем имя файла для скриншота
                                    screenshot_filename = os.path.join(current_directory, 'screenshot.png')

                                    # Делаем скриншот и сохраняем его
                                    screenshot = pyautogui.screenshot()
                                    screenshot.save(screenshot_filename)
                                    return p.text

                            # print("Ошибка в ожиданнии получения ответа")
                        # print("Произошла ошибка в поисках ответа нейронки:", e)
                        """

                except Exception as e:
                    #print("Ошбика в ожидании ответа!")
                    pass
                if time.time() - start_time > wait_time:
                    # print("Время ожидания истекло.")
                    break

        try:
            # Найдите все элементы <p> и <label> на странице
            elements_to_click = self.driver.find_elements(By.XPATH, "//p | //label")

            # Фильтруем элементы, чтобы исключить интерактивные
            non_interactive_elements = []
            for element in elements_to_click:
                # Проверяем, что элемент не имеет атрибутов, которые могут указывать на интерактивность
                if not element.get_attribute('onclick') and not element.get_attribute('href'):
                    non_interactive_elements.append(element)

            # Если есть элементы для клика, выберите случайный элемент и кликните по нему
            if non_interactive_elements:
                random_element = random.choice(non_interactive_elements)

                # Прокрутка к элементу
                self.driver.execute_script("arguments[0].scrollIntoView();", random_element)

                # Ожидание, чтобы убедиться, что элемент видим
                time.sleep(0.5)  # Можно заменить на WebDriverWait для более надежного ожидания

                # Клик по элементу
                random_element.click()
                print(f"Кликнули по элементу: {random_element.tag_name} с текстом: '{random_element.text}'")
        except:
            pass

        # Пример нажатия клавиши Enter
        body = self.driver.find_element(By.TAG_NAME, 'body')  # Получаем элемент body
        body.send_keys(Keys.ENTER)  # Нажимаем Enter
        print("Нажали клавишу Enter")

        # Ждем некоторое время, чтобы страница загрузилась
        #time.sleep(5)  # Задержка в 5 секунд (можно заменить на WebDriverWait)

        # Перезагрузка страницы
        #self.driver.refresh()
        try:
            return self.GetPrompt(text)
        except:
            self.new_chat()

            return self.GetPrompt(text)


    """
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
                                        # asdas = buff_element.text
                                        # if (buff_element.text == "GPT-4o mini"):
                                        if (self.model in buff_element.text):
                                            break

                                        if time.time() - start_time1 > wait_time:
                                            # print("Время ожидания истекло.")
                                            break

                                    except Exception as e:
                                        pass
                                        # print("Не то: ", e)
                                    if time.time() - start_time1 > wait_time:
                                        # print("Время ожидания истекло.")
                                        break
    """





    def new_chat(self):
        buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
        )
        # print("2!")
        # Извлекаем текст из всех label
        for button in buttons:
            button_text = button.text

            # Проверяем, содержит ли текст нужный фрагмент
            if "New Chat" in button_text:
                # print("3!", label_text)
                # Находим кнопку, связанную с этим label
                # button = self.driver.find_element(By.XPATH,f"//label[text()='{label_text}']")
                button.click()
                # print("4!")
                # button.click()  # Нажимаем на кнопку
                # print("5!")
                break  # Выходим из цикла, если нашли и нажали на кнопку

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
        try:
            self.__close_tor_browser()
        except:
            pass
        self.driver = None