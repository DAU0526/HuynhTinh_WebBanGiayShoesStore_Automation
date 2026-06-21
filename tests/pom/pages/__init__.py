"""
Package init — POM Pages
"""
from .base_page import BasePage
from .login_page import LoginPage
from .register_page import RegisterPage
from .home_page import HomePage
from .product_page import ProductPage
from .cart_page import CartPage
from .order_page import OrderPage

__all__ = [
    "BasePage",
    "LoginPage",
    "RegisterPage",
    "HomePage",
    "ProductPage",
    "CartPage",
    "OrderPage",
]
