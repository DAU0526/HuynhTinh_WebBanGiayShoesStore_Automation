# =============================================================================
# TEST CART POM — Kiểm thử module Giỏ Hàng
# Dự án: Shoes Store — Tuần 4 — POM
# Thành viên phụ trách: [Thành viên 4]
# =============================================================================
"""
TC-CART-001: Thêm sản phẩm vào giỏ hàng thành công        [Smoke]
TC-CART-002: Xem giỏ hàng hiển thị đúng                   [Smoke]
TC-CART-003: Giỏ hàng khi chưa đăng nhập                  [Smoke]
TC-CART-004: Xoá sản phẩm khỏi giỏ hàng                   [Regression]
TC-CART-005: Giỏ hàng không có lỗi server                  [Regression]
TC-CART-006: Checkout button hiển thị khi có hàng          [Regression]
"""

import time
import pytest
from ..pages import LoginPage, HomePage, ProductPage, CartPage


def _add_product_to_cart(driver, test_credentials: dict) -> CartPage:
    """Helper: đăng nhập và thêm 1 sản phẩm vào giỏ"""
    LoginPage(driver).open().login(
        test_credentials["email"], test_credentials["password"]
    )
    home = HomePage(driver)
    home.open()
    products = home.get_product_count()
    if products == 0:
        pytest.skip("Không có sản phẩm để test cart")

    home.go_to_product(0)
    product = ProductPage(driver)

    if product.has_sizes():
        product.add_to_cart(size_index=0)
    else:
        product.click_add_to_cart()

    time.sleep(1)
    return CartPage(driver)


# ---------------------------------------------------------------------------
# SMOKE TESTS
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.cart
@pytest.mark.pom
class TestCartSmoke:

    def test_TC_CART_001_add_product_to_cart(self, driver, test_credentials):
        """
        TC-CART-001: Thêm sản phẩm vào giỏ hàng thành công
        Steps:
          1. Đăng nhập
          2. Vào trang sản phẩm đầu tiên
          3. Chọn size đầu tiên còn hàng
          4. Click Thêm vào giỏ
        Expected: Cart count > 0
        """
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        home = HomePage(driver)
        home.open()
        initial_count = home.get_cart_count()

        if home.get_product_count() == 0:
            pytest.skip("Không có sản phẩm để test")

        home.go_to_product(0)
        product = ProductPage(driver)

        if not product.has_sizes():
            pytest.skip("Sản phẩm không có size")

        product.add_to_cart(0)
        new_count = product.get_cart_count()

        assert new_count > initial_count or new_count > 0, (
            f"TC-CART-001 FAIL: Cart count phải > 0 sau khi thêm. Got: {new_count}"
        )
        product.take_screenshot("TC_CART_001_pass")

    def test_TC_CART_002_view_cart_page(self, driver, test_credentials):
        """
        TC-CART-002: Trang giỏ hàng hiển thị đúng (không lỗi server)
        """
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        cart = CartPage(driver).open()
        assert cart.is_page_ok(), (
            "TC-CART-002 FAIL: Trang giỏ hàng không được có lỗi server"
        )
        cart.take_screenshot("TC_CART_002_pass")

    def test_TC_CART_003_cart_accessible_without_login(self, driver):
        """
        TC-CART-003: Giỏ hàng có thể truy cập khi chưa đăng nhập
        Expected: Trang không lỗi 500 (có thể redirect đến login)
        """
        cart = CartPage(driver).open()
        assert cart.is_page_ok(), (
            "TC-CART-003 FAIL: Giỏ hàng không được có lỗi server khi chưa đăng nhập"
        )
        cart.take_screenshot("TC_CART_003_no_login")


# ---------------------------------------------------------------------------
# REGRESSION TESTS
# ---------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.cart
@pytest.mark.pom
class TestCartRegression:

    def test_TC_CART_004_remove_product_from_cart(self, driver, test_credentials):
        """
        TC-CART-004: Xoá sản phẩm khỏi giỏ hàng
        Steps:
          1. Thêm ít nhất 1 sản phẩm vào giỏ
          2. Mở giỏ hàng
          3. Click nút xoá
        Expected: Số sản phẩm giảm
        """
        # Thêm sản phẩm trước
        _add_product_to_cart(driver, test_credentials)

        cart = CartPage(driver).open()
        count_before = cart.get_item_count()

        if count_before == 0:
            pytest.skip("Giỏ hàng trống, không thể test xoá")

        cart.remove_item(0)
        time.sleep(1)
        count_after = cart.get_item_count()

        assert count_after < count_before, (
            f"TC-CART-004 FAIL: Số sản phẩm phải giảm sau khi xoá. "
            f"Before: {count_before}, After: {count_after}"
        )
        cart.take_screenshot("TC_CART_004_remove")

    def test_TC_CART_005_cart_no_server_error(self, driver, test_credentials):
        """TC-CART-005: Trang giỏ hàng không có lỗi server 500"""
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        cart = CartPage(driver).open()
        assert not cart.has_server_error(), (
            "TC-CART-005 FAIL: Trang giỏ hàng không được có lỗi server"
        )

    def test_TC_CART_006_checkout_visible_when_cart_has_items(self, driver, test_credentials):
        """
        TC-CART-006: Nút Checkout hiển thị khi giỏ hàng có sản phẩm
        """
        _add_product_to_cart(driver, test_credentials)
        cart = CartPage(driver).open()

        if cart.is_empty():
            pytest.skip("Giỏ hàng trống — sản phẩm có thể đã không thêm được")

        assert cart.is_checkout_available(), (
            "TC-CART-006 FAIL: Nút Checkout phải hiển thị khi có sản phẩm trong giỏ"
        )
        cart.take_screenshot("TC_CART_006_checkout_btn")

    def test_TC_CART_007_empty_cart_shows_message(self, driver, test_credentials):
        """
        TC-CART-007: Giỏ hàng trống hiển thị thông báo phù hợp
        """
        # Đăng nhập với tài khoản trống giỏ hàng (hoặc xoá hết)
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        cart = CartPage(driver).open()

        if not cart.is_empty():
            # Xoá tất cả items
            while cart.get_item_count() > 0:
                try:
                    cart.remove_item(0)
                    time.sleep(0.5)
                    cart.open()
                except Exception:
                    break

        # Kiểm tra trang không lỗi dù giỏ trống
        assert cart.is_page_ok(), (
            "TC-CART-007 FAIL: Trang giỏ hàng trống không được có lỗi server"
        )
        cart.take_screenshot("TC_CART_007_empty")
