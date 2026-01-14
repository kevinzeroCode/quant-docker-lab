# 使用輕量級的 Python 映像檔
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 先複製 requirements.txt 並安裝 (利用 Docker 快取機制)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製剩下的程式碼
COPY app/ .

# 開放 Streamlit 預設的 Port 8501
EXPOSE 8501

# 設定健康檢查 (這是好習慣，確保網頁真的有在跑)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 啟動 Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]