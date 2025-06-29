import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Gold Swing Bot", page_icon="📈")
st.title("📊 Gold Swing Bot")
st.write("نظام ذكي لتوقع حركة الذهب بناءً على نماذج تحليلية.")

# تحميل بيانات الذهب
data = yf.download("XAUUSD=X", period="60d", interval="1d")

# حذف أي بيانات ناقصة
data.dropna(inplace=True)

# إنشاء الهدف (True لو أغلق السعر أعلى من اليوم السابق)
data['Target'] = data['Close'].shift(-1) > data['Close']
data.dropna(inplace=True)

# اختيار الخصائص - بدون Volume لأنها فاضية
features = ['Open', 'High', 'Low', 'Close']
X = data[features]
y = data['Target']

# تدريب النموذج
model = RandomForestClassifier()
model.fit(X, y)

# توقع على آخر صف
latest_data = X.iloc[-1:]
prediction = model.predict(latest_data)[0]

# عرض النتيجة
st.subheader("🔮 التوقع:")
if prediction:
    st.success("📈 من المتوقع صعود الذهب خلال اليوم القادم.")
else:
    st.error("📉 من المتوقع هبوط الذهب خلال اليوم القادم.")

st.caption("جميع الحقوق محفوظة © 2025")