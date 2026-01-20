FROM python:3.10-slim

WORKDIR /app

# 1. 先複製 requirements.txt (它現在跟 Dockerfile 在同一層 dashboard/ 下)
COPY requirements.txt .

# 2. 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 3. 複製所有檔案 (這會把 app/ 資料夾也複製進去)
COPY . .

# 4. 關鍵修正：確認路徑指向 app/main.py
EXPOSE 8501

# 注意：這裡假設你的程式碼在 /app/app/main.py
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]