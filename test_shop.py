"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity

        assert product.check_quantity(0)
        assert product.check_quantity(1)
        assert product.check_quantity(999)
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy

        product.buy(1)
        assert product.quantity == 999

        product.buy(2)
        assert product.quantity == 997

        product.buy(997)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1001)


@pytest.fixture
def empty_cart():
    return Cart()

@pytest.fixture
def full_cart(product):
    cart = Cart()
    cart.add_product(product, 10)
    return cart


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_init_empty_cart(self, empty_cart, product):
        assert len(empty_cart.products) == 0

    def test_add_product(self, empty_cart, product):
        empty_cart.add_product(product, 1)
        assert empty_cart.products[product] == 1
        empty_cart.add_product(product, 2)
        assert empty_cart.products[product] == 3

    def test_remove_product(self, full_cart, product):
        full_cart.remove_product(product, 1)
        assert full_cart.products[product] == 9
        full_cart.remove_product(product,2)
        assert full_cart.products[product] == 7

    def test_remove_full_product(self, full_cart, product):
        full_cart.remove_product(product)
        assert product not in full_cart.products

    def test_remove_product_exceed(self, full_cart, product):
        full_cart.remove_product(product, 11)
        assert product not in full_cart.products

    def test_clear_cart(self, full_cart, product):
         full_cart.clear()
         assert full_cart.products == {}

    def test_get_total_price(self,full_cart,empty_cart,product):
        assert full_cart.get_total_price() == 1000
        product2 = Product("kolbasa", 1, "Tupa kolbasa", 3)
        full_cart.add_product(product2, 2)
        assert full_cart.get_total_price() == 1002


    def test_buy(self, empty_cart, product):
        empty_cart.add_product(product, 1)
        empty_cart.buy()
        assert len(empty_cart.products) == 0
        assert product.quantity == 999

    def test_buy_more_than_available(self, empty_cart, product):
        empty_cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            empty_cart.buy()
