# =============================================================================
# TEST AUTH POM — Kiểm thử module Đăng Nhập/Đăng Xuất
# Dự án: Shoes Store — Tuần 4 (Chương 7+8) — POM
# Thành viên phụ trách: [Thành viên 1]
# =============================================================================
"""
Test Suite: Auth — Đăng Nhập & Đăng Xuất
  TC-AUTH-001: Đăng nhập thành công bằng Email         [Smoke]
  TC-AUTH-002: Đăng nhập thành công bằng SĐT           [Smoke]
  TC-AUTH-003: Đăng nhập thất bại — Email sai           [Smoke]
  TC-AUTH-004: Đăng nhập thất bại — Mật khẩu sai        [Smoke]
  TC-AUTH-005: Bỏ trống tất cả trường                   [Smoke]
  TC-AUTH-006: Bỏ trống trường Email                    [Regression]
  TC-AUTH-007: Bỏ trống trường Mật khẩu                 [Regression]
  TC-AUTH-008: Đăng xuất thành công                     [Smoke]
"""

import pytest
from ..pages import LoginPage


# ---------------------------------------------------------------------------
# SMOKE TESTS — Kiểm tra luồng chính
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.auth
@pytest.mark.pom
class TestLoginSmoke:
    """Smoke Tests — Đăng nhập cơ bản"""

    def test_TC_AUTH_001_login_success_with_email(self, driver, test_credentials):
        """
        TC-AUTH-001: Đăng nhập thành công bằng Email
        Precondition: Tài khoản testuser@gmail.com / Test@1234 tồn tại
        Steps:
          1. Mở trang /users/login/
          2. Nhập email hợp lệ và mật khẩu đúng
          3. Click Đăng Nhập
        Expected: Redirect về trang chủ (/)
        """
        page = LoginPage(driver)
        page.open()
        page.login(test_credentials["email"], test_credentials["password"])
        assert page.is_logged_in(), (
            f"TC-AUTH-001 FAIL: Đăng nhập bằng email phải redirect về home. "
            f"URL hiện tại: {page.get_current_url()}"
        )
        page.take_screenshot("TC_AUTH_001_pass")

    def test_TC_AUTH_002_login_success_with_phone(self, driver, test_credentials):
        """
        TC-AUTH-002: Đăng nhập thành công bằng Số Điện Thoại
        Steps:
          1. Mở trang /users/login/
          2. Nhập SĐT hợp lệ và mật khẩu đúng
          3. Click Đăng Nhập
        Expected: Redirect về trang chủ (/)
        """
        page = LoginPage(driver)
        page.open()
        page.login(test_credentials["phone"], test_credentials["password"])
        assert page.is_logged_in(), (
            f"TC-AUTH-002 FAIL: Đăng nhập bằng SĐT phải redirect về home. "
            f"URL: {page.get_current_url()}"
        )
        page.take_screenshot("TC_AUTH_002_pass")

    def test_TC_AUTH_003_login_fail_invalid_email(self, driver, test_credentials):
        """
        TC-AUTH-003: Đăng nhập thất bại — Email không tồn tại
        Steps:
          1. Nhập email không tồn tại
          2. Nhập mật khẩu đúng
          3. Submit
        Expected: Hiển thị thông báo lỗi
        """
        page = LoginPage(driver)
        page.open()
        page.login("invalid_notexist@test.com", test_credentials["password"])
        msg = page.get_error_message()
        msg_lower = msg.lower()
        assert msg and ("không đúng" in msg_lower or "sai" in msg_lower
                        or "không tồn tại" in msg_lower or "invalid" in msg_lower), (
            f"TC-AUTH-003 FAIL: Phải có thông báo lỗi. Got: {msg!r}"
        )
        page.take_screenshot("TC_AUTH_003_pass")

    def test_TC_AUTH_004_login_fail_wrong_password(self, driver, test_credentials):
        """
        TC-AUTH-004: Đăng nhập thất bại — Mật khẩu sai
        Steps:
          1. Nhập email đúng
          2. Nhập mật khẩu SAI
          3. Submit
        Expected: Hiển thị thông báo lỗi
        """
        page = LoginPage(driver)
        page.open()
        page.login(test_credentials["email"], "WrongPassword@999")
        msg = page.get_error_message()
        assert msg, (
            f"TC-AUTH-004 FAIL: Phải có thông báo lỗi khi sai mật khẩu. Got: {msg!r}"
        )
        page.take_screenshot("TC_AUTH_004_pass")

    def test_TC_AUTH_005_login_empty_all_fields(self, driver):
        """
        TC-AUTH-005: Bỏ trống cả 2 trường
        Expected: HTML5 validation chặn submit
        """
        page = LoginPage(driver)
        page.open()
        # Click submit mà không nhập gì
        page.driver.execute_script(
            "document.querySelector('button[type=\"submit\"]').click();"
        )
        assert page.is_html5_blocked(), (
            "TC-AUTH-005 FAIL: HTML5 validation phải chặn form khi trống cả 2 trường"
        )
        page.take_screenshot("TC_AUTH_005_pass")

    def test_TC_AUTH_008_logout_success(self, driver, test_credentials):
        """
        TC-AUTH-008: Đăng xuất thành công
        Steps:
          1. Đăng nhập thành công
          2. Truy cập URL logout
          3. Redirect về trang chủ
        Expected: Trang chứa nút/link Đăng Nhập
        """
        page = LoginPage(driver)
        page.open()
        page.login(test_credentials["email"], test_credentials["password"])
        assert page.is_logged_in(), "Cần đăng nhập trước để test logout"

        # Đăng xuất
        page.navigate("/users/logout/")
        import time; time.sleep(1)

        page_source = page.get_page_source().lower()
        assert "đăng nhập" in page_source or "login" in page_source, (
            "TC-AUTH-008 FAIL: Sau đăng xuất phải hiện link Đăng Nhập"
        )
        page.take_screenshot("TC_AUTH_008_pass")


# ---------------------------------------------------------------------------
# REGRESSION TESTS — Kiểm tra chi tiết
# ---------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.auth
@pytest.mark.pom
class TestLoginRegression:
    """Regression Tests — Kiểm tra các trường hợp biên và edge case"""

    def test_TC_AUTH_006_login_empty_username(self, driver, test_credentials):
        """
        TC-AUTH-006: Bỏ trống trường Email/SĐT
        Expected: HTML5 validation chặn submit
        """
        page = LoginPage(driver)
        page.open()
        page.enter_password(test_credentials["password"])
        page.click_submit()
        assert page.is_username_field_required(), (
            "TC-AUTH-006 FAIL: HTML5 validation phải chặn khi trống username"
        )

    def test_TC_AUTH_007_login_empty_password(self, driver, test_credentials):
        """
        TC-AUTH-007: Bỏ trống trường Mật khẩu
        Expected: HTML5 validation chặn submit
        """
        page = LoginPage(driver)
        page.open()
        page.enter_username(test_credentials["email"])
        page.click_submit()
        assert page.is_password_field_required(), (
            "TC-AUTH-007 FAIL: HTML5 validation phải chặn khi trống password"
        )

    def test_TC_AUTH_009_remember_me_or_stay_on_login(self, driver, test_credentials):
        """
        TC-AUTH-009: Sau đăng nhập thất bại, vẫn ở trang login
        """
        page = LoginPage(driver)
        page.open()
        page.login("nonexistent@test.com", "wrong_pass_123")
        import time; time.sleep(1.5)
        assert page.is_on_login_page(), (
            "TC-AUTH-009 FAIL: Sau đăng nhập thất bại phải ở lại trang login"
        )

    def test_TC_AUTH_010_register_link_present(self, driver):
        """
        TC-AUTH-010: Trang login có link đăng ký
        """
        page = LoginPage(driver)
        page.open()
        assert page.is_element_present(page.REGISTER_LINK), (
            "TC-AUTH-010 FAIL: Trang login phải có link đến trang đăng ký"
        )

    def test_TC_AUTH_011_login_page_no_server_error(self, driver):
        """
        TC-AUTH-011: Trang login không có lỗi server
        """
        page = LoginPage(driver)
        page.open()
        assert not page.has_server_error(), (
            "TC-AUTH-011 FAIL: Trang login không được có lỗi 500/server error"
        )
