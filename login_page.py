import webbrowser

from selenium.webdriver.common.by import By

from base_page import BasePage
from locators import LoginPageLocators

browser = webbrowser.Chrome()


class LoginPage(BasePage):
    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_page()
        self.should_be_register_page()

    def should_be_login_url(self):
        login_url = browser.current_url
        assert "login" in browser.current_url

    def should_be_login_page(self):
        login_page = self.browser.find_element(By.CSS_SELECTOR, "#login_form")
        assert True

    def should_be_register_page(self):
        register_page = self.browser.find_element(By.CSS_SELECTOR, "#register_form")
        assert True
