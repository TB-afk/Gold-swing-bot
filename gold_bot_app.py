import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# تحميل البيانات من yfinance
df = yf.download('GC=F', period='6mo', interval='1d')

# التأكد من عدم وجود بيانات ناقصة
df.dropna(inplace=True)

# إنشاء أعمدة فنية بسيطة (مؤشرات)
df['SMA_5'] = df['Close'].rolling(window=5).mean()
df['SMA_10'] = df['Close'].rolling(window=10).mean()
df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)

# تنظيف البيانات
df.dropna(inplace=True)  # للتأكد من عدم وجود NaN

# اختيار الأعمدة للمدخلات والمخرجات
X = df[['SMA_5', 'SMA_10']]
y = df['Target']

# التحقق من التناسق
X = X.select_dtypes(include=[np.number])
y = y[:len(X)]

# تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# تدريب النموذج
model = RandomForestClassifier()
model.fit(X_train, y_train)

# التنبؤ
prediction = model.predict(X_test)

# الواجهة في Streamlit
st.title("📈 Gold Swing Bot")
st.write("نظام ذكي لتوقّع حركة الذهب بناءً على مؤشرات بسيطة (SMA)")

# عرض آخر البيانات والتوقّعات
st.subheader("آخر بيانات الذهب")
st.line_chart(df['Close'])

# زر للتوقّع
if st.button("تحليل السوق الآن"):
    current = df[['SMA_5', 'SMA_10']].iloc[-1:]
    result = model.predict(current)[0]
    if result == 1:
        st.success("✅ التوقع: السعر سيرتفع")
    else:
        st.error("❌ التوقع: السعر سينخفض")