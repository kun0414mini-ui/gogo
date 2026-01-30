import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 網通戰情室", layout="wide")
st.title("🚀 標的 (2368) 核心戰情監控系統")

# 2. 側邊欄：設定
st.sidebar.header("⚙️ 戰情室設定")
user_tickers = st.sidebar.text_input("輸入自選對照組 (代號)", "2303.TW, 3481.TW")
custom_list = [t.strip() for t in user_tickers.split(",") if t.strip()]

# 3. 核心數據定義 (2026-01-30 更新)
CORE_DATA = {
    "2368.TW": {"name": "金像電", "eps": "5.82", "gm": "39.5%", "logic": "170億資本支出鎖定800G/ASIC"},
    "2383.TW": {"name": "台光電", "eps": "7.45", "gm": "29.8%", "logic": "M9等級高階材料壟斷地位"},
    "2345.TW": {"name": "智邦", "eps": "4.91", "gm": "22.3%", "logic": "800G交換器需求出海口"}
}

def get_live(ticker):
    try:
        s = yf.Ticker(ticker); i = s.fast_info
        return i['last_price'], (i['last_price'] - i['previous_close']) / i['previous_close'] * 100
    except: return 0.0, 0.0

# 4. 區塊 A：核心族群監控
st.header("💹 區塊 A：AI 網通核心即時市況")
cols = st.columns(3)
gce_price, gce_chg = get_live("2368.TW")
emc_price, emc_chg = get_live("2383.TW")
acct_price, acct_chg = get_live("2345.TW")

cols[0].metric("標的 (2368)", f"{gce_price:.1f}", f"{gce_chg:+.2f}%")
cols[1].metric("標的 (2383)", f"{emc_price:.1f}", f"{emc_chg:+.2f}%")
cols[2].metric("標的 (2345)", f"{acct_price:.1f}", f"{acct_chg:+.2f}%")

# 5. 區塊 B：獲利邏輯驗證 (恢復原有表格)
st.header("📊 區塊 B：獲利邏輯驗證")
finance_df = pd.DataFrame([
    {"標的 (代號)": v['name'], "最新單季 EPS": v['eps'], "最新毛利率": v['gm'], "獲利邏輯拆解": v['logic']}
    for v in CORE_DATA.values()
])
st.table(finance_df)

# 6. 區塊 C：自選股相對強弱監控 (與 2368 互動)
st.header("⚖️ 區塊 C：自選股與標的 (2368) 相對強度")
if custom_list:
    custom_cols = st.columns(len(custom_list))
    for i, tid in enumerate(custom_list):
        p, c = get_live(tid)
        rel_strength = c - gce_chg # 與金像電的漲跌差
        custom_cols[i].metric(f"標的 ({tid[:4]})", f"{p:.1f}", f"{rel_strength:+.2f}%", help="相對於金像電的強弱差")

# 7. 區塊 D：價格防禦判定
st.header("🚩 區塊 D：狀態判定警示")
spread = gce_chg - emc_chg
if spread < -2:
    st.error(f"⚠️ 強弱差 {spread:.2f}%：上游領跑，標的 (2368) 存在補漲空間。")
elif spread > 2:
    st.warning(f"⚠️ 強弱差 {spread:.2f}%：標的 (2368) 過熱，觀察下游需求。")
else:
    st.success(f"✅ 強弱差 {spread:.2f}%：產業鏈步調同步。")