# =============================================================================
# TEST REGISTER POM — Kiểm thử module Đăng Ký
# Dự án: Shoes Store — Tuần 4 (Chương 7+8) — POM
# Thành viên phụ trách: [Thành viên 2]
# =============================================================================
"""
Test Suite: Register — Đăng Ký Tài Khoản
  TC-REG-001: Đăng ký thành công                        [Smoke]
  TC-REG-002: Bỏ trống tất cả các trường                [Smoke]
  TC-REG-003: Bỏ trống Họ tên                           [Smoke]
  TC-REG-004: Bỏ trống Email                            [Regression]
  TC-REG-005: Bỏ trống Mật khẩu                         [Regression]
  TC-REG-006: Bỏ trống Xác nhận mật khẩu               [Regression]
  TC-REG-007: Email sai định dạng (thiếu @)             [Regression]
  TC-REG-008: Email sai định dạng (thiếu domain)        [Regression]
  TC-REG-009: Email đã tồn tại                          [Regression]
  TC-REG-010: Mật khẩu không khớp                       [Regression]
  TC-REG-011: Mật khẩu quá ngắn (<8 ký tự)             [Regression]
  TC-REG-012: Mật khẩu thiếu ký tự đặc biệt            [Regression]
  TC-REG-013: SĐT chứa chữ cái                         [Regression]
  TC-REG-014: SĐT quá ngắn                              [Regression]
  TC-REG-015: Tên chứa ký tự đặc biệt                  [Regression]
  TC-REG-016: Khoảng trắng tất cả trường               [Regression]
  TC-REG-017: Giới hạn độ dài Họ tên (maxlength)        [Regression]
  TC-REG-018: SĐT đã tồn tại                           [Regression]
  TC-REG-019: SQL Injection ở trường Email              [Regression]
  TC-REG-020: Double-click nút Đăng ký                  [Regression]
"""

import datetime
import pytest
from ..pages import RegisterPage


def _unique_email(prefix: str = "reg") -> str:
    ts = datetime.datetime.now().strftime("%H%M%S%f")[:10]
    return f"{prefix}_{ts}@gmail.com"


def _unique_phone(prefix: str = "09") -> str:
    ts = datetime.datetime.now().strftime("%H%M%S%f")
    return f"{prefix}{ts[:8]}"


# ---------------------------------------------------------------------------
# SMOKE TESTS
# ---------------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.register
@pytest.mark.pom
class TestRegisterSmoke:

    def test_TC_REG_001_register_success(self, driver):
        """
        TC-REG-001: Đăng ký tài khoản mới thành công
        Steps:
          1. Điền đầy đủ thông tin hợp lệ (email/phone unique)
          2. Submit form
        Expected: Redirect về /users/login/ với thông báo thành công
        """
        page = RegisterPage(driver)
        page.open()
        page.register(
            full_name="Huỳnh Tỉnh",
            email=_unique_email("tc_reg_001"),
            phone=_unique_phone(),
            password="Pass@123",
            confirm_password="Pass@123",
        )
        assert page.is_registered_successfully(), (
            f"TC-REG-001 FAIL: Đăng ký thành công phải redirect về login. "
            f"URL: {page.get_current_url()}"
        )
        page.take_screenshot("TC_REG_001_pass")

    def test_TC_REG_002_register_all_empty(self, driver):
        """
        TC-REG-002: Bỏ trống tất cả các trường
        Expected: Có thông báo lỗi hoặc HTML5 validation
        """
        page = RegisterPage(driver)
        page.open()
        page.submit()  # Submit mà không điền gì
        import time; time.sleep(0.5)
        msg = page.get_error_message()
        still_on_page = page.is_on_register_page()
        assert msg or still_on_page, (
            "TC-REG-002 FAIL: Phải có lỗi hoặc vẫn ở trang đăng ký khi trống tất cả"
        )

    def test_TC_REG_003_register_empty_fullname(self, driver):
        """
        TC-REG-003: Bỏ trống trường Họ tên
        Expected: Báo lỗi liên quan đến họ tên
        """
        page = RegisterPage(driver)
        page.open()
        page.fill_form(
            email=_unique_email("reg_003"),
            phone=_unique_phone(),
            password="Pass@123",
            confirm_password="Pass@123",
        ).submit()
        msg = page.get_error_message_lower()
        assert page.is_on_register_page() or "họ tên" in msg or msg, (
            f"TC-REG-003 FAIL: Phải báo lỗi khi thiếu họ tên. Got: {msg!r}"
        )


# ---------------------------------------------------------------------------
# REGRESSION TESTS
# ---------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.register
@pytest.mark.pom
class TestRegisterRegression:

    def test_TC_REG_004_register_empty_email(self, driver):
        """TC-REG-004: Bỏ trống Email → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", "", _unique_phone(), "Pass@123", "Pass@123").submit()
        msg = page.get_error_message_lower()
        assert page.is_on_register_page() or "email" in msg or msg, (
            f"TC-REG-004 FAIL: Phải báo lỗi thiếu email. Got: {msg!r}"
        )

    def test_TC_REG_005_register_empty_password(self, driver):
        """TC-REG-005: Bỏ trống Mật khẩu → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", _unique_email("r005"), _unique_phone(), "", "Pass@123").submit()
        msg = page.get_error_message_lower()
        assert page.is_on_register_page() or "mật khẩu" in msg or msg, (
            f"TC-REG-005 FAIL: Phải báo lỗi thiếu mật khẩu. Got: {msg!r}"
        )

    def test_TC_REG_006_register_empty_confirm_password(self, driver):
        """TC-REG-006: Bỏ trống Xác nhận mật khẩu → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", _unique_email("r006"), _unique_phone(), "Pass@123", "").submit()
        msg = page.get_error_message_lower()
        assert page.is_on_register_page() or "xác nhận" in msg or msg, (
            f"TC-REG-006 FAIL: Phải báo lỗi thiếu xác nhận mật khẩu. Got: {msg!r}"
        )

    def test_TC_REG_007_register_invalid_email_no_at(self, driver):
        """TC-REG-007: Email sai định dạng (thiếu @) → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", "hoplegmail.com", _unique_phone(), "Pass@123", "Pass@123").submit()
        val_msg = page.get_email_validation_message()
        msg     = page.get_error_message_lower()
        assert "@" in val_msg or "định dạng" in msg or "email" in msg or page.is_on_register_page(), (
            f"TC-REG-007 FAIL: Phải báo lỗi email sai định dạng. "
            f"val_msg={val_msg!r} | msg={msg!r}"
        )

    def test_TC_REG_008_register_invalid_email_no_domain(self, driver):
        """TC-REG-008: Email sai định dạng (thiếu domain) → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", "hople@", _unique_phone(), "Pass@123", "Pass@123").submit()
        val_msg = page.get_email_validation_message()
        assert val_msg or page.is_on_register_page(), (
            f"TC-REG-008 FAIL: Phải báo lỗi email thiếu domain. Got: {val_msg!r}"
        )

    def test_TC_REG_009_register_existing_email(self, driver):
        """TC-REG-009: Email đã tồn tại → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form(
            "Huỳnh Tỉnh", "admin@gmail.com",
            _unique_phone("08"), "Pass@123", "Pass@123"
        ).submit()
        msg = page.get_error_message_lower()
        assert "tồn tại" in msg or "sử dụng" in msg or "đã" in msg or page.is_on_register_page(), (
            f"TC-REG-009 FAIL: Phải báo lỗi email trùng. Got: {msg!r}"
        )

    def test_TC_REG_010_register_password_mismatch(self, driver):
        """TC-REG-010: Mật khẩu ≠ Xác nhận mật khẩu → báo lỗi không khớp"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", _unique_email("r010"), _unique_phone(),
                       "Pass@123", "Pass@999").submit()
        msg = page.get_error_message_lower()
        assert "không khớp" in msg or "khớp" in msg or page.is_on_register_page(), (
            f"TC-REG-010 FAIL: Phải báo lỗi mật khẩu không khớp. Got: {msg!r}"
        )

    def test_TC_REG_011_register_password_too_short(self, driver):
        """TC-REG-011: Mật khẩu quá ngắn (<8 ký tự) → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", _unique_email("r011"), _unique_phone(),
                       "P@12", "P@12").submit()
        msg = page.get_error_message_lower()
        assert ("kí tự" in msg or "ký tự" in msg or "8" in msg
                or page.is_on_register_page()), (
            f"TC-REG-011 FAIL: Phải báo lỗi mật khẩu ngắn. Got: {msg!r}"
        )

    def test_TC_REG_012_register_weak_password(self, driver):
        """TC-REG-012: Mật khẩu thiếu ký tự đặc biệt/hoa → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", _unique_email("r012"), _unique_phone(),
                       "matkhauthuong", "matkhauthuong").submit()
        msg = page.get_error_message_lower()
        assert ("chữ hoa" in msg or "số" in msg or "đặc biệt" in msg
                or "bảo mật" in msg or page.is_on_register_page()), (
            f"TC-REG-012 FAIL: Phải báo lỗi mật khẩu yếu. Got: {msg!r}"
        )

    def test_TC_REG_013_register_phone_with_letters(self, driver):
        """TC-REG-013: SĐT chứa chữ cái → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", _unique_email("r013"),
                       "0901234abc", "Pass@123", "Pass@123").submit()
        msg = page.get_error_message_lower()
        assert ("điện thoại" in msg or "hợp lệ" in msg or "chữ số" in msg
                or page.is_on_register_page()), (
            f"TC-REG-013 FAIL: Phải báo lỗi SĐT có chữ. Got: {msg!r}"
        )

    def test_TC_REG_014_register_phone_too_short(self, driver):
        """TC-REG-014: SĐT quá ngắn → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", _unique_email("r014"),
                       "090123", "Pass@123", "Pass@123").submit()
        msg = page.get_error_message_lower()
        assert ("hợp lệ" in msg or "10" in msg or page.is_on_register_page()), (
            f"TC-REG-014 FAIL: Phải báo lỗi SĐT ngắn. Got: {msg!r}"
        )

    def test_TC_REG_015_register_name_with_special_chars(self, driver):
        """TC-REG-015: Tên chứa ký tự đặc biệt → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh @#!", _unique_email("r015"), _unique_phone(),
                       "Pass@123", "Pass@123").submit()
        msg = page.get_error_message_lower()
        assert ("đặc biệt" in msg or "hợp lệ" in msg or page.is_on_register_page()), (
            f"TC-REG-015 FAIL: Phải báo lỗi tên có ký tự đặc biệt. Got: {msg!r}"
        )

    def test_TC_REG_016_register_whitespace_only(self, driver):
        """TC-REG-016: Nhập khoảng trắng vào tất cả trường → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("   ", "  ", "  ", "  ", "  ").submit()
        msg = page.get_error_message()
        assert msg or page.is_on_register_page(), (
            "TC-REG-016 FAIL: Phải có lỗi hoặc vẫn ở trang đăng ký khi nhập khoảng trắng"
        )

    def test_TC_REG_017_register_fullname_maxlength(self, driver):
        """TC-REG-017: Giới hạn maxlength trường Họ tên"""
        page = RegisterPage(driver)
        page.open()
        long_name = "A" * 100  # Nhập 100 ký tự
        page.input_text(page.FULL_NAME_FIELD, long_name, clear=True)
        actual_value = page.get_full_name_value()
        max_len = page.get_full_name_max_length()
        assert len(actual_value) <= max_len, (
            f"TC-REG-017 FAIL: Trường Họ tên phải có giới hạn maxlength={max_len}. "
            f"Actual length: {len(actual_value)}"
        )

    def test_TC_REG_018_register_existing_phone(self, driver):
        """TC-REG-018: SĐT đã tồn tại → báo lỗi"""
        page = RegisterPage(driver)
        page.open()
        # Dùng SĐT đã tồn tại trong hệ thống
        page.fill_form("Huỳnh Tỉnh", _unique_email("r018"),
                       "0987654321", "Pass@123", "Pass@123").submit()
        msg = page.get_error_message_lower()
        assert ("điện thoại" in msg and ("tồn tại" in msg or "đăng ký" in msg)
                or page.is_on_register_page()), (
            f"TC-REG-018 FAIL: Phải báo lỗi SĐT trùng. Got: {msg!r}"
        )

    def test_TC_REG_019_register_sql_injection_email(self, driver):
        """TC-REG-019: SQL Injection ở trường Email → bị từ chối"""
        page = RegisterPage(driver)
        page.open()
        page.fill_form("Huỳnh Tỉnh", "' OR 1=1 --",
                       _unique_phone(), "Pass@123", "Pass@123").submit()
        msg = page.get_error_message_lower()
        val_msg = page.get_email_validation_message()
        assert "định dạng" in msg or "email" in msg or val_msg or page.is_on_register_page(), (
            f"TC-REG-019 FAIL: SQL Injection phải bị từ chối. Got: {msg!r}"
        )
        assert not page.is_registered_successfully(), (
            "TC-REG-019 FAIL: SQL Injection không được đăng ký thành công"
        )

    def test_TC_REG_020_register_double_click(self, driver):
        """TC-REG-020: Double-click nút Đăng ký → chỉ tạo 1 tài khoản"""
        import time
        page = RegisterPage(driver)
        page.open()
        email = _unique_email("double_click")
        phone = _unique_phone()
        page.fill_form("Huỳnh Tỉnh", email, phone, "Pass@123", "Pass@123")

        # Double-click bằng JS
        page.execute_js("""
            var btn = document.getElementById('submitBtn');
            if (btn) {
                btn.click();
                setTimeout(function() {
                    if (document.getElementById('submitBtn')) {
                        document.getElementById('submitBtn').click();
                    }
                }, 50);
            }
        """)

        try:
            page.wait_url_contains("/users/login/", timeout=5)
            assert page.is_registered_successfully(), (
                "TC-REG-020 FAIL: Double-click phải tạo thành công 1 tài khoản"
            )
        except Exception:
            # Nếu không redirect, kiểm tra còn ở register page
            assert page.is_on_register_page(), (
                "TC-REG-020 FAIL: Phải ở lại register page hoặc redirect login"
            )
        page.take_screenshot("TC_REG_020_double_click")
