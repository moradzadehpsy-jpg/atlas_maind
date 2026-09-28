import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="اطلس مایند | Mind Atlas", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    .stButton>button { background-color: #4A154B; color: white; border-radius: 8px; width: 100%; }
    .stTextInput>div>div>input { text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 پلتفرم هوشمند اطلس مایند (Mind Atlas)")
st.caption("شناسنامه اختصاصی اثر انگشت جنسی و همراه هوشمند خودیاری زوجین")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}

if st.session_state.step == 1:
    st.subheader("سلام، خوش آمدید. ما اینجا هستیم تا بدون هیچ قضاوتی شنونده شما باشیم.")
    complaint = st.text_area("چه دغدغه یا مشکلی در رابطه عاطفی یا جنسی خود احساس می‌کنید؟", 
                             placeholder="مثلاً: مدتی است نسبت به همسرم حس و تمایلی ندارم...")
    
    if st.button("ادامه و شروع ارزیابی اختصاصی"):
        if complaint.strip():
            st.session_state.answers['chief_complaint'] = complaint
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("لطفاً ابتدا دغدغه اصلی خود را کوتاه بنویسید.")

elif st.session_state.step == 2:
    st.subheader("ارزیابی عمیق‌تر الگوی ارتباطی")
    st.info("پاسخ‌های شما کاملاً محرمانه نگه داشته می‌شوند.")
    
    q1 = st.radio("وقتی بین شما و همسرتان سردی یا مشکلی پیش می‌آید، معمولاً کدام رفتار رخ می‌دهد؟",
                  ["من سکوت می‌کنم و عقب می‌کشم، ولی همسرم بحث را ادامه می‌دهد.",
                   "همسرم سکوت می‌کند و من اصرار به صحبت و حل آن دارم.",
                   "هر دو عصبانی می‌شویم و بحث شدید پیش می‌آید.",
                   "هیچ‌کدام حرفی نمی‌زنیم و فقط فاصله می‌گیریم."])
    
    q2 = st.text_area("در صورت پیشنهاد صمیمیت از طرف همسرتان، چه حس یا فکری سراغتان می‌آید؟",
                      placeholder="مثلاً: احساس خستگی، احساس اجبار یا خشم...")
    
    if st.button("تحلیل و ساخت اثر انگشت جنسی"):
        st.session_state.answers['q1'] = q1
        st.session_state.answers['q2'] = q2
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.success("ارزیابی شما با موفقیت انجام شد!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("اثر انگشت جنسی اختصاصی شما")
        categories = ['دلبستگی ایمن', 'شفقت به خود', 'ابراز صمیمیت', 'امنیت بدنی', 'انعطاف شناختی']
        values = [40, 30, 25, 50, 45]
        
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
        st.subheader("بسته خودیاری اختصاصی شما")
        st.write("بر اساس شناسنامه شما، این راهکارهای ویژه آماده شده است:")
        
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.caption("🎧 پادکست ۵ دقیقه‌ای: «آرامش بدنی و رهایی از سرزنش خود»")
        
        st.download_button("📖 دانلود کتابچه راهنمای اختصاصی (PDF)", 
                           data="محتوای کتابچه خودیاری...", 
                           file_name="Self_Help_Guide.txt")
        
        if st.button("شروع مجدد ارزیابی"):
            st.session_state.step = 1
            st.rerun()
            
