import streamlit as st
from google import genai
import time

# تنظیمات اولیه صفحه
st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="centered")

st.title("🧠 اطلس مایند")
st.caption("فضایی امن، صمیمانه و بدون قضاوت برای گفتگو درباره روابط و سلامت روان")

# بررسی وجود کلید API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("لطفاً کلید GEMINI_API_KEY را در بخش Secrets اضافه کنید.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# دستورالعمل بالینی و لحن هوش مصنوعی
SYSTEM_PROMPT = """
تو «اطلس مایند» هستی؛ یک روانشناس بالینی و زوج‌درمانگر بسیار صمیمی، آرام، همدل و با تجربه.
پاسخ‌های تو باید کاملاً انسانی، عاطفی و بدون لحن رباتیک یا خشک باشد.

قوانین گفتگو:
۱. در اولین واکنش، احساسات مراجع را تایید و با او همدلی کن (Validation).
۲. از کلمات پیچیده کتابی، نصیحت کردن یا راهکار دادن سریع خودداری کن.
۳. پاسخ‌ها کوتاه (۲ تا ۴ جمله) باشد.
۴. در پایان هر پاسخ فقط یک سوال باز جهت ارزیابی عمیق‌تر احساسات بپرس.
"""

# راه‌اندازی کلاینت جدید گوگل
client = genai.Client(api_key=api_key)

# لیست مدل‌ها به ترتیب اولویت (در صورت شلوغی سرور، مدل بعدی تست می‌شود)
MODELS_TO_TRY = ['gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']

def generate_response_with_retry(prompt):
    for model_name in MODELS_TO_TRY:
        # ۳ بار تلاش برای هر مدل در صورت شلوغی سرور
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={'system_instruction': SYSTEM_PROMPT}
                )
                return response.text
            except Exception as e:
                # اگر خطای شلوغی سرور (503) بود، چند ثانیه صبر کن و دوباره بزن
                if "503" in str(e) or "high demand" in str(e).lower():
                    time.sleep(2)  # ۲ ثانیه صبر
                    continue
                else:
                    # اگر خطای دیگری بود برو سراغ مدل بعدی
                    break
    raise Exception("سرورهای گوگل در حال حاضر بسیار شلوغ هستند. لطفاً چند لحظه بعد دوباره پیام دهید.")

# مدیریت حافظه چت
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام، خوش اومدید. من اینجام تا در یک فضای کاملاً امن و محرمانه، بدون هیچ قضاوت یا تعارفی به حرفاتون گوش بدم.\n\nدوست داری از کجای رابطه‌تون یا دغدغه‌ای که الان داری شروع کنیم؟"}
    ]

# نمایش پیام‌های قبلی
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# دریافت ورودی مراجع و پاسخ‌دهی
if prompt := st.chat_input("هر چی توی دلت هست رو اینجا بنویس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("در حال فکر کردن..."):
            try:
                reply_text = generate_response_with_retry(prompt)
                st.markdown(reply_text)
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            except Exception as e:
                st.error(f"خطا: {e}")
                
