import streamlit as st
import yfinance as yf

# 1. 網頁基礎設定
st.set_page_config(page_title="AI 網通戰情室", layout="wide")
st.title("🚀 金像電 (2368) 產業鏈即時儀表板")

# 2. 抓取數據邏輯 (與第二課相同)
def get_data(ticker):
    data = yf.Ticker(ticker).fast_info
    change = (data['last_price'] - data['previous_close']) / data['previous_close'] * 100
    return data['last_price'], change

gce_price, gce_chg = get_data("2368.TW")
emc_price, emc_chg = get_data("2383.TW")

# --- 區塊 A：即時股價連動 ---
st.header("📊 區塊 A：即時股價監控")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("金像電 (2368)", f"{gce_price:.1f}", f"{gce_chg:+.2f}%")
with col2:
    st.metric("台光電 (2383) - 上游領先指標", f"{emc_price:.1f}", f"{emc_chg:+.2f}%")
with col3:
    spread = gce_chg - emc_chg
    st.metric("產業強弱差 (Spread)", f"{spread:+.2f}%", help="金像電漲幅減去台光電漲幅")

# --- 區塊 B：產業新聞與邏輯拆解 ---
st.header("🔍 區塊 B：新聞與產業邏輯惡補")
with st.expander("點擊展開：金像電 170 億資本支出背後含義"):
    st.write("""
    1. **ASIC 訂單滿載**：目前 CSP 大廠自研晶片需求遠超預期。
    2. **800G 換代潮**：800G 交換器板層數提升至 30 層以上，單價與毛利翻倍。
    3. **泰國產能預期**：Q2 投產將是營收第二次跳增的關鍵點。
    """)

# --- 區塊 C：連動邏輯自動判斷 ---
st.header("⚖️ 區塊 C：連動策略判定")
if spread < -2:
    st.error("🚨 警告：上游台光電已發動，金像電存在補漲機會，請確認 B/B Ratio 是否穩定。")
elif spread > 2:
    st.warning("⚠️ 提醒：金像電短線衝刺過快，需觀察下游智邦 (2345) 是否同步跟進。")
else:
    st.success("✅ 狀態：產業鏈步調一致，多頭趨勢健康。")

    st.info("### 如何安裝與執行\n"
            "1. 先安裝必要套件：\n"
            "（如遇安裝權限問題，請直接在指令後加上 --user 參數）\n"
            "```\n"
            "python -m pip install --user streamlit yfinance\n"
            "```\n"
            "2. 進入此程式所在的資料夾，再執行：\n"
            "```\n"
            "python -m streamlit run app.py\n"
            "```\n"
            "依照畫面指示於瀏覽器瀏覽儀表板即可。")
            # 在原本的 get_data 下方加入智邦 2345.TW
acct_price, acct_chg = get_data("2345.TW")

# 在區塊 A 的 st.columns 中改為 3 欄
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("金像電 (2368)", f"{gce_price:.1f}", f"{gce_chg:+.2f}%")
with col2:
    st.metric("台光電 (2383) - 上游", f"{emc_price:.1f}", f"{emc_chg:+.2f}%")
with col3:
    st.metric("智邦 (2345) - 下游", f"{acct_price:.1f}", f"{acct_chg:+.2f}%")