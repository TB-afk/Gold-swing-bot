import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Gold Swing Bot", page_icon="📈")
st.title("📊 Gold Swing Bot")
st.write("نظام ذكي لتوقع حركة الذهب بناءً على نماذج تحليلية.")

# تحميل بيانات الذهب
data = yf.download("XAUUSD=X", period="60d", interval="1d")

# إزالة الصفوف اللي فيها قيم ناقصة
data = data.dropna()

# حذف عمود Volume لأنه غالبًا فيه مشاكل
if 'Volume' in data.columns:
    data = data.drop(columns=['Volume'])

# إنشاء عمود الهدف
data['Target'] = data['Close'].shift(-1) > data['Close']
data = data.dropna()

# تحديد الميزات
features = ['Open', 'High', 'Low', 'Close']
X = data[features]
y = data['Target']

# تأكد أن البيانات أرقام فقط
X = X.apply(pd.to_numeric, errors='coerce')
X = X.dropna()
y = y.loc[X.index]

# تدريب النموذج
model = RandomForestClassifier()
model.fit(X, y)

# التوقع باستخدام آخر صف
latest_data = X.iloc[-1:]
prediction = model.predict(latest_data)[0]

# عرض النتيجة
st.subheader("🔮 التوقع:")
if prediction:
    st.success("📈 من المتوقع صعود الذهب خلال اليوم القادم.")
else:
    st.error("📉 من المتوقع هبوط الذهب خلال اليوم القادم.")

st.caption("جميع الحقوق محفوظة © 2025")