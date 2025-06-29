import yfinance as yf
import pandas as pd
import streamlit as st
from MACD import ta.momentum 
import RSIIndicator
import plotly.graph_objects as go

st.set_page_config(page_title="🪙 Gold Swing Bot", layout="centered")
st.title("🪙 Gold Swing Bot")
st.markdown("### 🔍 تحليل ذكي لحركة الذهب باستخدام المؤشرات الفنية")

df = yf.download('GC=F', period='6mo', interval='1d')

if df.empty:
    st.error("❌ فشل تحميل بيانات الذهب. تأكد من اتصال الإنترنت.")
    st.stop()

df['SMA_10'] = df['Close'].rolling(window=10).mean()
df['RSI'] = RSIIndicator(close=df['Close']).rsi()
macd = MACD(close=df['Close'])
df['MACD'] = macd.macd()
df['MACD_signal'] = macd.macd_signal()
df.dropna(inplace=True)

latest = df.iloc[-1]

if latest['RSI'] < 30 and latest['MACD'] > latest['MACD_signal']:
    recommendation = "🟢 **شراء** - السعر منخفض وإشارة صعود"
elif latest['RSI'] > 70 and latest['MACD'] < latest['MACD_signal']:
    recommendation = "🔴 **بيع** - السعر مرتفع وإشارة هبوط"
else:
    recommendation = "🟡 **انتظار** - لا توجد إشارة واضحة حالياً"

st.subheader("📌 توصية التداول:")
st.markdown(f"### {recommendation}")

st.subheader("📊 الرسم البياني:")
fig = go.Figure(data=[go.Candlestick(
    x=df.tail(10).index,
    open=df.tail(10)['Open'],
    high=df.tail(10)['High'],
    low=df.tail(10)['Low'],
    close=df.tail(10)['Close']
)])
fig.update_layout(
    title="رسم الشموع الذهب - آخر 10 أيام",
    xaxis_title="التاريخ",
    yaxis_title="السعر (دولار)",
    height=500
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📈 المؤشرات الفنية لآخر 10 أيام"):
    st.dataframe(df.tail(10)[['Close', 'SMA_10', 'RSI', 'MACD', 'MACD_signal']])