*** Settings ***
Documentation     Suite kiểm thử tự động cho chức năng Đăng nhập (Smoke Test)
...               Kiểm tra đăng nhập bằng Email và Số điện thoại
Library           SeleniumLibrary
Library           String
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser
Test Setup        Go To Login Page

*** Variables ***
${LOGIN_URL}        http://127.0.0.1:8000/users/login/
${HOME_URL}         http://127.0.0.1:8000/
${BROWSER}          Chrome
${VALID_EMAIL}      testuser@gmail.com
${VALID_PHONE}      0901234567
${VALID_PASSWORD}   Test@1234
${INVALID_EMAIL}    invalid@test.com
${INVALID_PASSWORD}  wrongpass123

*** Keywords ***
Open Browser To Login Page
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage
    Open Browser    ${LOGIN_URL}    ${BROWSER}    options=${options}
    Maximize Browser Window

Go To Login Page
    Go To    ${LOGIN_URL}
    Wait Until Element Is Visible    id=username    timeout=5s

Input Login And Submit
    [Arguments]    ${username}    ${password}
    Clear Element Text    id=username
    Clear Element Text    id=password
    Run Keyword If    $username != ""    Input Text    id=username    ${username}
    Run Keyword If    $password != ""    Input Text    id=password    ${password}
    # Dùng JS submit để bỏ qua HTML5 required validation
    Execute Javascript    document.querySelector('form').submit()
    Sleep    1s

Input Login And Click
    [Arguments]    ${username}    ${password}
    Clear Element Text    id=username
    Clear Element Text    id=password
    Run Keyword If    $username != ""    Input Text    id=username    ${username}
    Run Keyword If    $password != ""    Input Text    id=password    ${password}
    Scroll Element Into View    css=button[type="submit"]
    Execute Javascript    document.querySelector('button[type="submit"]').click()

Get Alert Message
    ${is_visible}=    Run Keyword And Return Status    Wait Until Element Is Visible    css=.messages-container .premium-alert    timeout=3s
    ${msg}=    Run Keyword If    ${is_visible}    Get Text    css=.messages-container .premium-alert
    ...    ELSE    Set Variable    ${EMPTY}
    RETURN    ${msg}

Check HTML5 Validation Blocked
    [Documentation]    Kiểm tra HTML5 validation có chặn submit không
    ${username_valid}=    Execute Javascript    return document.getElementById('username').validity.valid
    ${password_valid}=    Execute Javascript    return document.getElementById('password').validity.valid
    ${blocked}=    Evaluate    not (${username_valid} and ${password_valid})
    RETURN    ${blocked}

*** Test Cases ***
TC-AUTH-001 Đăng nhập thành công bằng Email
    [Documentation]    Xác nhận đăng nhập thành công khi nhập đúng email và mật khẩu
    [Tags]             Smoke    Auth    Priority-High
    Input Login And Click    ${VALID_EMAIL}    ${VALID_PASSWORD}
    Wait Until Location Is    ${HOME_URL}    timeout=5s
    Location Should Be    ${HOME_URL}

TC-AUTH-002 Đăng nhập thành công bằng Số điện thoại
    [Documentation]    Xác nhận đăng nhập thành công khi nhập đúng số điện thoại và mật khẩu
    [Tags]             Smoke    Auth    Priority-High
    Input Login And Click    ${VALID_PHONE}    ${VALID_PASSWORD}
    Wait Until Location Is    ${HOME_URL}    timeout=5s
    Location Should Be    ${HOME_URL}

TC-AUTH-003 Đăng nhập thất bại với Email sai
    [Documentation]    Xác nhận báo lỗi khi nhập email không tồn tại
    [Tags]             Smoke    Auth
    Input Login And Submit    ${INVALID_EMAIL}    ${VALID_PASSWORD}
    ${msg}=    Get Alert Message
    ${msg_lower}=    Convert To Lower Case    ${msg}
    Should Be True    'không đúng' in '${msg_lower}' or 'sai' in '${msg_lower}'

TC-AUTH-004 Đăng nhập thất bại với Mật khẩu sai
    [Documentation]    Xác nhận báo lỗi khi nhập đúng email nhưng sai mật khẩu
    [Tags]             Smoke    Auth
    Input Login And Submit    ${VALID_EMAIL}    ${INVALID_PASSWORD}
    ${msg}=    Get Alert Message
    ${msg_lower}=    Convert To Lower Case    ${msg}
    Should Be True    'không đúng' in '${msg_lower}' or 'sai' in '${msg_lower}'

TC-AUTH-005 Đăng nhập với trường trống
    [Documentation]    Xác nhận HTML5 validation chặn submit khi bỏ trống cả 2 trường
    [Tags]             Smoke    Auth
    Input Login And Click    ${EMPTY}    ${EMPTY}
    ${blocked}=    Check HTML5 Validation Blocked
    Should Be True    ${blocked}    HTML5 validation phải chặn submit khi trống

TC-AUTH-006 Đăng nhập bỏ trống Email
    [Documentation]    Xác nhận HTML5 validation chặn submit khi chỉ nhập mật khẩu
    [Tags]             Auth
    Input Login And Click    ${EMPTY}    ${VALID_PASSWORD}
    ${blocked}=    Check HTML5 Validation Blocked
    Should Be True    ${blocked}    HTML5 validation phải chặn submit khi trống email

TC-AUTH-007 Đăng nhập bỏ trống Mật khẩu
    [Documentation]    Xác nhận HTML5 validation chặn submit khi chỉ nhập email
    [Tags]             Auth
    Input Login And Click    ${VALID_EMAIL}    ${EMPTY}
    ${blocked}=    Check HTML5 Validation Blocked
    Should Be True    ${blocked}    HTML5 validation phải chặn submit khi trống mật khẩu

TC-AUTH-008 Đăng xuất thành công
    [Documentation]    Xác nhận đăng xuất và quay về trang chủ
    [Tags]             Smoke    Auth    Priority-High
    # Đăng nhập trước
    Input Login And Click    ${VALID_EMAIL}    ${VALID_PASSWORD}
    Wait Until Location Is    ${HOME_URL}    timeout=5s
    # Đăng xuất
    Go To    http://127.0.0.1:8000/users/logout/
    Wait Until Location Is    ${HOME_URL}    timeout=5s
    Page Should Contain    Đăng Nhập
