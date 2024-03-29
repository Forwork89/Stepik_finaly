import math
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
# from selenium.webdriver.chrome.webdriver import RemoteWebDriver

from .locators import BasePageLocators


class RemoteWebDriver:
    def find_element(self, param):
        pass

    def get_screenshot_as_file(self, namefile):
        pass


class BasePage:
    def __init__(self, browser: RemoteWebDriver, url: str):
        self.browser = browser
        self.url = url
        # не используем т.к. timeout используется в проверке наличия элемента
        # self.browser.implicitly_wait(10)

    def open(self):
        self.browser.get(self.url)

    # проверка на наличие элемента с ожиданием timeout
    def is_element_present(self, how, what, timeout=4, screenshot=True):
        try:
            # self.browser.find_element(how, what)
            WebDriverWait(self.browser, timeout). \
                until(EC.presence_of_element_located((how, what)))

        except TimeoutException:
            if screenshot:
                self.take_screenshot()
            return False

        except NoSuchElementException:
            if screenshot:
                self.take_screenshot()
            return False

        return True

    # проверка на отсутствие элемента с ожиданием timeout
    def is_not_element_present(self, how, what, timeout=4, screenshot=True):
        try:
            WebDriverWait(self.browser, timeout). \
                until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            if screenshot:
                self.take_screenshot()

            return True

        return False

    # проверка на исчезновение элемента в течении timeout
    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False

        return True

    def take_screenshot(self):
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        namefile = f"screenshot-{now}.png"
        self.browser.get_screenshot_as_file(namefile)
        print(f"Taked screenshot: {namefile}")

    # общие для всех страниц методы
    def go_to_basket_page(self):
        link = self.browser.find_element(*BasePageLocators.BTN_BASKET)
        link.click()

    def go_to_login_page(self):
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()

    def should_be_btn_basket(self):
        assert self.is_element_present(*BasePageLocators.BTN_BASKET), "Button of basket not presented"

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"

    def solve_quiz_and_get_code(self):
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")
