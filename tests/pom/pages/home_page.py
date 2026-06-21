"""
Home Page — Page Object Model
Trang: / (Trang chủ / Danh sách sản phẩm)
Module: Product (Sản phẩm)
Thành viên phụ trách: [Thành viên 3 — Product Module]
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage


class HomePage(BasePage):
    """
    Page Object cho trang Chủ — Shoes Store.
    Liên quan: TC-PROD-001 → TC-PROD-004, TC-SEARCH-001 → 003
    """

    PATH = "/"

    # ------------------------------------------------------------------
    # LOCATORS
    # ------------------------------------------------------------------
    # Product Listing
    PRODUCT_CARDS    = (By.CSS_SELECTOR, ".premium-product-card")
    PRODUCT_LINKS    = (By.CSS_SELECTOR, ".premium-product-card a, a.product-link")
    PRODUCT_NAMES    = (By.CSS_SELECTOR, ".premium-product-card .product-name, "
                                          ".premium-product-card h3")
    PRODUCT_PRICES   = (By.CSS_SELECTOR, ".premium-product-card .price, "
                                          ".premium-product-card .product-price")

    # Navigation / Cart
    CART_COUNT       = (By.ID, "cart-count")
    CART_ICON        = (By.CSS_SELECTOR, "a[href*='cart'], .cart-icon")
    LOGIN_LINK       = (By.CSS_SELECTOR, "a[href*='login']")
    REGISTER_LINK    = (By.CSS_SELECTOR, "a[href*='register']")

    # Search
    SEARCH_INPUT     = (By.CSS_SELECTOR,
                        "input[type='search'], #search-input, "
                        "input[name='q'], .search-input")
    SEARCH_BUTTON    = (By.CSS_SELECTOR, "button[type='submit'].search-btn, "
                                          ".search-form button")

    # Category / Filter
    CATEGORY_LINKS   = (By.CSS_SELECTOR, ".category-link, nav a[href*='category']")
    SORT_SELECT      = (By.CSS_SELECTOR, "select[name='sort'], #sort-select")

    # Pagination
    NEXT_PAGE_BTN    = (By.CSS_SELECTOR, ".pagination .next, a[rel='next']")
    PAGE_NUMBERS     = (By.CSS_SELECTOR, ".pagination .page-link, .page-number")

    # Hero / Banner
    HERO_SECTION     = (By.CSS_SELECTOR, ".hero, .banner, .carousel")

    # ------------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------------
    def open(self) -> "HomePage":
        """Mở trang chủ"""
        self.navigate(self.PATH)
        return self

    def wait_for_products(self, timeout: int = 15) -> "HomePage":
        """Chờ danh sách sản phẩm load xong"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.PRODUCT_CARDS)
        )
        return self

    def go_to_product(self, index: int = 0) -> str:
        """
        Click vào sản phẩm theo index và trả về URL trang chi tiết.
        index=0 = sản phẩm đầu tiên
        """
        cards = self.find_all(self.PRODUCT_CARDS)
        if not cards or index >= len(cards):
            raise IndexError(f"Không có sản phẩm tại index {index}")

        # Tìm link trong card
        try:
            link = cards[index].find_element(By.XPATH, "ancestor::a[1]")
        except NoSuchElementException:
            link = cards[index].find_element(By.TAG_NAME, "a")

        href = link.get_attribute("href")
        self.execute_js("arguments[0].click();", link)
        time.sleep(1)
        return href

    def search(self, keyword: str) -> "HomePage":
        """Tìm kiếm sản phẩm theo từ khoá"""
        try:
            search_el = self.driver.find_element(*self.SEARCH_INPUT)
            search_el.clear()
            search_el.send_keys(keyword)
            search_el.send_keys(Keys.RETURN)
            time.sleep(2)
        except NoSuchElementException:
            raise AssertionError("Không tìm thấy ô tìm kiếm trên trang chủ")
        return self

    def go_to_cart(self) -> "HomePage":
        """Click vào biểu tượng giỏ hàng"""
        self.click(self.CART_ICON)
        time.sleep(1)
        return self

    def go_to_login(self) -> "HomePage":
        self.click(self.LOGIN_LINK)
        return self

    # ------------------------------------------------------------------
    # STATE CHECKS
    # ------------------------------------------------------------------
    def get_product_count(self) -> int:
        """Đếm số sản phẩm hiển thị"""
        return len(self.find_all(self.PRODUCT_CARDS))

    def get_cart_count(self) -> int:
        """Lấy số lượng sản phẩm trong giỏ hàng từ header"""
        try:
            text = self.get_text(self.CART_COUNT, timeout=3)
            return int(text) if text and text.isdigit() else 0
        except Exception:
            return 0

    def is_search_available(self) -> bool:
        """Kiểm tra có ô tìm kiếm không"""
        return self.is_element_present(self.SEARCH_INPUT)

    def is_logged_in(self) -> bool:
        """Kiểm tra user đã đăng nhập (thấy user menu hoặc không thấy nút Login)"""
        page_lower = self.get_page_source().lower()
        return "đăng xuất" in page_lower or "logout" in page_lower

    def get_all_product_names(self) -> list:
        """Lấy danh sách tên tất cả sản phẩm hiển thị"""
        elements = self.find_all(self.PRODUCT_NAMES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_all_product_prices(self) -> list:
        """Lấy danh sách giá tất cả sản phẩm hiển thị"""
        elements = self.find_all(self.PRODUCT_PRICES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def is_page_ok(self) -> bool:
        """Trang không có lỗi server"""
        return not self.has_server_error()

    def has_pagination(self) -> bool:
        """Kiểm tra có phân trang không"""
        return self.is_element_present(self.PAGE_NUMBERS)
