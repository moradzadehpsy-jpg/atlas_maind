import streamlit as st
import google.generativeai as genai
import numpy as np
import matplotlib.pyplot as plt

# تنظیمات کلید API
API_KEY = "AQ.Ab8RN6LMAHhN8qtYAgijv7EgRlUjs_aqRGEt2wJsJVmO0cZwag"
genai.configure(api_key=API_KEY)

# ساخت مدل هوش مصنوعی با دستورالعمل بالینی (System Instruction)
system_prompt = """
تو یک روانشناس بالینی متخصص در حوزه اختلالات جنسی و زوج‌درمانی هستی. 
وظیفه تو مدیریت یک مصاحبه بالینی کوتاه، همدلانه و دقیق برای پلتفرم «اطلس مایند» است.

قوانین مهم:
۱. فقط و فقط بر اساس کلمات و اظهارات خود مراجع صحبت کن. هیچ فرض، حس، یا برچسبی (مثل خشم، انزجار، خیانت و...) که مراجع مستقیماً به آن اشاره نکرده را به او نسبت نده.
۲. لحن تو باید کاملاً همدلانه، بدون قضاوت، حرفه‌ای و کوتاه باشد (حداکثر ۲ تا ۳ جمله).
۳. در هر مرحله پس از انعکاس همدلانه، فقط یک سوال شفاف و عمیق برای شفاف‌تر شدن الگوهای ارتباطی یا جنسی بپرس.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

st.set_page_config(page_title="اطلس مایند | مصاحبه بالینی هوشمند", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 اطلس مایند | مصاحبه بالینی هوشمند")
st.caption("ارزیابی تخصصی و پویا جهت تحلیل الگوهای ارتباطی و ساخت اثر انگشت جنسی")

# مقداردهی حافظه چت
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    initial_msg = "سلام، خوش آمدید. من اینجا هستم تا بدون هیچ قضاوت یا محدودیتی شنونده شما باشم.\n\nچه دغدغه یا مشکلی در رابطه عاطفی یا جنسی خود احساس می‌کنید؟ هر طور راحت هستید برام بنویسید."
    st.session_state.messages = [{"role": "assistant", "content": initial_msg}]

# نمایش پیام‌های قبلی
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# دریافت ورودی مراجع
if prompt := st.chat_input("پاسخ خود را اینجا بنویسید..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ارسال به هوش مصنوعی و دریافت پاسخ پویا
    try:
        response = st.session_state.chat_session.send_message(prompt)
        ai_response = response.text
    except Exception as e:
        ai_response = "خطا در برقراری ارتباط با مدل هوش مصنوعی. لطفاً دوباره تلاش کنید."

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    # نمایش اثر انگشت جنسی پس از چند قدم مصاحبه
    user_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    if user_count >= 3:
        st.divider()
        st.subheader("📊 اثر انگشت جنسی و بسته خودیاری اختصاصی شما")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            categories = ['دلبستگی ایمن', 'شفقت به خود', 'ابراز صمیمیت', 'امنیت بدنی', 'انعطاف شناختی']
            values = [35, 25, 30, 45, 50]
            
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            values += values[:1]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
            ax.fill(angles, values, color='#8B5CF6', alpha=0.4)
            ax.plot(angles, values, color='#6D28D9', linewidth=2)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, fontsize=9)
            st.pyplot(fig)
            
        with col2:
            st.write("**بسته تمرینات خودیاری و پیگیری:**")
            st.caption("🎧 پادکست ۱: «درک الگوهای صمیمیت در رابطه»")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
