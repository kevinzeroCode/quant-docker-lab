import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os

# 1. 建立資料庫連線
# 我們從環境變數讀取連線字串 (這就是在 compose.yaml 設定的那一行)
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

st.set_page_config(page_title="Quant Dashboard + DB", layout="wide")
st.title("💰 Docker 量化儀表板 (含資料庫版)")

# 側邊欄
st.sidebar.header("設定參數")
ticker = st.sidebar.text_input("輸入股票代碼", value="NVDA")
start_date = st.sidebar.date_input("開始日期", value=pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("結束日期", value=pd.to_datetime("today"))

if st.sidebar.button("分析股價"):
    try:
        table_name = f"{ticker}_data"
        
        # --- 策略：先檢查資料庫有沒有 ---
        st.info(f"🔍 正在查詢資料庫中的 {table_name}...")
        
        # 嘗試從資料庫讀取
        try:
            # 使用 Pandas 直接讀 SQL
            df = pd.read_sql(table_name, engine)
            # 設定日期為索引 (因為存進去時索引會變成普通欄位)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
            st.success(f"🚀 命中快取！從資料庫讀取了 {len(df)} 筆資料 (速度超快)")
        
        except Exception:
            # 如果資料庫沒這張表，會報錯，我們就進入下載流程
            st.warning("⚠️ 資料庫沒資料，正在從 Yahoo Finance 下載...")
            
            df = yf.download(ticker, start=start_date, end=end_date)
            
            if df.empty:
                st.error("❌ 找不到資料")
                st.stop()
            
            # 處理多層索引 (上次的修復)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # 【關鍵】寫入資料庫！
            # if_exists='replace' 代表如果有舊資料就覆蓋
            df.to_sql(table_name, engine, if_exists='replace')
            st.success("✅ 下載完成，並已自動存入 PostgreSQL 資料庫！")

        # --- 繪圖區 (跟之前一樣) ---
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['Open'], high=df['High'],
                        low=df['Low'], close=df['Close'], name='K線')])
        
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], 
                                 line=dict(color='orange'), name='SMA 20'))
        
        fig.update_layout(title=f'{ticker} 股價走勢', height=500, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📊 數據預覽")
        st.dataframe(df.tail())

    except Exception as e:
        st.error(f"系統錯誤: {e}")