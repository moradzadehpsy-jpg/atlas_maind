import streamlit as st
from google import genai

# ۱. تنظیمات اولیه صفحه
st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="centered")

st.title("🧠 اطلس مایند")
st.caption("فضایی امن، صمیمانه و بدون قضاوت برای گفتگو درباره روابط و سلامت روان")

# ۲. بررسی وجود کلید API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("لطفاً کلید GEMINI_API_KEY را در بخش Secrets اضافه کنید.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# ۳. دستورالعمل بالینی و لحن هوش مصنوعی
SYSTEM_PROMPT = """
تو «اطلس مایند» هستی؛ یک روانشناس بالینی و زوج‌درمانگر بسیار صمیمی، آرام، همدل و با تجربه.
پاسخ‌های تو باید کاملاً انسانی، عاطفی و بدون لحن رباتیک یا خشک باشد.

قوانین گفتگو:
۱. در اولین واکنش، احساسات مراجع را تایید و با او همدلی کن (Emotional Validation).
۲. از کلمات پیچیده کتابی یا نصیحت کردن خودداری کن.
۳. پاسخ‌ها کوتاه (۲ تا ۴ جمله) باشد.
۴. در پایان هر پاسخ فقط یک سوال باز جهت ردیابی طرحواره‌ها و الگوهای ارتباطی بپرس.
"""

# ۴. راه‌اندازی کلاینت گوگل
client = genai.Client(api_key=api_key)

# ۵. مدیریت حافظه چت
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام، خوش اومدید. من اینجام تا در یک فضای کاملاً امن و محرمانه، بدون هیچ قضاوت یا تعارفی به حرفاتون گوش بدم.\n\nدوست داری از کجای رابطه‌تون یا دغدغه‌ای که الان داری شروع کنیم؟"}
    ]

# ۶. نمایش پیام‌های قبلی
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ۷. دریافت ورودی مراجع و پاسخ‌دهی
if prompt := st.chat_input("هر چی توی دلت هست رو اینجا بنویس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("در حال فکر کردن..."):
            try:
                # تبدیل تاریخچه برای ارسال به مدل
                contents_history = []
                for m in st.session_state.messages:
                    contents_history.append({"role": m["role"], "parts": [{"text": m["content"]}]})

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents_history,
                    config={'system_instruction': SYSTEM_PROMPT}
                )

                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطا در دریافت پاسخ: {e}")
                
