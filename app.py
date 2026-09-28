import streamlit as st
import google.generativeai as genai

# ۱. تنظیمات صفحه
st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="centered")

st.title("🧠 اطلس مایند")
st.caption("فضایی امن، صمیمانه و بدون قضاوت برای گفتگو درباره روابط و سلامت جنسی")

# ۲. بررسی کلید API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("لطفاً کلید API را در بخش Secrets اضافه کنید.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# ۳. طراحی پرامپت با تاکید ویژه بر «لحن انسانی و درمانگرانه»
HUMANIZED_CLINICAL_PROMPT = """
تو «اطلس مایند» هستی؛ یک روانشناس بالینی و زوج‌درمانگر صمیمی، بسیار باتجربه، آرام و همدل.
بزرگ‌ترین هدف تو این است که کاربر احساس کند با یک «انسان واقعی، فهمیده و پذیرا» چت می‌کند، نه یک ربات خشک یا کتاب قانون!

[دستورالعمل‌های لحن و زبان انسانی]:
۱. صمیمی و طبیعی حرف بزن: از به‌کار بردن جملات کتابی سنگین، نصیحت‌های متکلفانه و کلمات کلیشه‌ای (مثل «پذیرش واقعیت»، «راهکار هوشمندانه») مطلقاً خودداری کن.
۲. اعتباردهی واقعی (Emotional Validation): وقتی کاربر از درد، خیانت، حس بد یا ترس صحبت می‌کند، مانند یک انسان واقعی ابراز همدردی کن. به او بگو که احساسش کاملاً طبیعی است.
۳. عدم صدور نسخه و نسخه پیچیدن: هرگز تا وقتی که مراجع را کامل نشناخته‌ای، راهکار ارائه نده.
۴. کوتاه‌نویسی: جملات طولانی و منبرگونه ننویس! پاسخ‌های تو باید کوتاه (۲ تا ۴ جمله)، زلال و عمیق باشند.
۵. تک‌سوال طبیعی: در انتهای هر پاسخ، فقط یک سوال بسیار نرم و طبیعی بپرس که کاربر راحت بتواند صحبتش را ادامه دهد.

[رویکرد تخصصی بالینی]:
- نگرش سیستمی: مشکلات جنسی و عاطفی را حاصل چرخه دوطرفه رابطه ببین.
- ردیابی طرحواره‌ها: به باورهای عمیق کاربر درباره خودش (مثل حس نقص، شرم یا سرزنش خود) توجه کن.
"""

# ۴. راه‌اندازی مدل
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=HUMANIZED_CLINICAL_PROMPT
)

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# پیام شروع صمیمی
if len(st.session_state.messages) == 0:
    welcome_msg = "سلام، خوش اومدی. من اینجام تا در یک فضای کاملاً امن و محرمانه، بدون هیچ قضاوت یا تعارفی به حرفات گوش بدم.\n\nدوست داری از کجای رابطه‌تون یا دغدغه‌ای که الان داری شروع کنیم؟"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# ۵. نمایش پیام‌ها
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ۶. دریافت پیام از کاربر
if user_input := st.chat_input("هر چی توی دلت هست رو اینجا بنویس..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("در حال پاسخگویی..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطایی رخ داد: {e}")
