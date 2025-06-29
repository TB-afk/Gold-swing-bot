import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

st.title("📈 توقع سعر الذهب - Gold Swing Bot")


data = yf.download("XAUUSD=X", period="90d", interval="1d")
data['Target'] =data['Close'].shift(-1) > data['Close']
data.dropna(inplace=True)


X = data[['Open', 'High', 'Low', 'Close', 'Volume']]
y = data['Target']
model = RandomForestClassifier()
model.fit(X, y)


latest = X.iloc[-1:]
prediction = model.predict(latest)[0]
result = "📉 هبوط متوقع" if not prediction else "📈 صعود متوقع"

st.subheader("🔮 توقع:")
st.success(result)


st.subheader("📊 حركة السعر")
fig, ax = plt.subplots()
ax.plot(data['Close'], label="السعر")
ax.set_title("سعر الذهب آخر 90 يوم")
ax.legend()
st.pyplot(fig)