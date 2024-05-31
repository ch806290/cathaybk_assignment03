import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import re


@pytest.fixture(scope="module")
def browser():
    # 初始化 Chrome 選項
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-fullscreen")  # 全螢幕模式

    # 初始化 WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def take_screenshot(driver, name, directory="screenshots"):
    # 確保目錄存在
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # 截取螢幕截圖並客製化命名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join(directory, screenshot_name)
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at {screenshot_path}")
    return screenshot_path

def extract_version(text):
    # 使用正則表達式提取版本號
    match = re.search(r"\d+\.\d+\.\d+", text)
    return match.group(0) if match else None

def test_cathaybk(browser):
    # 1. 開啟國泰世華官方網站並截圖
    url = "https://www.cathaybk.com.tw/cathaybk"

    browser.get(url)
    wait = WebDriverWait(browser, 10)
    title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'cubre-a-kvTitle'))).text
    print(f'The home page title is : {title}')
    take_screenshot(browser, "home_page")

    # 2. 點擊『開戶』button，等待新頁面loading完成並截圖
    open_account_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "開戶"))
    )
    open_account_button.click()

    # 等待頁面loading完成
    WebDriverWait(browser, 10).until(EC.title_contains("開戶"))
    take_screenshot(browser, "open_account_page")

    # 3. 於線上他行帳戶驗證區塊點擊 [下載CUBE App]，並成功另開分頁，前往下載CUBE App頁面
    download_cube_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "下載CUBE App"))
    )
    download_cube_button.click()

    # 切換到新分頁
    browser.switch_to.window(browser.window_handles[-1])

    # 4. 抓頁面上，Android與iOS版本號須一致
    android_version_text = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "android"))
    ).text
    ios_version_text = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "ios"))
    ).text

    android_version = extract_version(android_version_text)
    ios_version = extract_version(ios_version_text)
    assert android_version == ios_version, f"Android and iOS versions do not match: {android_version} != {ios_version}"

    # 5. 下載Cube App的QR Code icon高寬檢查，是否都是均為160px，並截圖
    qr_code_icon = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@src='Content/images/qrcode.png']"))
    )
    print(f'the qrcode display is : {qr_code_icon.is_displayed()}')
    
    isQRcodeMeetHeight = ( qr_code_icon.size['width'] == 160 and qr_code_icon.size['height'] == 160 )
    print(f'check the Height is 160px: {isQRcodeMeetHeight}')
    assert qr_code_icon.size['width'] == 160 and qr_code_icon.size['height'] == 160, "QR Code icon dimensions are incorrect"

    take_screenshot(browser, "download_cube_app_page")

    # 6. 切換為行動版(Webview)時，檢查QR Code不顯示於畫面，並截圖
    browser.set_window_size(390, 844)  # iPhone 12 pro resolution
    take_screenshot(browser, "mobile_view")

    qr_code_icon_mobile = browser.find_element(By.XPATH, "//img[@src='Content/images/qrcode.png']")
    print(f'the qrcode display is : {qr_code_icon_mobile.is_displayed()}')

    assert not qr_code_icon_mobile.is_displayed(), "QR Code icon should not be visible in mobile view"