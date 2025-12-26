# key_stores

這個專案會從 `key.csv` 讀取鎖印行資料，並在 `docs/` 目錄下產生 GitHub Pages 可直接使用的靜態網站：
- `docs/index.html`：所有鎖印行的入口頁。
- `docs/stores/<店名>.html`：每一家店的獨立介紹頁，內含照片、地址、電話與 Google 地圖連結。

## 產生頁面
1. 安裝 Python（內建函式庫即可）。
2. 執行產生指令：
   ```bash
   python generate_sites.py
   ```
   會依照 `key.csv` 內容重新輸出 `docs/` 內的 HTML 與樣式檔案。

## 部署到 GitHub Pages
1. 將變更推送到 GitHub。
2. 在 GitHub 專案設定中啟用 Pages，Source 選擇 `Deploy from a branch`，Branch 選 `main`，資料夾選 `docs/`。
3. 儲存後，GitHub Pages 就會針對 `docs/` 內容建立公開網站，每筆鎖印行都會有獨立網址可分享。
