"""
Cart Page — Page Object Model
Trang: /cart/
Module: Cart (Giỏ hàng)
Thành viên phụ trách: [Thành viên 4 — Cart Module]
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage


class CartPage(BasePage):
    """
    Page Object cho trang Giỏ Hàng — Shoes Store.
    Liên quan: TC-CART-001 → TC-CART-006
    """

    PATH = "/cart/"

    # ------------------------------------------------------------------
    # LOCATORS
    # ------------------------------------------------------------------
    # Cart Items
    CART_ITEMS       = (By.CSS_SELECTOR, ".cart-item, tr.cart-row, .cart-product")
    ITEM_NAMES       = (By.CSS_SELECTOR, ".cart-item .item-name, .cart-product-name")
    ITEM_PRICES      = (By.CSS_SELECTOR, ".cart-item .item-price, .cart-product-price")
    ITEM_QUANTITIES  = (By.CSS_SELECTOR, ".cart-item input[name='quantity'], "
                                          ".quantity-input")
    REMOVE_BUTTONS   = (By.CSS_SELECTOR, ".remove-item, .delete-item, "
                                          "button[data-action='remove'], "
                                          "a[href*='remove'], .cart-remove")

    # Totals
    SUBTOTAL         = (By.CSS_SELECTOR, ".subtotal, .cart-subtotal, #subtotal")
    TOTAL_PRICE      = (By.CSS_SELECTOR, ".cart-total, .total-price, "
                                          "#cart-total, .grand-total")

    # Empty Cart
    EMPTY_CART_MSG   = (By.CSS_SELECTOR, ".cart-empty, .empty-cart, "
                                          ".cart-empty-message")

    # Actions
    CHECKOUT_BUTTON  = (By.CSS_SELECTOR, ".checkout-btn, a[href*='checkout'], "
                                          "#checkout-btn, .proceed-checkout")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, "a[href*='/'], .continue-shopping, "
                                           ".back-to-shop")
    UPDATE_CART_BTN  = (By.CSS_SELECTOR, ".update-cart, #update-cart")

    # Messages
    SUCCESS_ALERT    = (By.CSS_SELECTOR, ".messages-container .premium-alert")

    # ------------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------------
    def open(self) -> "CartPage":
        """Mở trang giỏ hàng"""
        self.navigate(self.PATH)
        time.sleep(1)
        return self

    def remove_item(self, index: int = 0) -> "CartPage":
        """
        Xoá sản phẩm khỏi giỏ hàng theo index.
        index=0 = sản phẩm đầu tiên
        """
        remove_btns = self.find_all(self.REMOVE_BUTTONS)
        if not remove_btns:
            raise AssertionError("Không tìm thấy nút xoá sản phẩm")
        if index >= len(remove_btns):
            raise IndexError(f"Không có nút xoá tại index {index}")
        self.execute_js("arguments[0].click();", remove_btns[index])
        time.sleep(1)
        return self

    def update_quantity(self, index: int = 0, quantity: int = 2) -> "CartPage":
        """Cập nhật số lượng sản phẩm"""
        qty_inputs = self.find_all(self.ITEM_QUANTITIES)
        if qty_inputs and index < len(qty_inputs):
            inp = qty_inputs[index]
            inp.clear()
            inp.send_keys(str(quantity))
            # Submit form hoặc click update
            if self.is_element_present(self.UPDATE_CART_BTN):
                self.click(self.UPDATE_CART_BTN)
            else:
                from selenium.webdriver.common.keys import Keys
                inp.send_keys(Keys.RETURN)
            time.sleep(1)
        return self

    def click_checkout(self) -> "CartPage":
        """Click nút Đặt hàng / Thanh toán"""
        self.scroll_to_element(self.CHECKOUT_BUTTON)
        self.click(self.CHECKOUT_BUTTON)
        time.sleep(1)
        return self

    def continue_shopping(self) -> "CartPage":
        """Click link tiếp tục mua hàng"""
        if self.is_element_present(self.CONTINUE_SHOPPING):
            self.click(self.CONTINUE_SHOPPING)
        else:
            self.navigate("/")
        return self

    # ------------------------------------------------------------------
    # STATE CHECKS
    # ------------------------------------------------------------------
    def is_page_ok(self) -> bool:
        """Trang giỏ hàng không có lỗi server"""
        return not self.has_server_error()

    def is_empty(self) -> bool:
        """Giỏ hàng có trống không"""
        return (
            self.get_item_count() == 0
            or self.is_visible(self.EMPTY_CART_MSG, timeout=2)
        )

    def get_item_count(self) -> int:
        """Số sản phẩm trong giỏ hàng"""
        return len(self.find_all(self.CART_ITEMS))

    def get_item_names(self) -> list:
        """Danh sách tên sản phẩm trong giỏ"""
        els = self.find_all(self.ITEM_NAMES)
        return [el.text.strip() for el in els]

    def get_total(self) -> str:
        """Tổng tiền giỏ hàng"""
        return self.get_text(self.TOTAL_PRICE, timeout=3)

    def get_subtotal(self) -> str:
        return self.get_text(self.SUBTOTAL, timeout=3)

    def is_checkout_available(self) -> bool:
        """Có nút thanh toán không"""
        return self.is_visible(self.CHECKOUT_BUTTON, timeout=3)

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_ALERT, timeout=3)

    def is_on_cart_page(self) -> bool:
        return self.PATH in self.get_current_url() or "/cart" in self.get_current_url()

    def get_quantity_of_item(self, index: int = 0) -> int:
        """Lấy số lượng của sản phẩm tại index"""
        qty_inputs = self.find_all(self.ITEM_QUANTITIES)
        if qty_inputs and index < len(qty_inputs):
            val = qty_inputs[index].get_attribute("value")
            return int(val) if val and val.isdigit() else 0
        return 0
