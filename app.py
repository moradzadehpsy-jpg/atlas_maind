import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="اطلس مایند | چت اختصاصی", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stChatMessage { text-align: right; direction: rtl; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 اطلس مایند | مصاحبه بالینی هوشمند")
st.caption("مصاحبه تطبیقی و همدلانه جهت تحلیل الگوهای ارتباطی و ساخت اثر انگشت جنسی")

# مقداردهی اولیه تاریخچه چت
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام، خوش آمدید. من اینجا هستم تا بدون هیچ قضاوت یا محدودیتی شنونده شما باشم.\n\nچه دغدغه یا مشکلی در رابطه عاطفی یا جنسی خود احساس می‌کنید؟ هر طور راحت هستید برام بنویسید."}
    ]

# نمایش پیام‌های قبلی چت
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# دریافت پاسخ مراجع
if prompt := st.chat_input("پاسخ خود را اینجا بنویسید..."):
    # افزودن پاسخ مراجع به چت
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # شبیه‌سازی منطق تحلیل همدلانه و سوال باز بعدی توسط AI
    user_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    
    if user_count == 1:
        ai_response = (
            "متوجه فشار و حس خستگی سنگینی که تحمل می‌کنید هستم... اینکه با وجود تمام این سختی‌ها مایلید درباره‌اش صحبت کنید، نشان‌دهنده اهمیت و ارزش این رابطه برای شماست.\n\n"
            "برای اینکه ابعاد بیشتری از این الگو را شفاف کنیم: **وقتی در برابر خواسته یا رفتار همسرتان حس خشم یا انزجار سراغتان می‌آید، در آن لحظه دقیقاً چه فکر یا صدایی در ذهنتان می‌پیچد؟**"
        )
    elif user_count == 2:
        ai_response = (
            "این حس بد نسبت به خودتان و داد زدن، در واقع یک «سپر دفاعی کاملاً طبیعی» برای حفاظت از مرزهای آسیب‌دیده‌تان است، نه یک رفتار بی‌دلیل.\n\n"
            "دوست دارم کمی عمیق‌تر شویم: **وقتی این خشم فروکش می‌کند، رابطه عاطفی و گفتگوهای غیرجنسی شما به چه شکلی درمی‌آید؟ آیا فضای صمیمیت هم قفل می‌شود؟**"
        )
    else:
        ai_response = (
            "ممنون از پاسخ‌های شفاف و شجاعانه‌تان. تا این مرحله الگوی اصلی ارتباطی شما استخراج شد.\n\n"
            "اکنون شناسنامه بصری **«اثر انگشت جنسی»** شما آماده است و می‌توانید بسته خودیاری اختصاصی‌تان را مشاهده کنید."
        )

    # افزودن پاسخ AI به چت
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    # نمایش اثر انگشت جنسی در انتهای مصاحبه
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
            st.caption("🎧 پادکست ۱: «رهایی از سرزنش خود و خشم ناگهانی»")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            
