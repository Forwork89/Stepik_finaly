from faker import Faker
import pytest
from .pages.base_page import BasePage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.basket_page import BasketPage

# link = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"

link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207"


@pytest.mark.need_review
# @pytest.mark.parametrize('link', [n if n != 7 else pytest.param(n, marks=pytest.mark.xfail(marker="bug detected")) for n in range(0, 10)])
def test_guest_can_add_product_to_basket(browser, link):
    link = f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{link}"
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket_and_calculate()


# @pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    page = ProductPage(browser, link)
    page.open()
    page.should_be_add_button()
    page.add_product_to_basket_and_calculate()
    page.should_not_be_success_message()


@pytest.mark.add_to_basket
class TestAddToBasketFromProductPage(object):
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, ProductFactory=None):
        self.product = ProductFactory(title="Best book created by robot")
        self.link = self.product.link
        yield
        self.product.delete()


def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.should_not_be_success_message()


def test_message_disappeared_after_adding_product_to_basket(browser):
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket()
    page.is_disappered_success_message()

    # def test_guest_should_see_login_link_on_product_page(browser):
    # page = ProductPage(browser, link)
    # page.open()
    # page.should_be_login_link()


@pytest.mark.login
class TestLoginFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, ProductFactory=None):
        self.product = ProductFactory(title="Best book created by robot")
        # создаем по апи
        self.link = self.product.link
        yield
        # после этого ключевого слова начинается teardown
        # выполнится после каждого теста в классе
        # удаляем те данные, которые мы создали 
        self.product.delete()


def test_guest_can_go_to_login_page_from_product_page(browser):
    page = ProductPage(browser, link)
    page.open()
    page.go_to_login_page()


def test_guest_should_see_login_link(self, browser):
    page = ProductPage(browser, self.link)
    page.open()
    page.should_be_login_link()

    login_page = LoginPage(browser, browser.current_url)

    login_page.should_be_login_page()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    page = ProductPage(browser, link)
    page.open()
    page.should_be_btn_basket()
    page.go_to_basket_page()

    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()


class TestUserAddToBasketFromProductPage:
    password = 'Qw21eR4t50'
    faker: Faker = Faker(locale='ru-RU')


@pytest.fixture(scope="function", autouse=True)
def setup(self, browser):
    """
        открыть страницу регистрации
        зарегистрировать нового пользователя
        проверить, что пользователь залогинен

        так обычно не делают в setup это просто для примера
    """
    page = ProductPage(browser, link)
    page.open()
    page.go_to_login_page()

    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()

    login_page.register_new_user(self.faker.email(), self.password)
    login_page.should_be_authorized_user()


def test_user_cant_see_success_message(self, browser):
    page = ProductPage(browser, link)
    page.open()
    page.should_be_btn_basket()
    page.go_to_basket_page()

    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()


@pytest.mark.need_review
def test_user_can_add_product_to_basket(self, browser):
    page = ProductPage(browser, link)
    page.open()
    page.add_product_to_basket_and_calculate()
