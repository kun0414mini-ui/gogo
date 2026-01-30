import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 伺服器全鏈戰情室", layout="wide")
st.title("🚀 金像電 (2368) 垂直產業鏈數據流動監控")

# 2. 數據庫 (數據基準：2025 Q3 vs Q2)
CHAIN_DATA = {
    "2330.TW": {"name": "台積電 (2330)", "role": "上游：封裝", "gm": "53.4%", "q2": 0, "q3": 0, "base": "2025 Q3"},
    "2383.TW": {"name": "台光電 (2383)", "role": "上游：材料", "gm": "29.8%", "q2": 51.5, "q3": 52.12, "base": "2025 Q3"},
    "2368.TW": {"name": "金像電 (2368)", "role": "中游：PCB", "gm": "39.5%", "q2": 90.9, "q3": 73.01, "base": "2025 Q3"},
    "2345.TW": {"name": "智邦 (2345)", "role": "下游：交換器", "gm": "22.3%", "q2": 45.4, "q3": 43.25, "base": "2025 Q3"},
    "2317.TW": {"name": "鴻海 (2317)", "role": "下游：組裝", "gm": "6.4%", "q2": 50.1, "q3": 49.51, "base": "2025 Q3"}
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

# 4. 區塊 B：獲利邏輯與庫存數據流動
st.header("📊 區塊 B：獲利邏輯與存貨週轉流動")
table_data = []
for tid, v in CHAIN_DATA.items():
    if v['q2'] > 0:
        change = (v['q3'] - v['q2']) / v['q2']
        trend = "📉 下滑 (好)" if change < 0 else "📈 上升 (警惕)"
        alert_light = "🔴 警戒" if change > 0.1 else "🟢 正常"
        flow_text = f"{v['q2']} → {v['q3']} ({change:+.1%})"
    else:
        flow_text, alert_light, trend = "N/A", "⚪ 略過", "N/A"
    
    table_data.append({
        "產業位置": v['role'],
        "股票名稱 (代號)": v['name'],
        "最新毛利率": v['gm'],
        "週轉流動 (Q2→Q3)": flow_text,
        "庫存趨勢": trend,
        "庫存警戒燈": alert_light,
        "數據基準": v['base']
    })
st.table(pd.DataFrame(table_data))

# 燈號說明備註
st.caption("💡 **庫存警戒燈判定說明**：🟢 正常：週轉天數持平或下滑；🔴 警戒：週轉天數較上一季增加超過 10%，代表下游拉貨動能可能放緩。")

# 5. 區塊 C：價格防禦判定
st.header("⚖️ 區塊 C：產業鏈強弱差判定")
spread_up = prices["2368.TW"] - prices["2383.TW"]
if spread_up < -2:
    st.error(f"⚠️ 強弱差 {spread_up:.2f}%：台光電 (2383) 領漲，金像電 (2368) 存在補漲空間。")
elif spread_up > 2:
    st.warning(f"⚠️ 強弱差 {spread_up:.2f}%：金像電 (2368) 漲幅過大，需核實下游庫存去化。")
else:
    st.success(f"✅ 強弱差 {spread_up:.2f}%：產業鏈步調同步。")

# 6. 區塊 D：後續追蹤資訊清單
st.header("📋 區塊 D：後續追蹤與決策清單")
st.checkbox("追蹤金像電 (2368) 泰國廠二期設備入廠進度，確保 170 億產能如期兌現。")
st.checkbox("觀察台光電 (2383) M9 材料之毛利率是否受競爭者影響而跌破 28%。")
st.checkbox("核實智邦 (2345) 800G 交換器出貨佔比，驗證下游去化天數是否維持在 45 天以下。")
st.checkbox("比對鴻海 (2317) AI 伺服器營收占比，作為產業鏈終極拉貨動能之保險。")