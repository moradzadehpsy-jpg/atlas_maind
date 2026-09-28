import streamlit as st
import google.generativeai as genai

# ۱. تنظیمات صفحه
st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stTextInput>div>div>input { text-align: right; }
    .stTextArea>div>div>textarea { text-align: right; }
    </style>
""", unsafe_style_modal=True)

st.title("🧠 پلتفرم هوشمند اطلس مایند")
st.caption("همراه هوشمند و ارزیابی اختصاصی روابط زوجین و سلامت جنسی")

# ۲. فراخوانی کلید API از Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("لطفاً کلید GEMINI_API_KEY را در بخش Secrets تعریف کنید.")
    st.stop()

# ۳. مدیریت حافظه گفتگو
if "messages" not in st.session_state:
    st.session_state.messages = []
    # دستورالعمل بالینی اولیه برای هوش مصنوعی
    system_prompt = """
    تو یک روانشناس بالینی، متخصص روابط زوجین و سلامت جنسی با زبان بسیار ساده، روان و همدلانه هستی.
    نام تو «اطلس مایند» است.
    وظیفه داری با مراجع کاملاً بدون قضاوت، صمیمی و آرام صحبت کنی. 
    از به‌کار بردن اصطلاحات پیچیده پزشکی یا بالینی خودداری کن. 
    در هر پیام فقط یک سوال باز و عمیق بپرس تا مراجع احساس فشار نکند.
    """
    st.session_state.chat = model.start_chat(history=[])
    # ارسال دستورالعمل ساختاری به عنوان پیام اول
    st.session_state.chat.send_message(system_prompt)

# ۴. نمایش پیام‌های قبلی
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ۵. دریافت پیام جدید از مراجع
if prompt := st.chat_input("پاسخ یا دغدغه خود را اینجا بنویسید..."):
    # نمایش پیام مراجع
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # دریافت و نمایش پاسخ هوش مصنوعی
    with st.chat_message("assistant"):
        with st.spinner("در حال نوشتن پاسخ..."):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
