import streamlit as st
import pandas as pd
import yfinance as yf
import ta
import plotly.graph_objs as go
# 🪙 عنوان التطبيق
st.set_page_config(page_title="توقعات سعر الذهب", layout="wide")
st.title(":moneybag: Gold Swing Bot")
st.subheader(":mag: تحليل ذكي لحركة الذهب باستخدام المؤشرات الفنية")

# 📈 جلب البيانات
@st.cache_data
def load_data():
    df = yf.download('GC=F', period='6mo', interval='1d')
    df.dropna(inplace=True)
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close']).rsi()
    macd = ta.trend.MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    return df

df = load_data()

# 🌍 معلومات الرسم البياني
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             name='Candlestick'))
fig.add_trace(go.Scatter(x=df.index, y=df['SMA_10'], line=dict(color='blue', width=1), name='SMA 10'))
fig.update_layout(title='رسم شموع للذهب + متوسط 10 أيام', xaxis_title='Date', yaxis_title='Price', template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

# نستعرض المؤشرات
st.subheader("🔢 مؤشرات فنية")
st.line_chart(df[['RSI', 'MACD', 'MACD_signal']])

# توقع بسيط مبني على قيم مؤشرات
last_rsi = df['RSI'].iloc[-1]
last_macd = df['MACD'].iloc[-1]
last_signal = df['MACD_signal'].iloc[-1]

st.subheader(":crystal_ball: توقع")
if last_rsi < 30 and last_macd > last_signal:
    st.success("احتمال الصعود عالي الفرص")
elif last_rsi > 70 and last_macd < last_signal:
    st.error("احتمال الهبوط وارد")
else:
    st.info("حركة افقية أو غير واضحة")