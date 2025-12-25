# key_stores

利用 `generate_sites.py` 可以從 `key.csv` 產生 GitHub Pages 的靜態網站。

## 使用方式
1. 確定系統有 Python 3。
2. 在專案根目錄執行：
   ```bash
   python generate_sites.py
   ```
3. 產出的靜態檔案會放在 `docs/`，包含首頁與每間鎖印行的獨立頁面。將此資料夾設定為 GitHub Pages 的來源即可發布。

## 資料來源
- `key.csv`：以 CP950 編碼儲存的鎖印行列表，包括 Google 地圖連結、店名、Google 分數、地址與聯絡電話。
