import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 伺服器全鏈戰情室", layout="wide")
st.title("🚀 標的 (2368) 高階伺服器垂直產業鏈監控")

# 2. 產業鏈數據庫 (2026-01-30 更新)
CHAIN_DATA = {
    "2330.TW": {"role": "上游：封裝", "name": "台積電", "metric": "CoWoS 產能", "status": "🚀 供給關鍵"},
    "2383.TW": {"role": "上游：材料", "name": "台光電", "metric": "GM: 29.8%", "status": "💎 材料霸主"},
    "2368.TW": {"role": "中游：PCB", "name": "金像電", "metric": "GM: 39.5%", "status": "🔥 極度擴張"},
    "2345.TW": {"role": "下游：交換器", "name": "智邦", "metric": "GM: 22.3%", "status": "✅ 需求穩健"},
    "2317.TW": {"role": "下游：組裝", "name": "鴻海", "metric": "AI伺服器佔比", "status": "🛡️ 防禦穩健"}
}

def get_live(ticker):
    try:
        s = yf.Ticker(ticker); i = s.fast_info
        return i['last_price'], (i['last_price'] - i['previous_close']) / i['previous_close'] * 100
    except: return 0.0, 0.0

# 3. 區塊 A：即時市況與垂直連動
st.header("💹 區塊 A：產業鏈即時動能對照")
st.caption("觀察邏輯：上游動能領先中游，下游出貨驗證獲利。")
cols = st.columns(len(CHAIN_DATA))
prices = {}

for i, (tid, info) in enumerate(CHAIN_DATA.items()):
    p, c = get_live(tid)
    prices[tid] = c
    cols[i].metric(f"{info['name']} ({tid[:4]})", f"{p:.1f}", f"{c:+.2f}%")

# 4. 區塊 B：獲利邏輯驗證 (垂直縱深版)
st.header("📊 區塊 B：全鏈獲利邏輯拆解")
finance_df = pd.DataFrame([
    {
        "產業位置": v['role'],
        "標的（代號）": v['name'] + f" ({k[:4]})",
        "最新狀態": v['status'],
        "核心數據/指標": v['metric'],
        "投資邏輯": "連動觀察晶片供給與下游出貨之平衡點"
    } for k, v in CHAIN_DATA.items()
])
st.table(finance_df)

# 5. 區塊 C：跨層級價格防禦判定
st.header("⚖️ 區塊 C：產業鏈強弱差警示 (Spread)")
# 計算「中游-上游材料」與「中游-下游交換器」的強弱差
spread_up = prices["2368.TW"] - prices["2383.TW"]
spread_down = prices["2368.TW"] - prices["2345.TW"]

col_up, col_down = st.columns(2)
with col_up:
    st.subheader("中游 vs 上游 (材料)")
    if spread_up < -2: st.error(f"⚠️ 價差 {spread_up:.2f}%：材料端領漲，標的 (2368) 存在補漲機會。")
    else: st.success(f"✅ 價差 {spread_up:.2f}%：材料供應與板材加工估值同步。")

with col_down:
    st.subheader("中游 vs 下游 (交換器)")
    if spread_down > 2: st.warning(f"⚠️ 價差 {spread_down:.2f}%：標的 (2368) 衝刺過快，需核實下游智邦拉貨動能。")
    else: st.success(f"✅ 價差 {spread_down:.2f}%：下游需求足以支撐中游產能。")