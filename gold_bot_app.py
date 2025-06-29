import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

st.title("📈 توقع سعر الذهب - Gold Swing Bot")

# تحميل بيانات الذهب
data = yf.download("XAUUSD=X", period="90d", interval="1d")
data['Target'] = data['Close'].shift(-1) > data['Close']

# حذف الصفوف التي فيها بيانات ناقصة
data.dropna(inplace=True)

# تجهيز البيانات
X = data[['Open', 'High', 'Low', 'Close', 'Volume']]
y = data['Target']

# حذف أي صفوف ناقصة (احتياط)
X = X.dropna()
y = y.loc[X.index]

# تدريب النموذج
model = RandomForestClassifier()
model.fit(X, y)

# توقع اليوم
latest = X.iloc[-1:]
prediction = model.predict(latest)[0]
result = "📉 هبوط متوقع" if not prediction else "📈 صعود متوقع"

st.subheader("🔮 توقع:")
st.success(result)

# رسم السعر
st.subheader("📊 حركة السعر")
fig, ax = plt.subplots()
ax.plot(data['Close'], label="السعر")
ax.set_title("سعر الذهب آخر 90 يوم")
ax.legend()
st.pyplot(fig)