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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام، خوش آمدید. من اینجا هستم تا بدون هیچ قضاوت یا محدودیتی شنونده شما باشیم.\n\nچه دغدغه یا مشکلی در رابطه عاطفی یا جنسی خود احساس می‌کنید؟ هر طور راحت هستید برام بنویسید."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("پاسخ خود را اینجا بنویسید..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    
    if user_count == 1:
        # پاسخی که کلمات مراجع را نشانه می‌رود بدون فرض حس‌های دیگر
        ai_response = (
            f"متوجه هستم... تجربه سردی در رابطه و اختلافاتی که به دنبالش ایجاد میشه، احساس کلافگی زیادی به همراه داره.\n\n"
            f"برای اینکه بهتر شرایط رو درک کنم: **وقتی حس می‌کنید این سردی بین شما پیش اومده، واکنش همسرتان در برابرش چیه و چطور درباره‌اش صحبت می‌کنید؟**"
        )
    elif user_count == 2:
        ai_response = (
            "ممنون از توضیحتان. برای اینکه الگوی ارتباطی‌تان دقیق‌تر مشخص شود:\n\n"
            "**این سردی و فاصله‌ای که ایجاد شده، بیشتر روی بخش صمیمیت و رابطه جنسی اثر گذاشته، یا اینکه رفتارهای عاطفی و گفتگوهای روزمره‌تان هم دچار تغییر شده؟**"
        )
    else:
        ai_response = (
            "ممنون از پاسخ‌های شفاف شما. اطلاعات لازم برای تحلیل الگوی شما ثبت شد.\n\n"
            "شناسنامه بصری **«اثر انگشت جنسی»** شما در ادامه آماده مشاهده است."
        )

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)

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
            st.caption("🎧 پادکست ۱: «درک الگوهای سردی و صمیمیت در رابطه»")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            
