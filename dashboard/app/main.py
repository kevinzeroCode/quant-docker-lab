import streamlit as st
import requests
import os
import pandas as pd

# --- 設定 API URL ---
# 前端不連資料庫，只連後端 API
# 如果環境變數沒設定，就預設連到 agent-service:8000
API_URL = os.getenv("API_URL", "http://agent-service:8000")

st.set_page_config(page_title="FinAgent Dashboard", layout="wide")

st.title("🤖 FinAgent: AI 金融分析助理")
st.markdown("---")

# --- 側邊欄：輸入區 ---
with st.sidebar:
    st.header("設定")
    ticker = st.text_input("輸入美股代號", value="AAPL")
    period = st.selectbox("分析區間", ["1y", "2y", "5y", "10y"], index=1)
    
    # 按鈕
    if st.button("開始分析 🚀"):
        st.session_state['run_analysis'] = True

# --- 主畫面：顯示區 ---
if st.session_state.get('run_analysis'):
    st.subheader(f"📊 分析結果: {ticker}")
    
    with st.spinner("Agent 正在呼叫 yfinance 計算數據中..."):
        try:
            # 呼叫後端 API (注意：這裡是 requests.post，不是 SQL 查詢)
            payload = {"ticker": ticker, "period": period}
            response = requests.post(f"{API_URL}/tools/analyze_stock", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # 顯示關鍵指標
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("年化報酬率 (CAGR)", f"{data.get('cagr_pct', 'N/A')}%")
                col2.metric("波動率 (Volatility)", f"{data.get('volatility_pct', 'N/A')}%")
                col3.metric("夏普值 (Sharpe)", data.get('sharpe_ratio', 'N/A'))
                col4.metric("最大回撤", f"{data.get('max_drawdown_pct', 'N/A')}%")
                
                st.success("數據計算完成！(來自 Agent Backend)")
                
                # 顯示原始數據方便除錯
                with st.expander("查看原始 JSON 數據"):
                    st.json(data)
                
            else:
                st.error(f"分析失敗: {response.text}")
                
        except Exception as e:
            st.error(f"連線錯誤: {e}")
            st.info("請確認 docker-compose 裡的 agent-service 是否正常執行中。")