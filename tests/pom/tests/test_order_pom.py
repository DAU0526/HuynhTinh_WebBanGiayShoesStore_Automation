# =============================================================================
# TEST ORDER POM — Kiểm thử module Đặt Hàng
# Dự án: Shoes Store — Tuần 4 — POM
# Thành viên phụ trách: [Thành viên 5]
# =============================================================================
"""
TC-ORD-001: Truy cập trang lịch sử đơn hàng              [Smoke]
TC-ORD-002: Lịch sử đơn hàng không có lỗi server         [Smoke]
TC-ORD-003: Trang checkout có thể truy cập               [Smoke]
TC-ORD-004: Lịch sử đơn hàng khi chưa đăng nhập         [Regression]
TC-ORD-005: Trang đặt hàng (orders) không lỗi server     [Regression]
TC-ORD-006: Số đơn hàng hiển thị đúng                    [Regression]
"""

import pytest
from ..pages import LoginPage, OrderPage


# ---------------------------------------------------------------------------
# SMOKE TESTS
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.order
@pytest.mark.pom
class TestOrderSmoke:

    def test_TC_ORD_001_order_history_accessible(self, driver, test_credentials):
        """
        TC-ORD-001: Truy cập trang lịch sử đơn hàng khi đã đăng nhập
        Expected: Trang load được, không có lỗi server
        """
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        page = OrderPage(driver).open_history()
        assert page.is_page_accessible(), (
            "TC-ORD-001 FAIL: Trang lịch sử đơn hàng không được có lỗi server"
        )
        page.take_screenshot("TC_ORD_001_pass")

    def test_TC_ORD_002_order_history_no_server_error(self, driver, test_credentials):
        """TC-ORD-002: Trang lịch sử đơn hàng không có lỗi 500"""
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        page = OrderPage(driver).open_history()
        assert not page.has_server_error(), (
            "TC-ORD-002 FAIL: Trang lịch sử đơn hàng không được có lỗi 500"
        )

    def test_TC_ORD_003_checkout_page_accessible(self, driver, test_credentials):
        """
        TC-ORD-003: Trang checkout có thể truy cập (khi đã đăng nhập)
        Note: Có thể redirect về cart nếu giỏ hàng trống — OK
        """
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        page = OrderPage(driver).open_checkout()
        assert page.is_page_accessible(), (
            "TC-ORD-003 FAIL: Trang checkout không được có lỗi server"
        )
        page.take_screenshot("TC_ORD_003_checkout")


# ---------------------------------------------------------------------------
# REGRESSION TESTS
# ---------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.order
@pytest.mark.pom
class TestOrderRegression:

    def test_TC_ORD_004_order_history_requires_login(self, driver):
        """
        TC-ORD-004: Lịch sử đơn hàng khi chưa đăng nhập
        Expected: Redirect về login hoặc trang không có lỗi server
        """
        # Không đăng nhập
        page = OrderPage(driver)
        page.navigate(OrderPage.HISTORY_PATH)
        import time; time.sleep(1)

        # Kiểm tra: redirect về login HOẶC không có lỗi server
        current_url = page.get_current_url().lower()
        assert (
            "login" in current_url
            or page.is_page_accessible()
        ), "TC-ORD-004 FAIL: Chưa login phải redirect về login hoặc trang không lỗi server"
        page.take_screenshot("TC_ORD_004_no_login")

    def test_TC_ORD_005_orders_page_no_server_error(self, driver, test_credentials):
        """TC-ORD-005: Trang /orders/ không có lỗi server"""
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        page = OrderPage(driver).open_orders()
        assert page.is_page_accessible(), (
            "TC-ORD-005 FAIL: Trang /orders/ không được có lỗi server"
        )

    def test_TC_ORD_006_order_count_is_non_negative(self, driver, test_credentials):
        """
        TC-ORD-006: Số đơn hàng hiển thị là số không âm (≥ 0)
        """
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        page = OrderPage(driver).open_history()
        count = page.get_order_count()
        assert count >= 0, (
            f"TC-ORD-006 FAIL: Số đơn hàng phải >= 0. Got: {count}"
        )
        page.take_screenshot("TC_ORD_006_order_count")
