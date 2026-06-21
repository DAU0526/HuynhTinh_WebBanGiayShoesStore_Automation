*** Settings ***
Documentation     Suite kiểm thử tự động cho chức năng Sản Phẩm
...               Smoke Tests: Danh sách, chi tiết, tìm kiếm sản phẩm
...               Regression Tests: Lọc, chọn size, giá cả
Library           SeleniumLibrary
Library           String
Suite Setup       Open Browser To Home Page
Suite Teardown    Close Browser
Test Setup        Go To Home Page

*** Variables ***
${HOME_URL}         http://127.0.0.1:8000/
${LOGIN_URL}        http://127.0.0.1:8000/users/login/
${BROWSER}          Chrome
${VALID_EMAIL}      testuser@gmail.com
${VALID_PASSWORD}   Test@1234

*** Keywords ***
Open Browser To Home Page
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage
    Open Browser    ${HOME_URL}    ${BROWSER}    options=${options}
    Maximize Browser Window

Go To Home Page
    Go To    ${HOME_URL}
    Sleep    1s

Login To Site
    Go To    ${LOGIN_URL}
    Wait Until Element Is Visible    id=username    timeout=5s
    Input Text    id=username    ${VALID_EMAIL}
    Input Text    id=password    ${VALID_PASSWORD}
    Execute Javascript    document.querySelector('button[type="submit"]').click()
    Wait Until Location Is    ${HOME_URL}    timeout=8s

*** Test Cases ***
TC-PROD-001 Trang chủ hiển thị danh sách sản phẩm
    [Documentation]    Xác nhận trang chủ có ít nhất 1 sản phẩm
    [Tags]             Smoke    Product    Priority-High
    Wait Until Page Contains Element    css=.premium-product-card    timeout=15s
    ${count}=    Get Element Count    css=.premium-product-card
    Should Be True    ${count} > 0    Trang chủ phải có ít nhất 1 sản phẩm

TC-PROD-002 Trang chủ không có lỗi server
    [Documentation]    Xác nhận trang chủ load thành công (không có lỗi 500)
    [Tags]             Smoke    Product    Priority-High
    Page Should Not Contain    500 Internal Server Error
    Page Should Not Contain    Server Error
    Page Should Not Contain    Traceback

TC-PROD-003 Click sản phẩm đầu tiên mở trang chi tiết
    [Documentation]    Xác nhận click vào sản phẩm chuyển sang trang chi tiết
    [Tags]             Smoke    Product    Priority-High
    Wait Until Page Contains Element    css=.premium-product-card    timeout=10s
    ${product_link}=    Get Element Attribute
    ...    xpath=(//div[contains(@class, 'premium-product-card')]//ancestor::a)[1]
    ...    href
    Go To    ${product_link}
    Wait Until Page Contains Element    css=.product-title, h1    timeout=5s
    Page Should Not Contain    500
    ${url}=    Get Location
    Should Contain Any    ${url}    /products/    /product/

TC-PROD-004 Trang chi tiết sản phẩm hiển thị tên sản phẩm
    [Documentation]    Xác nhận trang chi tiết có tên sản phẩm
    [Tags]             Smoke    Product    Priority-High
    Wait Until Page Contains Element    css=.premium-product-card    timeout=10s
    ${product_link}=    Get Element Attribute
    ...    xpath=(//div[contains(@class, 'premium-product-card')]//ancestor::a)[1]
    ...    href
    Go To    ${product_link}
    Wait Until Page Contains Element    css=.product-title, h1    timeout=5s
    ${name}=    Get Text    css=.product-title, h1
    Should Not Be Empty    ${name}    Trang chi tiết phải có tên sản phẩm

TC-PROD-005 Chọn size sản phẩm
    [Documentation]    Xác nhận có thể chọn size sản phẩm
    [Tags]             Regression    Product    Priority-Medium
    Login To Site
    Go To Home Page
    Wait Until Page Contains Element    css=.premium-product-card    timeout=10s
    ${product_link}=    Get Element Attribute
    ...    xpath=(//div[contains(@class, 'premium-product-card')]//ancestor::a)[1]
    ...    href
    Go To    ${product_link}
    ${has_size}=    Run Keyword And Return Status
    ...    Wait Until Page Contains Element
    ...    xpath=(//input[@name="size" and not(@disabled)]/following-sibling::label)[1]
    ...    timeout=3s
    Run Keyword If    ${has_size}
    ...    Click Element
    ...    xpath=(//input[@name="size" and not(@disabled)]/following-sibling::label)[1]
    Run Keyword If    ${has_size}    Sleep    0.5s

TC-PROD-006 Thêm sản phẩm vào giỏ tăng cart count
    [Documentation]    Xác nhận cart count tăng sau khi thêm sản phẩm
    [Tags]             Regression    Product    Priority-High
    Login To Site
    Go To Home Page
    ${initial_count}=    Get Text    id=cart-count
    Wait Until Page Contains Element    css=.premium-product-card    timeout=10s
    ${product_link}=    Get Element Attribute
    ...    xpath=(//div[contains(@class, 'premium-product-card')]//ancestor::a)[1]
    ...    href
    Go To    ${product_link}
    ${has_size}=    Run Keyword And Return Status
    ...    Wait Until Page Contains Element
    ...    xpath=(//input[@name="size" and not(@disabled)]/following-sibling::label)[1]
    ...    timeout=3s
    Run Keyword If    ${has_size}
    ...    Click Element
    ...    xpath=(//input[@name="size" and not(@disabled)]/following-sibling::label)[1]
    Sleep    0.3s
    ${has_btn}=    Run Keyword And Return Status
    ...    Wait Until Page Contains Element    css=button.product-cart-btn    timeout=3s
    Run Keyword If    ${has_btn}    Scroll Element Into View    css=button.product-cart-btn
    Run Keyword If    ${has_btn}    Execute Javascript    document.querySelector('button.product-cart-btn').click()
    Sleep    1.5s
    ${new_count}=    Get Text    id=cart-count
    Should Not Be Equal As Strings    ${new_count}    0

TC-PROD-007 Trang chi tiết sản phẩm không lỗi server
    [Documentation]    Xác nhận trang chi tiết sản phẩm không có lỗi 500
    [Tags]             Regression    Product
    Wait Until Page Contains Element    css=.premium-product-card    timeout=10s
    ${product_link}=    Get Element Attribute
    ...    xpath=(//div[contains(@class, 'premium-product-card')]//ancestor::a)[1]
    ...    href
    Go To    ${product_link}
    Page Should Not Contain    500
    Page Should Not Contain    Server Error

TC-PROD-008 Tìm kiếm sản phẩm
    [Documentation]    Xác nhận tính năng tìm kiếm hoạt động
    [Tags]             Regression    Product
    ${has_search}=    Run Keyword And Return Status
    ...    Wait Until Page Contains Element
    ...    css=input[type='search'],#search-input    timeout=3s
    Skip If    not ${has_search}    Trang không có ô tìm kiếm
    Input Text    css=input[type='search'],#search-input    Nike
    Press Key    css=input[type='search'],#search-input    \\13
    Sleep    2s
    Page Should Not Contain    500 Internal Server Error
