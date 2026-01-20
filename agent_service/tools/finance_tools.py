import yfinance as yf
import numpy as np
import pandas as pd

def safe_round(value, decimals=2):
    """
    安全四捨五入函數：處理 NaN 和 Infinity，避免 JSON 報錯
    """
    if value is None:
        return None
    # 檢查是否為數字
    if not isinstance(value, (int, float, np.number)):
        return None
    # 檢查是否為 NaN 或 無限大
    if np.isnan(value) or np.isinf(value):
        return None
    return round(float(value), decimals)

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_technical_analysis(df):
    """
    產生「客觀」的趨勢解讀
    """
    # 確保有足夠資料計算技術指標，否則回傳資料不足
    if len(df) < 60:
        return "⚠️ 資料不足，無法進行完整技術分析（需至少 60 天交易資料）。"

    current_price = df['Close'].iloc[-1]
    sma_20 = df['SMA_20'].iloc[-1]
    sma_60 = df['SMA_60'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    
    # 處理指標可能為 NaN 的情況
    if pd.isna(sma_20) or pd.isna(sma_60) or pd.isna(rsi):
        return "⚠️ 技術指標計算不完整，請稍後再試。"

    analysis = []
    
    # 1. 趨勢判斷
    if current_price > sma_20 > sma_60:
        analysis.append("🚀 **多頭排列 (Bullish)**：股價站上月線與季線，處於上升循環。")
    elif current_price < sma_20 < sma_60:
        analysis.append("🐻 **空頭排列 (Bearish)**：股價跌破均線，目前處於修正或下跌循環。")
    elif abs(current_price - sma_20) / sma_20 < 0.05:
        analysis.append("⚖️ **盤整階段 (Consolidation)**：股價在月線附近震盪，方向尚未明確。")
    else:
        analysis.append("🔄 **震盪整理**：股價與均線乖離，可能出現反彈或回檔。")

    # 2. 動能判斷
    if rsi > 70:
        analysis.append(f"⚠️ **過熱訊號 (RSI={safe_round(rsi)})**：短線留意回檔風險。")
    elif rsi < 30:
        analysis.append(f"🟢 **超賣訊號 (RSI={safe_round(rsi)})**：已進入超賣區，可能有反彈機會。")
    else:
        analysis.append(f"ℹ️ **動能中性 (RSI={safe_round(rsi)})**：市場情緒平穩。")

    return " ".join(analysis)

def calculate_performance_metrics(ticker: str, period: str = "2y", risk_free_rate: float = 0.02) -> dict:
    try:
        # 1. 抓取資料
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, auto_adjust=True)
        
        if df.empty:
            return {"error": f"找不到 {ticker} 的資料"}

        # --- 2. 計算均線 (Moving Averages) ---
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA60'] = df['Close'].rolling(window=60).mean()
        
        # 為了給 Agent 寫評語用
        df['SMA_20'] = df['MA20']
        df['SMA_60'] = df['MA60']
        df['RSI'] = calculate_rsi(df['Close'])

        # --- 3. 計算 KPI ---
        close_prices = df['Close']
        
        # 簡單報酬率計算
        total_return = (close_prices.iloc[-1] / close_prices.iloc[0]) - 1
        
        # 年化報酬率 (CAGR)
        days = (df.index[-1] - df.index[0]).days
        if days > 0:
            years = days / 365.25
            cagr = (close_prices.iloc[-1] / close_prices.iloc[0]) ** (1 / years) - 1
        else:
            cagr = 0

        # 波動率與夏普值
        daily_returns = close_prices.pct_change().dropna()
        if len(daily_returns) > 0:
            volatility = daily_returns.std() * np.sqrt(252)
            if volatility != 0:
                sharpe_ratio = (cagr - risk_free_rate) / volatility
            else:
                sharpe_ratio = None
        else:
            volatility = None
            sharpe_ratio = None

        # 最大回撤
        rolling_max = close_prices.cummax()
        drawdown = (close_prices - rolling_max) / rolling_max
        max_drawdown = drawdown.min()

        # 產生 AI 分析文字
        analysis_text = get_technical_analysis(df)

        # --- 4. 資料清理 (關鍵修復步驟) ---
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # 將 DataFrame 中的 NaN 轉為 Python 的 None (JSON null)
        # 這裡用 replace 很重要，因為 where 有時會遺漏
        df = df.replace({np.nan: None})

        chart_data = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'MA5', 'MA20', 'MA60']].to_dict('records')

        return {
            "ticker": ticker,
            # 使用 safe_round 保護每一個數字
            "cagr_pct": safe_round(cagr * 100),
            "volatility_pct": safe_round(volatility * 100),
            "sharpe_ratio": safe_round(sharpe_ratio),
            "max_drawdown_pct": safe_round(max_drawdown * 100),
            "analysis": analysis_text,
            "history": chart_data
        }

    except Exception as e:
        print(f"Error calculating metrics: {e}") # 印出錯誤以便除錯
        return {"error": f"計算錯誤: {str(e)}"}