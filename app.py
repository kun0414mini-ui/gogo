import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 頁面配置
st.set_page_config(page_title="AI網通戰情室-自動版", layout="wide")
st.title("🚀 2368 金像電：全鏈自動監控系統")

# 定義監控標的
stocks = {
    "2368.TW": "金像電 (中游)",
    "2383.TW": "台光電 (上游)",
    "2345.TW": "智邦 (下游)"
}

# 2. 數據抓取函數 (含錯誤處理邏輯)
def fetch_all_data(ticker_id):
    stock = yf.Ticker(ticker_id)
    
    # 抓取股價 (fast_info 較穩定)
    price = stock.fast_info['last_price']
    change = (price - stock.fast_info['previous_close']) / stock.fast_info['previous_close'] * 100
    
    # 抓取財報 (自動計算毛利率)
    try:
        q_fin = stock.quarterly_financials
        # 取得最新一季數據
        latest_q = q_fin.columns[0].strftime('%Y-Q%q')
        rev = q_fin.loc['Total Revenue'].iloc[0]
        gp = q_fin.loc['Gross Profit'].iloc[0]
        gm = (gp / rev) * 100
        # 取得淨利計算簡易 EPS (僅為參考值)
        ni = q_fin.loc['Net Income Common Stockholders'].iloc[0]
        shares = stock.info.get('sharesOutstanding', 1)
        est_eps = ni / shares
    except:
        latest_q, gm, est_eps = "數據更新中", 0.0, 0.0
        
    return {
        "price": price,
        "change": change,
        "gm": gm,
        "eps": est_eps,
        "period": latest_q
    }

# 3. 畫面呈現 - 區塊 A：即時市況
st.header("💹 區塊 A：產業鏈即時價格")
cols = st.columns(len(stocks))
results = {}

for i, (tid, name) in enumerate(stocks.items()):
    data = fetch_all_data(tid)
    results[tid] = data
    cols[i].metric(name, f"{data['price']:.1f}", f"{data['change']:+.2f}%")

# 4. 畫面呈現 - 區塊 B：自動財報對比
st.header("📊 區塊 B：自動化財務指標")
df_list = []
for tid, name in stocks.items():
    df_list.append({
        "公司": name,
        "資料季度": results[tid]['period'],
        "自動計毛利率": f"{results[tid]['gm']:.2f}%",
        "預估單季EPS": f"{results[tid]['eps']:.2f}"
    })
st.table(pd.DataFrame(df_list))

# 5. 畫面呈現 - 區塊 C：價格防禦判定
st.header("🛡️ 區塊 C：產業鏈強弱監控")
gce_c = results["2368.TW"]["change"]
emc_c = results["2383.TW"]["change"]
spread = gce_c - emc_c

if spread < -2:
    st.error(f"🚨 警報：強弱差 {spread:.2f}%。上游材料(台光電)已漲，中游(金像電)補漲機率高！")
elif spread > 2:
    st.warning(f"⚠️ 提醒：強弱差 {spread:.2f}%。金像電漲幅過大，注意 800G 訂單是否提前反應。")
else:
    st.success(f"✅ 穩健：強弱差 {spread:.2f}%。產業鏈連動步調一致。")

st.caption(f"最後更新時間：{pd.Timestamp.now(tz='Asia/Taipei')}")
