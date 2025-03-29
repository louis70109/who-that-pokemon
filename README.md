# Who That Pokemon

This is a simple FastAPI application that includes:
- A health check endpoint (`/health`) to verify the service status.
- An index route (`/`) that renders an HTML page using Jinja2 templates.
- Functionality to search for Pokémon by name or by height and weight.

---

## 中文說明

這是一個簡單的 FastAPI 應用程式，包含以下功能：
- 健康檢查端點 (`/health`) 用於檢查服務狀態。
- 主頁路由 (`/`) 使用 Jinja2 模板渲染 HTML 頁面。
- 提供根據寶可夢名稱或身高體重進行搜尋的功能。

---

## Requirements / 系統需求

Make sure you have Python 3.7+ installed. / 確保已安裝 Python 3.7+。

Install the required dependencies using the following command:  
使用以下指令安裝所需的依賴套件：

```bash
pip install -r requirements.txt
```

---

## Setting Up a Virtual Environment / 建立虛擬環境

It is recommended to use a virtual environment to manage dependencies. Follow these steps:  
建議使用虛擬環境來管理依賴套件，請按照以下步驟操作：

1. Create a virtual environment:  
   建立虛擬環境：
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:  
   啟用虛擬環境：
   - On **Windows** / 在 **Windows** 上：
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux** / 在 **macOS/Linux** 上：
     ```bash
     source venv/bin/activate
     ```

3. Install the required dependencies:  
   安裝所需的依賴套件：
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run / 如何執行

1. Start the FastAPI application using Uvicorn:  
   使用 Uvicorn 啟動 FastAPI 應用程式：

   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to:  
   打開瀏覽器並進入以下網址：
   - Health check: [http://127.0.0.1:8080/health](http://127.0.0.1:8080/health)
   - Index page: [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

---

## Project Structure / 專案結構

```
/who-that-pokemon
├── main.py                # FastAPI application / FastAPI 應用程式
├── requirements.txt       # Dependencies / 依賴套件
├── templates/
│   └── index.html         # HTML template for the index route / 主頁的 HTML 模板
├── static/                # Directory for static files (optional) / 靜態檔案目錄（可選）
├── utils/
│   └── pokemon.py         # Utility functions for Pokémon data / 寶可夢數據的工具函數
├── Dockerfile             # Dockerfile for containerization / 用於容器化的 Dockerfile
├── .gitignore             # Git ignore file / Git 忽略文件
└── README.md              # Project documentation / 專案文件
```

---

## Endpoints / API 端點

### `/health`
- **Method**: GET
- **Description**: Returns a JSON response with the service status.  
  **描述**: 返回服務狀態的 JSON 響應。
- **Response**:  
  **回應**:
  ```json
  {
    "status": "ok"
  }
  ```

### `/`
- **Method**: GET
- **Description**: Renders the `index.html` template.  
  **描述**: 渲染 `index.html` 模板。

---

## Notes / 注意事項

- You can add static files (e.g., CSS, JS) to the `static/` directory if needed.  
  如果需要，可以將靜態檔案（例如 CSS、JS）添加到 `static/` 目錄。
- Modify the `templates/index.html` file to customize the front-end content.  
  修改 `templates/index.html` 文件以自定義前端內容。