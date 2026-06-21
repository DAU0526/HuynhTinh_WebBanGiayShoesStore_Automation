@echo off
REM =============================================================================
REM  RUN TESTS — Shoes Store QC Automation Project
REM  Dự án nhóm — Tuần 3 & Tuần 4
REM =============================================================================
REM  Cách dùng:
REM    run_tests.bat                    -> Chạy tất cả tests
REM    run_tests.bat smoke              -> Chỉ chạy Smoke tests
REM    run_tests.bat regression         -> Chỉ chạy Regression tests
REM    run_tests.bat robot              -> Chỉ chạy Robot Framework tests
REM    run_tests.bat pom                -> Chỉ chạy POM tests (pytest)
REM    run_tests.bat auth               -> Chỉ chạy module Auth
REM    run_tests.bat register           -> Chỉ chạy module Register
REM    run_tests.bat product            -> Chỉ chạy module Product
REM    run_tests.bat cart               -> Chỉ chạy module Cart
REM    run_tests.bat order              -> Chỉ chạy module Order
REM =============================================================================

setlocal
cd /d "%~dp0\..\..\.."

REM Tạo thư mục results
if not exist "results\robot" mkdir results\robot
if not exist "results\pom" mkdir results\pom
if not exist "results\screenshots" mkdir results\screenshots

REM Hiện tiêu đề
echo.
echo =====================================================================
echo   SHOES STORE QC AUTOMATION — TEST RUNNER
echo   Duong dan: %CD%
echo   Thoi gian: %DATE% %TIME%
echo =====================================================================
echo.

REM Parse tham số
set "MODE=%1"
if "%MODE%"=="" set "MODE=all"

if /i "%MODE%"=="robot" goto :run_robot
if /i "%MODE%"=="pom" goto :run_pom
if /i "%MODE%"=="smoke" goto :run_smoke
if /i "%MODE%"=="regression" goto :run_regression
if /i "%MODE%"=="auth" goto :run_auth
if /i "%MODE%"=="register" goto :run_register
if /i "%MODE%"=="product" goto :run_product
if /i "%MODE%"=="cart" goto :run_cart
if /i "%MODE%"=="order" goto :run_order
if /i "%MODE%"=="all" goto :run_all

:run_all
echo [ALL] Chay toan bo tests...
echo.

:run_robot
echo --- ROBOT FRAMEWORK TESTS ---
echo.

echo [Smoke] Chay Robot Smoke Tests...
robot --include Smoke ^
      --outputdir results/robot/smoke ^
      --output smoke_output.xml ^
      --log smoke_log.html ^
      --report smoke_report.html ^
      tests/robot/
echo.

echo [Regression] Chay Robot Regression Tests...
robot --include Regression ^
      --outputdir results/robot/regression ^
      --output regression_output.xml ^
      --log regression_log.html ^
      --report regression_report.html ^
      tests/robot/
echo.

echo [ALL Robot] Tong hop report Robot...
robot --outputdir results/robot ^
      --output output.xml ^
      --log log.html ^
      --report report.html ^
      tests/robot/
echo.
if /i "%MODE%"=="robot" goto :end

:run_pom
echo --- POM TESTS (PYTEST) ---
echo.

echo [POM Smoke] Chay POM Smoke Tests...
python -m pytest tests/pom/tests/ -m smoke ^
    -v --tb=short ^
    --html=results/pom/smoke_report.html --self-contained-html
echo.

echo [POM Regression] Chay POM Regression Tests...
python -m pytest tests/pom/tests/ -m regression ^
    -v --tb=short ^
    --html=results/pom/regression_report.html --self-contained-html
echo.

echo [POM ALL] Tong hop report POM...
python -m pytest tests/pom/tests/ ^
    -v --tb=short ^
    --html=results/pom/full_report.html --self-contained-html
echo.
if /i "%MODE%"=="pom" goto :end
if /i "%MODE%"=="all" goto :end

:run_smoke
echo [SMOKE] Chi chay Smoke Tests...
echo.
echo  1. Robot Smoke:
robot --include Smoke --outputdir results/robot/smoke tests/robot/
echo.
echo  2. POM Smoke:
python -m pytest tests/pom/tests/ -m smoke -v --html=results/pom/smoke_report.html --self-contained-html
goto :end

:run_regression
echo [REGRESSION] Chi chay Regression Tests...
echo.
echo  1. Robot Regression:
robot --include Regression --outputdir results/robot/regression tests/robot/
echo.
echo  2. POM Regression:
python -m pytest tests/pom/tests/ -m regression -v --html=results/pom/regression_report.html --self-contained-html
goto :end

:run_auth
echo [AUTH] Chi chay Auth Module Tests...
robot --include Auth --outputdir results/robot/auth tests/robot/auth_tests.robot
python -m pytest tests/pom/tests/test_auth_pom.py -v --html=results/pom/auth_report.html --self-contained-html
goto :end

:run_register
echo [REGISTER] Chi chay Register Module Tests...
robot --include Smoke --outputdir results/robot/register tests/robot/register_tests.robot
python -m pytest tests/pom/tests/test_register_pom.py -v --html=results/pom/register_report.html --self-contained-html
goto :end

:run_product
echo [PRODUCT] Chi chay Product Module Tests...
robot --outputdir results/robot/product tests/robot/product_tests.robot
python -m pytest tests/pom/tests/test_product_pom.py -v --html=results/pom/product_report.html --self-contained-html
goto :end

:run_cart
echo [CART] Chi chay Cart Module Tests...
robot --outputdir results/robot/cart tests/robot/cart_tests.robot
python -m pytest tests/pom/tests/test_cart_pom.py -v --html=results/pom/cart_report.html --self-contained-html
goto :end

:run_order
echo [ORDER] Chi chay Order Module Tests...
robot --outputdir results/robot/order tests/robot/order_tests.robot
python -m pytest tests/pom/tests/test_order_pom.py -v --html=results/pom/order_report.html --self-contained-html
goto :end

:end
echo.
echo =====================================================================
echo   HOAN THANH! Xem reports tai:
echo   - Robot: results\robot\report.html
echo   - POM  : results\pom\full_report.html
echo   - Screenshots: results\screenshots\
echo =====================================================================
echo.
endlocal
