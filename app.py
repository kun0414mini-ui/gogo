import streamlit as st
import yfinance as yf
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 1. 頁面配置
st.set_page_config(page_title="AI 伺服器全鏈決策中心", layout="wide")
st.title("🚀 金像電 (2368) 垂直產業鏈監控系統")

# 【郵件設定區】
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "kun0414.mini@gmail.com"
SENDER_PASSWORD = "rlxq bgpi bwie otjl"  # 非登入密碼，需至 Google 帳號申請
RECEIVER_EMAIL = "kun0414@gmail.com"

# 2. 數據基準
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

def send_email(subject, content):
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = Header(subject, 'utf-8')
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"郵件發送失敗: {e}")
        return False

# 區塊 A：即時市況
st.header("💹 區塊 A：產業鏈即時動能對照")
cols = st.columns(len(CHAIN_DATA))
prices = {}
for i, (tid, info) in enumerate(CHAIN_DATA.items()):
    p, c = get_live(tid); prices[tid] = c
    cols[i].metric(info['name'], f"{p:.1f}", f"{c:+.2f}%")

# 區塊 B：獲利與存貨週轉
st.header("📊 區塊 B：獲利邏輯與存貨週轉監控")
table_data = []
for tid, v in CHAIN_DATA.items():
    if v['q2'] > 0:
        change = (v['q3'] - v['q2']) / v['q2']
        flow = f"{v['q2']} → {v['q3']} ({change:+.1%})"
        alert = "🔴 警戒" if change > 0.1 else "🟢 正常"
    else: flow, alert = "N/A", "⚪ 略過"
    table_data.append({"股票名稱 (代號)": v['name'], "最新毛利率": v['gm'], "週轉流動 (Q2→Q3)": flow, "庫存警戒燈": alert, "數據基準": "2025 Q3"})
st.table(pd.DataFrame(table_data))

# 區塊 C：價格防禦判定
st.header("⚖️ 區塊 C：產業鏈價格防禦判定")
spread = prices["2368.TW"] - prices["2383.TW"]
status_msg = "✅ 步調同步"
if spread < -2: status_msg = "⚠️ 台光電 (2383) 領漲，補漲空間存"
elif spread > 2: status_msg = "🚩 金像電 (2368) 過熱，留意去化"
st.info(f"強弱差：{spread:.2f}% | 判定：{status_msg}")

# 區塊 D：長期策略備忘
st.header("🧠 區塊 D：長期策略備忘錄：營運槓桿核心邏輯")
strategy_data = [
    {"股票名稱 (代號)": "金像電 (2368)", "判定邏輯": "EPS 成長率 > 營收成長率", "狀態": "🚀 營運槓桿爆發"},
    {"股票名稱 (代號)": "台光電 (2383)", "判定邏輯": "毛利率維持 > 29.8%", "狀態": "💎 材料霸主"},
    {"股票名稱 (代號)": "智邦 (2345)", "判定邏輯": "週轉天數 < 45 天", "狀態": "✅ 需求強勁"}
]
st.table(pd.DataFrame(strategy_data))

# 區塊 E：Email 發送功能
st.header("📧 區塊 E：投資決策 Email 通報")
note_text = f"""
【AI 伺服器垂直鏈投資週報】
數據基準：2025 Q3 財報
📅 發送日期：{pd.Timestamp.now().strftime('%Y-%m-%d')}

1. 即時動能：
   金像電 (2368) 與 台光電 (2383) 強弱差為 {spread:.2f}%。
   判定：{status_msg}。

2. 庫存監控：
   金像電 (2368) 週轉天數流動：90.9 → 73.01。
   智邦 (2345) 週轉天數流動：45.4 → 43.25。
   目前全鏈庫存燈號正常。

3. 營運槓桿策略：
   170 億資本支出攤提中，後續觀察 EPS 成長斜率是否超越毛利率斜率。
"""

if st.button("🚀 發送投資週報到 Email"):
    if send_email(f"AI伺服器週報_{pd.Timestamp.now().strftime('%Y%m%d')}", note_text):
        st.success("✅ 週報已成功發送至 Email！")