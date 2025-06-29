import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble 
import 
RandomForestClassifier

st.set_page_config(page_title="Gold Swing Bot", page_icon="📈")
st.title("📊 Gold Swing Bot")
st.write("نظام ذكي لتوقع حركة الذهب بناءً على نماذج تحليلية.")

# تحميل بيانات الذهب (بدون إظهار التفاصيل)
data = yf.download("XAUUSD=X", period="60d", interval="1d")

# إنشاء الهدف
data['Target'] = data['Close'].shift(-1) > data['Close']
data.dropna(inplace=True)

# تجهيز المدخلات للنموذج (نخفي التفاصيل)
features = ['Open', 'High', 'Low', 'Close', 'Volume']
X = data[features].dropna()
y = data['Target'].loc[X.index]

# تدريب نموذج التوقع (بدون ذكر اسمه)
model = RandomForestClassifier()
model.fit(X, y)

# استخدام آخر بيانات للتوقع
latest_data = X.iloc[-1:]
prediction = model.predict(latest_data)[0]

# عرض النتيجة فقط
st.subheader("🔮 التوقع:")
if prediction:
    st.success("📈 من المتوقع صعود الذهب خلال اليوم القادم.")
else:
    st.error("📉 من المتوقع هبوط الذهب خلال اليوم القادم.")

# بدون عرض الرسم البياني ولا الكود ولا المصدر
st.caption("جميع الحقوق محفوظة © 2025")