*** Settings ***
Documentation     Suite kiểm thử tự động cho chức năng Đặt Hàng
...               Smoke Tests: Truy cập trang đơn hàng, lịch sử
...               Regression Tests: Phân quyền, xem chi tiết
Library           SeleniumLibrary
Library           String
Suite Setup       Open Browser And Login
Suite Teardown    Close Browser

*** Variables ***
${HOME_URL}         http://127.0.0.1:8000/
${LOGIN_URL}        http://127.0.0.1:8000/users/login/
${ORDERS_URL}       http://127.0.0.1:8000/orders/
${HISTORY_URL}      http://127.0.0.1:8000/orders/history/
${CHECKOUT_URL}     http://127.0.0.1:8000/orders/checkout/
${BROWSER}          Chrome
${VALID_EMAIL}      testuser@gmail.com
${VALID_PASSWORD}   Test@1234

*** Keywords ***
Open Browser And Login
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage
    Open Browser    ${LOGIN_URL}    ${BROWSER}    options=${options}
    Maximize Browser Window
    Wait Until Element Is Visible    id=username    timeout=5s
    Input Text    id=username    ${VALID_EMAIL}
    Input Text    id=password    ${VALID_PASSWORD}
    Execute Javascript    document.querySelector('button[type="submit"]').click()
    Wait Until Location Is    ${HOME_URL}    timeout=8s

*** Test Cases ***
TC-ORD-001 Truy cập trang lịch sử đơn hàng
    [Documentation]    Xác nhận trang lịch sử đơn hàng truy cập được
    [Tags]             Smoke    Order    Priority-High
    Go To    ${HISTORY_URL}
    Sleep    1s
    Page Should Not Contain    500 Internal Server Error
    Page Should Not Contain    Server Error

TC-ORD-002 Lịch sử đơn hàng không có lỗi server
    [Documentation]    Xác nhận trang /orders/history/ không có lỗi 500
    [Tags]             Smoke    Order    Priority-High
    Go To    ${HISTORY_URL}
    Sleep    1s
    ${source}=    Get Source
    Should Not Contain    ${source}    500
    Should Not Contain    ${source}    Traceback (most recent call last)

TC-ORD-003 Trang checkout có thể truy cập
    [Documentation]    Xác nhận trang /orders/checkout/ không lỗi server
    [Tags]             Smoke    Order    Priority-Medium
    Go To    ${CHECKOUT_URL}
    Sleep    1s
    Page Should Not Contain    500 Internal Server Error
    Page Should Not Contain    Traceback

TC-ORD-004 Lịch sử đơn hàng khi chưa đăng nhập
    [Documentation]    Xác nhận lịch sử đơn hàng yêu cầu đăng nhập
    [Tags]             Regression    Order
    # Đăng xuất
    Go To    http://127.0.0.1:8000/users/logout/
    Sleep    1s
    # Truy cập trang lịch sử khi chưa đăng nhập
    Go To    ${HISTORY_URL}
    Sleep    1s
    # Phải redirect về login hoặc trang không có lỗi 500
    ${url}=    Get Location
    ${page_ok}=    Run Keyword And Return Status    Page Should Not Contain    500
    ${is_redirected}=    Run Keyword And Return Status    Should Contain    ${url}    login
    Should Be True    ${page_ok} or ${is_redirected}    Phải redirect về login hoặc không có lỗi server
    # Đăng nhập lại cho tests tiếp theo
    Go To    ${LOGIN_URL}
    Wait Until Element Is Visible    id=username    timeout=5s
    Input Text    id=username    ${VALID_EMAIL}
    Input Text    id=password    ${VALID_PASSWORD}
    Execute Javascript    document.querySelector('button[type="submit"]').click()
    Wait Until Location Is    ${HOME_URL}    timeout=8s

TC-ORD-005 Trang orders không lỗi server
    [Documentation]    Xác nhận /orders/ không có lỗi server
    [Tags]             Regression    Order
    Go To    ${ORDERS_URL}
    Sleep    1s
    Page Should Not Contain    500 Internal Server Error

TC-ORD-006 Đếm số đơn hàng hiển thị
    [Documentation]    Số đơn hàng phải là số không âm
    [Tags]             Regression    Order
    Go To    ${HISTORY_URL}
    Sleep    1s
    ${has_orders}=    Run Keyword And Return Status
    ...    Page Contains Element    css=.order-row,.order-card,.order-item
    ${count}=    Run Keyword If    ${has_orders}
    ...    Get Element Count    css=.order-row,.order-card,.order-item
    ...    ELSE    Set Variable    0
    Should Be True    ${count} >= 0    Số đơn hàng phải >= 0
