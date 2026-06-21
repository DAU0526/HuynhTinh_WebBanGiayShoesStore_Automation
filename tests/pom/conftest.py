# =============================================================================
# CONFTEST.PY — Pytest Fixtures cho POM Test Suite
# Dự án: Shoes Store — QC Automation Internship (Tuần 4)
# =============================================================================
"""
Fixtures dùng chung cho toàn bộ pytest test suite:
  - driver()        : Chrome WebDriver (mỗi test một driver)
  - auth_driver()   : Driver đã đăng nhập sẵn
  - base_url        : URL gốc của ứng dụng
  - test_credentials: Thông tin đăng nhập test
"""

import os
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ---------------------------------------------------------------------------
# Cấu hình
# ---------------------------------------------------------------------------
BASE_URL       = "http://127.0.0.1:8000"
TEST_EMAIL     = "testuser@gmail.com"
TEST_PASSWORD  = "Test@1234"
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results", "screenshots")
HEADLESS       = os.environ.get("HEADLESS", "false").lower() == "true"

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def base_url():
    """URL gốc của ứng dụng"""
    return BASE_URL


@pytest.fixture(scope="session")
def test_credentials():
    """Thông tin đăng nhập test account"""
    return {
        "email"   : TEST_EMAIL,
        "phone"   : "0901234567",
        "password": TEST_PASSWORD,
    }


def _make_driver() -> webdriver.Chrome:
    """Tạo ChromeDriver với options chuẩn"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)
    return driver


@pytest.fixture
def driver():
    """
    Fixture: Chrome WebDriver — mở mới cho mỗi test.
    Tự động đóng sau khi test chạy xong.
    """
    drv = _make_driver()
    yield drv
    drv.quit()


@pytest.fixture
def auth_driver():
    """
    Fixture: Chrome WebDriver đã đăng nhập sẵn.
    Dùng cho các tests cần authentication (Cart, Order).
    """
    drv = _make_driver()

    # Đăng nhập
    drv.get(f"{BASE_URL}/users/login/")
    wait = WebDriverWait(drv, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "username")))
    drv.find_element(By.ID, "username").send_keys(TEST_EMAIL)
    drv.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    drv.execute_script("document.querySelector('button[type=\"submit\"]').click();")
    wait.until(EC.url_contains(BASE_URL + "/"))

    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver=None):
    """
    Tự động chụp ảnh màn hình khi test FAIL.
    (autouse=True — áp dụng cho tất cả tests)
    """
    yield
    # Sau khi test chạy, kiểm tra kết quả
    if request.node.rep_call is not None and request.node.rep_call.failed:
        # Lấy driver từ fixture
        for fixture_name in ["driver", "auth_driver"]:
            try:
                drv = request.getfixturevalue(fixture_name)
                if drv:
                    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
                    tc_id = request.node.name.replace(" ", "_")
                    path  = os.path.join(SCREENSHOT_DIR, f"FAIL_{tc_id}.png")
                    drv.save_screenshot(path)
                    logger.error(f"❌ Screenshot: {path}")
                    break
            except Exception:
                pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook để lưu trạng thái test call cho screenshot_on_failure fixture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ---------------------------------------------------------------------------
# Pytest Configuration
# ---------------------------------------------------------------------------
def pytest_configure(config):
    """Đăng ký markers"""
    config.addinivalue_line("markers", "smoke: Smoke tests — chạy nhanh, kiểm tra luồng chính")
    config.addinivalue_line("markers", "regression: Regression tests — kiểm tra đầy đủ")
    config.addinivalue_line("markers", "auth: Kiểm tra module xác thực")
    config.addinivalue_line("markers", "register: Kiểm tra module đăng ký")
    config.addinivalue_line("markers", "product: Kiểm tra module sản phẩm")
    config.addinivalue_line("markers", "cart: Kiểm tra module giỏ hàng")
    config.addinivalue_line("markers", "order: Kiểm tra module đặt hàng")
    config.addinivalue_line("markers", "pom: Tests dùng Page Object Model")
