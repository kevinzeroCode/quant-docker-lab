# 使用輕量級的 Python 基礎映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 先複製需求檔，利用 Docker Cache 加速 Build
COPY requirements.txt .

# 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有程式碼
COPY . .

# 告訴 Docker 我們會用 8000 Port
EXPOSE 8000

# 啟動 FastAPI 服務
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]