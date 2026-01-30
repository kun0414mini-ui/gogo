import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 伺服器垂直全鏈戰情室", layout="wide")
st.title("🚀 金像電 (2368) 獲利趨勢與庫存流動監控")

# 2. 歷史趨勢數據庫 (數據基準：2025 Q1-Q3 毛利率)
TREND_DATA = {
    "季度": ["2025 Q1", "2025 Q2", "2025 Q3"],
    "金像電 (2368)": [34.2, 36.8, 39.5],
    "台光電 (2383)": [26.5, 27.2, 29.8],
    "智邦 (2345)": [21.8, 22.1, 22.3]
}

# 3. 實時庫存數據庫
CHAIN_DATA = {
    "2330.TW": {"name": "台積電 (2330)", "role": "上游：封裝", "q2": 0, "q3": 0, "base": "2025 Q3"},
    "2383.TW": {"name": "台光電 (2383)", "role": "上游：材料", "q2": 51.5, "q3": 52.12, "base": "2025 Q3"},
    "2368.TW": {"name": "金像電 (2368)", "role": "中游：PCB", "q2": 90.9, "q3": 73.01, "base": "2025 Q3"},
    "2345.TW": {"name": "智邦 (2345)", "role": "下游：交換器", "q2": 45.4, "q3": 43.25, "base": "2025 Q3"},
    "2317.TW": {"name": "鴻海 (2317)", "role": "下游：組裝", "q2": 50.1, "q3": 49.51, "base": "2025 Q3"}
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

# 區塊 B：週轉天數數據流動表
st.header("📊 區塊 B：存貨週轉流動與警戒監控")
table_data = []
for tid, v in CHAIN_DATA.items():
    if v['q2'] > 0:
        change = (v['q3'] - v['q2']) / v['q2']
        trend = "📉 下滑 (好)" if change < 0 else "📈 上升 (警惕)"
        alert_light = "🔴 警戒" if change > 0.1 else "🟢 正常"
        flow_text = f"{v['q2']} → {v['q3']} ({change:+.1%})"
    else: flow_text, alert_light, trend = "N/A", "⚪ 略過", "N/A"
    
    table_data.append({
        "產業位置": v['role'],
        "股票名稱 (代號)": v['name'],
        "週轉流動 (Q2→Q3)": flow_text,
        "庫存趨勢": trend,
        "庫存警戒燈": alert_light,
        "數據基準": v['base']
    })
st.table(pd.DataFrame(table_data))
st.caption("💡 **燈號判定**：🟢 正常：天數下滑；🔴 警戒：較上季增加 > 10%。")

# 區塊 C：獲利趨勢視覺化 (新增)
st.header("📈 區塊 C：毛利率獲利趨勢折線圖")
df_trend = pd.DataFrame(TREND_DATA).set_index("季度")
st.line_chart(df_trend)
st.caption("數據解讀：斜率越陡代表技術溢價越高。目前 金像電 (2368) 毛利率趨勢最為強勁。")

# 區塊 D：價格防禦與強弱差
st.header("⚖️ 區塊 D：產業鏈價格防禦判定")
spread = prices["2368.TW"] - prices["2383.TW"]
if spread < -2:
    st.error(f"⚠️ 強弱差 {spread:.2f}%：台光電 (2383) 領漲，金像電 (2368) 存在補漲空間。")
elif spread > 2:
    st.warning(f"⚠️ 強弱差 {spread:.2f}%：金像電 (2368) 漲幅過大，需核實下游庫存去化。")
else:
    st.success(f"✅ 強弱差 {spread:.2f}%：產業鏈步調同步。")

# 區塊 E：後續追蹤清單
st.header("📋 區塊 E：後續追蹤與決策清單")
st.checkbox("追蹤 金像電 (2368) 泰國廠二期進度，確保 170 億產能產出。")
st.checkbox("核實 智邦 (2345) 800G 出貨佔比，驗證週轉天數是否維持低位。")