# =============================================================================
# BASE PAGE — Lớp cơ sở POM
# tests/pom/pages/base_page.py
# =============================================================================
"""
BasePage chứa tất cả các utilities chung:
  - navigate(), find(), click(), input_text()
  - wait strategies (explicit wait)
  - screenshot, scroll, JS executor
  - is_visible(), get_text(), wait_url()
"""

import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class BasePage:
    """
    Lớp cơ sở cho tất cả Page Objects trong dự án Shoes Store.

    Sử dụng:
        class LoginPage(BasePage):
            def __init__(self, driver):
                super().__init__(driver)
    """

    BASE_URL    = "http://127.0.0.1:8000"
    DEFAULT_WAIT = 10  # giây

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait   = WebDriverWait(driver, self.DEFAULT_WAIT)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def navigate(self, path: str = "") -> "BasePage":
        """Điều hướng đến URL = BASE_URL + path"""
        url = f"{self.BASE_URL}{path}"
        self.driver.get(url)
        logger.debug(f"[Navigate] → {url}")
        return self

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def get_page_source(self) -> str:
        return self.driver.page_source

    def refresh(self):
        self.driver.refresh()

    def go_back(self):
        self.driver.back()

    # ------------------------------------------------------------------
    # Element Interaction
    # ------------------------------------------------------------------
    def find(self, locator: tuple, timeout: int = None):
        """Tìm element với explicit wait"""
        t = timeout or self.DEFAULT_WAIT
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def find_all(self, locator: tuple) -> list:
        """Tìm tất cả elements"""
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def click(self, locator: tuple, use_js: bool = True):
        """Click element — dùng JS để tránh ElementClickInterceptedException"""
        el = WebDriverWait(self.driver, self.DEFAULT_WAIT).until(
            EC.element_to_be_clickable(locator)
        )
        if use_js:
            self.driver.execute_script("arguments[0].click();", el)
        else:
            el.click()

    def input_text(self, locator: tuple, text: str, clear: bool = True):
        """Nhập text vào input"""
        el = self.find(locator)
        if clear:
            el.clear()
        if text:
            el.send_keys(text)

    def press_enter(self, locator: tuple):
        """Nhấn Enter trên element"""
        self.find(locator).send_keys(Keys.RETURN)

    def get_text(self, locator: tuple, timeout: int = 3) -> str:
        """Lấy text của element, trả về '' nếu không tìm thấy"""
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return el.text.strip()
        except TimeoutException:
            return ""

    def get_attribute(self, locator: tuple, attr: str) -> str:
        """Lấy thuộc tính của element"""
        try:
            el = self.find(locator)
            return el.get_attribute(attr) or ""
        except TimeoutException:
            return ""

    # ------------------------------------------------------------------
    # Wait / State
    # ------------------------------------------------------------------
    def wait_url_contains(self, text: str, timeout: int = 10):
        """Chờ URL chứa chuỗi"""
        WebDriverWait(self.driver, timeout).until(EC.url_contains(text))

    def wait_url_to_be(self, url: str, timeout: int = 10):
        """Chờ URL bằng đúng giá trị"""
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))

    def is_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """Kiểm tra element có hiển thị không"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Kiểm tra element có trong DOM không"""
        return len(self.driver.find_elements(*locator)) > 0

    def wait_for_text(self, locator: tuple, text: str, timeout: int = 10) -> bool:
        """Chờ element chứa text nhất định"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------------
    # JavaScript
    # ------------------------------------------------------------------
    def execute_js(self, script: str, *args):
        """Thực thi JavaScript"""
        return self.driver.execute_script(script, *args)

    def scroll_to_element(self, locator: tuple):
        """Scroll tới element"""
        el = self.driver.find_element(*locator)
        self.execute_js("arguments[0].scrollIntoView({behavior:'smooth',block:'center'});", el)

    def scroll_to_top(self):
        self.execute_js("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        self.execute_js("window.scrollTo(0, document.body.scrollHeight);")

    def get_js_validation_message(self, element_id: str) -> str:
        """Lấy HTML5 validation message"""
        return self.execute_js(
            f"return document.getElementById('{element_id}').validationMessage;"
        ) or ""

    def is_field_valid(self, element_id: str) -> bool:
        """Kiểm tra HTML5 field validity"""
        return bool(self.execute_js(
            f"return document.getElementById('{element_id}').validity.valid;"
        ))

    # ------------------------------------------------------------------
    # Screenshot
    # ------------------------------------------------------------------
    def take_screenshot(self, name: str, directory: str = None) -> str:
        """Chụp ảnh màn hình"""
        if directory is None:
            directory = os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "results", "screenshots"
            )
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"{name}.png")
        self.driver.save_screenshot(path)
        logger.info(f"📷 Screenshot: {path}")
        return path

    # ------------------------------------------------------------------
    # Page Health
    # ------------------------------------------------------------------
    def has_server_error(self) -> bool:
        """Kiểm tra trang có lỗi 500 không"""
        source = self.get_page_source().lower()
        return "500" in source or "server error" in source or "traceback" in source

    def is_page_loaded(self) -> bool:
        """Kiểm tra trang đã load xong (readyState = complete)"""
        return self.execute_js("return document.readyState;") == "complete"
