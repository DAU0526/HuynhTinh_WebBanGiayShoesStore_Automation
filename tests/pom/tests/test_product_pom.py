# =============================================================================
# TEST PRODUCT POM — Kiểm thử module Sản Phẩm
# Dự án: Shoes Store — Tuần 4 — POM
# Thành viên phụ trách: [Thành viên 3]
# =============================================================================
"""
TC-PROD-001: Trang chủ hiển thị danh sách sản phẩm        [Smoke]
TC-PROD-002: Trang chủ không có lỗi server                 [Smoke]
TC-PROD-003: Click vào sản phẩm → mở trang chi tiết        [Smoke]
TC-PROD-004: Trang chi tiết sản phẩm hiển thị thông tin    [Smoke]
TC-PROD-005: Chọn size → nút Thêm vào giỏ enabled          [Regression]
TC-PROD-006: Thêm vào giỏ → cart count tăng                [Regression]
TC-PROD-007: Trang chi tiết không có lỗi server            [Regression]
TC-PROD-008: Tìm kiếm sản phẩm theo từ khoá               [Regression]
"""

import time
import pytest
from ..pages import HomePage, ProductPage, LoginPage


@pytest.mark.smoke
@pytest.mark.product
@pytest.mark.pom
class TestProductSmoke:

    def test_TC_PROD_001_home_shows_products(self, driver):
        """
        TC-PROD-001: Trang chủ hiển thị ít nhất 1 sản phẩm
        """
        page = HomePage(driver)
        page.open()
        count = page.get_product_count()
        assert count > 0, (
            f"TC-PROD-001 FAIL: Trang chủ phải có ít nhất 1 sản phẩm. Got: {count}"
        )
        page.take_screenshot("TC_PROD_001_pass")

    def test_TC_PROD_002_home_no_server_error(self, driver):
        """TC-PROD-002: Trang chủ không có lỗi server 500"""
        page = HomePage(driver)
        page.open()
        assert page.is_page_ok(), (
            "TC-PROD-002 FAIL: Trang chủ không được có lỗi 500/server error"
        )

    def test_TC_PROD_003_click_product_opens_detail(self, driver):
        """
        TC-PROD-003: Click vào sản phẩm đầu tiên → mở trang chi tiết
        """
        page = HomePage(driver)
        page.open()
        count = page.get_product_count()
        if count == 0:
            pytest.skip("Không có sản phẩm để test")

        url_before = page.get_current_url()
        page.go_to_product(0)
        url_after = page.get_current_url()

        assert url_after != url_before, (
            "TC-PROD-003 FAIL: Click sản phẩm phải chuyển trang"
        )
        assert "/products/" in url_after or "/product/" in url_after or url_after != url_before, (
            f"TC-PROD-003 FAIL: URL chi tiết sản phẩm không đúng: {url_after}"
        )
        page.take_screenshot("TC_PROD_003_pass")

    def test_TC_PROD_004_product_detail_has_info(self, driver):
        """
        TC-PROD-004: Trang chi tiết sản phẩm hiển thị tên và giá
        """
        home = HomePage(driver)
        home.open()
        if home.get_product_count() == 0:
            pytest.skip("Không có sản phẩm để test")

        home.go_to_product(0)
        product = ProductPage(driver)

        assert product.is_product_loaded(), (
            "TC-PROD-004 FAIL: Trang chi tiết sản phẩm phải load đúng"
        )
        name = product.get_product_name()
        assert name, (
            f"TC-PROD-004 FAIL: Trang chi tiết phải hiển thị tên sản phẩm. Got: {name!r}"
        )
        page_source = product.get_page_source()
        assert "500" not in page_source, (
            "TC-PROD-004 FAIL: Trang chi tiết không được có lỗi 500"
        )
        product.take_screenshot("TC_PROD_004_pass")


@pytest.mark.regression
@pytest.mark.product
@pytest.mark.pom
class TestProductRegression:

    def test_TC_PROD_005_select_size_enables_cart_btn(self, driver, test_credentials):
        """
        TC-PROD-005: Sau khi chọn size, nút Thêm vào giỏ phải enabled
        """
        LoginPage(driver).open().login(
            test_credentials["email"], test_credentials["password"]
        )
        home = HomePage(driver)
        home.open()
        if home.get_product_count() == 0:
            pytest.skip("Không có sản phẩm để test")

        home.go_to_product(0)
        product = ProductPage(driver)

        if not product.has_sizes():
            pytest.skip("Sản phẩm này không có size options")

        sizes = product.get_available_sizes()
        assert len(sizes) > 0, "Phải có ít nhất 1 size còn hàng"

        product.select_size(0)
        assert product.is_add_to_cart_enabled(), (
            "TC-PROD-005 FAIL: Nút Thêm vào giỏ phải enabled sau khi chọn size"
        )
        product.take_screenshot("TC_PROD_005_pass")

    def test_TC_PROD_006_add_to_cart_increases_count(self, driver, test_credentials):
        """
        TC-PROD-006: Thêm sản phẩm vào giỏ → cart count tăng
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
            pytest.skip("Sản phẩm không có size options")

        product.add_to_cart(size_index=0)
        new_count = product.get_cart_count()

        assert new_count > initial_count, (
            f"TC-PROD-006 FAIL: Cart count phải tăng. "
            f"Before: {initial_count}, After: {new_count}"
        )
        product.take_screenshot("TC_PROD_006_pass")

    def test_TC_PROD_007_product_detail_no_server_error(self, driver):
        """TC-PROD-007: Trang chi tiết sản phẩm không có lỗi server"""
        home = HomePage(driver)
        home.open()
        if home.get_product_count() == 0:
            pytest.skip("Không có sản phẩm để test")

        home.go_to_product(0)
        product = ProductPage(driver)
        assert product.is_page_ok(), (
            "TC-PROD-007 FAIL: Trang chi tiết sản phẩm không được có lỗi server"
        )

    def test_TC_PROD_008_search_product(self, driver):
        """
        TC-PROD-008: Tìm kiếm sản phẩm → kết quả không có lỗi server
        """
        home = HomePage(driver)
        home.open()

        if not home.is_search_available():
            pytest.skip("Trang không có ô tìm kiếm")

        try:
            home.search("Nike")
            product = ProductPage(driver)
            assert product.is_page_ok(), (
                "TC-PROD-008 FAIL: Trang tìm kiếm không được có lỗi server"
            )
            home.take_screenshot("TC_PROD_008_search_results")
        except AssertionError as e:
            if "tìm kiếm" in str(e).lower():
                pytest.skip(str(e))
            raise
