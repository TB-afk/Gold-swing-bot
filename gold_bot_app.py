import yfinance as yf
import pandas as pd
import streamlit as st
from ta.trend import MACD
from ta.momentum import RSIIndicator
import plotly.graph_objects as go

st.set_page_config(page_title="🪙 Gold Swing Bot", layout="centered")

st.title("🪙 Gold Swing Bot")
st.markdown("### 🔍 تحليل ذكي لحركة الذهب باستخدام المؤشرات الفنية ونموذج التعلم الآلي")

# تحميل بيانات الذهب من Yahoo Finance
df = yf.download('GC=F', period='6mo', interval='1d')
# التأكد من وجود البيانات
if df.empty:
    st.error("فشل تحميل بيانات الذهب.")
    st.stop()

# حساب SMA لمدة 10 أيام
df['SMA_10'] = df['Close'].rolling(window=10).mean()

# حساب مؤشر القوة النسبية RSI
rsi = RSIIndicator(close=df['Close'])
df['RSI'] = rsi.rsi()

# حساب مؤشر MACD
macd = MACD(close=df['Close'])
df['MACD'] = macd.macd().squeeze()
df['MACD_signal'] = macd.macd_signal().squeeze()

# عرض مخطط الشموع اليابانية لآخر 10 أيام
latest_data = df.tail(10)
fig = go.Figure(data=[go.Candlestick(
    x=latest_data.index,
    open=latest_data['Open'],
    high=latest_data['High'],
    low=latest_data['Low'],
    close=latest_data['Close']
)])
fig.update_layout(title='📊 رسم شموع الذهب - آخر 10 أيام', xaxis_title='التاريخ', yaxis_title='السعر')
st.plotly_chart(fig)

# عرض جدول المؤشرات
with st.expander("📈 المؤشرات الفنية"):
    st.dataframe(df.tail(10)[['Close', 'SMA_10', 'RSI', 'MACD', 'MACD_signal']])