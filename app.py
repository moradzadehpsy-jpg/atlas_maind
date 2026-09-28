import streamlit as st
import requests

st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="centered")

st.title("🧠 پلتفرم هوشمند اطلس مایند")
st.caption("همراه هوشمند و ارزیابی اختصاصی روابط زوجین")

# بررسی وجود کلید API
if "OPENROUTER_API_KEY" not in st.secrets:
    st.error("لطفاً کلید OPENROUTER_API_KEY را در بخش Secrets تنظیم کنید.")
    st.stop()

api_key = st.secrets["OPENROUTER_API_KEY"]

# مقداردهی اولیه پیام‌ها
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام، خوش آمدید. من اینجا هستم تا بدون هیچ قضاوت یا محدودیتی شنونده شما باشم.\n\nچه دغدغه یا مشکلی در رابطه عاطفی یا جنسی خود احساس می‌کنید؟"}
    ]

# نمایش تاریخچه گفتگو
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
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            # آماده‌سازی پرامپت‌ها
            api_messages = [{"role": "system", "content": system_prompt}]
            for m in st.session_state.messages:
                api_messages.append({"role": m["role"], "content": m["content"]})

            payload = {
                "model": "deepseek/deepseek-chat:free", # استفاده از مدل رایگان و فوق‌العاده سریع DeepSeek
                "messages": api_messages
            }

            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    bot_reply = result['choices'][0]['message']['content']
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    st.error(f"خطای ارتباطی سرور: {response.status_code}. لطفاً مجدداً تلاش کنید.")
            except Exception as e:
                st.error(f"خطا در ارسال درخواست: {e}")
