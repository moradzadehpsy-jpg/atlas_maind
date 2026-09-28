import streamlit as st
from google import genai
import time

st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="centered")

st.title("🧠 پلتفرم هوشمند اطلس مایند")
st.caption("همراه هوشمند و ارزیابی اختصاصی روابط زوجین")

# بررسی وجود کلید در Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("لطفاً کلید API را در بخش Secrets در Streamlit وارد کنید.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام، خوش آمدید. من اینجا هستم تا بدون هیچ قضاوت یا محدودیتی شنونده شما باشم.\n\nچه دغدغه یا مشکلی در رابطه عاطفی یا جنسی خود احساس می‌کنید؟"}
    ]

# نمایش تاریخچه پیام‌ها
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# دریافت ورودی کاربر
if prompt := st.chat_input("پاسخ خود را بنویسید..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("در حال تحلیل و پاسخگویی..."):
            system_prompt = "تو یک روانشناس بالینی متخصص زوج‌درمانی و سلامت جنسی هستی. پاسخ‌های تو باید کاملاً همدلانه، صمیمی، بدون قضاوت و کوتاه (حدود ۲ تا ۳ جمله) باشد. در پایان هر پاسخ فقط یک سوال باز جهت ارزیابی عمیق‌تر بپرس."
            
            # تلاش مجدد هوشمند در صورت شلوغی سرور
            success = False
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                        config={'system_instruction': system_prompt}
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except Exception as e:
                    time.sleep(2) # ۲ ثانیه صبر برای تلاش مجدد
            
            if not success:
                st.error("سرورها در حال حاضر شلوغ هستند، لطفاً چند لحظه بعد دوباره پیام بفرستید.")
