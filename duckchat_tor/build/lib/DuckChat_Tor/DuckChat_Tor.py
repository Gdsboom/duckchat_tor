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
from selenium.common.exceptions import NoSuchElementException

import asyncio
import pyautogui
import os
import tempfile

buff_amt = 0


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
    debug : bool
        Режим отладки (вывод ошибок в консоль).
    """

    def __init__(self, tor_browser_path, headless, url, browser, service, model="GPT-4o mini", debug=False):

        self.browser = browser
        self.model = model
        self.service = service
        self.url = url
        self.tor_browser_path = tor_browser_path  # "D:/Tor Browser/Browser/"
        self.headless = headless
        self.driver = None
        self.debug = debug
        try:
            self.__close_tor_browser()
        except:
            pass
        try:
            self.__close_tor_browser()
        except:
            pass
        self.initialization()

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            self.screenshot_path = tmp.name

    def initialization(self):
        profile_dir = self.tor_browser_path + "TorBrowser/Data/Browser/profile.default"

        self.firefox_options = Options()

        self.firefox_options.profile = profile_dir

        self.firefox_options.set_preference("dom.webdriver.enabled", False)
        self.firefox_options.set_preference("useAutomationExtension", False)
        self.firefox_options.set_preference("webgl.disabled", True)  # Отключаем WebGL
        self.firefox_options.set_preference("permissions.default.image", 2)  # Блокируем изображения
        self.firefox_options.binary_location = f"{self.tor_browser_path}/{self.browser}"

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

        self.firefox_options.add_argument("--window-size=1920,1080")  # убрать!!!!

        if (self.headless):
            self.firefox_options.add_argument("--headless")
        # self.firefox_options.add_argument("--profile")
        # self.firefox_options.add_argument(f"{tor_browser_path}/TorBrowser/Data/Browser/profile.default")
        self.driver = webdriver.Firefox(service=FirefoxService(self.service), options=self.firefox_options)

        wait_time = 15
        start_time = time.time()

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
                    # print("<head> элемент не пуст:", head_content)

            except Exception as e:
                pass
                # print(f"Ошибка при ожидании <head>: {e}")
            if time.time() - start_time > wait_time:
                # print("Время ожидания истекло.")
                break

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
                    # print("<body> элемент не пуст:", body_content)
            except Exception as e:
                pass
                # print(f"Ошибка при ожидании <body>: {e}")

        # print("Произошла ошибка ожидания:", e)
        # Ожидание полной загрузки страницы
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        # Открываем сайт
        self.driver.get(self.url)
        self.__waiting()
        self.change_model()

    def change_model(self):
        # nrcWY09Dfq7ESacde0NN wZ4JdaHxSAhGy1HoNVja d26Geqs1C__RaCO7MUs2 - model
        #
        # buff_element = element.find_element(By.CSS_SELECTOR,'p[class="nrcWY09Dfq7ESacde0NN wZ4JdaHxSAhGy1HoNVja d26Geqs1C__RaCO7MUs2"]')
        wait_time = 35
        start_time = time.time()
        while True:
            try:
                # нахождение используемой модели
                buff_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         'span[class="nrcWY09Dfq7ESacde0NN wZ4JdaHxSAhGy1HoNVja d26Geqs1C__RaCO7MUs2"]')))
                spans = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'span'))
                )
                break
            except Exception as e:
                # print("Ошбика в ожидании ответа!")
                pass

            if time.time() - start_time > wait_time:
                # print("Время ожидания истекло.")
                break

        # print("2!")
        # Извлекаем текст из всех label
        if not (any(1 for span in spans if self.model in span.text)):  # not (buff_element.text in self.model) or
            buff_element.click()
            try:
                # Ждем, пока элементы label будут загружены
                # print("1!")
                labels = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'label'))
                )
                # print("2!")
                # Извлекаем текст из всех label
                for label in labels:
                    label_text = label.text

                    # Проверяем, содержит ли текст нужный фрагмент
                    if self.model in label_text:
                        # print("3!", label_text)
                        # Находим кнопку, связанную с этим label
                        # button = self.driver.find_element(By.XPATH,f"//label[text()='{label_text}']")
                        label.click()
                        # print("4!")
                        # button.click()  # Нажимаем на кнопку
                        # print("5!")
                        break  # Выходим из цикла, если нашли и нажали на кнопку
            except:
                print("Ошибка!")
                # time.sleep(5)  # Ждем немного, чтобы увидеть результат
                self.driver.quit()  # Закрываем браузер

            self.wait_page()
            try:
                # Локатор кнопки (например, по атрибуту aria-label)
                button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')

                # Ждём, пока кнопка станет включённой (атрибут 'disabled' исчезнет)
                buttons = WebDriverWait(self.driver, 10).until(
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
                if self.debug:
                    print("Произошла ошибка в согласии:", e)

    def __close_tor_browser(self):
        """Закрывает все экземпляры Tor Browser."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.browser or proc.info[
                'name'] == self.service:  # Убедитесь, что имя процесса соответствует вашему Tor Browser
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

    def wait_page(self):
        wait_time = 15
        start_time = time.time()
        while True:
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                return
            except:
                # Сохраняем изображение во временный файл
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    self.driver.save_screenshot(temp_file.name)
                    os.startfile(temp_file.name)

                try:
                    self.__close_tor_browser()
                except:
                    pass
                try:
                    self.__close_tor_browser()
                except:
                    pass
                self.initialization()
            if time.time() - start_time > wait_time:
                # print("Время ожидания истекло.")
                # Сохраняем изображение во временный файл
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    self.driver.save_screenshot(temp_file.name)
                    os.startfile(temp_file.name)

                try:
                    self.__close_tor_browser()
                except:
                    pass
                try:
                    self.__close_tor_browser()
                except:
                    pass
                self.initialization()
                break

    def __agree(self):
        self.wait_page()
        try:
            # Локатор кнопки (например, по атрибуту aria-label)
            button_locator = (By.CSS_SELECTOR, 'button[type="button"]')

            # Ждём, пока кнопка станет включённой (атрибут 'disabled' исчезнет)
            buttons = WebDriverWait(self.driver, 10).until(
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
            if self.debug:
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
                    # time.sleep(1)

                # Проверяем, не истекло ли время ожидания
                if time.time() - start_time > wait_time:
                    # print("Время ожидания истекло.")
                    break
        except Exception as e:
            pass
            # print("Произошла ошибка в user-prompt:", e)

    def delete_space(self, text):
        try:
            while True:
                text.remove("")
        except:
            pass

    def find_last_div(self, element):
        """Рекурсивно находит самый глубокий div в цепочке"""
        nested_divs = element.find_elements(By.XPATH, "./div")

        # Если внутри ровно один div - углубляемся
        if len(nested_divs) == 1:
            return self.find_last_div(nested_divs[0])

        # Иначе возвращаем текущий элемент
        return element

    def clicks(self, button_locator):
        # if (WebDriverWait(self.driver, 10).until(
        #        lambda d: d.find_element(*button_locator).get_attribute("disabled") is None
        # )):
        WebDriverWait(self.driver, 5).until(
            lambda d: d.find_element(*button_locator).get_attribute("disabled") is None
        )
        # buttons = WebDriverWait(self.driver, 10).until(
        #    lambda d: [button for button in d.find_elements(*button_locator) if
        #               button.find_elements(By.TAG_NAME, 'svg') and button.get_attribute('type') == 'submit']
        # )
        buttons = WebDriverWait(self.driver, 20).until(
            lambda d: [
                button for button in d.find_elements(*button_locator)
                if button.find_elements(By.TAG_NAME, 'svg') and
                   button.get_attribute('type') == 'submit'
            ]
        )

        return buttons

    def SendPrompt(self, text):

        self.wait_page()
        # self.driver.find_element(By.NAME, "user-prompt").click()
        # print("0")
        # bufelement = self.driver.find_element(By.NAME, "user-prompt").send_keys(text)
        # textarea = WebDriverWait(self.driver, 10).until(
        #    EC.presence_of_element_located((By.NAME, "user-prompt"))
        # )
        textarea = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "user-prompt"))
        )

        self.driver.execute_script("""
            const textarea = arguments[0];
            const text = arguments[1];

            // Получаем нативный setter для value
            const valueSetter = Object.getOwnPropertyDescriptor(
                HTMLTextAreaElement.prototype, 
                'value'
            ).set;

            // Устанавливаем значение через нативный setter (для React/Vue)
            valueSetter.call(textarea, text);

            // Триггерим события
            textarea.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
            textarea.dispatchEvent(new Event('change', { bubbles: true }));
        """, textarea, text)

        # print("1")
        # for char in text:
        # bufelement.send_keys(char)
        # time.sleep(0.01)  # Задержка между вводом каждого символа

        # Локатор кнопки (например, по атрибуту aria-label)
        button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')
        # Ждём, пока кнопка станет включённой (атрибут 'disabled' исчезнет)

        # time.sleep(10)
        for _ in range(10):
            try:
                buttons = self.clicks(button_locator)
                break
            except Exception as e:
                if self.debug:
                    print("Ошбика в клике по кнопке отправки запроса:", "\n", str(e))

        for button in buttons:
            try:
                # Используем JavaScript для клика по кнопке
                self.driver.execute_script("arguments[0].click();", button)
                break  # Выходим из цикла, если клик успешен
            except Exception as e:
                if self.debug:
                    print(f"Не удалось кликнуть по кнопке: {e}")

    def GetPrompt(self, text):
        self.SendPrompt(text)

        wait = WebDriverWait(self.driver, 10)

        button_locator = (By.CSS_SELECTOR, 'button[aria-label="Стереть чат"], button[aria-label="Clear chat"]')
        wait_time = 20
        start_time = time.time()

        while True:
            try:
                # Проверяем все условия кликабельности
                button = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(button_locator)
                )

                # Дополнительная проверка, что элемент действительно видим и активен
                if (button.is_displayed() and
                        button.is_enabled() and
                        button.get_attribute("disabled") is None):
                    break

            except Exception as e:
                # Если кнопка ещё не готова, продолжаем ожидание
                pass

            # Проверяем таймаут
            if time.time() - start_time > wait_time:
                print("Время ожидания истекло, кнопка не стала кликабельной")
                return None

        # print("1111111111111111")

        target_divs = self.driver.find_elements(By.XPATH, "//div[count(div)=2]")

        results = None

        for div in target_divs:
            try:
                # 2. Проверяем div[0] на наличие нужного span
                first_child = div.find_element(By.XPATH, "./div[1]")
                span = first_child.find_element(
                    By.XPATH,
                    f".//span[contains(text(), '{self.model}')]"
                )

                # 3. Обрабатываем div[1]
                second_child = div.find_element(By.XPATH, "./div[2]")
                last_div = self.find_last_div(second_child)

                # Ищем все элементы внутри last_div
                elements = last_div.find_elements(By.XPATH, ".//*")  # или укажите конкретные теги

                header_texts = []
                processed_parents = set()

                for elem in elements:  # Теперь итерируемся по коллекции элементов
                    # Проверяем, является ли элемент чьим-то дочерним элементом без класса
                    parent = elem.find_element(By.XPATH, "./..")
                    if parent in processed_parents:
                        continue

                    # Получаем только текст, который НЕ находится в дочерних элементах
                    direct_text = self.driver.execute_script(
                        """
                        var node = arguments[0];
                        var text = '';
                        for (var i = 0; i < node.childNodes.length; i++) {
                            var child = node.childNodes[i];
                            if (child.nodeType === Node.TEXT_NODE) {
                                text += child.textContent.trim() + ' ';
                            }
                        }
                        return text.trim();
                        """,
                        elem
                    )

                    if direct_text:
                        header_texts.append(direct_text)
                        processed_parents.add(elem)

                self.delete_space(header_texts)
                p_texts = "\n".join(header_texts)
                if p_texts:
                    results = p_texts
                # time.sleep(2)

                # self.driver.save_screenshot(self.screenshot_path)

                # os.startfile(self.screenshot_path)
                return results
            except NoSuchElementException:
                continue

        '''
        wait_time = 20
        start_time = time.time()
        while True:
                try:
                    # Явное ожидание, чтобы убедиться, что элемент загружен

                    # Используйте XPath для поиска элемента <p> внутри нужного <div>
                    #p_elements = wait.until(EC.presence_of_all_elements_located(
                    #    (By.XPATH, f"//div[starts-with(@heading, '{self.model}')]//*[not(@class)]")
                    #))

                            #p_elements = second_child_div.find_elements(By.XPATH,f".//*[starts-with(@heading, '{self.model}')]//*[not(@class)]")

                    header_texts = []

                    # Множество для отслеживания уже обработанных родителей
                    processed_parents = set()

                    for elem in p_elements:
                        # Проверяем, является ли элемент чьим-то дочерним элементом без класса
                        # (если его родитель без класса и уже был обработан)
                        parent = elem.find_element(By.XPATH, "./..")
                        if parent in processed_parents: #not parent.get_attribute("class") and
                            continue  # Пропускаем дочерний элемент

                        # Получаем только текст, который НЕ находится в дочерних элементах
                        direct_text = self.driver.execute_script(
                            """
                            var node = arguments[0];
                            var text = '';
                            for (var i = 0; i < node.childNodes.length; i++) {
                                var child = node.childNodes[i];
                                if (child.nodeType === Node.TEXT_NODE) {
                                    text += child.textContent.trim() + ' ';
                                }
                            }
                            return text.trim();
                            """,
                            elem
                        )

                        if direct_text:
                            header_texts.append(direct_text)
                            processed_parents.add(elem)  # Запоминаем родительский элемент

                    self.delete_space(header_texts)
                    #print(header_texts)
                    p_texts = "\n".join(header_texts)

                    #self.driver.quit()
                    #print(p_texts)
                    return p_texts
                    """
                    # Извлеките текст из каждого элемента <p>
                    p_texts = [p.text for p in p_elements]
                    print(p_texts)
                    self.delete_space(p_texts)
                    print(p_texts)
                    p_texts = "\n".join(p_texts)
                    print(p_texts)
                    """
                except Exception as e:
                    #print("Ошбика в ожидании ответа!:", e)
                    pass

                if time.time() - start_time > wait_time:
                    # print("Время ожидания истекло.")
                    break
        '''

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

                self.wait_page()

                # Клик по элементу
                random_element.click()
                # print(f"Кликнули по элементу: {random_element.tag_name} с текстом: '{random_element.text}'")
        except:
            pass

        # Пример нажатия клавиши Enter
        body = self.driver.find_element(By.TAG_NAME, 'body')  # Получаем элемент body
        body.send_keys(Keys.ENTER)  # Нажимаем Enter
        # print("Нажали клавишу Enter")

        # Ждем некоторое время, чтобы страница загрузилась
        # time.sleep(5)  # Задержка в 5 секунд (можно заменить на WebDriverWait)

        # Перезагрузка страницы
        # self.driver.refresh()
        global buff_amt

        try:
            buff_amt += 1
            if (buff_amt > 5):
                """
                # Сохраняем изображение во временный файл
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    temp_file_name = temp_file.name
                    self.driver.save_screenshot(temp_file)
                    os.startfile(temp_file_name)
                """
                try:
                    self.__close_tor_browser()
                except:
                    pass
                try:
                    self.__close_tor_browser()
                except:
                    pass
                buff_amt = 0
                self.initialization()
            if (buff_amt > 2):
                print("Ошибка!!!!! Лучше перезапустить!" + " " + str(buff_amt))
                # buff_amt = 0
                raise
            # print(buff_amt)
            time.sleep(random.randint(1, 5))
            return self.GetPrompt(text)
        except:
            self.new_chat()
            return self.GetPrompt(text)

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
        self.driver.quit()