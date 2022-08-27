import math
import time
from telnetlib import EC

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common import alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from locators import BasketPageLocators, LoginPageLocators, BasePageLocators
from base_page import BasePage
from locators import ProductPageLocators
import datetime


def pytest_configure(config):
    if not config.option.resultlog:
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H-%M-%S')
        config.option.resultlog = 'log.' + timestamp


class ProductPage(BasePage):
    def add_product_to_basket_and_calculate(self):
        self.should_be_name()
        self.should_be_price()
        self.should_be_description()
        self.should_be_add_button()
        self.should_not_be_success_message()


class BasketPage(BasePage):
    def should_be_empty_basket(self):
        assert self.is_not_element_present(*BasketPageLocators.BASKET_TITLE, timeout=1), "Basket not empty"
        assert self.is_element_present(*BasketPageLocators.BASKET_INNER), "Wrong basket section"
        text_in_basket = self.browser.find_element(*BasketPageLocators.BASKET_INNER).text
        language = self.browser.execute_script(
            "return window.navigator.userLanguage || window.navigator.language")
        assert BasketPageLocators.empty_text[language] in text_in_basket, "Empty basket text not found"

    class LoginPage(BasePage):
        def register_new_user(self, email: str, password: str):
            assert self.is_element_present(*LoginPageLocators.REGISTER_EMAIL), "Email field not presented"
            assert self.is_element_present(*LoginPageLocators.REGISTER_PASS1), "Pass field not presented"
            assert self.is_element_present(*LoginPageLocators.REGISTER_PASS2), "Confirm pass field not presented"
            assert self.is_element_present(*LoginPageLocators.REGISTER_BTN), "Register button not presented"

            self.browser.find_element(*LoginPageLocators.REGISTER_EMAIL).send_keys(email)
            self.browser.find_element(*LoginPageLocators.REGISTER_PASS1).send_keys(password)
            self.browser.find_element(*LoginPageLocators.REGISTER_PASS2).send_keys(password)
            self.browser.find_element(*LoginPageLocators.REGISTER_BTN).click()

        def should_be_authorized_user(self):
            assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
                                                                         " probably unauthorised user"

        def should_be_login_page(self):
            self.should_be_login_url()
            self.should_be_login_form()
            self.should_be_register_form()

        def should_be_login_url(self):
            # проверка на корректный url адрес
            assert LoginPageLocators.PART_URL in self.browser.current_url, "Current url is incorrect"

        def should_be_login_form(self):
            # проверка, что есть форма логина
            assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), "Login form is not presented"

        def should_be_register_form(self):
            # проверка, что есть форма регистрации на странице
            assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), "Register form is not presented"