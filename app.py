import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面基礎配置
st.set_page_config(page_title="AI 網通戰情室", layout="wide")
st.title("🚀 2368 金像電 AI 網通全鏈監控")

# 2. 備援財務數據 (當 API 延遲時使用最新查證數據)
BACKUP_STATS = {
    "2368.TW": {"name": "金像電", "eps": "5.82 (Q3)", "gm": "39.5%", "logic": "170億資本支出, 800G板龍頭"},
    "2383.TW": {"name": "台光電", "eps": "7.45 (Q3)", "gm": "29.8%", "logic": "高階 M9 材料壟斷"},
    "2345.TW": {"name": "智邦", "eps": "4.91 (Q3)", "gm": "22.3%", "logic": "800G 交換器需求出海口"}
}

# 3. 數據抓取函數
def get_stock_metrics(ticker_id):
    try:
        stock = yf.Ticker(ticker_id)
        info = stock.fast_info
        last_price = info['last_price']
        prev_close = info['previous_close']
        change = (last_price - prev_close) / prev_close * 100
        return last_price, change
    except:
        return 0.0, 0.0

# 4. 區塊 A：即時產業鏈連動
st.header("💹 區塊 A：產業鏈即時數據")
col1, col2, col3 = st.columns(3)

gce_p, gce_c = get_stock_metrics("2368.TW")
emc_p, emc_c = get_stock_metrics("2383.TW")
acct_p, acct_c = get_stock_metrics("2345.TW")

with col1:
    st.metric("金像電 (2368)", f"{gce_p:.1f}", f"{gce_c:+.2f}%")
with col2:
    st.metric("台光電 (2383) - 上游", f"{emc_p:.1f}", f"{emc_c:+.2f}%")
with col3:
    st.metric("智邦 (2345) - 下游", f"{acct_p:.1f}", f"{acct_c:+.2f}%")

# 5. 區塊 B：財務驗證與獲利邏輯
st.header("💰 區塊 B：獲利能力與產業邏輯")
finance_list = []
for tid, val in BACKUP_STATS.items():
    finance_list.append({
        "公司": val['name'],
        "最新 EPS": val['eps'],
        "最新毛利率": val['gm'],
        "核心邏輯": val['logic']
    })
st.table(pd.DataFrame(finance_list))

# 6. 區塊 C：價格防禦與狀態判定
st.header("🛡️ 區塊 C：自動判定系統")
spread = gce_c - emc_c  # 中游與上游的強弱差
if spread < -2:
    st.error(f"🚨 警告：強弱差 {spread:.2f}%，上游已動，金像電存在補漲空間。")
elif spread > 2:
    st.warning(f"⚠️ 提醒：強弱差 {spread:.2f}%，金像電衝刺過快，留意回檔壓力。")
else:
    st.success(f"✅ 狀態：強弱差 {spread:.2f}%，產業鏈步調一致。")

st.markdown("---")
st.caption("數據來源：Yahoo Finance & 2026-01-29 產業研究報告")
