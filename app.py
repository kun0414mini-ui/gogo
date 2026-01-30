import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 伺服器垂直全鏈戰情室", layout="wide")
st.title("🚀 金像電 (2368) 垂直產業鏈暨庫存監控系統")

# 2. 產業鏈暨庫存數據庫 (2026-01-30 更新)
CHAIN_DATA = {
    "2330.TW": {"name": "台積電 (2330)", "role": "上游：封裝", "gm": "53.4%", "inv": 0, "prev_inv": 0, "base": "2025 Q3"},
    "2383.TW": {"name": "台光電 (2383)", "role": "上游：材料", "gm": "29.8%", "inv": 52.12, "prev_inv": 51.5, "base": "2025 Q3"},
    "2368.TW": {"name": "金像電 (2368)", "role": "中游：PCB", "gm": "39.5%", "inv": 73.01, "prev_inv": 90.9, "base": "2025 Q3"},
    "2345.TW": {"name": "智邦 (2345)", "role": "下游：交換器", "gm": "22.3%", "inv": 43.25, "prev_inv": 45.4, "base": "2025 Q3"},
    "2317.TW": {"name": "鴻海 (2317)", "role": "下游：組裝", "gm": "6.4%", "inv": 49.51, "prev_inv": 50.1, "base": "2025 Q3"}
}

def get_live(ticker):
    try:
        s = yf.Ticker(ticker); i = s.fast_info
        return i['last_price'], (i['last_price'] - i['previous_close']) / i['previous_close'] * 100
    except: return 0.0, 0.0

# 3. 區塊 A：即時市況
st.header("💹 區塊 A：產業鏈即時動能對照")
cols = st.columns(len(CHAIN_DATA))
prices = {}
for i, (tid, info) in enumerate(CHAIN_DATA.items()):
    p, c = get_live(tid)
    prices[tid] = c
    cols[i].metric(info['name'], f"{p:.1f}", f"{c:+.2f}%")

# 4. 區塊 B：獲利與庫存驗證
st.header("📊 區塊 B：獲利邏輯與庫存監控")
table_data = []
for tid, v in CHAIN_DATA.items():
    inv_change = 0 if v['prev_inv'] == 0 else (v['inv'] - v['prev_inv']) / v['prev_inv']
    alert_light = "🔴 警戒" if inv_change > 0.1 else "🟢 正常"
    
    table_data.append({
        "產業位置": v['role'],
        "股票名稱 (代號)": v['name'],
        "最新毛利率": v['gm'],
        "存貨週轉天數": f"{v['inv']} 天" if v['inv'] > 0 else "N/A",
        "庫存警戒燈": alert_light,
        "數據基準": v['base']
    })
st.table(pd.DataFrame(table_data))

# 5. 區塊 C：價格防禦判定
st.header("⚖️ 區塊 C：價格防禦與強弱差判定")
spread_up = prices["2368.TW"] - prices["2383.TW"]
if spread_up < -2:
    st.error(f"⚠️ 強弱差 {spread_up:.2f}%：台光電 (2383) 領漲，金像電 (2368) 存在補漲空間。")
elif spread_up > 2:
    st.warning(f"⚠️ 強弱差 {spread_up:.2f}%：金像電 (2368) 漲幅過大，需核實下游庫存去化。")
else:
    st.success(f"✅ 強弱差 {spread_up:.2f}%：產業鏈步調同步。")