import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 伺服器全鏈視覺戰情室", layout="wide")
st.title("🚀 金像電 (2368) 量價獲利三維監控系統")

# 2. 數據庫 (數據基準：2025 Q1-Q3)
GM_TREND = {
    "季度": ["2025 Q1", "2025 Q2", "2025 Q3"],
    "金像電 (2368)": [34.2, 36.8, 39.5],
    "台光電 (2383)": [26.5, 27.2, 29.8],
    "智邦 (2345)": [21.8, 22.1, 22.3]
}

EPS_TREND = {
    "季度": ["2025 Q1", "2025 Q2", "2025 Q3"],
    "金像電 (2368)": [2.50, 3.58, 5.82],
    "台光電 (2383)": [4.64, 6.25, 7.45],
    "智邦 (2345)": [4.02, 4.51, 4.91]
}

CHAIN_DATA = {
    "2330.TW": {"name": "台積電 (2330)", "q2": 0, "q3": 0},
    "2383.TW": {"name": "台光電 (2383)", "q2": 51.5, "q3": 52.12},
    "2368.TW": {"name": "金像電 (2368)", "q2": 90.9, "q3": 73.01},
    "2345.TW": {"name": "智邦 (2345)", "q2": 45.4, "q3": 43.25},
    "2317.TW": {"name": "鴻海 (2317)", "q2": 50.1, "q3": 49.51}
}

def get_market_data(ticker):
    try:
        s = yf.Ticker(ticker)
        i = s.fast_info
        # 抓取最近 5 日成交量均值
        hist = s.history(period="5d")
        avg_vol = hist['Volume'].mean()
        return i['last_price'], (i['last_price'] - i['previous_close']) / i['previous_close'] * 100, avg_vol
    except: return 0.0, 0.0, 0.0

# 區塊 A：即時動能
st.header("💹 區塊 A：產業鏈即時動能與量能")
cols = st.columns(len(CHAIN_DATA))
prices, volumes = {}, {}
for i, (tid, info) in enumerate(CHAIN_DATA.items()):
    p, c, v = get_market_data(tid)
    prices[tid], volumes[info['name']] = c, v
    cols[i].metric(info['name'], f"{p:.1f}", f"{c:+.2f}%")

# 區塊 B：存貨流動表
st.header("📊 區塊 B：存貨週轉天數流動監控")
table_data = []
for tid, v in CHAIN_DATA.items():
    if v['q2'] > 0:
        change = (v['q3'] - v['q2']) / v['q2']
        alert = "🔴 警戒" if change > 0.1 else "🟢 正常"
        flow = f"{v['q2']} → {v['q3']} ({change:+.1%})"
    else: flow, alert = "N/A", "⚪ 略過"
    table_data.append({"股票名稱 (代號)": v['name'], "週轉流動 (Q2→Q3)": flow, "庫存警戒燈": alert, "數據基準": "2025 Q3"})
st.table(pd.DataFrame(table_data))

# 區塊 C：獲利趨勢折線圖 (GM & EPS 對照)
st.header("📈 區塊 C：獲利趨勢對照 (毛利率 vs EPS)")
col_gm, col_eps = st.columns(2)
with col_gm:
    st.subheader("毛利率 (%) 趨勢")
    st.line_chart(pd.DataFrame(GM_TREND).set_index("季度"))
with col_eps:
    st.subheader("單季 EPS (元) 趨勢")
    st.line_chart(pd.DataFrame(EPS_TREND).set_index("季度"))

# 區塊 D：成交量柱狀圖 (新增)
st.header("📊 區塊 D：產業鏈 5 日平均成交量對照")
st.bar_chart(pd.Series(volumes))
st.caption("💡 成交量判讀：量能穩定放大代表趨勢具備延續性。")

# 區塊 E：價格防禦判定
st.header("⚖️ 區塊 E：產業鏈價格防禦判定")
spread = prices["2368.TW"] - prices["2383.TW"]
if spread < -2: st.error(f"⚠️ 強弱差 {spread:.2f}%：台光電 (2383) 領漲，金像電 (2368) 存在補漲空間。")
elif spread > 2: st.warning(f"⚠️ 強弱差 {spread:.2f}%：金像電 (2368) 過熱，需核實成交量是否異常放量。")
else: st.success(f"✅ 強弱差 {spread:.2f}%：產業鏈步調健康。")

# 區塊 F：決策清單
st.header("📋 區塊 F：後續追蹤與決策清單")
st.checkbox("追蹤 金像電 (2368) 170 億資本支出轉化為 EPS 的加速度。")
st.checkbox("觀察 智邦 (2345) 800G 出貨量與週轉天數的連動。")