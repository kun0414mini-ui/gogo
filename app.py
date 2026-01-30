import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 網通戰情室", layout="wide")
st.title("🚀 AI 網通全鏈監控戰情室")

# 2. 週報精選數據 (2026-01-30 更新)
MONITOR_DATA = {
    "2368.TW": {"name": "金像電 (2368)", "eps": "5.82", "gm": "39.5%", "status": "🚀 極度擴張", "logic": "170億資本支出鎖定800G/ASIC"},
    "2383.TW": {"name": "台光電 (2383)", "eps": "7.45", "gm": "29.8%", "status": "💎 材料霸主", "logic": "M9等級高階材料壟斷地位"},
    "2345.TW": {"name": "智邦 (2345)", "eps": "4.91", "gm": "22.3%", "status": "✅ 穩健成長", "logic": "800G交換器需求出海口"}
}

# 3. 數據抓取函數
def fetch_live_price(ticker_id):
    try:
        stock = yf.Ticker(ticker_id)
        info = stock.fast_info
        return info['last_price'], (info['last_price'] - info['previous_close']) / info['previous_close'] * 100
    except:
        return 0.0, 0.0

# 4. 區塊 A：即時價格與強弱監控
st.header("💹 區塊 A：即時市況監控")
cols = st.columns(3)
prices = {}

for i, tid in enumerate(MONITOR_DATA.keys()):
    p, c = fetch_live_price(tid)
    prices[tid] = c
    cols[i].metric(MONITOR_DATA[tid]['name'], f"{p:.1f}", f"{c:+.2f}%")

# 5. 區塊 B：週報核心獲利對比
st.header("📊 區塊 B：獲利邏輯驗證")
finance_df = pd.DataFrame([
    {
        "標的（代號）": v['name'],
        "狀態判定": v['status'],
        "最新單季 EPS": v['eps'],
        "最新毛利率": v['gm'],
        "獲利邏輯拆解": v['logic']
    } for v in MONITOR_DATA.values()
])
st.table(finance_df)

# 6. 區塊 C：產業鏈強弱差 (Spread) 判定
st.header("⚖️ 區塊 C：價格防禦判定")
spread = prices["2368.TW"] - prices["2383.TW"]
if spread < -2:
    st.error(f"🚩 強弱差 {spread:.2f}%：上游領跑，標的（2368）存在補漲空間。")
elif spread > 2:
    st.warning(f"🚩 強弱差 {spread:.2f}%：標的（2368）過熱，觀察下游需求。")
else:
    st.success(f"🚩 強弱差 {spread:.2f}%：產業鏈步調同步。")

st.caption("數據來源：Yahoo Finance & 2026-01-30 週報數據")
