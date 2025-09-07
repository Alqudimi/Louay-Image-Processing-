import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import cv2
import numpy as np
from PIL import Image
import io
import base64
import time
from streamlit_option_menu import option_menu
import os


# إعداد صفحة Streamlit
st.set_page_config(
    page_title="معالجة الصور التفاعلية",
    page_icon="🖼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# شعار أعلى الصفحة بشكل فخم
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@700&family=Tajawal:wght@500;700&display=swap" rel="stylesheet">
<style>
    .stApp {
        background: linear-gradient(120deg, #f8fafc 0%, #e0f7fa 100%);
        min-height: 100vh;
    }
    h1 {
        color: #1976d2;
        text-align: center;
        font-weight: 700;
        font-family: 'Cairo', 'Tajawal', Arial, sans-serif;
        font-size: 2.7rem;
        margin-top: 10px;
        margin-bottom: 0px;
        letter-spacing: 2px;
        text-shadow: 0 2px 8px #bbdefb;
    }
    h2, h3, h4 {
        color: #388e3c;
        font-family: 'Tajawal', 'Cairo', Arial, sans-serif;
        font-weight: 700;
        text-shadow: 0 1px 4px #c8e6c9;
    }
    body, .stApp, .stMarkdown, .stText, .stExpander, .stButton>button, .stCheckbox>label, .stTextInput>label {
        color: #111 !important;
        font-family: 'Tajawal', 'Cairo', Arial, sans-serif;
        font-size: 1.1rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff9800 0%, #1976d2 100%);
        color: #fff;
        border: none;
        padding: 14px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        margin: 12px 0px;
        cursor: pointer;
        border-radius: 16px;
        transition: background 0.3s, box-shadow 0.3s;
        box-shadow: 0 4px 16px rgba(38,166,154,0.12);
        font-family: 'Cairo', 'Tajawal', Arial, sans-serif;
        position: relative;
        right: 0;
        left: auto;
        float: right;
        clear: both;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #f57c00 0%, #1565c0 100%);
        box-shadow: 0 6px 24px rgba(38,166,154,0.18);
    }
    .stSlider>div>div>div {
        background: #1976d2;
    }
    .stCheckbox>label {
        color: #388e3c;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stTextInput>label {
        color: #1976d2;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .streamlit-expanderHeader {
        background-color: #bbdefb;
        color: #1976d2;
        font-weight: bold;
        font-size: 1.1rem;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .camera-container {
        border: 2px solid #1976d2;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 24px;
        background: linear-gradient(120deg, #e3f2fd 0%, #e8f5e9 100%);
        box-shadow: 0 2px 12px rgba(38,166,154,0.08);
    }
    .stImage>img {
        border-radius: 16px;
        box-shadow: 0 2px 12px #bbdefb;
        margin-bottom: 8px;
    }
    .stSidebar {
        background: linear-gradient(120deg, #bbdefb 0%, #c8e6c9 100%);
        border-radius: 0 16px 16px 0;
        box-shadow: 2px 0 12px #bbdefb;
    }
    .stMarkdown ul {
        background: #e3f2fd;
        border-radius: 8px;
        padding: 12px 18px;
        box-shadow: 0 1px 6px #bbdefb;
    }
    .stMarkdown li {
        margin-bottom: 8px;
        font-size: 1.1rem;
    }
</style>
<div style='text-align:center; margin-bottom:0px;'>
    <img src='https://i.imgur.com/2yaf2wb.png' width='120' style='margin-bottom:10px; box-shadow:0 2px 12px #bbdefb; border-radius:50%;'>
    <h1>🖼 معالجة الصور التفاعلية</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #1976d2; margin-top:0px; margin-bottom:16px;'>", unsafe_allow_html=True)

# تعريف فكرة المشروع في أعلى الصفحة
st.markdown("""
<div style='background:linear-gradient(90deg,#e0f7fa 0%,#b2dfdb 100%);border-radius:16px;padding:18px 24px;margin-bottom:18px;box-shadow:0 2px 8px #b2dfdb;'>
    <h2 style='color:#1976d2;margin-bottom:8px;'>مشروع: سلسلة محاضرات تفاعلية في معالجة الصور (Streamlit)</h2>
    <p style='color:#222;font-size:1.1rem;font-weight:bold;'>
    فكرة المشروع:<br>
    بناء تطبيق تعليمي باستخدام Streamlit يشرح أهم عمليات معالجة الصور.<br>
    كل محاضرة تتكوّن من شرح نظري مختصر وتجربة عملية بالأدوات.<br>
    المستخدم لا يكتب كود، فقط يتفاعل مع أزرار وقوائم ومنزلقات.<br>
    المحاور النهائية:
    </p>
    <ul style='color:#222;font-size:1.05rem;'>
        <li>مدخل ومعمارية الصور الرقمية: رفع صورة، عرض معلومات الصورة.</li>
        <li>أنظمة الألوان: التحويل بين RGB/Gray/HSV، تقسيم القنوات.</li>
        <li>العمليات على البكسل: تعديل السطوع/التباين، الصور السالبة، Thresholding.</li>
        <li>الفلاتر والالتفاف: اختيار نوع الفلتر، التحكم بحجم Kernel، مقارنة قبل/بعد.</li>
        <li>إزالة الضوضاء: إضافة ضوضاء، تطبيق Median/Bilateral Filtering.</li>
        <li>كشف الحواف: اختيار نوع كشف الحافة، التحكم بالعتبات، عرض قبل/بعد.</li>
        <li>العمليات المورفولوجية: تحويل إلى ثنائي، تطبيق عمليات مورفولوجية.</li>
        <li>التحويلات الهندسية: تدوير، تكبير/تصغير، انعكاس، قص جزء من الصورة.</li>
        <li>مشروع ختامي: سلسلة عمليات تفاعلية، حفظ الصورة النهائية.</li>
    </ul>
    <p style='color:#1976d2;font-size:1.05rem;font-weight:bold;'>الأدوات المطلوبة: Python، Streamlit، OpenCV، NumPy</p>
</div>
""", unsafe_allow_html=True)

# تخصيص التصميم باستخدام CSS مدمج

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    }
    h1 {
        color: #2e7d32;
        text-align: center;
        font-weight: bold;
        letter-spacing: 2px;
        font-family: 'Cairo', 'Tajawal', Arial, sans-serif;
    }
    h2, h3, h4 {
        color: #388e3c;
        font-family: 'Cairo', 'Tajawal', Arial, sans-serif;
    }
    body, .stApp, .stMarkdown, .stText, .stExpander, .stButton>button, .stCheckbox>label, .stTextInput>label {
        color: #111 !important;
        font-family: 'Cairo', 'Tajawal', Arial, sans-serif;
    }
    .stButton>button {
        background: linear-gradient(90deg, #43a047 0%, #81c784 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        transition: background 0.3s;
        box-shadow: 0 2px 8px rgba(67,160,71,0.08);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #388e3c 0%, #66bb6a 100%);
    }
    .stSlider>div>div>div {
        background: #43a047;
    }
    .stCheckbox>label {
        color: #388e3c;
        font-weight: bold;
    }
    .stTextInput>label {
        color: #388e3c;
        font-weight: bold;
    }
    .streamlit-expanderHeader {
        background-color: #c8e6c9;
        color: #388e3c;
        font-weight: bold;
    }
    .camera-container {
        border: 2px solid #1976d2;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 24px;
        background: linear-gradient(120deg, #e3f2fd 0%, #e8f5e9 100%);
        box-shadow: 0 2px 12px rgba(38,166,154,0.08);
    }
    .stImage>img {
        border-radius: 16px;
        box-shadow: 0 2px 12px #bbdefb;
        margin-bottom: 8px;
    }
    .stSidebar {
        background: linear-gradient(120deg, #bbdefb 0%, #c8e6c9 100%);
        border-radius: 0 16px 16px 0;
        box-shadow: 2px 0 12px #bbdefb;
    }
    .stMarkdown ul {
        background: #e3f2fd;
        border-radius: 8px;
        padding: 12px 18px;
        box-shadow: 0 1px 6px #bbdefb;
    }
    .stMarkdown li {
        margin-bottom: 8px;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.title("🖼 معالجة الصور التفاعلية")
st.markdown("---")


# شريط جانبي للتنقل بين الوحدات + صفحة حول التطبيق وزر إعادة تعيين
with st.sidebar:
    selected = option_menu(
        menu_title="الوحدات التعليمية",
        options=[
            "مدخل ومعمارية الصور",
            "أنظمة الألوان",
            "العمليات على البكسل",
            "الفلاتر والالتفاف",
            "إزالة الضوضاء",
            "كشف الحواف",
            "العمليات المورفولوجية",
            "التحويلات الهندسية",
            "المعالجة المباشرة بالكاميرا",
            "المشروع الختامي",
            "حول التطبيق"
        ],
        icons=[
            "house",
            "palette",
            "sliders",
            "filter",
            "ear",
            "vector-pen",
            "circle",
            "arrow-left-right",
            "camera",
            "code",
            "info-circle"
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background": "linear-gradient(120deg, #e3f2fd 0%, #e8f5e9 100%)", "border-radius": "0 16px 16px 0"},
            "icon": {"color": "#ff9800", "font-size": "22px"},
            "nav-link": {"font-size": "18px", "text-align": "right", "margin": "0px", "color": "#222", "font-weight": "bold"},
            "nav-link-selected": {"background": "linear-gradient(90deg, #43a047 0%, #1976d2 100%)", "color": "#fff", "font-weight": "bold", "box-shadow": "0 2px 8px #b2dfdb"},
            "menu-title": {"color": "#1976d2", "font-size": "20px", "font-weight": "bold"}
        }
    )
    st.markdown("---")
    if st.button("🔄 إعادة تعيين الخيارات"):
        st.session_state.clear()
        st.experimental_rerun()
    st.markdown("---")
    st.markdown("""
    <div style='font-size:14px; color:#2E7D32;'>
    <b>طور بواسطة:</b> GitHub Copilot<br>
    <b>للتواصل:</b> mjlo@example.com
    </div>
    """, unsafe_allow_html=True)

# وظيفة لتحميل الصورة
def load_image():
    # خيارات تحميل الصورة
    option = st.radio("اختر طريقة تحميل الصورة:", ("رفع صورة", "استخدام صورة افتراضية"))
    
    img = None
    if option == "رفع صورة":
        uploaded_file = st.file_uploader("اختر صورة", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            st.success("تم تحميل الصورة بنجاح!")
    
    else:  # صورة افتراضية
        default_option = st.selectbox("اختر صورة افتراضية:", 
                                    ("لينا", "بابون", "منظر طبيعي"))
        
        if default_option == "لينا":
            # إنشاء صورة لينا افتراضية (شبكة ألوان)
            img_array = np.zeros((512, 512, 3), dtype=np.uint8)
            cv2.rectangle(img_array, (0, 0), (256, 256), (255, 0, 0), -1)  # أحمر
            cv2.rectangle(img_array, (256, 0), (512, 256), (0, 255, 0), -1)  # أخضر
            cv2.rectangle(img_array, (0, 256), (256, 512), (0, 0, 255), -1)  # أزرق
            cv2.rectangle(img_array, (256, 256), (512, 512), (255, 255, 255), -1)  # أبيض
            img = Image.fromarray(img_array)
            
        elif default_option == "بابون":
            # إنشاء صورة بابون افتراضية (تدرج رمادي)
            img_array = np.zeros((512, 512), dtype=np.uint8)
            for i in range(512):
                img_array[i, :] = i // 2
            img = Image.fromarray(img_array)
            
        else:
            # إنشاء منظر طبيعي افتراضي (تدرج ألوان)
            img_array = np.zeros((512, 512, 3), dtype=np.uint8)
            for i in range(512):
                # سماء زرقاء
                img_array[i, :, 0] = 255 - i // 2  # أزرق
                img_array[i, :, 1] = 200 - i // 3  # أخضر
                img_array[i, :, 2] = 150 - i // 4  # أحمر
                
                # أرض خضراء
                if i > 400:
                    img_array[i, :, 0] = 50  # أزرق
                    img_array[i, :, 1] = 200  # أخضر
                    img_array[i, :, 2] = 50  # أحمر
            img = Image.fromarray(img_array)
    
    return img

# وظيفة لعرض معلومات الصورة
def display_image_info(img):
    if img is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("الصورة الأصلية")
            st.image(img, use_column_width=True)
        
        with col2:
            st.subheader("معلومات الصورة")
            if isinstance(img, np.ndarray):
                if len(img.shape) == 3:
                    height, width, channels = img.shape
                    st.write(f"*الأبعاد:* {width} × {height} بكسل")
                    st.write(f"*عدد القنوات:* {channels}")
                else:
                    height, width = img.shape
                    st.write(f"*الأبعاد:* {width} × {height} بكسل")
                    st.write(f"*عدد القنوات:* 1 (تدرج رمادي)")
            else:
                st.write(f"*الأبعاد:* {img.width} × {img.height} بكسل")
                st.write(f"*الوضع:* {img.mode}")


# رسالة توضيحية أعلى الصفحة: المستخدم لا يحتاج لكتابة كود
st.markdown("""
    <div style='background:#fff3e0;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;font-weight:bold;font-size:1.08rem;'>
    <span style='font-size:1.15rem;'>هذا التطبيق تفاعلي بالكامل، لا تحتاج لكتابة أي كود.<br>فقط استخدم الأزرار، القوائم، والمنزلقات لتجربة العمليات بنفسك.</span>
    </div>
""", unsafe_allow_html=True)

# تخصيص مربع المعلومات ليكون النص داكن وواضح
st.markdown("""
<style>
    .stAlert {
        background: linear-gradient(90deg, #e0f7fa 0%, #b2dfdb 100%) !important;
        color: #222 !important;
        font-weight: bold;
        font-size: 1.15rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px #b2dfdb;
        padding: 12px 24px !important;
    }
    .stInfo {
        color: #222 !important;
    }
</style>
""", unsafe_allow_html=True)

# تخصيص مربع st.info ليكون النص أسود دائماً
st.markdown("""
<style>
    div[data-testid="stNotificationContent"], .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: #222 !important;
        font-weight: bold;
        font-size: 1.15rem;
    }
    .stMarkdown p {
        color: #222 !important;
    }
</style>
""", unsafe_allow_html=True)

# رسالة تفاعلية أعلى كل وحدة تؤكد أن كل شيء تفاعلي ولا يحتاج المستخدم لكتابة كود
interactive_message = "<div style='background:#fff3e0;border-radius:8px;padding:8px 16px;margin-bottom:10px;color:#222;font-weight:bold;font-size:1.05rem;'>هذا التطبيق تفاعلي بالكامل، لا تحتاج لكتابة أي كود. فقط استخدم الأزرار والقوائم والمنزلقات لتجربة العمليات بنفسك.</div>"

# شرح نظري مختصر لكل وحدة (4-6 أسطر)
theory_summaries = {
    "مدخل ومعمارية الصور": "الصورة الرقمية عبارة عن شبكة من البكسلات، كل بكسل يحمل قيمة لونية. الأبعاد تحدد عدد البكسلات، والقنوات تحدد مكونات اللون (مثل RGB). العمق اللوني يحدد عدد الألوان الممكنة. الصور الرقمية تُستخدم في العديد من التطبيقات مثل التصوير الطبي، الذكاء الاصطناعي، والأمن. كلما زادت الدقة والعمق اللوني، زادت جودة الصورة وحجمها. فهم هذه الأساسيات ضروري لأي معالجة صور.",
    "أنظمة الألوان": "أنظمة الألوان هي طرق مختلفة لتمثيل الألوان في الصور. RGB هو الأكثر شيوعاً في الشاشات، بينما BGR يُستخدم في OpenCV. Grayscale يبسط المعالجة ويقلل حجم البيانات. HSV يفصل بين اللون والسطوع، مما يسهل معالجة الألوان. اختيار النظام المناسب يعتمد على نوع المعالجة المطلوبة.",
    "العمليات على البكسل": "تشمل العمليات على البكسل تعديل السطوع والتباين، وعكس الألوان، وتطبيق العتبة لتحويل الصورة إلى أبيض وأسود. هذه العمليات تُستخدم لتحسين الصور أو تجهيزها للمعالجة المتقدمة. يمكن تطبيقها على كل بكسل بشكل منفصل. فهم هذه العمليات يساعد في التحكم بجودة الصورة.",
    "الفلاتر والالتفاف": "الفلاتر تستخدم نواة صغيرة لتطبيق تأثيرات مثل التنعيم أو التعزيز أو كشف الحواف. الالتفاف هو عملية رياضية تُطبق على كل بكسل باستخدام النواة. الفلاتر تساعد في إزالة الضوضاء أو إبراز التفاصيل. يمكن التحكم بحجم النواة ونوع الفلتر حسب الحاجة. المقارنة بين الصورة الأصلية والمفلترة توضح تأثير الفلتر.",
    "إزالة الضوضاء": "الضوضاء تؤثر على جودة الصور وتنتج عن عوامل مثل الإضاءة أو أجهزة التصوير. يمكن إضافة ضوضاء للصورة واستخدام فلاتر مثل Median أو Bilateral لإزالتها. إزالة الضوضاء ضرورية لتحسين نتائج المعالجة اللاحقة. المقارنة بين الصورة الأصلية والمعدلة توضح فعالية الفلاتر.",
    "كشف الحواف": "كشف الحواف يحدد الحدود بين الأجسام في الصورة باستخدام خوارزميات مثل Sobel وLaplacian وCanny. هذه العمليات تُستخدم في التعرف على الأشكال وتتبع الأجسام. يمكن التحكم بالعتبات للحصول على نتائج دقيقة. عرض الصورة الأصلية وصورة الحواف يساعد في فهم تأثير العملية.",
    "العمليات المورفولوجية": "العمليات المورفولوجية مثل التآكل والتوسيع والفتح والإغلاق تُستخدم لمعالجة الصور الثنائية وتحسينها. هذه العمليات تعتمد على شكل النواة وتُستخدم لإزالة الشوائب أو فصل الأجسام. فهم هذه العمليات مهم في تطبيقات مثل التعرف على النصوص أو الأجسام.",
    "التحويلات الهندسية": "تشمل التحويلات الهندسية تدوير الصورة، تكبيرها أو تصغيرها، انعكاسها أفقياً أو رأسياً، وقص جزء منها. هذه العمليات تُستخدم لتجهيز الصور أو تعديلها حسب الحاجة. يمكن التحكم في معايير التحويل بسهولة. المقارنة بين الصورة الأصلية والمعدلة توضح تأثير التحويل.",
    "المشروع الختامي": "في المشروع الختامي يمكنك رفع صورة واختيار سلسلة من العمليات (Pipeline) مثل تحويل إلى رمادي ثم تطبيق Blur ثم كشف الحواف. الهدف هو دمج عدة تقنيات لمعالجة صورة واحدة. يمكنك حفظ النتيجة النهائية ومقارنتها مع الأصل. هذا المشروع يختبر فهمك لجميع الوحدات السابقة."
}

# عرض الشرح النظري المختصر أعلى كل وحدة
if selected in theory_summaries:
    st.markdown(f"""
    <div style='background:#fffde7;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;font-size:1.05rem;'>
    <b>شرح نظري مختصر:</b><br>{theory_summaries[selected]}
    </div>
    """, unsafe_allow_html=True)

# الوحدة 1: مدخل ومعمارية الصور الرقمية
if selected == "مدخل ومعمارية الصور":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("مدخل ومعمارية الصور الرقمية")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    الصورة الرقمية هي تمثيل مرئي مكون من شبكة من البكسلات. كل بكسل يحمل معلومات اللون، وتحدد الأبعاد عدد البكسلات في العرض والارتفاع، بينما تحدد القنوات مكونات اللون (مثل RGB). العمق اللوني يحدد عدد الألوان الممكنة لكل بكسل.<br>كلما زادت دقة الصورة وعمقها اللوني، زادت جودتها وحجمها.
    </div>
    """, unsafe_allow_html=True)
    # تحميل الصورة
    img = load_image()
    st.session_state.img = img

    # عرض معلومات الصورة
    display_image_info(img)

    # إضافة مساحة رأسية
    add_vertical_space(2)

    # زر لحفظ الصورة
    if st.button("💾 حفظ الصورة"):
        if img is not None:
            # تحويل الصورة إلى مصفوفة NumPy
            if isinstance(img, Image.Image):
                img_array = np.array(img)
            else:
                img_array = img

            # ترميز الصورة بتنسيق JPEG
            _, img_encoded = cv2.imencode('.jpg', img_array)

            # تحويل البيانات المشفرة إلى سلسلة بايتات
            img_bytes = img_encoded.tobytes()

            # ترميز بايتات الصورة إلى Base64
            img_base64 = base64.b64encode(img_bytes).decode()

            # إنشاء رابط تحميل الصورة
            st.markdown(f"<a href='data:image/jpeg;base64,{img_base64}' download='image.jpg'>اضغط هنا لتحميل الصورة</a>", unsafe_allow_html=True)
        else:
            st.warning("يرجى تحميل صورة أولاً.")

# الوحدة 2: أنظمة الألوان

elif selected == "أنظمة الألوان":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("أنظمة الألوان (Color Spaces)")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    أنظمة الألوان مثل RGB وBGR وGrayscale وHSV هي طرق مختلفة لتمثيل الألوان في الصور الرقمية. يستخدم RGB في الشاشات، بينما BGR في OpenCV. Grayscale يبسط المعالجة، وHSV مفيد لفصل الألوان.<br>لكل نظام استخداماته حسب الحاجة.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        if st.button("تحويل إلى HSV"):
            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            img_hsv_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
            st.image(img_hsv_rgb, caption="بعد العملية (HSV)", use_column_width=True)
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# الوحدة 3: العمليات على البكسل

elif selected == "العمليات على البكسل":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("العمليات على البكسل (Point Operations)")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    العمليات على البكسل تشمل تعديل السطوع والتباين، وعكس الألوان (الصورة السالبة)، وتطبيق العتبة لتحويل الصورة إلى أبيض وأسود.<br>هذه العمليات أساسية لتحسين الصور وتجهيزها للمعالجة المتقدمة.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        brightness = st.slider("تعديل السطوع:", -100, 100, 0)
        contrast = st.slider("تعديل التباين:", -100, 100, 0)

        if st.button("تطبيق"):
            # تعديل السطوع والتباين
            img_bright_contrast = cv2.convertScaleAbs(img_bgr, alpha=contrast/100+1, beta=brightness)
            st.image(img_bright_contrast, caption="بعد العملية (تعديل السطوع والتباين)", use_column_width=True)
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# الوحدة 4: الفلاتر والالتفاف

elif selected == "الفلاتر والالتفاف":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("الفلاتر والالتفاف (Filtering & Convolution)")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    الفلاتر تستخدم نواة (Kernel) صغيرة لتطبيق تأثيرات مثل التنعيم (Blur) أو التعزيز (Sharpen) أو كشف الحواف. يمكن التحكم بحجم النواة ونوع الفلتر.<br>قارن بين الصورة الأصلية والصورة بعد تطبيق الفلتر.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        filter_type = st.selectbox("اختر نوع الفلتر:", ("Gaussian Blur", "Median Blur", "Bilateral Filter"))

        if st.button("تطبيق"):
            if filter_type == "Gaussian Blur":
                # تطبيق فلتر Gaussian Blur
                img_filtered = cv2.GaussianBlur(img_bgr, (15, 15), 0)
                st.image(img_filtered, caption="بعد العملية (Gaussian Blur)", use_column_width=True)
            elif filter_type == "Median Blur":
                # تطبيق فلتر Median Blur
                img_filtered = cv2.medianBlur(img_bgr, 15)
                st.image(img_filtered, caption="بعد العملية (Median Blur)", use_column_width=True)
            else:
                # تطبيق فلتر Bilateral Filter
                img_filtered = cv2.bilateralFilter(img_bgr, 15, 75, 75)
                st.image(img_filtered, caption="بعد العملية (Bilateral Filter)", use_column_width=True)
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# الوحدة 5: إزالة الضوضاء

elif selected == "إزالة الضوضاء":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("إزالة الضوضاء (Denoising)")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    الضوضاء مثل Salt & Pepper أو Gaussian Noise تؤثر على جودة الصور. يمكن إضافة ضوضاء للصورة واستخدام فلاتر مثل Median أو Bilateral لإزالتها.<br>قارن بين الصورة الأصلية والصورة بعد إزالة الضوضاء.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        # زر لإضافة ضوضاء للصورة
        if st.button("إضافة ضوضاء"):
            # إضافة ضوضاء Salt & Pepper
            noise_img = img_bgr.copy()
            cv2.randu(noise_img, 0, 255)
            noise_img = cv2.addWeighted(img_bgr, 0.8, noise_img, 0.2, 0)
            st.image(noise_img, caption="بعد إضافة الضوضاء", use_column_width=True)

        # خيارات إزالة الضوضاء
        denoise_method = st.selectbox("اختر طريقة إزالة الضوضاء:", ("Median Filtering", "Bilateral Filtering"))

        if st.button("تطبيق"):
            if denoise_method == "Median Filtering":
                # تطبيق Median Filtering
                img_denoised = cv2.medianBlur(img_bgr, 5)
                st.image(img_denoised, caption="بعد إزالة الضوضاء باستخدام Median Filtering", use_column_width=True)
            else:
                # تطبيق Bilateral Filtering
                img_denoised = cv2.bilateralFilter(img_bgr, 9, 75, 75)
                st.image(img_denoised, caption="بعد إزالة الضوضاء باستخدام Bilateral Filtering", use_column_width=True)
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# الوحدة 6: كشف الحواف

elif selected == "كشف الحواف":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("كشف الحواف (Edge Detection)")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    كشف الحواف يحدد الحدود بين الأجسام في الصورة باستخدام خوارزميات مثل Sobel وLaplacian وCanny. يمكن التحكم بالعتبات في Canny.<br>شاهد الفرق بين الصورة الأصلية وصورة الحواف.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        # خيارات كشف الحواف
        edge_detection_method = st.selectbox("اختر طريقة كشف الحواف:", ("Sobel", "Laplacian", "Canny"))

        if st.button("تطبيق"):
            if edge_detection_method == "Sobel":
                # تطبيق خوارزمية Sobel
                sobelx = cv2.Sobel(img_bgr, cv2.CV_64F, 1, 0, ksize=5)
                sobely = cv2.Sobel(img_bgr, cv2.CV_64F, 0, 1, ksize=5)
                img_edges = cv2.magnitude(sobelx, sobely)
                st.image(img_edges, caption="بعد تطبيق Sobel", use_column_width=True, channels="GRAY")
            elif edge_detection_method == "Laplacian":
                # تطبيق خوارزمية Laplacian
                img_edges = cv2.Laplacian(img_bgr, cv2.CV_64F)
                st.image(img_edges, caption="بعد تطبيق Laplacian", use_column_width=True, channels="GRAY")
            else:
                # تطبيق خوارزمية Canny
                lower_threshold = st.slider("العتبة السفلى لكشف الحواف:", 0, 255, 100)
                upper_threshold = st.slider("العتبة العليا لكشف الحواف:", 0, 255, 200)
                img_edges = cv2.Canny(img_bgr, lower_threshold, upper_threshold)
                st.image(img_edges, caption="بعد تطبيق Canny Edge Detection", use_column_width=True, channels="GRAY")
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# الوحدة 7: العمليات المورفولوجية

elif selected == "العمليات المورفولوجية":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("العمليات المورفولوجية (Morphological Operations)")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    العمليات المورفولوجية مثل التآكل والتوسيع والفتح والإغلاق تُستخدم لمعالجة الصور الثنائية وتحسينها.<br>يمكنك التحكم بحجم النواة ومقارنة النتائج مع الأصل.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        # خيارات العمليات المورفولوجية
        morph_operation = st.selectbox("اختر العملية المورفولوجية:", ("Erosion", "Dilation", "Opening", "Closing"))

        if st.button("تطبيق"):
            if morph_operation == "Erosion":
                # تطبيق عملية التآكل
                kernel_size = st.slider("اختر حجم النواة:", 1, 20, 5)
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                img_morphed = cv2.erode(img_bgr, kernel, iterations=1)
                st.image(img_morphed, caption="بعد تطبيق التآكل", use_column_width=True)
            elif morph_operation == "Dilation":
                # تطبيق عملية التوسيع
                kernel_size = st.slider("اختر حجم النواة:", 1, 20, 5)
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                img_morphed = cv2.dilate(img_bgr, kernel, iterations=1)
                st.image(img_morphed, caption="بعد تطبيق التوسيع", use_column_width=True)
            elif morph_operation == "Opening":
                # تطبيق عملية الفتح
                kernel_size = st.slider("اختر حجم النواة:", 1, 20, 5)
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                img_morphed = cv2.morphologyEx(img_bgr, cv2.MORPH_OPEN, kernel)
                st.image(img_morphed, caption="بعد تطبيق الفتح", use_column_width=True)
            else:
                # تطبيق عملية الإغلاق
                kernel_size = st.slider("اختر حجم النواة:", 1, 20, 5)
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                img_morphed = cv2.morphologyEx(img_bgr, cv2.MORPH_CLOSE, kernel)
                st.image(img_morphed, caption="بعد تطبيق الإغلاق", use_column_width=True)
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# الوحدة 8: التحويلات الهندسية

elif selected == "التحويلات الهندسية":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("التحويلات الهندسية (Geometric Transforms)")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    التحويلات الهندسية تشمل تدوير الصورة، تكبيرها أو تصغيرها، انعكاسها أفقياً أو رأسياً، وقص جزء منها.<br>جرب التحكم في هذه العمليات وشاهد الفرق.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        # خيارات التحويلات الهندسية
        transform_type = st.selectbox("اختر نوع التحويل:", ("Rotation", "Scaling", "Translation", "Flipping"))

        if st.button("تطبيق"):
            if transform_type == "Rotation":
                angle = st.slider("اختر زاوية التدوير (بالدرجات):", 0, 360, 90)
                (h, w) = img_bgr.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                img_transformed = cv2.warpAffine(img_bgr, M, (w, h))
                st.image(img_transformed, caption="بعد التدوير", use_column_width=True)
            elif transform_type == "Scaling":
                scale_percent = st.slider("نسبة التكبير/التصغير (%):", 10, 300, 100)
                width = int(img_bgr.shape[1] * (scale_percent / 100))
                height = int(img_bgr.shape[0] * (scale_percent / 100))
                img_transformed = cv2.resize(img_bgr, (width, height), interpolation=cv2.INTER_LINEAR)
                st.image(img_transformed, caption="بعد التكبير/التصغير", use_column_width=True)
            elif transform_type == "Translation":
                x_shift = st.slider("التحويل الأفقي (بكسل):", -100, 100, 0)
                y_shift = st.slider("التحويل الرأسي (بكسل):", -100, 100, 0)
                M = np.float32([[1, 0, x_shift], [0, 1, y_shift]])
                img_transformed = cv2.warpAffine(img_bgr, M, (img_bgr.shape[1], img_bgr.shape[0]))
                st.image(img_transformed, caption="بعد التحويل", use_column_width=True)
            else:
                # Flipping
                flip_direction = st.selectbox("اختر اتجاه الانعكاس:", ("أفقي", "رأسي"))
                if flip_direction == "أفقي":
                    img_transformed = cv2.flip(img_bgr, 1)
                else:
                    img_transformed = cv2.flip(img_bgr, 0)
                st.image(img_transformed, caption="بعد الانعكاس", use_column_width=True)
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# الوحدة 9: المعالجة المباشرة بالكاميرا

elif selected == "المعالجة المباشرة بالكاميرا":
    st.header("المعالجة المباشرة بالكاميرا")
    st.info("شغل الكاميرا وطبق المعالجة على البث المباشر.")
    
    # زر لتشغيل الكاميرا
    if st.button("تشغيل الكاميرا"):
        # إعداد الكاميرا
        cap = cv2.VideoCapture(0)

        # التحقق من فتح الكاميرا بنجاح
        if not cap.isOpened():
            st.error("فشل فتح الكاميرا.")
        else:
            st.success("الكاميرا تعمل. اضغط 'q' لإيقاف البث.")

            # قراءة وإظهار الفيديو المباشر
            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("فشل في قراءة الإطار من الكاميرا.")
                    break

                # تحويل الإطار إلى RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # عرض الإطار
                st.image(frame_rgb, channels="RGB", use_column_width=True)

                # كسر الحلقة عند الضغط على 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # تحرير الكاميرا
        cap.release()
        cv2.destroyAllWindows()

# الوحدة 10: المشروع الختامي

elif selected == "المشروع الختامي":
    st.markdown(interactive_message, unsafe_allow_html=True)
    st.header("المشروع الختامي: سلسلة عمليات معالجة الصور")
    st.markdown("""
    <div style='background:#e3f2fd;border-radius:8px;padding:10px 16px;margin-bottom:10px;color:#222;'>
    في المشروع الختامي يمكنك رفع صورة واختيار سلسلة من العمليات (Pipeline) مثل تحويل إلى رمادي ثم تطبيق Blur ثم كشف الحواف.<br>شاهد النتيجة النهائية وقارنها مع الأصل، ويمكنك حفظ الصورة الناتجة.
    </div>
    """, unsafe_allow_html=True)
    # تجربة عملية موحدة: رفع صورة أو استخدام صورة جاهزة، تطبيق العملية، عرض قبل/بعد

    def get_image():
        uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.session_state['uploaded_image'] = image
                st.success("تم رفع الصورة بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء رفع الصورة: {e}")
        elif st.button("استخدم صورة افتراضية"):
            image = Image.open("default.jpg") if os.path.exists("default.jpg") else Image.new('RGB', (256,256), (200,200,200))
            st.session_state['uploaded_image'] = image
            st.info("تم اختيار صورة افتراضية.")
        return st.session_state.get('uploaded_image', None)

    # تطبيق التجربة العملية
    image = get_image()
    if image is not None:
        st.image(image, caption="قبل العملية", use_column_width=True)
        img_bgr = pil_to_bgr(image)
        # خيارات المشروع الختامي
        st.subheader("اختر العمليات التي تريد تطبيقها:")
        operations = []
        if st.checkbox("تحويل إلى رمادي"):
            operations.append("Grayscale")
        if st.checkbox("تعديل السطوع والتباين"):
            operations.append("Brightness/Contrast")
        if st.checkbox("تطبيق Gaussian Blur"):
            operations.append("Gaussian Blur")
        if st.checkbox("كشف الحواف باستخدام Canny"):
            operations.append("Canny Edge Detection")

        if st.button("تطبيق العمليات"):
            img_final = img_bgr.copy()

            for op in operations:
                if op == "Grayscale":
                    img_final = cv2.cvtColor(img_final, cv2.COLOR_BGR2GRAY)
                elif op == "Brightness/Contrast":
                    img_final = cv2.convertScaleAbs(img_final, alpha=1.2, beta=30)
                elif op == "Gaussian Blur":
                    img_final = cv2.GaussianBlur(img_final, (15, 15), 0)
                elif op == "Canny Edge Detection":
                    img_final = cv2.Canny(img_final, 100, 200)

            st.image(img_final, caption="بعد تطبيق العمليات", use_column_width=True)
    else:
        st.info("يرجى رفع صورة أو اختيار صورة جاهزة لتجربة العملية.")

# صفحة حول التطبيق
elif selected == "حول التطبيق":
    st.header("حول التطبيق")
    st.success("تطبيق تفاعلي لمعالجة الصور مقدم باللغة العربية، يتيح لك تجربة تقنيات معالجة الصور بسهولة. جميع الحقوق محفوظة © 2025.")
    st.markdown("""
    <ul>
        <li>المطور: GitHub Copilot</li>
        <li>للتواصل: mjlo@example.com</li>
        <li>الإصدار: 1.0</li>
        <li>جميع الحقوق محفوظة</li>
    </ul>
    """, unsafe_allow_html=True)

# إضافة CSS لضمان أن جميع النصوص تظهر باللون الأسود في كل عناصر Streamlit
st.markdown("""
    <style>
    body, .stApp, .stMarkdown, .stHeader, .stText, .stInfo, .stAlert, .stNotificationContent, .stSuccess, .stWarning, .stError, .stSidebar, .stButton, .stRadio, .stSelectbox, .stExpander, .stFileUploader, .stSlider, .stTextInput, .stTextArea {
        color: #111 !important;
        font-family: 'Cairo', 'Tajawal', sans-serif !important;
    }
    .stNotificationContent, .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        background: #e3f2fd !important;
        color: #111 !important;
    }
    .stButton>button, .stSidebar .stButton>button {
        color: #111 !important;
        font-weight: bold;
        background: linear-gradient(90deg,#aeea00,#00bfae);
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 8px #0001;
    }
    .stFileUploader label, .stFileUploader .uploadedFileName {
        color: #111 !important;
    }
    .stExpanderHeader {
        color: #111 !important;
    }
    .stRadio label, .stSelectbox label {
        color: #111 !important;
    }
    </style>
""", unsafe_allow_html=True)

# تعريف دالة pil_to_bgr في أعلى الملف لحل جميع أخطاء التعريف

def pil_to_bgr(img_pil):
    import numpy as np
    import cv2
    img_rgb = np.array(img_pil.convert('RGB'))
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return img_bgr

# إصلاح مشاكل رفع الصور وتطبيق الفلاتر
# التأكد من أن رفع الصورة يعمل بشكل صحيح
if 'uploaded_image' not in st.session_state:
    st.session_state['uploaded_image'] = None

uploaded_file = st.file_uploader("رفع صورة", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.session_state['uploaded_image'] = image
        st.success("تم رفع الصورة بنجاح!")
    except Exception as e:
        st.error(f"حدث خطأ أثناء رفع الصورة: {e}")

# التأكد من أن تطبيق الفلاتر لا يسبب أخطاء إذا لم توجد صورة
if st.session_state['uploaded_image'] is not None:
    image = st.session_state['uploaded_image']
    st.image(image, caption="الصورة الأصلية", use_column_width=True)
    # مثال: تطبيق فلتر Blur
    if st.button("تطبيق Blur"):
        try:
            img_np = np.array(image)
            img_blur = cv2.GaussianBlur(img_np, (7,7), 0)
            st.image(img_blur, caption="بعد تطبيق Blur", use_column_width=True)
        except Exception as e:
            st.error(f"حدث خطأ أثناء تطبيق الفلتر: {e}")
else:
    st.info("يرجى رفع صورة أولاً لتجربة الفلاتر.")

# إصلاح مشاكل الفلاتر وتحويل الصور بين PIL وOpenCV بشكل صحيح
# دالة لتحويل صورة PIL إلى NumPy بصيغة BGR لاستخدام OpenCV

def pil_to_bgr(img_pil):
    import numpy as np
    import cv2
    img_rgb = np.array(img_pil.convert('RGB'))
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return img_bgr

# دالة لتحويل صورة NumPy BGR إلى PIL

def bgr_to_pil(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)

# مثال استخدام في وحدة أنظمة الألوان
if selected == "أنظمة الألوان" and st.session_state['uploaded_image'] is not None:
    image = st.session_state['uploaded_image']
    img_bgr = pil_to_bgr(image)
    st.image(image, caption="الصورة الأصلية", use_column_width=True)
    if st.button("تحويل إلى HSV"):
        try:
            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            img_hsv_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
            st.image(img_hsv_rgb, caption="صورة HSV", use_column_width=True)
        except Exception as e:
            st.error(f"خطأ في التحويل: {e}")