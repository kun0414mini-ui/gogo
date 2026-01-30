import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面配置
st.set_page_config(page_title="AI 網通自選戰情室", layout="wide")
st.title("🚀 AI 網通全鏈暨自選監控系統")

# 2. 側邊欄：自選股輸入邏輯
st.sidebar.header("⚙️ 戰情室設定")
user_tickers = st.sidebar.text_input("輸入自選標的 (用逗號隔開)", "2303.TW, 3481.TW")
ticker_list = [t.strip() for t in user_tickers.split(",") if t.strip()]

# 3. 核心標的固定監控 (維持三劍客)
CORE_STOCKS = {"2368.TW": "金像電", "2383.TW": "台光電", "2345.TW": "智邦"}

def get_data(ticker):
    try:
        s = yf.Ticker(ticker)
        i = s.fast_info
        return i['last_price'], (i['last_price'] - i['previous_close']) / i['previous_close'] * 100
    except: return 0, 0

# 4. 區塊 A：核心族群即時狀態
st.header("💹 區塊 A：AI 網通核心連動")
cols = st.columns(3)
core_results = {}
for i, (tid, name) in enumerate(CORE_STOCKS.items()):
    p, c = get_data(tid)
    core_results[tid] = c
    cols[i].metric(f"{name} ({tid[:4]})", f"{p:.1f}", f"{c:+.2f}%")

# 5. 區塊 B：自選股即時監控
st.header("📂 區塊 B：自選標的價格防禦")
if ticker_list:
    custom_cols = st.columns(len(ticker_list))
    for i, tid in enumerate(ticker_list):
        p, c = get_data(tid)
        custom_cols[i].metric(f"標的 ({tid.split('.')[0]})", f"{p:.1f}", f"{c:+.2f}%")

# 6. 區塊 C：價格防禦與邏輯警示
st.header("⚖️ 區塊 C：產業鏈強弱差判定")
spread = core_results["2368.TW"] - core_results["2383.TW"]
if spread < -2:
    st.error(f"🚩 強弱差 {spread:.2f}%：上游台光電領跑，金像電存在補漲空間。")
elif spread > 2:
    st.warning(f"🚩 強弱差 {spread:.2f}%：金像電過熱，注意下游智邦需求。")
else:
    st.success(f"🚩 強弱差 {spread:.2f}%：產業鏈步調健康。")

st.caption(f"最後更新：{pd.Timestamp.now(tz='Asia/Taipei')}")
