from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.finance_tools import calculate_performance_metrics

# 初始化 API App
app = FastAPI(title="FinAgent Service")

# 定義傳入資料的格式 (Schema)
class StockRequest(BaseModel):
    ticker: str
    period: str = "2y"

@app.get("/")
def home():
    return {"status": "Agent Service is running"}

@app.post("/tools/analyze_stock")
def run_analysis_tool(request: StockRequest):
    """
    這是一個 API 端點，專門讓外部 (如 Streamlit) 呼叫 'finance_tools'。
    """
    result = calculate_performance_metrics(request.ticker, request.period)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result