"""
Order Page — Page Object Model
Trang: /orders/ và /orders/history/
Module: Order (Đặt hàng)
Thành viên phụ trách: [Thành viên 5 — Order Module]
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class OrderPage(BasePage):
    """
    Page Object cho trang Đặt Hàng và Lịch Sử Đơn Hàng — Shoes Store.
    Liên quan: TC-ORD-001 → TC-ORD-006
    """

    ORDERS_PATH  = "/orders/"
    HISTORY_PATH = "/orders/history/"
    CHECKOUT_PATH = "/orders/checkout/"

    # ------------------------------------------------------------------
    # LOCATORS — Checkout Page
    # ------------------------------------------------------------------
    # Shipping Form
    RECIPIENT_NAME   = (By.CSS_SELECTOR, "input[name='recipient_name'], #recipient-name")
    PHONE_FIELD      = (By.CSS_SELECTOR, "input[name='phone'], #phone")
    ADDRESS_FIELD    = (By.CSS_SELECTOR, "input[name='address'], textarea[name='address'], "
                                          "#address")
    CITY_FIELD       = (By.CSS_SELECTOR, "input[name='city'], select[name='city']")
    NOTE_FIELD       = (By.CSS_SELECTOR, "textarea[name='note'], #note")

    # Payment
    PAYMENT_OPTIONS  = (By.CSS_SELECTOR, "input[name='payment_method']")
    COD_OPTION       = (By.CSS_SELECTOR, "input[value='cod'], input[value='COD']")
    BANK_OPTION      = (By.CSS_SELECTOR, "input[value='bank'], input[value='BANK']")

    # Submit
    PLACE_ORDER_BTN  = (By.CSS_SELECTOR, ".place-order-btn, #place-order, "
                                          "button[type='submit'].checkout-submit")

    # Order Summary
    ORDER_SUMMARY    = (By.CSS_SELECTOR, ".order-summary, .checkout-summary")
    SUMMARY_ITEMS    = (By.CSS_SELECTOR, ".order-summary .item, .summary-item")
    SUMMARY_TOTAL    = (By.CSS_SELECTOR, ".order-total, .checkout-total")

    # ------------------------------------------------------------------
    # LOCATORS — Order History Page
    # ------------------------------------------------------------------
    ORDER_ROWS       = (By.CSS_SELECTOR, ".order-row, tr.order-item, .order-card, "
                                          ".order-list .order")
    ORDER_CODES      = (By.CSS_SELECTOR, ".order-code, .order-id, td:first-child")
    ORDER_STATUSES   = (By.CSS_SELECTOR, ".order-status, .status-badge, "
                                          ".order-state")
    ORDER_DATES      = (By.CSS_SELECTOR, ".order-date, .created-at")
    ORDER_TOTALS     = (By.CSS_SELECTOR, ".order-total-price, .order-amount")

    EMPTY_ORDER_MSG  = (By.CSS_SELECTOR, ".no-orders, .empty-orders, .order-empty")
    ORDER_DETAIL_LINK= (By.CSS_SELECTOR, ".order-detail-link, a[href*='/orders/']")

    # Messages
    SUCCESS_ALERT    = (By.CSS_SELECTOR, ".messages-container .premium-alert, "
                                          ".alert-success")
    ERROR_ALERT      = (By.CSS_SELECTOR, ".messages-container .alert-danger, "
                                          ".alert-error")

    # ------------------------------------------------------------------
    # ACTIONS — Checkout
    # ------------------------------------------------------------------
    def open_checkout(self) -> "OrderPage":
        """Mở trang thanh toán"""
        self.navigate(self.CHECKOUT_PATH)
        time.sleep(1)
        return self

    def fill_shipping_info(self, name: str = "", phone: str = "",
                           address: str = "", city: str = "") -> "OrderPage":
        """Điền thông tin giao hàng"""
        if name and self.is_element_present(self.RECIPIENT_NAME):
            self.input_text(self.RECIPIENT_NAME, name)
        if phone and self.is_element_present(self.PHONE_FIELD):
            self.input_text(self.PHONE_FIELD, phone)
        if address and self.is_element_present(self.ADDRESS_FIELD):
            self.input_text(self.ADDRESS_FIELD, address)
        return self

    def select_payment_method(self, method: str = "cod") -> "OrderPage":
        """Chọn phương thức thanh toán (cod/bank)"""
        if method.lower() == "cod" and self.is_element_present(self.COD_OPTION):
            self.click(self.COD_OPTION)
        elif method.lower() == "bank" and self.is_element_present(self.BANK_OPTION):
            self.click(self.BANK_OPTION)
        return self

    def click_place_order(self) -> "OrderPage":
        """Click nút Đặt hàng"""
        if self.is_element_present(self.PLACE_ORDER_BTN):
            self.scroll_to_element(self.PLACE_ORDER_BTN)
            self.click(self.PLACE_ORDER_BTN)
            time.sleep(2)
        return self

    # ------------------------------------------------------------------
    # ACTIONS — Order History
    # ------------------------------------------------------------------
    def open_history(self) -> "OrderPage":
        """Mở trang lịch sử đơn hàng"""
        self.navigate(self.HISTORY_PATH)
        time.sleep(1)
        return self

    def open_orders(self) -> "OrderPage":
        """Mở trang quản lý đơn hàng"""
        self.navigate(self.ORDERS_PATH)
        time.sleep(1)
        return self

    def click_order_detail(self, index: int = 0) -> "OrderPage":
        """Xem chi tiết đơn hàng"""
        links = self.find_all(self.ORDER_DETAIL_LINK)
        if links and index < len(links):
            self.execute_js("arguments[0].click();", links[index])
            time.sleep(1)
        return self

    # ------------------------------------------------------------------
    # STATE CHECKS
    # ------------------------------------------------------------------
    def is_page_accessible(self) -> bool:
        """Trang có thể truy cập (không có lỗi server)"""
        return not self.has_server_error()

    def is_page_ok(self) -> bool:
        return self.is_page_accessible()

    def get_order_count(self) -> int:
        """Số lượng đơn hàng hiển thị"""
        return len(self.find_all(self.ORDER_ROWS))

    def has_orders(self) -> bool:
        """Có đơn hàng nào không"""
        return self.get_order_count() > 0

    def get_all_order_statuses(self) -> list:
        """Lấy danh sách trạng thái các đơn hàng"""
        els = self.find_all(self.ORDER_STATUSES)
        return [el.text.strip() for el in els]

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_ALERT, timeout=3)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_ALERT, timeout=3)

    def is_order_placed_successfully(self) -> bool:
        """Đặt hàng thành công (redirect về trang xác nhận hoặc lịch sử)"""
        url = self.get_current_url().lower()
        return (
            "success" in url
            or "confirm" in url
            or "history" in url
            or "orders" in url
        ) and self.is_page_accessible()

    def is_checkout_page(self) -> bool:
        return "checkout" in self.get_current_url().lower()

    def get_order_summary_total(self) -> str:
        return self.get_text(self.SUMMARY_TOTAL, timeout=3)
