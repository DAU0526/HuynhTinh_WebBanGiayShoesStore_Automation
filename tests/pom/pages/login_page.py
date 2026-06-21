"""
Login Page — Page Object Model
Trang: /users/login/
Module: Auth (Xác thực người dùng)
Thành viên phụ trách: [Thành viên 1 — Auth Module]
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object cho trang Đăng Nhập — Shoes Store.

    Locators tuân theo chuẩn POM:
      - Tất cả selectors đặt trong class constants
      - Không có By.* trong methods test
      - Methods trả về self hoặc Page Object khác (Fluent Interface)

    Liên quan: TC-AUTH-001 → TC-AUTH-008
    """

    # ------------------------------------------------------------------
    # URL Path
    # ------------------------------------------------------------------
    PATH = "/users/login/"

    # ------------------------------------------------------------------
    # LOCATORS — Tất cả CSS/XPath selectors ở đây
    # ------------------------------------------------------------------
    # Form Fields
    USERNAME_FIELD  = (By.ID, "username")
    PASSWORD_FIELD  = (By.ID, "password")
    SUBMIT_BUTTON   = (By.CSS_SELECTOR, "button[type='submit']")

    # Messages
    ERROR_ALERT     = (By.CSS_SELECTOR, ".messages-container .premium-alert")
    SUCCESS_ALERT   = (By.CSS_SELECTOR, ".messages-container .alert-success")

    # Navigation
    REGISTER_LINK   = (By.CSS_SELECTOR, "a[href*='register']")
    FORGOT_PWD_LINK = (By.CSS_SELECTOR, "a[href*='forgot'], a[href*='reset']")

    # Post-login Elements (on Home page)
    USER_MENU       = (By.CSS_SELECTOR, ".user-menu, .user-dropdown, #user-menu")
    LOGOUT_BTN      = (By.CSS_SELECTOR, "a[href*='logout']")
    CART_COUNT      = (By.ID, "cart-count")

    # ------------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------------
    def open(self) -> "LoginPage":
        """Mở trang đăng nhập và đợi form xuất hiện"""
        self.navigate(self.PATH)
        self.find(self.USERNAME_FIELD)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Nhập tên đăng nhập (email hoặc SĐT)"""
        self.input_text(self.USERNAME_FIELD, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Nhập mật khẩu"""
        self.input_text(self.PASSWORD_FIELD, password)
        return self

    def click_submit(self) -> "LoginPage":
        """Click nút Đăng Nhập"""
        self.scroll_to_element(self.SUBMIT_BUTTON)
        self.click(self.SUBMIT_BUTTON)
        time.sleep(0.5)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """
        Thực hiện đầy đủ luồng đăng nhập.
        Dùng: page.login("email", "password")
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
        return self

    def click_register_link(self) -> "LoginPage":
        """Click link 'Đăng ký tài khoản'"""
        self.click(self.REGISTER_LINK)
        return self

    # ------------------------------------------------------------------
    # ASSERTIONS / STATE CHECKS
    # ------------------------------------------------------------------
    def is_logged_in(self) -> bool:
        """Kiểm tra đăng nhập thành công (URL đã rời trang login)"""
        try:
            self.wait_url_contains(self.BASE_URL + "/", timeout=8)
            return self.PATH not in self.get_current_url()
        except TimeoutException:
            return False

    def get_error_message(self) -> str:
        """Lấy thông báo lỗi (nếu có)"""
        return self.get_text(self.ERROR_ALERT, timeout=3)

    def is_error_visible(self) -> bool:
        """Kiểm tra có thông báo lỗi không"""
        return self.is_visible(self.ERROR_ALERT)

    def is_on_login_page(self) -> bool:
        """Kiểm tra đang ở trang đăng nhập"""
        return self.PATH in self.get_current_url()

    def is_username_field_required(self) -> bool:
        """Kiểm tra HTML5 required validation trên username field"""
        return not self.is_field_valid("username")

    def is_password_field_required(self) -> bool:
        """Kiểm tra HTML5 required validation trên password field"""
        return not self.is_field_valid("password")

    def is_html5_blocked(self) -> bool:
        """
        Kiểm tra HTML5 validation chặn form submit.
        True = form bị chặn (có field invalid)
        """
        return not (self.is_field_valid("username") and self.is_field_valid("password"))

    def get_username_validation_message(self) -> str:
        """Lấy HTML5 validation message của username field"""
        return self.get_js_validation_message("username")

    def get_password_validation_message(self) -> str:
        """Lấy HTML5 validation message của password field"""
        return self.get_js_validation_message("password")

    # ------------------------------------------------------------------
    # LOGOUT (khi đang ở trang khác, dùng URL trực tiếp)
    # ------------------------------------------------------------------
    def logout(self) -> "LoginPage":
        """Đăng xuất và mở lại trang login"""
        self.navigate("/users/logout/")
        time.sleep(1)
        self.navigate(self.PATH)
        self.find(self.USERNAME_FIELD)
        return self
