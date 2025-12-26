# key_stores

利用 `key.csv` 的鎖印行資料，自動產生 GitHub Pages 靜態網站：

- `docs/index.html`：店家總覽，連結到每一間店的獨立網站。
- `docs/stores/store-*/index.html`：每一筆鎖印行的專屬頁面，包含地圖連結、地址、電話與照片。

## 如何重新產生網站

1. 確認已安裝 Python 3，且 `key.csv` 維持原始（Big5/CP950 編碼）格式。
2. 執行：

   ```bash
   python generate_site.py
   ```

   指令會讀取 `key.csv` 並寫入最新版的 `docs/` 靜態檔案。

## 發佈到 GitHub Pages

- 專案已將輸出放在 `docs/`，可直接在 GitHub Pages 設定 **Source = Deploy from a branch -> branch: main, folder: /docs**。
- 生成完成後推送至 GitHub，即可透過 Pages 查看總覽與每間店的獨立網站。
