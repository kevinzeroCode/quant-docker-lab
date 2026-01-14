\# 📈 Docker Quant Dashboard (量化金融儀表板)



這是一個基於微服務架構 (Microservices) 的金融數據分析系統。

整合了 \*\*Python Streamlit\*\* 前端視覺化與 \*\*PostgreSQL\*\* 資料庫，並透過 \*\*Docker Compose\*\* 實現一鍵部署。



\## ✨ 專案亮點 (Key Features)



\* \*\*容器化架構 (Dockerized):\*\* 使用 Docker Compose 編排 App 與 DB 服務。

\* \*\*資料持久化 (Persistence):\*\* 透過 Docker Volume 確保資料庫資料不丟失。

\* \*\*智慧快取機制:\*\* 優先查詢 PostgreSQL 資料庫，若無資料才透過 API 下載，大幅提升效能。

\* \*\*互動式圖表:\*\* 整合 K 線圖 (Candlestick) 與移動平均線 (SMA) 指標。



\## 🛠️ 技術堆疊 (Tech Stack)



\* \*\*Infrastructure:\*\* Docker, Docker Compose

\* \*\*Backend/Frontend:\*\* Python 3.10, Streamlit

\* \*\*Database:\*\* PostgreSQL 15

\* \*\*Data Processing:\*\* Pandas, SQLAlchemy, YFinance

\* \*\*Visualization:\*\* Plotly



\## 🚀 如何執行 (How to Run)



你不需要安裝 Python 或 PostgreSQL，只要有 Docker 即可。



\### 1. Clone 專案

```bash

git clone https://github.com/kevinzeroCode/quant-docker-lab.git

cd quant-docker-lab

```

\### 2. 啟動專案

```bash

docker compose up

```

\### 3. 開始使用

打開瀏覽器前往： http://localhost:8501



quant-docker-lab/

├── app/

│   ├── main.py          # 核心邏輯

│   └── requirements.txt # Python 依賴

├── compose.yaml         # 系統架構藍圖

├── Dockerfile           # App 映像檔設定

└── README.md            # 說明文件











