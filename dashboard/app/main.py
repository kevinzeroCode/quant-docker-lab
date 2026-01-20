import streamlit as st
import requests
import os
import pandas as pd
import plotly.graph_objects as go

API_URL = os.getenv("API_URL", "http://agent-service:8000")

st.set_page_config(page_title="FinAgent Dashboard", layout="wide")
st.title("🤖 FinAgent: AI 金融分析助理")
st.markdown("---")

with st.sidebar:
    st.header("設定")
    ticker = st.text_input("輸入美股代號", value="NVDA")
    period = st.selectbox("分析區間", ["1y", "2y", "5y", "10y"], index=1)
    if st.button("開始分析 🚀"):
        st.session_state['run_analysis'] = True

if st.session_state.get('run_analysis'):
    with st.spinner(f"正在連線 Agent 分析 {ticker} ..."):
        try:
            payload = {"ticker": ticker, "period": period}
            response = requests.post(f"{API_URL}/tools/analyze_stock", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # KPI 指標區
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("年化報酬率", f"{data.get('cagr_pct', 'N/A')}%")
                col2.metric("波動率", f"{data.get('volatility_pct', 'N/A')}%")
                col3.metric("夏普值", data.get('sharpe_ratio', 'N/A'))
                col4.metric("最大回撤", f"{data.get('max_drawdown_pct', 'N/A')}%")

                st.markdown("### 🧠 Agent 技術分析觀點")
                st.info(data.get('analysis', '暫無分析'))

                # --- 繪圖區 (重點修改) ---
                if 'history' in data:
                    st.markdown("### 📈 技術分析圖表")
                    df = pd.DataFrame(data['history'])
                    
                    fig = go.Figure()

                    # 1. 畫 K 線 (Candlestick)
                    fig.add_trace(go.Candlestick(
                        x=df['Date'],
                        open=df['Open'], high=df['High'],
                        low=df['Low'], close=df['Close'],
                        name=f'{ticker} K線'
                    ))

                    # 2. 畫均線 (MA Lines)
                    # Line width 設定細一點比較精緻
                    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA5'], mode='lines', name='周線 (5MA)', line=dict(color='orange', width=1)))
                    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], mode='lines', name='月線 (20MA)', line=dict(color='purple', width=1.5)))
                    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA60'], mode='lines', name='季線 (60MA)', line=dict(color='blue', width=1.5)))

                    # 3. 優化操作體驗 (UX)
                    fig.update_layout(
                        height=600,
                        xaxis_rangeslider_visible=True,  # 開啟下方時間軸拉桿 (關鍵！)
                        dragmode='pan',                  # 預設滑鼠行為改成「拖曳移動」而不是「框選縮放」
                        hovermode='x unified',           # 滑鼠移過去顯示所有指標數值
                        margin=dict(l=20, r=20, t=20, b=20),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) # 圖例放上面
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"分析失敗: {response.text}")
                
        except Exception as e:
            st.error(f"連線錯誤: {e}")