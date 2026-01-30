import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面配置
st.set_page_config(page_title="AI 伺服器精簡戰情室", layout="wide")
st.title("🚀 金像電 (2368) 垂直產業鏈監控系統")

# 2. 數據庫 (數據基準：2025 Q3)
CHAIN_DATA = {
    "2330.TW": {"name": "台積電 (2330)", "role": "上游：封裝", "q2": 0, "q3": 0, "gm": "53.4%"},
    "2383.TW": {"name": "台光電 (2383)", "role": "上游：材料", "q2": 51.5, "q3": 52.12, "gm": "29.8%"},
    "2368.TW": {"name": "金像電 (2368)", "role": "中游：PCB", "q2": 90.9, "q3": 73.01, "gm": "39.5%"},
    "2345.TW": {"name": "智邦 (2345)", "role": "下游：交換器", "q2": 45.4, "q3": 43.25, "gm": "22.3%"},
    "2317.TW": {"name": "鴻海 (2317)", "role": "下游：組裝", "q2": 50.1, "q3": 49.51, "gm": "6.4%"}
}

def get_live(ticker):
    try:
        s = yf.Ticker(ticker); i = s.fast_info
        return i['last_price'], (i['last_price'] - i['previous_close']) / i['previous_close'] * 100
    except: return 0.0, 0.0

# 區塊 A：即時市況
st.header("💹 區塊 A：產業鏈即時動能對照")
cols = st.columns(len(CHAIN_DATA))
prices = {}
for i, (tid, info) in enumerate(CHAIN_DATA.items()):
    p, c = get_live(tid)
    prices[tid] = c
    cols[i].metric(info['name'], f"{p:.1f}", f"{c:+.2f}%")

# 區塊 B：獲利邏輯與存貨週轉流動
st.header("📊 區塊 B：獲利邏輯與存貨週轉監控")
table_data = []
for tid, v in CHAIN_DATA.items():
    if v['q2'] > 0:
        change = (v['q3'] - v['q2']) / v['q2']
        alert = "🔴 警戒" if change > 0.1 else "🟢 正常"
        flow = f"{v['q2']} → {v['q3']} ({change:+.1%})"
    else: flow, alert = "N/A", "⚪ 略過"
    
    table_data.append({
        "股票名稱 (代號)": v['name'],
        "最新毛利率": v['gm'],
        "週轉流動 (Q2→Q3)": flow,
        "庫存警戒燈": alert,
        "數據基準": "2025 Q3"
    })
st.table(pd.DataFrame(table_data))
st.caption("💡 燈號說明：🟢 正常：天數下滑；🔴 警戒：較上季增加 > 10%。")

# 區塊 C：價格防禦判定
st.header("⚖️ 區塊 C：產業鏈價格防禦判定")
spread = prices["2368.TW"] - prices["2383.TW"]
if spread < -2:
    st.error(f"⚠️ 強弱差 {spread:.2f}%：台光電 (2383) 領漲，金像電 (2368) 存在補漲空間。")
elif spread > 2:
    st.warning(f"⚠️ 強弱差 {spread:.2f}%：金像電 (2368) 漲幅過大，需核實下游去化。")
else:
    st.success(f"✅ 強弱差 {spread:.2f}%：產業鏈步調同步。")

# 區塊 D：後續追蹤與決策清單
st.header("📋 區塊 D：後續追蹤清單")
st.checkbox("核實 金像電 (2368) 獲利爆發期指標：EPS 成長斜率是否超越毛利率。")
st.checkbox("觀察 智邦 (2345) 800G 交換器出貨，驗證下游週轉天數是否低於 45 天。")
st.checkbox("追蹤 鴻海 (2317) AI 伺服器量產時程，作為產業鏈去化之保險。")