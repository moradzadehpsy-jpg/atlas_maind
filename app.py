import streamlit as st
from google import genai

# ۱. تنظیمات صفحه
st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="centered")

st.title("🧠 اطلس مایند")
st.caption("فضایی امن، صمیمانه و بدون قضاوت برای گفتگو درباره روابط و سلامت جنسی")

# ۲. بررسی کلید API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("لطفاً کلید GEMINI_API_KEY را در بخش Secrets اضافه کنید.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# ۳. طراحی پرامپت با تاکید ویژه بر لحن انسانی و روانشناختی
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

# ۴. راه‌اندازی کلاینت جدید گوگل
client = genai.Client(api_key=api_key)

# ۵. مدیریت حافظه چت
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام، خوش اومدید. من اینجام تا در یک فضای کاملاً امن و محرمانه، بدون هیچ قضاوت یا تعارفی به حرفاتون گوش بدم.\n\nدوست داری از کجای رابطه‌تون یا دغدغه‌ای که الان داری شروع کنیم؟"}
    ]

# ۶. نمایش پیام‌ها
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ۷. دریافت ورودی و ارسال پاسخ
if prompt := st.chat_input("هر چی توی دلت هست رو اینجا بنویس..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("در حال نوشتن پاسخ..."):
            try:
                # بازسازی تاریخچه گفتگو برای مدل
                contents_history = []
                for m in st.session_state.messages:
                    contents_history.append({"role": m["role"], "parts": [{"text": m["content"]}]})

                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=contents_history,
                    config={'system_instruction': HUMANIZED_CLINICAL_PROMPT}
                )

                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطا در دریافت پاسخ: {e}")
                
