"""
Register Page — Page Object Model
Trang: /users/register/
Module: Register (Đăng ký tài khoản)
Thành viên phụ trách: [Thành viên 2 — Register Module]
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class RegisterPage(BasePage):
    """
    Page Object cho trang Đăng Ký tài khoản — Shoes Store.
    Liên quan: TC-REG-001 → TC-REG-020
    """

    PATH = "/users/register/"

    # ------------------------------------------------------------------
    # LOCATORS
    # ------------------------------------------------------------------
    FULL_NAME_FIELD      = (By.ID, "full_name")
    EMAIL_FIELD          = (By.ID, "email")
    PHONE_FIELD          = (By.ID, "phone")
    PASSWORD_FIELD       = (By.ID, "password")
    CONFIRM_PWD_FIELD    = (By.ID, "confirm_password")
    SUBMIT_BUTTON        = (By.ID, "submitBtn")

    ERROR_ALERT          = (By.CSS_SELECTOR, ".messages-container .premium-alert")
    SUCCESS_ALERT        = (By.CSS_SELECTOR, ".messages-container .alert-success")

    LOGIN_LINK           = (By.CSS_SELECTOR, "a[href*='login']")

    # ------------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------------
    def open(self) -> "RegisterPage":
        """Mở trang đăng ký"""
        self.navigate(self.PATH)
        self.find(self.FULL_NAME_FIELD)
        return self

    def enter_full_name(self, full_name: str) -> "RegisterPage":
        self.input_text(self.FULL_NAME_FIELD, full_name)
        return self

    def enter_email(self, email: str) -> "RegisterPage":
        self.input_text(self.EMAIL_FIELD, email)
        return self

    def enter_phone(self, phone: str) -> "RegisterPage":
        self.input_text(self.PHONE_FIELD, phone)
        return self

    def enter_password(self, password: str) -> "RegisterPage":
        self.input_text(self.PASSWORD_FIELD, password)
        return self

    def enter_confirm_password(self, confirm_pwd: str) -> "RegisterPage":
        self.input_text(self.CONFIRM_PWD_FIELD, confirm_pwd)
        return self

    def click_submit(self) -> "RegisterPage":
        """Click nút Đăng Ký"""
        self.scroll_to_element(self.SUBMIT_BUTTON)
        self.click(self.SUBMIT_BUTTON)
        time.sleep(0.5)
        return self

    def fill_form(self, full_name: str = "", email: str = "",
                  phone: str = "", password: str = "",
                  confirm_password: str = "") -> "RegisterPage":
        """
        Điền đầy đủ form đăng ký.
        Chỉ điền các trường được cung cấp (trống = bỏ qua).
        """
        if full_name:
            self.enter_full_name(full_name)
        if email:
            self.enter_email(email)
        if phone:
            self.enter_phone(phone)
        if password:
            self.enter_password(password)
        if confirm_password:
            self.enter_confirm_password(confirm_password)
        return self

    def submit(self) -> "RegisterPage":
        """Submit form (alias cho click_submit)"""
        return self.click_submit()

    def register(self, full_name: str, email: str, phone: str,
                 password: str, confirm_password: str) -> "RegisterPage":
        """Thực hiện đầy đủ luồng đăng ký"""
        return self.fill_form(full_name, email, phone, password, confirm_password).submit()

    # ------------------------------------------------------------------
    # STATE CHECKS
    # ------------------------------------------------------------------
    def is_registered_successfully(self) -> bool:
        """Đăng ký thành công = redirect về /users/login/"""
        try:
            self.wait_url_contains("/users/login/", timeout=5)
            return True
        except TimeoutException:
            return False

    def get_error_message(self) -> str:
        """Lấy thông báo lỗi validation"""
        return self.get_text(self.ERROR_ALERT, timeout=3)

    def get_error_message_lower(self) -> str:
        """Lấy thông báo lỗi dạng lowercase"""
        return self.get_error_message().lower()

    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_ALERT)

    def is_on_register_page(self) -> bool:
        return self.PATH in self.get_current_url()

    def get_full_name_max_length(self) -> int:
        """Lấy maxlength của trường họ tên"""
        attr = self.get_attribute(self.FULL_NAME_FIELD, "maxlength")
        return int(attr) if attr and attr.isdigit() else 9999

    def get_full_name_value(self) -> str:
        """Lấy giá trị hiện tại của trường họ tên"""
        return self.get_attribute(self.FULL_NAME_FIELD, "value")

    def get_email_validation_message(self) -> str:
        return self.get_js_validation_message("email")

    def is_submit_button_visible(self) -> bool:
        return self.is_visible(self.SUBMIT_BUTTON)
