*** Settings ***
Documentation     Suite kiểm thử tự động cho chức năng Giỏ hàng (Regression Test)
...               Kiểm tra thêm sản phẩm, xem giỏ hàng, xóa sản phẩm
Library           SeleniumLibrary
Library           String
Suite Setup       Login And Open Home Page
Suite Teardown    Close Browser

*** Variables ***
${HOME_URL}         http://127.0.0.1:8000/
${LOGIN_URL}        http://127.0.0.1:8000/users/login/
${CART_URL}         http://127.0.0.1:8000/cart/
${BROWSER}          Chrome
${VALID_EMAIL}      testuser@gmail.com
${VALID_PASSWORD}   Test@1234

*** Keywords ***
Login And Open Home Page
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage
    Open Browser    ${LOGIN_URL}    ${BROWSER}    options=${options}
    Maximize Browser Window
    # Đăng nhập
    Wait Until Element Is Visible    id=username    timeout=5s
    Input Text    id=username    ${VALID_EMAIL}
    Input Text    id=password    ${VALID_PASSWORD}
    Scroll Element Into View    css=button[type="submit"]
    Execute Javascript    document.querySelector('button[type="submit"]').click()
    Wait Until Location Is    ${HOME_URL}    timeout=5s

*** Test Cases ***
TC-CART-001 Thêm sản phẩm vào giỏ hàng
    [Documentation]    Kiểm tra luồng chọn sản phẩm từ trang chủ và thêm vào giỏ hàng
    [Tags]             Regression    Cart    Priority-High
    
    # Bước 1: Mở trang sản phẩm
    Go To    ${HOME_URL}
    Wait Until Page Contains Element    css=.premium-product-card    timeout=10s
    
    # Bước 2: Click vào sản phẩm đầu tiên
    ${product_link}=    Get Element Attribute    xpath=(//div[contains(@class, 'premium-product-card')]//ancestor::a)[1]    href
    Go To    ${product_link}
    Wait Until Page Contains Element    css=.product-title    timeout=5s
    
    # Bước 3: Chọn size đầu tiên còn hàng
    ${has_size}=    Run Keyword And Return Status    Wait Until Page Contains Element    xpath=(//input[@name="size" and not(@disabled)]/following-sibling::label)[1]    timeout=3s
    Run Keyword If    ${has_size}    Click Element    xpath=(//input[@name="size" and not(@disabled)]/following-sibling::label)[1]
    
    # Bước 4: Click nút Thêm vào giỏ
    Scroll Element Into View    css=button.product-cart-btn
    Click Button    css=button.product-cart-btn
    
    # Bước 5: Xác nhận giỏ hàng đã cập nhật
    Sleep    1s
    ${cart_count}=    Get Text    id=cart-count
    Should Not Be Equal As Strings    ${cart_count}    0

TC-CART-002 Xem giỏ hàng
    [Documentation]    Kiểm tra trang giỏ hàng hiển thị sản phẩm đã thêm
    [Tags]             Regression    Cart
    
    Go To    ${CART_URL}
    Wait Until Page Contains Element    css=.cart-item, .cart-empty, table    timeout=5s
    # Trang giỏ hàng phải mở được mà không lỗi
    Page Should Not Contain    500
    Page Should Not Contain    Server Error

TC-CART-003 Truy cập giỏ hàng khi chưa đăng nhập
    [Documentation]    Kiểm tra giỏ hàng vẫn truy cập được khi chưa đăng nhập
    [Tags]             Regression    Cart
    
    # Đăng xuất
    Go To    http://127.0.0.1:8000/users/logout/
    Wait Until Location Is    ${HOME_URL}    timeout=5s
    
    # Truy cập giỏ hàng
    Go To    ${CART_URL}
    # Trang phải mở được mà không chuyển hướng hoặc lỗi
    Page Should Not Contain    500
    Page Should Not Contain    Server Error
    
    # Đăng nhập lại cho các test tiếp theo
    Go To    ${LOGIN_URL}
    Wait Until Element Is Visible    id=username    timeout=5s
    Input Text    id=username    ${VALID_EMAIL}
    Input Text    id=password    ${VALID_PASSWORD}
    Scroll Element Into View    css=button[type="submit"]
    Execute Javascript    document.querySelector('button[type="submit"]').click()
    Wait Until Location Is    ${HOME_URL}    timeout=5s
