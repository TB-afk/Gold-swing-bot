import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import ta

# إعداد الواجهة
st.set_page_config(page_title="Gold Swing Bot", layout="wide")

st.markdown("<h1 style='text-align: center; color: gold;'>🪙 Gold Swing Bot</h1>", unsafe_allow_html=True)
st.markdown("### 🔍 تحليل ذكي لحركة الذهب باستخدام المؤشرات الفنية ونموذج التعلم الآلي")

# تحميل البيانات
df = yf.download('GC=F', period='6mo', interval='1d')
df.dropna(inplace=True)

# المؤشرات الفنية
df['SMA_5'] = df['Close'].rolling(window=5).mean()
df['SMA_10'] = df['Close'].rolling(window=10).mean()

# RSI وMACD
df['RSI'] = 
ta.momentum.RSIIndicator(close=df['Close']).rsi()
macd = ta.trend.MACD(close=df['Close'])
df['MACD'] = macd.macd()
df['MACD_signal'] = macd.macd_signal()

# الهدف للتعلم الآلي
df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
df.dropna(inplace=True)

# المتغيرات
features = ['SMA_5', 'SMA_10', 'RSI', 'MACD', 'MACD_signal']
X = df[features]
y = df['Target']

# تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

# واجهة الشموع
st.subheader("📈 مخطط الشموع لسعر الذهب")
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    increasing_line_color='green',
    decreasing_line_color='red'
)])
fig.update_layout(height=400, xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# عرض المؤشرات
with st.expander("📘 المؤشرات الفنية المستخدمة"):
    st.markdown("""
    - **SMA 5 و 10**: المتوسطات المتحركة
    - **RSI**: مؤشر القوة النسبية لتحديد التشبع الشرائي أو البيعي
    - **MACD**: تقاطع المتوسطات لتحديد الاتجاهات
    """)

# زر التوقع
if st.button("🔍 تحليل وتوقع الآن"):
    latest = df[features].iloc[-1:]
    pred = model.predict(latest)[0]
    prob = model.predict_proba(latest)[0][pred] * 100

    if pred == 1:
        st.success(f"🔼 التوقع: السعر سيرتفع\n\n🎯 نسبة الثقة: {prob:.2f}%")
    else:
        st.error(f"🔽 التوقع: السعر سينخفض\n\n🎯 نسبة الثقة: {prob:.2f}%")

    st.metric("📊 دقة النموذج", f"{accuracy * 100:.2f}%")

# عرض بيانات توقعات سابقة
with st.expander("📜 سجل التوقعات السابقة"):
    df_copy = df.copy()
    df_copy['توقع'] = model.predict(df[features])
    df_copy['تطابق'] = np.where(df_copy['توقع'] == df_copy['Target'], "✔️", "❌")
    st.dataframe(df_copy[['Close', 'توقع', 'Target', 'تطابق']].tail(15))