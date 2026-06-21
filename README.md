# 🛒 Shoes Store — QA Automation Framework

> **Dự án thực tập QC Automation** | Kiểm thử tự động toàn bộ chức năng của website thương mại điện tử bán giày

---

## 👤 Thông Tin Sinh Viên Thực Tập

| Thông tin | Chi tiết |
|-----------|----------|
| **Họ và tên** | Huỳnh Tỉnh |
| **MSSV** | 2251220008 |
| **Vai trò** | QC Automation Intern (Nhân viên kiểm thử tự động) |
| **Dự án** | Shoes Store — Hệ thống TMĐT bán giày |
| **Công nghệ kiểm thử** | Python · Selenium · Robot Framework · pytest · Page Object Model |

---

## 🎯 Mục Tiêu Dự Án

Dự án này xây dựng một **QA Automation Framework hoàn chỉnh** để kiểm thử tự động toàn bộ các chức năng chính của website **Shoes Store** (Django). Framework được thiết kế theo kiến trúc **Page Object Model (POM)** chuẩn công nghiệp, cho phép:

- ✅ Kiểm tra tự động **5 module chức năng chính** của hệ thống
- ✅ Phân loại rõ ràng **Smoke Test** (kiểm tra nhanh) và **Regression Test** (kiểm tra đầy đủ)
- ✅ Sinh báo cáo HTML **tự động** sau mỗi lần chạy
- ✅ Dễ dàng **mở rộng thêm chức năng con** mà không ảnh hưởng code cũ

---

## 🌐 Link Trang Web Đã Deploy

🔗 **Website Demo / Deploy:** [https://shoes-store-dtpp.onrender.com](https://shoes-store-dtpp.onrender.com)

---

## 🏗️ Kiến Trúc Framework

Framework được tổ chức theo chuẩn **Page Object Model (POM)**, tách biệt hoàn toàn giữa phần định vị giao diện (Page Objects) và phần logic kiểm thử (Test Cases):

```
Shoes_Store/
│
├── tests/
│   ├── robot/                        ← Robot Framework Test Suites (Tuần 3)
│   │   ├── auth_tests.robot          # Kiểm thử Đăng nhập / Đăng xuất
│   │   ├── register_tests.robot      # Kiểm thử Đăng ký tài khoản
│   │   ├── cart_tests.robot          # Kiểm thử Giỏ hàng
│   │   ├── product_tests.robot       # Kiểm thử Sản phẩm
│   │   └── order_tests.robot         # Kiểm thử Đặt hàng
│   │
│   └── pom/                          ← POM Framework chính (Tuần 4)
│       ├── conftest.py               # Fixtures dùng chung (driver, auth, credentials)
│       ├── run_tests.bat             # Script chạy tests (Windows)
│       │
│       ├── pages/                    ← PAGE OBJECTS (Tầng giao diện)
│       │   ├── base_page.py          # BasePage — methods dùng chung
│       │   ├── login_page.py         # Trang Đăng Nhập
│       │   ├── register_page.py      # Trang Đăng Ký
│       │   ├── home_page.py          # Trang Chủ / Danh sách sản phẩm
│       │   ├── product_page.py       # Trang Chi Tiết Sản Phẩm
│       │   ├── cart_page.py          # Trang Giỏ Hàng
│       │   └── order_page.py         # Trang Đặt Hàng / Lịch Sử
│       │
│       └── tests/                    ← TEST CASES (Tầng kiểm thử)
│           ├── test_auth_pom.py      # 11 TCs — Đăng nhập/Đăng xuất
│           ├── test_register_pom.py  # 20 TCs — Đăng ký tài khoản
│           ├── test_product_pom.py   #  8 TCs — Sản phẩm
│           ├── test_cart_pom.py      #  7 TCs — Giỏ hàng
│           └── test_order_pom.py     #  6 TCs — Đặt hàng
│
├── pytest.ini                        ← Cấu hình pytest + markers
└── results/                          ← Báo cáo HTML tự động sinh ra
    ├── robot/report.html
    ├── pom/full_report.html
    └── screenshots/
```

---

## 📋 Danh Sách Chức Năng Chính Được Kiểm Thử

### Module 1 — 🔐 Auth (Đăng Nhập / Đăng Xuất)
> **11 Test Cases** | `tests/pom/tests/test_auth_pom.py`

| TC ID | Tên Test Case | Loại |
|-------|---------------|------|
| TC-AUTH-001 | Đăng nhập thành công bằng Email | 🔥 Smoke |
| TC-AUTH-002 | Đăng nhập thành công bằng Số Điện Thoại | 🔥 Smoke |
| TC-AUTH-003 | Đăng nhập thất bại — Email không tồn tại | 🔥 Smoke |
| TC-AUTH-004 | Đăng nhập thất bại — Mật khẩu sai | 🔥 Smoke |
| TC-AUTH-005 | Bỏ trống cả hai trường → HTML5 chặn | 🔥 Smoke |
| TC-AUTH-008 | Đăng xuất thành công | 🔥 Smoke |
| TC-AUTH-006 | Bỏ trống trường Email | 🔄 Regression |
| TC-AUTH-007 | Bỏ trống trường Mật khẩu | 🔄 Regression |
| TC-AUTH-009 | Sau đăng nhập thất bại vẫn ở trang Login | 🔄 Regression |
| TC-AUTH-010 | Trang Login có link đến Đăng Ký | 🔄 Regression |
| TC-AUTH-011 | Trang Login không có lỗi Server 500 | 🔄 Regression |

---

### Module 2 — 📝 Register (Đăng Ký Tài Khoản)
> **20 Test Cases** | `tests/pom/tests/test_register_pom.py`

| TC ID | Tên Test Case | Loại |
|-------|---------------|------|
| TC-REG-001 | Đăng ký thành công với dữ liệu hợp lệ | 🔥 Smoke |
| TC-REG-002 | Bỏ trống tất cả các trường | 🔥 Smoke |
| TC-REG-003 | Bỏ trống trường Họ tên | 🔥 Smoke |
| TC-REG-004 | Bỏ trống trường Email | 🔄 Regression |
| TC-REG-005 | Bỏ trống trường Mật khẩu | 🔄 Regression |
| TC-REG-006 | Bỏ trống Xác nhận mật khẩu | 🔄 Regression |
| TC-REG-007 | Email sai định dạng (thiếu @) | 🔄 Regression |
| TC-REG-008 | Email sai định dạng (thiếu domain) | 🔄 Regression |
| TC-REG-009 | Email đã tồn tại trong hệ thống | 🔄 Regression |
| TC-REG-010 | Mật khẩu và Xác nhận không khớp | 🔄 Regression |
| TC-REG-011 | Mật khẩu quá ngắn (dưới 8 ký tự) | 🔄 Regression |
| TC-REG-012 | Mật khẩu thiếu ký tự đặc biệt/hoa | 🔄 Regression |
| TC-REG-013 | Số điện thoại chứa chữ cái | 🔄 Regression |
| TC-REG-014 | Số điện thoại quá ngắn | 🔄 Regression |
| TC-REG-015 | Tên chứa ký tự đặc biệt | 🔄 Regression |
| TC-REG-016 | Nhập khoảng trắng vào tất cả các trường | 🔄 Regression |
| TC-REG-017 | Kiểm tra giới hạn maxlength trường Họ tên | 🔄 Regression |
| TC-REG-018 | Số điện thoại đã tồn tại | 🔄 Regression |
| TC-REG-019 | SQL Injection vào trường Email | 🔄 Regression |
| TC-REG-020 | Double-click nút Đăng ký (chỉ tạo 1 tài khoản) | 🔄 Regression |

---

### Module 3 — 👟 Product (Sản Phẩm)
> **8 Test Cases** | `tests/pom/tests/test_product_pom.py`

| TC ID | Tên Test Case | Loại |
|-------|---------------|------|
| TC-PROD-001 | Trang chủ hiển thị danh sách sản phẩm | 🔥 Smoke |
| TC-PROD-002 | Trang chủ không có lỗi Server | 🔥 Smoke |
| TC-PROD-003 | Click sản phẩm → mở trang chi tiết | 🔥 Smoke |
| TC-PROD-004 | Trang chi tiết hiển thị tên sản phẩm | 🔥 Smoke |
| TC-PROD-005 | Chọn size → nút Thêm vào giỏ enabled | 🔄 Regression |
| TC-PROD-006 | Thêm vào giỏ → Cart count tăng | 🔄 Regression |
| TC-PROD-007 | Trang chi tiết sản phẩm không có lỗi Server | 🔄 Regression |
| TC-PROD-008 | Tìm kiếm sản phẩm theo từ khoá | 🔄 Regression |

---

### Module 4 — 🛒 Cart (Giỏ Hàng)
> **7 Test Cases** | `tests/pom/tests/test_cart_pom.py`

| TC ID | Tên Test Case | Loại |
|-------|---------------|------|
| TC-CART-001 | Thêm sản phẩm vào giỏ hàng thành công | 🔥 Smoke |
| TC-CART-002 | Trang giỏ hàng hiển thị đúng | 🔥 Smoke |
| TC-CART-003 | Giỏ hàng truy cập được khi chưa đăng nhập | 🔥 Smoke |
| TC-CART-004 | Xoá sản phẩm khỏi giỏ hàng | 🔄 Regression |
| TC-CART-005 | Trang giỏ hàng không có lỗi Server | 🔄 Regression |
| TC-CART-006 | Nút Checkout hiển thị khi giỏ có hàng | 🔄 Regression |
| TC-CART-007 | Giỏ hàng trống hiển thị không lỗi | 🔄 Regression |

---

### Module 5 — 📦 Order (Đặt Hàng)
> **6 Test Cases** | `tests/pom/tests/test_order_pom.py`

| TC ID | Tên Test Case | Loại |
|-------|---------------|------|
| TC-ORD-001 | Truy cập trang lịch sử đơn hàng | 🔥 Smoke |
| TC-ORD-002 | Lịch sử đơn hàng không có lỗi Server | 🔥 Smoke |
| TC-ORD-003 | Trang Checkout có thể truy cập | 🔥 Smoke |
| TC-ORD-004 | Lịch sử đơn hàng yêu cầu đăng nhập | 🔄 Regression |
| TC-ORD-005 | Trang /orders/ không có lỗi Server | 🔄 Regression |
| TC-ORD-006 | Số đơn hàng hiển thị là số không âm | 🔄 Regression |

---

## 📊 Tổng Kết Test Cases

| Module | 🔥 Smoke | 🔄 Regression | Tổng |
|--------|----------|---------------|------|
| Auth (Đăng nhập) | 6 | 5 | **11** |
| Register (Đăng ký) | 3 | 17 | **20** |
| Product (Sản phẩm) | 4 | 4 | **8** |
| Cart (Giỏ hàng) | 3 | 4 | **7** |
| Order (Đặt hàng) | 3 | 3 | **6** |
| **TỔNG** | **19** | **33** | **52** |

> ✅ **52 Test Cases** đã được verified — `pytest --collect-only` xác nhận thu thập thành công

---

## 🚀 Hướng Dẫn Chạy Tests

### Yêu cầu
- Django server đang chạy tại `http://127.0.0.1:8000/`
- Python 3.8+, Google Chrome đã cài sẵn
- Đã tạo tài khoản test: `testuser@gmail.com` / `Test@1234`

### Chạy nhanh (Windows)

```batch
# Chạy tất cả tests (Robot + POM)
cd tests\pom
run_tests.bat

# Chỉ Smoke Tests (nhanh ~3-5 phút)
run_tests.bat smoke

# Chỉ Regression Tests (đầy đủ ~10-15 phút)
run_tests.bat regression

# Theo từng module (phân công nhóm)
run_tests.bat auth       # Module đăng nhập
run_tests.bat register   # Module đăng ký
run_tests.bat product    # Module sản phẩm
run_tests.bat cart       # Module giỏ hàng
run_tests.bat order      # Module đặt hàng
```

### Chạy bằng lệnh trực tiếp

```bash
# Robot Framework — toàn bộ
robot --outputdir results/robot --log log.html --report report.html tests/robot/

# Robot Framework — chỉ Smoke
robot --include Smoke --outputdir results/robot/smoke tests/robot/

# pytest POM — toàn bộ với HTML report
python -m pytest tests/pom/tests/ -v --html=results/pom/full_report.html --self-contained-html

# pytest POM — chỉ Smoke Tests
python -m pytest tests/pom/tests/ -m smoke -v

# pytest POM — theo module
python -m pytest tests/pom/tests/test_auth_pom.py -v
```

### Xem Báo Cáo

Sau khi chạy, mở các file HTML trong thư mục `results/`:

```
results/
├── robot/report.html         ← Báo cáo Robot Framework (giao diện đẹp)
├── robot/log.html            ← Log chi tiết từng bước
├── pom/full_report.html      ← Báo cáo pytest HTML
└── screenshots/              ← Ảnh chụp màn hình khi test FAIL
```

---

## ➕ Cách Thêm Chức Năng Con Mới

Framework được thiết kế để **dễ dàng mở rộng**. Khi cần test thêm một chức năng con (ví dụ: *Lọc sản phẩm theo giá*, *Nhập mã giảm giá*, *Cập nhật hồ sơ người dùng*...), thực hiện theo 3 bước:

### Bước 1 — Cập nhật Page Object (`tests/pom/pages/`)

Mở file Page Object tương ứng với trang cần test và bổ sung:

```python
# Ví dụ: Thêm chức năng lọc giá vào home_page.py

# 1. Thêm LOCATOR (bộ định vị HTML)
PRICE_FILTER_MIN = (By.ID, "price-min")
PRICE_FILTER_MAX = (By.ID, "price-max")
FILTER_BUTTON    = (By.CSS_SELECTOR, ".btn-filter-apply")

# 2. Thêm ACTION (hành động)
def filter_by_price(self, min_price: int, max_price: int) -> "HomePage":
    self.input_text(self.PRICE_FILTER_MIN, str(min_price))
    self.input_text(self.PRICE_FILTER_MAX, str(max_price))
    self.click(self.FILTER_BUTTON)
    return self
```

### Bước 2 — Viết Test Case mới (`tests/pom/tests/`)

Mở file test tương ứng (ví dụ `test_product_pom.py`) và thêm hàm test mới:

```python
@pytest.mark.regression   # hoặc @pytest.mark.smoke nếu là chức năng quan trọng
@pytest.mark.product
def test_TC_PROD_009_filter_by_price(self, driver):
    """TC-PROD-009: Lọc sản phẩm theo khoảng giá"""
    page = HomePage(driver).open()
    page.filter_by_price(min_price=200000, max_price=500000)
    count = page.get_product_count()
    assert count >= 0, "Kết quả lọc phải hợp lệ (không lỗi server)"
```

### Bước 3 — Chạy test và cập nhật Git

```bash
# Chạy riêng test case mới để xác nhận
python -m pytest tests/pom/tests/test_product_pom.py::TestProductRegression::test_TC_PROD_009_filter_by_price -v

# Nếu pass → commit và push lên Git
git add tests/pom/
git commit -m "feat(test): Thêm TC-PROD-009 - Lọc sản phẩm theo giá"
git push
```

---

## 🧩 Hiểu Smoke Test vs Regression Test

| | 🔥 Smoke Test | 🔄 Regression Test |
|---|---|---|
| **Mục đích** | Kiểm tra nhanh hệ thống có "sống" không | Kiểm tra đầy đủ mọi trường hợp |
| **Khi nào chạy** | Sau mỗi lần deploy / merge code | Trước khi release chính thức |
| **Số lượng TCs** | Ít (~19 TCs) | Nhiều (~33 TCs) |
| **Thời gian** | ~3-5 phút | ~10-15 phút |
| **Marker pytest** | `@pytest.mark.smoke` | `@pytest.mark.regression` |
| **Tag Robot** | `[Tags] Smoke` | `[Tags] Regression` |

---

## 🛠️ Công Nghệ Sử Dụng

| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| Python | 3.12 | Ngôn ngữ lập trình chính |
| Selenium WebDriver | 4.x | Tự động hoá trình duyệt |
| Robot Framework | 6.x | Test framework dạng keyword |
| pytest | 9.x | Test runner cho POM tests |
| pytest-html | 4.x | Sinh báo cáo HTML |
| Google Chrome | Latest | Trình duyệt chạy tests |

---

## 📞 Liên Hệ

**Huỳnh Tỉnh** — MSSV: 2251220008  
QC Automation Intern — Shoes Store Project
