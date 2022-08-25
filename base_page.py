import math
from datetime import time
from telnetlib import EC

from selenium.common.exceptions import NoAlertPresentException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from locators import BasePageLocators, ProductPageLocators


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
            assert isinstance(EC)
            WebDriverWait(self.browser, timeout). \
                until(EC((how, what)))
        except TimeoutException:
            if screenshot:
                self.take_screenshot()

            return True

        return False

    # проверка на исчезновение элемента в течении timeout
    def is_disappeared(self, how, what, timeout=4, screenshot=True):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC((how, what)))
        except TimeoutException:
            if screenshot:
                self.take_screenshot()
            return False

        return True

    def take_screenshot(self):
        now = time.now().strftime('%Y-%m-%d_%H-%M-%S')
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

    def should_be_name(self):
        assert self.is_element_present(*ProductPageLocators.PRODUCT_NAME), "Name of product not found"
        self.product_name = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def should_be_price(self):
        assert self.is_element_present(*ProductPageLocators.PRODUCT_PRICE), "Price of product not found"
        self.product_price = self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def should_be_description(self):
        assert self.is_element_present(*ProductPageLocators.PRODUCT_DESCRIPTION), "Description of product not found"
        self.product_description = self.browser.find_element(*ProductPageLocators.PRODUCT_DESCRIPTION).text

    def should_be_success(self):
        assert self.is_element_present(*ProductPageLocators.SUCCESS_MESSAGES), "Message of Success added product in " \
                                                                               "basket not found "

    def add_product_to_basket(self):
        btn = self.browser.find_element(*ProductPageLocators.BTN_ADD_TO_BASKET)
        btn.click()

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGES), "Wrong show success message"

    def should_be_add_button(self):
        assert self.is_element_present(*ProductPageLocators.BTN_ADD_TO_BASKET), "Button 'Add to basket' is not " \
                                                                                "presented "

    def check_success_message(self):
        msg_lst = self.browser.find_elements(*ProductPageLocators.SUCCESS_MESSAGES)
        assert len(msg_lst) == 3, "Success message not found"

        assert self.product_name == msg_lst[0].text, "Wrong name product added to basket"
        assert self.product_price == msg_lst[2].text, "Wrong price product added to basket"

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
