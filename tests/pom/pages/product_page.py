"""
Product Detail Page — Page Object Model
Trang: /products/<slug>/
Module: Product (Chi tiết sản phẩm)
Thành viên phụ trách: [Thành viên 3 — Product Module]
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage


class ProductPage(BasePage):
    """
    Page Object cho trang Chi Tiết Sản Phẩm — Shoes Store.
    Liên quan: TC-PROD-005 → TC-PROD-008, TC-CART-001
    """

    # ------------------------------------------------------------------
    # LOCATORS
    # ------------------------------------------------------------------
    # Product Info
    PRODUCT_TITLE   = (By.CSS_SELECTOR, ".product-title, h1.product-name, .detail-title")
    PRODUCT_PRICE   = (By.CSS_SELECTOR, ".product-price, .price, .detail-price")
    PRODUCT_DESC    = (By.CSS_SELECTOR, ".product-description, .product-desc")
    PRODUCT_IMAGE   = (By.CSS_SELECTOR, ".product-image img, .detail-image img")
    BREADCRUMB      = (By.CSS_SELECTOR, ".breadcrumb, nav[aria-label='breadcrumb']")

    # Size Selection
    SIZE_OPTIONS    = (By.CSS_SELECTOR, "input[name='size']")
    SIZE_LABELS     = (By.XPATH,
                       "//input[@name='size']/following-sibling::label")
    AVAILABLE_SIZE  = (By.XPATH,
                       "//input[@name='size' and not(@disabled)]/following-sibling::label")
    SELECTED_SIZE   = (By.CSS_SELECTOR, "input[name='size']:checked + label")

    # Cart Actions
    ADD_TO_CART_BTN = (By.CSS_SELECTOR,
                       "button.product-cart-btn, .add-to-cart, #add-to-cart-btn")
    BUY_NOW_BTN     = (By.CSS_SELECTOR, ".buy-now-btn, button[name='buy_now']")
    QUANTITY_INPUT  = (By.CSS_SELECTOR, "input[name='quantity'], #quantity")

    # Feedback
    CART_COUNT      = (By.ID, "cart-count")
    SUCCESS_MSG     = (By.CSS_SELECTOR, ".messages-container .premium-alert, "
                                         ".alert-success")
    STOCK_STATUS    = (By.CSS_SELECTOR, ".stock-status, .in-stock, .out-of-stock")

    # Related Products
    RELATED_PRODUCTS = (By.CSS_SELECTOR, ".related-products .product-card")

    # ------------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------------
    def open_by_url(self, url: str) -> "ProductPage":
        """Mở trang chi tiết sản phẩm theo URL đầy đủ"""
        self.driver.get(url)
        time.sleep(1)
        return self

    def select_size(self, index: int = 0) -> "ProductPage":
        """Chọn size theo index (mặc định size đầu tiên còn hàng)"""
        sizes = self.find_all(self.AVAILABLE_SIZE)
        if not sizes:
            raise AssertionError("Không có size nào còn hàng")
        target = sizes[index] if index < len(sizes) else sizes[0]
        self.execute_js("arguments[0].click();", target)
        time.sleep(0.3)
        return self

    def select_size_by_text(self, size_text: str) -> "ProductPage":
        """Chọn size theo tên (ví dụ: '40', '41', 'M', 'L')"""
        sizes = self.find_all(self.AVAILABLE_SIZE)
        for size in sizes:
            if size.text.strip() == size_text:
                self.execute_js("arguments[0].click();", size)
                time.sleep(0.3)
                return self
        raise ValueError(f"Không tìm thấy size '{size_text}'")

    def set_quantity(self, qty: int) -> "ProductPage":
        """Đặt số lượng sản phẩm"""
        if self.is_element_present(self.QUANTITY_INPUT):
            qty_el = self.driver.find_element(*self.QUANTITY_INPUT)
            qty_el.clear()
            qty_el.send_keys(str(qty))
        return self

    def click_add_to_cart(self) -> "ProductPage":
        """Click nút Thêm vào giỏ hàng"""
        self.scroll_to_element(self.ADD_TO_CART_BTN)
        self.click(self.ADD_TO_CART_BTN)
        time.sleep(1.5)  # Chờ AJAX response
        return self

    def add_to_cart(self, size_index: int = 0) -> "ProductPage":
        """
        Luồng đầy đủ: Chọn size → Click thêm vào giỏ.
        """
        self.select_size(size_index)
        self.click_add_to_cart()
        return self

    # ------------------------------------------------------------------
    # STATE CHECKS
    # ------------------------------------------------------------------
    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_TITLE)

    def get_product_price(self) -> str:
        return self.get_text(self.PRODUCT_PRICE)

    def get_cart_count(self) -> int:
        try:
            text = self.get_text(self.CART_COUNT, timeout=3)
            return int(text) if text and text.isdigit() else 0
        except Exception:
            return 0

    def get_available_sizes(self) -> list:
        """Lấy danh sách các sizes còn hàng"""
        els = self.find_all(self.AVAILABLE_SIZE)
        return [el.text.strip() for el in els]

    def get_all_sizes(self) -> list:
        """Lấy tất cả sizes (kể cả hết hàng)"""
        els = self.find_all(self.SIZE_LABELS)
        return [el.text.strip() for el in els]

    def has_sizes(self) -> bool:
        """Kiểm tra sản phẩm có chọn size không"""
        return self.is_element_present(self.SIZE_OPTIONS)

    def is_product_loaded(self) -> bool:
        """Trang chi tiết sản phẩm đã load đủ"""
        return (
            self.is_visible(self.PRODUCT_TITLE)
            and not self.has_server_error()
        )

    def is_add_to_cart_enabled(self) -> bool:
        """Nút thêm vào giỏ có enabled không"""
        try:
            btn = self.driver.find_element(*self.ADD_TO_CART_BTN)
            return btn.is_enabled() and not btn.get_attribute("disabled")
        except NoSuchElementException:
            return False

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_MSG, timeout=3)

    def is_page_ok(self) -> bool:
        return not self.has_server_error()

    def has_related_products(self) -> bool:
        return len(self.find_all(self.RELATED_PRODUCTS)) > 0
