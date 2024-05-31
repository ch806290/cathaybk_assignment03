# cathaybk_assignment03

## 問題描述
題目：國泰線上開戶 - 引導至下載Cube App頁面

## 檢查與步驟
底下針對問題，思考脈絡如下:

1. 開啟國泰世華官方網站 (URL-https://www.cathaybk.com.tw/cathaybk)，並截圖。
2. 點擊『開戶』button，並等到page loading 完成，並檢查loading後的新title是否出現，並截圖。
3. 於線上他行帳戶驗證區塊點擊 [下載CUBE App] ，並成功另開分頁，前往下載CUBE App頁面，並截圖。
4. 抓頁面上，Android與iOS版本號 須一致
3. 下載Cube App的QR Code icon高寬檢查，是否都是均為160px
4. 切換為行動版(Webview)時，檢查，QR Code不顯示於畫面，並截圖。

### 相關考慮條件1: 每一步驟的畫面須進行截圖，並以當下時間作為檔名

- 使用take_screenshot()

### 相關考慮條件2: 使用Python + Selenium + Pytest


### 執行環境

- Python 版本: 3.9.6
- 確保已經安裝了 pytest 和 selenium：
```
pip install pytest selenium
```

### 使用方式

1. clone git repo: git clone https://github.com/ch806290/cathaybk_assignment03.git
2. 到專案目錄: cd cathaybk_assignment03
3. 執行單元測試:python3 -m pytest test_cathaybk_003.py
