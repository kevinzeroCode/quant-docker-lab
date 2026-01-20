import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(ticker: str, period: str = "5y") -> pd.DataFrame:
    """
    抓取指定股票的歷史資料。
    """
    stock = yf.Ticker(ticker)
    # auto_adjust=True 會自動處理除權息，這對計算報酬率很重要
    df = stock.history(period=period, auto_adjust=True)
    return df

def calculate_performance_metrics(ticker: str, period: str = "2y", risk_free_rate: float = 0.02) -> dict:
    """
    計算並回傳股票的關鍵績效指標 (KPIs)。
    Agent 將會使用這個工具來回答使用者的問題。
    """
    try:
        # 1. 獲取資料
        df = get_stock_data(ticker, period)
        if df.empty:
            return {"error": f"找不到 {ticker} 的資料"}

        # 只取收盤價
        close_prices = df['Close']

        # 2. 計算日報酬率
        daily_returns = close_prices.pct_change().dropna()

        # 3. 計算指標
        # A. 總報酬率 (Total Return)
        total_return = (close_prices.iloc[-1] / close_prices.iloc[0]) - 1

        # B. 年化報酬率 (CAGR)
        days = (df.index[-1] - df.index[0]).days
        years = days / 365.25
        cagr = (close_prices.iloc[-1] / close_prices.iloc[0]) ** (1 / years) - 1

        # C. 年化波動率 (Volatility) - 假設一年 252 個交易日
        volatility = daily_returns.std() * np.sqrt(252)

        # D. 夏普值 (Sharpe Ratio)
        # (年化報酬 - 無風險利率) / 年化波動率
        sharpe_ratio = (cagr - risk_free_rate) / volatility

        # E. 最大回撤 (Max Drawdown)
        rolling_max = close_prices.cummax()
        drawdown = (close_prices - rolling_max) / rolling_max
        max_drawdown = drawdown.min()

        return {
            "ticker": ticker,
            "period_years": round(years, 2),
            "total_return_pct": round(total_return * 100, 2),
            "cagr_pct": round(cagr * 100, 2),
            "volatility_pct": round(volatility * 100, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown_pct": round(max_drawdown * 100, 2)
        }

    except Exception as e:
        return {"error": str(e)}

# --- 本地測試區 (Local Test) ---
if __name__ == "__main__":
    # 這樣你可以直接執行這個檔案來測試邏輯對不對
    print("正在測試 Apple (AAPL)...")
    result = calculate_performance_metrics("AAPL")
    print(result)