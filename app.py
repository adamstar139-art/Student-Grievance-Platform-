import streamlit as st
import pandas as pd
import sqlite3
import datetime
import urllib.parse

import tempfile
import subprocess

def create_pdf_report_bytes(s_name, s_id, grade, sec, phone, created_at, comp_text, action_taken, r_id):
    html_doc = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="utf-8">
    <title>تقرير إداري - {s_name}</title>
    <style>
        body {{ font-family: 'Noto Naskh Arabic', 'Cairo', sans-serif; padding: 25px; direction: rtl; text-align: right; background: #fff; color: #1e293b; }}
        .card {{ border: 3px solid #005A2B; padding: 25px; border-radius: 12px; background: #ffffff; }}
        .header {{ text-align: right; border-right: 5px solid #005A2B; border-bottom: 2px solid #D4AF37; padding-bottom: 12px; margin-bottom: 18px; }}
        .header h2 {{ color: #005A2B; margin: 0; font-size: 20px; text-align: right; }}
        .header h3 {{ color: #475569; margin: 4px 0; font-size: 15px; text-align: right; }}
        .header h4 {{ color: #D4AF37; margin: 8px 0 0 0; font-size: 16px; text-align: right; }}
        .info-box {{ background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px 15px; border-radius: 8px; margin-bottom: 15px; font-size: 14px; line-height: 1.8; text-align: right; }}
        .section {{ margin-bottom: 15px; padding: 12px 15px; border-radius: 8px; font-size: 14px; line-height: 1.6; text-align: right; }}
        .sigs {{ display: table; width: 100%; margin-top: 30px; border-top: 2px dashed #CBD5E1; padding-top: 15px; text-align: center; }}
        .sig-col {{ display: table-cell; width: 33.33%; text-align: center; font-size: 13px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h2>المملكة العربية السعودية - وزارة التعليم</h2>
            <h3>الإدارة العامة للتعليم بمنطقة الرياض | متوسطة الثغر النموذجية الأهلية</h3>
            <h4>📋 تقرير قرار إداري سرّي رقم #{r_id}</h4>
        </div>
        <div class="info-box">
            <b>اسم الطالب:</b> {s_name} &nbsp;|&nbsp; <b>الهوية الوطنية:</b> {s_id}<br>
            <b>الصف الدراسي:</b> {grade} (فصل {sec}) &nbsp;|&nbsp; <b>جوال ولي الأمر:</b> {phone}<br>
            <b>تاريخ القرار:</b> {created_at}
        </div>
        <div class="section" style="background:#FFF9E6; border-right: 5px solid #D4AF37;">
            <b style="color:#5A4300;">📝 نص الشكوى المقدمة:</b><br>
            <div style="margin-top:6px; color:#453200;">{comp_text}</div>
        </div>
        <div class="section" style="background:#E6F4EA; border-right: 5px solid #28a745;">
            <b style="color:#064E3B;">✅ الإجراءات المتخذة من إدارة المدرسة:</b><br>
            <div style="margin-top:6px; color:#064E3B; font-weight:bold;">{action_taken}</div>
        </div>
        <div class="sigs">
            <div class="sig-col"><b>وكيل شؤون الطلاب</b><br><span style="color:#005A2B;">صالح بن عبدالله الدعجاني</span></div>
            <div class="sig-col"><b>وكيل شؤون المعلمين</b><br><span style="color:#005A2B;">محمد مبروك السيد</span></div>
            <div class="sig-col"><b>مدير المدرسة</b><br><span style="color:#005A2B;">إبراهيم بن موسى التميمي</span></div>
        </div>
    </div>
</body>
</html>"""

    with tempfile.NamedTemporaryFile(suffix='.html', mode='w', encoding='utf-8', delete=False) as f_html:
        f_html.write(html_doc)
        f_html_path = f_html.name

    f_pdf_path = f_html_path.replace('.html', '.pdf')
    try:
        subprocess.run(['wkhtmltopdf', '--quiet', '--enable-local-file-access', f_html_path, f_pdf_path], check=True)
        with open(f_pdf_path, 'rb') as f_pdf:
            pdf_bytes = f_pdf.read()
    except Exception:
        pdf_bytes = html_doc.encode('utf-8')
    finally:
        if os.path.exists(f_html_path): os.remove(f_html_path)
        if os.path.exists(f_pdf_path): os.remove(f_pdf_path)
    return pdf_bytes

import textwrap
import re

# دالة تنظيف HTML لمنع ظهور كود النص في Streamlit
def clean_html(html_str):
    lines = [line.strip() for line in html_str.strip().split('\n')]
    return '\n'.join(lines)

# محاولة استيراد مكتبة Supabase للتخزين السحابي الدائم
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False

# ===================================================================
# 1. تهيئة الصفحة والهوية الرسمية (تجاوب مع الجوال والكمبيوتر)
# ===================================================================
st.set_page_config(
    page_title="منصة شكاوى الطلاب - متوسطة الثغر النموذجية الأهلية",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="auto"
)

# إدارة حالة تسجيل الدخول في session_state لحفظ الجلسة عند الضغط على الأزرار
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if "reports_logged_in" not in st.session_state:
    st.session_state["reports_logged_in"] = False

# ===================================================================
# 2. تنسيقات CSS بالهوية الوطنية السعودية وتصميم أنيق للجوال
# ===================================================================
css_style = clean_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* الترويسة بالهوية الوطنية السعودية (الأخضر الملكي والذهبي) */
    .saudi-header {
        background: linear-gradient(135deg, #005A2B 0%, #003B1C 100%);
        color: #FFFFFF;
        padding: 25px 20px;
        border-radius: 16px;
        text-align: center;
        border-bottom: 5px solid #D4AF37;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12);
        margin-bottom: 22px;
    }
    .saudi-header h1 {
        color: #FFFFFF !important;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .saudi-header h3 {
        color: #D4AF37 !important;
        font-size: 18px;
        font-weight: 600;
        margin: 0;
    }
    
    /* صندوق التنبيه والأمان والسرية */
    .notice-box {
        background-color: #FFF9E6;
        border-right: 6px solid #D4AF37;
        border-left: 1px solid #FFEBA8;
        padding: 16px 20px;
        border-radius: 12px;
        color: #5A4300;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }
    
    /* مؤشر حفظ البيانات */
    .status-saved {
        background-color: #28a745;
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        font-weight: bold;
        text-align: center;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(40,167,69,0.3);
        margin-bottom: 18px;
    }
    .status-unsaved {
        background-color: #dc3545;
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        font-weight: bold;
        text-align: center;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(220,53,69,0.3);
        margin-bottom: 18px;
    }
    
    /* بطاقة التقرير والشكوى */
    .report-card {
        background: #FFFFFF;
        border: 2px solid #005A2B;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        direction: rtl !important;
        text-align: right !important;
    }
    .report-card *, .report-official-header *, .report-card div, .report-card p, .report-card h2, .report-card h3, .report-card h4 {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* ترويسة التقرير الرسمية */
    .report-official-header {
        text-align: right;
        border-right: 5px solid #005A2B;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    .report-official-header h2 {
        color: #005A2B;
        text-align: right;
        font-size: 20px;
        font-weight: 800;
        margin: 0;
    }
    .report-official-header p {
        color: #475569;
        font-weight: 700;
        margin: 4px 0 0 0;
        font-size: 14px;
    }
    
    /* التوقيعات الرسمية للإدارة */
    .signatures-block {
        margin-top: 25px;
        padding-top: 15px;
        border-top: 2px dashed #CBD5E1;
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        text-align: center;
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 15px;
    }
    .sig-item {
        margin: 5px 15px;
        font-size: 14px;
        font-weight: 700;
        color: #1E293B;
    }
    
    /* حقوق التطوير */
    .dev-footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        border-top: 1px solid #E2E8F0;
        color: #64748B;
        font-size: 14px;
        font-weight: 600;
    }
    
    @media (max-width: 768px) {
        .saudi-header h1 { font-size: 20px; }
        .saudi-header h3 { font-size: 14px; }
        .signatures-block { flex-direction: column; gap: 12px; }
    }
</style>
""")
st.markdown(css_style, unsafe_allow_html=True)

# ===================================================================
# 3. إعداد وقواعد البيانات (Supabase + SQLite المحلية الاحتياطية)
# ===================================================================
SUPABASE_URL = "https://yathpzoxjfpgahkbjzgz.supabase.co"
SUPABASE_KEY = "sb_publishable_4Igw4yxTyqcZzSvXei6TEg_cuxhLKcE"

try:
    if "supabase" in st.secrets:
        SUPABASE_URL = st.secrets["supabase"].get("url", SUPABASE_URL)
        SUPABASE_KEY = st.secrets["supabase"].get("key", SUPABASE_KEY)
except Exception:
    pass

# جميع طلاب متوسطة الثغر النموذجية الأهلية بالرياض (167 طالباً)
ALL_SCHOOL_STUDENTS = [
    # الأول المتوسط - 1
    ('1167628468', 'إبراهيم بن محمد بن علي الوهيبي', 'الأول المتوسط', '1', '966504158122'),
    ('2395664317', 'بلال عبدالرزاق عيسى العيسى', 'الأول المتوسط', '1', '966507448712'),
    ('1170582165', 'حسام بن محمد بن علي آل البارقي', 'الأول المتوسط', '1', '966504445699'),
    ('1169004353', 'ريان عبد الله جابر الأسمري', 'الأول المتوسط', '1', '966554260960'),
    ('2446713998', 'زيد زياد عبد اللطيف أبو قبع', 'الأول المتوسط', '1', '966590123455'),
    ('2527104554', 'سامي سعد عباس حمد', 'الأول المتوسط', '1', '966591781701'),
    ('1170111759', 'سعد ناصر سعد السيف', 'الأول المتوسط', '1', '966503219351'),
    ('1195559479', 'عبد العزيز عبد الله عبد العزيز العمار', 'الأول المتوسط', '1', '966555838394'),
    ('1153310501', 'عبد الله بن سليمان بن عبد الله الراجحي', 'الأول المتوسط', '1', '0551418881'),
    ('1170836520', 'عبد الله سعد محمد العيشان', 'الأول المتوسط', '1', '966504217660'),
    ('1171448515', 'علي أحمد علي كريري', 'الأول المتوسط', '1', '966558885481'),
    ('1170853053', 'علي سعد علي القحطاني', 'الأول المتوسط', '1', '966505466546'),
    ('1172018036', 'عمر عبد الله سعد الجبرين', 'الأول المتوسط', '1', '966555249420'),
    ('2552851368', 'مازن إسلام أحمد إبراهيم موسى', 'الأول المتوسط', '1', '966550490495'),
    ('013609321', 'محمد أحمد علي عقيل', 'الأول المتوسط', '1', '966546000184'),
    ('2394606749', 'محمد أشرف مسعود أبو خاطر', 'الأول المتوسط', '1', '966501276888'),
    ('1170042046', 'محمد بن فيصل بن مصلح الشمراني', 'الأول المتوسط', '1', '966555832145'),
    ('1169174164', 'محمد نايف فراج الدعجاني', 'الأول المتوسط', '1', '966554444782'),
    ('2380890976', 'وائل رشيد بولعيش', 'الأول المتوسط', '1', '966591534495'),

    # الأول المتوسط - 2
    ('1170348286', 'الوليد بن خالد بن فهد العتيبي', 'الأول المتوسط', '2', '966558522229'),
    ('1172433185', 'باسل محمد فرج الدوسري', 'الأول المتوسط', '2', '966537589781'),
    ('1173391556', 'بسام عبد الكريم عبد الله الدوسري', 'الأول المتوسط', '2', '966534467820'),
    ('1169185053', 'تركي عبد الله مسفر الدوسري', 'الأول المتوسط', '2', '966505258369'),
    ('1170108078', 'تميم فهد عبد العزيز العزاز', 'الأول المتوسط', '2', '966554435692'),
    ('1170970741', 'جاسر بن عبد الله بن جرمان الحارثي', 'الأول المتوسط', '2', '966559455545'),
    ('1168982427', 'راكان عبد الله يحيى كريري', 'الأول المتوسط', '2', '966581727444'),
    ('1172590968', 'ريان عبد الله منصور السبر', 'الأول المتوسط', '2', '966566959670'),
    ('2392863888', 'ريان وليد حسن حلاق', 'الأول المتوسط', '2', '966530527662'),
    ('1170420473', 'سيف عبد الكريم بريك العصيمي', 'الأول المتوسط', '2', '966504277904'),
    ('1168942108', 'صالح حسن فتحي سندي', 'الأول المتوسط', '2', '966557553922'),
    ('1173182138', 'عبد الرحمن إبراهيم عبد الله الحضيف', 'الأول المتوسط', '2', '966558822674'),
    ('1172448548', 'عبد الله صالح حمد الصفيان', 'الأول المتوسط', '2', '966558889978'),
    ('1170000945', 'فهد فهد بن أحمد العثمان', 'الأول المتوسط', '2', '966504484898'),
    ('1167092616', 'فهد عويض ثقل المطيري', 'الأول المتوسط', '2', '966508271056'),
    ('1170413171', 'فهد نايف فهد الحسينان', 'الأول المتوسط', '2', '966504140616'),
    ('1170294118', 'فيصل موينع عبد الله الموينع', 'الأول المتوسط', '2', '966541600918'),
    ('1171524604', 'فيصل ناصر سيف العريفي', 'الأول المتوسط', '2', '966505474606'),
    ('2502333707', 'محمد دراز محمد إسلام', 'الأول المتوسط', '2', '966556124553'),
    ('1170374993', 'مشاري عثمان سعد السعد', 'الأول المتوسط', '2', '966500330693'),
    ('1170884165', 'يزن محمد علي اليحيا', 'الأول المتوسط', '2', '966557072133'),
    ('1170548737', 'يوسف محمد عبد الله الدوسري', 'الأول المتوسط', '2', '966556666176'),

    # الثاني المتوسط - 1
    ('1163760935', 'أحمد بن سامي بن أحمد العمران', 'الثاني المتوسط', '1', '966551501503'),
    ('1153756612', 'الوليد عبد الله بن إبراهيم المبدل', 'الثاني المتوسط', '1', '966505241627'),
    ('1164269209', 'ذياب بن محمد بن ذياب القحطاني', 'الثاني المتوسط', '1', '966561169999'),
    ('1163187972', 'راكان سالم بن محمد القحطاني', 'الثاني المتوسط', '1', '966556609291'),
    ('1171617069', 'سعود خالد عبد الله الحمد', 'الثاني المتوسط', '1', '966555242944'),
    ('1163458878', 'سعود مشعل بن إبراهيم الشثري', 'الثاني المتوسط', '1', '966598887996'),
    ('1167623758', 'سلطان عبد الله حسن القحطاني', 'الثاني المتوسط', '1', '966563484825'),
    ('1164769430', 'عبد الرحمن حمد بن محمد العريفي', 'الثاني المتوسط', '1', '966555556856'),
    ('1167893740', 'عبد الرحمن ربيع جابر خبراني', 'الثاني المتوسط', '1', '966535924655'),
    ('1159740032', 'عبد العزيز سعود بن فهد العتيبي', 'الثاني المتوسط', '1', '966544155592'),
    ('1164747436', 'عبد المجيد بن محمد القحطاني', 'الثاني المتوسط', '1', '966555275591'),
    ('1160901128', 'فيصل بن عبد الله الجميعة', 'الثاني المتوسط', '1', '966554949948'),
    ('1162168627', 'مبارك صالح مبارك هليل', 'الثاني المتوسط', '1', '966553663819'),
    ('1163212978', 'محمد بن عبد الله بن عمران', 'الثاني المتوسط', '1', '966544779170'),
    ('1161858301', 'محمد عبد المحسن الحزام', 'الثاني المتوسط', '1', '966505264075'),
    ('1175902442', 'محمد فايز عبد الرحمن يوسف', 'الثاني المتوسط', '1', '966505482728'),
    ('1165686179', 'مشاري سلطان سالم الشمراني', 'الثاني المتوسط', '1', '966553908888'),
    ('1166040053', 'معاذ عبد الله سعود العريفي', 'الثاني المتوسط', '1', '966505473192'),
    ('1167081981', 'ناصر حسين محمد آل جبران', 'الثاني المتوسط', '1', '966550004952'),
    ('1171868639', 'وائل بن عبد الله آل عبيد الغامدي', 'الثاني المتوسط', '1', '966548888663'),
    ('1163191222', 'يزيد بن طارق بن علي الحديثي', 'الثاني المتوسط', '1', '966554084040'),

    # الثاني المتوسط - 2
    ('1166753291', 'إبراهيم بن مبارك آل موينع', 'الثاني المتوسط', '2', '966555212896'),
    ('1163613795', 'إبراهيم ياسر إبراهيم الحلوي', 'الثاني المتوسط', '2', '966502220990'),
    ('1167148251', 'حامد بن محمد بن حامد شباط', 'الثاني المتوسط', '2', '966595001616'),
    ('1164599977', 'حسام حسن محمد الشهري', 'الثاني المتوسط', '2', '966557775278'),
    ('1169057351', 'خالد تركي عايض القحطاني', 'الثاني المتوسط', '2', '966536201378'),
    ('1164120600', 'خالد داود عابد الحارثي', 'الثاني المتوسط', '2', '966501076244'),
    ('1165839455', 'سطام عبد العزيز عبد الله العريفي', 'الثاني المتوسط', '2', '966599791658'),
    ('1163778960', 'سعود سلطان هليل العتيبي', 'الثاني المتوسط', '2', '966554820082'),
    ('1166582989', 'طلال محمد منير المهدرس', 'الثاني المتوسط', '2', '966531167666'),
    ('1165143783', 'عبد الكريم مساعد الهزاع', 'الثاني المتوسط', '2', '966503210252'),
    ('1164277830', 'عبد اللطيف إبراهيم الطمرة', 'الثاني المتوسط', '2', '966505404365'),
    ('1165495258', 'عبد الله سامي سعد الحوشاني', 'الثاني المتوسط', '2', '966555219086'),
    ('013609088', 'علي أحمد علي عقيل', 'الثاني المتوسط', '2', '966546000184'),
    ('1164825802', 'عمر بن سعد بن هلال الشبانات', 'الثاني المتوسط', '2', '966505213725'),
    ('1163537838', 'فارس مشعل عبد الله الموينع', 'الثاني المتوسط', '2', '966555200719'),
    ('1162761306', 'فهد عيسى محمد العيسى', 'الثاني المتوسط', '2', '966554499908'),
    ('1164997858', 'مازن خالد دخيل المطيري', 'الثاني المتوسط', '2', '966501110052'),
    ('2348937422', 'مازن رفعت محمد حاج النيل', 'الثاني المتوسط', '2', '966501331089'),
    ('1172720045', 'محمد بن علي محسن العثيميني', 'الثاني المتوسط', '2', '966506256254'),
    ('1166803245', 'نايف بن بندر بن خلفان العلوي', 'الثاني المتوسط', '2', '966532225560'),
    ('1165668417', 'نواف عبد العزيز المرزوق', 'الثاني المتوسط', '2', '966501100076'),
    ('1164387977', 'هادي سلطان هادي القحطاني', 'الثاني المتوسط', '2', '966505936192'),
    ('1165002153', 'يزيد بن حسين كعكم', 'الثاني المتوسط', '2', '966550117805'),

    # الثاني المتوسط - 3
    ('1166911709', 'ثامر عمر إبراهيم عثمان', 'الثاني المتوسط', '3', '966538384444'),
    ('008464815', 'جهاد فارس عبد القادر حناوي', 'الثاني المتوسط', '3', '966562674178'),
    ('1164830562', 'خالد محمد عبد الكريم الخفاجي', 'الثاني المتوسط', '3', '966533074601'),
    ('1188914319', 'سعد بن مسفر القحطاني', 'الثاني المتوسط', '3', '966508057005'),
    ('1165099498', 'سعود بن عبد الله السحامي', 'الثاني المتوسط', '3', '966500650867'),
    ('1167770468', 'سعود ناصر سيف العريفي', 'الثاني المتوسط', '3', '966505474606'),
    ('2344500760', 'سعيد محمد باوزير', 'الثاني المتوسط', '3', '966553435135'),
    ('1164983874', 'طلال بن فهد الزهراني', 'الثاني المتوسط', '3', '966567837159'),
    ('2362260263', 'عبد الرحمن أحمد الحمدي', 'الثاني المتوسط', '3', '966503432054'),
    ('1167153434', 'عبد العزيز ماجد الزير', 'الثاني المتوسط', '3', '966500933390'),
    ('1164512566', 'عبد العزيز وليد السعران', 'الثاني المتوسط', '3', '966556660555'),
    ('1167267341', 'عبد الله بن بندر المسيحل', 'الثاني المتوسط', '3', '966500155334'),
    ('2358022958', 'عز الدين أحمد محمد سعد', 'الثاني المتوسط', '3', '966561317507'),
    ('1167515020', 'عزام خالد شلهوب بن شلهوب', 'الثاني المتوسط', '3', '966506404016'),
    ('1164747014', 'عزام فهد أحمد صلوي', 'الثاني المتوسط', '3', '966555796951'),
    ('4533080448', 'عمر وليد ياسين درويش علي', 'الثاني المتوسط', '3', '966557790508'),
    ('1163397811', 'فارس بن محمد الحربي', 'الثاني المتوسط', '3', '966583228278'),
    ('1166629798', 'يزيد بن حمد القحطاني', 'الثاني المتوسط', '3', '966505203795'),
    ('1167371093', 'يوسف عايد عواد البلوي', 'الثاني المتوسط', '3', '966531066289'),

    # الثالث المتوسط - 1
    ('1158966166', 'أصيل ناصر محمد مذكور', 'الثالث المتوسط', '1', '966552149044'),
    ('1162308223', 'خالد محمد مسدف معافا', 'الثالث المتوسط', '1', '966552680201'),
    ('1161109093', 'راكان بن عبد الله اليافعي', 'الثالث المتوسط', '1', '966504234219'),
    ('1160805899', 'زياد أحمد علي اللحيد', 'الثالث المتوسط', '1', '966504432362'),
    ('1160267124', 'سطام محمد سعود الدوسري', 'الثالث المتوسط', '1', '966555260669'),
    ('1163270869', 'سلطان أحمد صالح الفنتوخ', 'الثالث المتوسط', '1', '966555242266'),
    ('1161085236', 'ضاري صالح مهنا العازمي', 'الثالث المتوسط', '1', '966531111140'),
    ('1160585624', 'عبد العزيز عبد الله المالكي', 'الثالث المتوسط', '1', '966556999627'),
    ('1160050678', 'عبد العزيز عبد الله الأسمري', 'الثالث المتوسط', '1', '966555992269'),
    ('1161021314', 'عبد الله عبيد عبد الله العتيبي', 'الثالث المتوسط', '1', '966597882020'),
    ('1160857700', 'عبد الله فهد جلوي الشرعي', 'الثالث المتوسط', '1', '966555457732'),
    ('2502333723', 'عماد الدين إسلام دراز', 'الثالث المتوسط', '1', '966556124553'),
    ('1161418593', 'فهد عبد الرحمن العتيبي', 'الثالث المتوسط', '1', '966552270402'),
    ('1163074592', 'فيصل بن عبد المحسن العتيبي', 'الثالث المتوسط', '1', '966505552320'),
    ('1171918236', 'مازن خالد عبد ربه الزهراني', 'الثالث المتوسط', '1', '966540707365'),
    ('1158815876', 'محمد سلطان عبد العزيز العيد', 'الثالث المتوسط', '1', '966503167770'),
    ('1166075653', 'محمد مقعد ساير العتيبي', 'الثالث المتوسط', '1', '966536655992'),
    ('1160693949', 'مشاري إبراهيم المغربي', 'الثالث المتوسط', '1', '966542744245'),
    ('1160803878', 'مشاري علي موسى عقيلي', 'الثالث المتوسط', '1', '966502259722'),
    ('1161661846', 'مهند عبد الله فهد الزكري', 'الثالث المتوسط', '1', '966558794720'),
    ('1159404795', 'نواف وليد حمد الشعلان', 'الثالث المتوسط', '1', '966555798074'),
    ('1168385894', 'يوسف نايف مقعد العتيبي', 'الثالث المتوسط', '1', '966505290037'),

    # الثالث المتوسط - 2
    ('1156933093', 'تركي عبد العزيز المرزوق', 'الثالث المتوسط', '2', '966501100076'),
    ('1160223317', 'تركي عثمان العثمان', 'الثالث المتوسط', '2', '966505226153'),
    ('1159683497', 'راشد أحمد فهد آل سعيد', 'الثالث المتوسط', '2', '966555992829'),
    ('2310646332', 'راكان إبراهيم محمد عبده', 'الثالث المتوسط', '2', '966500030732'),
    ('1161397599', 'ريان ناصر عبد الرحمن المرشود', 'الثالث المتوسط', '2', '966550666662'),
    ('1163112129', 'صالح ممدوح صالح الجويعي', 'الثالث المتوسط', '2', '966549887719'),
    ('2508581135', 'عبد الرحمن محمد السيد', 'الثالث المتوسط', '2', '966507652707'),
    ('1162188872', 'عبد العزيز تركي اللهيم', 'الثالث المتوسط', '2', '966505256806'),
    ('1161340763', 'عبد العزيز عبد المحسن البديع', 'الثالث المتوسط', '2', '966554457163'),
    ('1171845140', 'عبد الله متعب الجبرين', 'الثالث المتوسط', '2', '966559898559'),
    ('1159200318', 'عبد المحسن طارق العروان', 'الثالث المتوسط', '2', '966506291294'),
    ('1162454266', 'عمر فهد محمد السقامي', 'الثالث المتوسط', '2', '966564234552'),
    ('1165152107', 'فيصل محمد صالح الفنتوخ', 'الثالث المتوسط', '2', '966556488802'),
    ('1162325722', 'ماجد فهد الكثيري', 'الثالث المتوسط', '2', '966557609015'),
    ('1162461857', 'محمد خالد المشرف', 'الثالث المتوسط', '2', '966551777559'),
    ('1161288897', 'محمد سعد العيشان', 'الثالث المتوسط', '2', '966504217660'),
    ('1156334813', 'محمد عبد العزيز الخالدي', 'الثالث المتوسط', '2', '966500091387'),
    ('1162044851', 'مهند ماجد علي كعبي', 'الثالث المتوسط', '2', '966533313738'),
    ('1158021137', 'ناصر محمد الزريعي', 'الثالث المتوسط', '2', '966505231121'),
    ('1161363443', 'نواف سعد علي القاسم', 'الثالث المتوسط', '2', '966504200199'),
    ('1162274086', 'ياسر تركي بن إسماعيل مسملي', 'الثالث المتوسط', '2', '966504261855'),

    # الثالث المتوسط - 3
    ('1163525544', 'ثامر وليد بن عبد العزيز الطليحي', 'الثالث المتوسط', '3', '966504437710'),
    ('1160712996', 'خالد عبد الرؤوف الشنيبر', 'الثالث المتوسط', '3', '966504173163'),
    ('1162560054', 'خالد عبد الله الخالدي', 'الثالث المتوسط', '3', '96658890881'),
    ('1174188647', 'خالد محمد آل درعان', 'الثالث المتوسط', '3', '966505556029'),
    ('1159155223', 'راشد سعيد آل عبد السلام', 'الثالث المتوسط', '3', '966533177877'),
    ('1174226389', 'راشد صالح الحلوان', 'الثالث المتوسط', '3', '966551112126'),
    ('1167756897', 'رواد محمد إبراهيم الخليل', 'الثالث المتوسط', '3', '966502555411'),
    ('1159394046', 'صالح بن محمد المطيري', 'الثالث المتوسط', '3', '96655097811'),
    ('1158551372', 'عبد الرحمن بدر الطريقي', 'الثالث المتوسط', '3', '966507004114'),
    ('1195815558', 'عبد الرحمن خالد محمد سعيد', 'الثالث المتوسط', '3', '966504411393'),
    ('1158561843', 'عبد الله تركي الأحمد', 'الثالث المتوسط', '3', '966542800700'),
    ('1159977451', 'عبد الله عبد الرحمن النجراني', 'الثالث المتوسط', '3', '966546416395'),
    ('1162387458', 'علي بن خالد العجيري', 'الثالث المتوسط', '3', '966505199500'),
    ('1158128270', 'علي عبد الله آل حمود', 'الثالث المتوسط', '3', '966545555161'),
    ('1161333677', 'فارس وليد الحوطي', 'الثالث المتوسط', '3', '966552805550'),
    ('1158198604', 'فهد خالد الزيد', 'الثالث المتوسط', '3', '966555198633'),
    ('1159551264', 'فيصل عبد الرحمن القحطاني', 'الثالث المتوسط', '3', '966556444082'),
    ('1186515613', 'متعب مطر الدوسري', 'الثالث المتوسط', '3', '966530545913'),
    ('1159852746', 'نواف فهد ناصر القحطاني', 'الثالث المتوسط', '3', '966556557210'),
    ('1163027392', 'يوسف عبد الله عوض العتيبي', 'الثالث المتوسط', '3', '966506371377')
]

def init_db():
    conn = sqlite3.connect("school_complaints.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS school_students (
            national_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT NOT NULL,
            section TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            grade TEXT NOT NULL,
            section TEXT NOT NULL,
            phone TEXT NOT NULL,
            complaint_text TEXT NOT NULL,
            action_taken TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    
    # تحديث وتعبئة جميع الطلاب الـ 167 في القاعدة المحلية
    cursor.executemany("""
        INSERT OR REPLACE INTO school_students (national_id, name, grade, section, phone)
        VALUES (?, ?, ?, ?, ?)
    """, ALL_SCHOOL_STUDENTS)
    conn.commit()
    return conn

conn = init_db()

# فحص حالة الاتصال بقاعدة البيانات
supabase_client = None
is_saved_status = False

if HAS_SUPABASE and SUPABASE_KEY and SUPABASE_KEY != "YOUR_SUPABASE_ANON_KEY":
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        is_saved_status = True
    except Exception:
        is_saved_status = False
else:
    is_saved_status = True

# ===================================================================
# 4. الترويسة والتنبيه الأمني للسرية
# ===================================================================
header_html = clean_html("""
<div class="saudi-header">
    <h1>🏛️ منصة سرية لشكاوى الطلاب</h1>
    <h3>متوسطة الثغر النموذجية الأهلية بالرياض</h3>
</div>
<div class="notice-box">
    <span style="font-size:24px;">⚠️</span>
    <span>تنبيه: عزيزي ولي الأمر / عزيزي الطالب هذه المنصة سرية لايطلع على شكواك غير إدارة المدرسة من مدير - وكيل.</span>
</div>
""")
st.markdown(header_html, unsafe_allow_html=True)

# ===================================================================
# 5. القائمة الجانبية ولوحة التحكم
# ===================================================================
st.sidebar.markdown("### 🎛️ لوحة التحكم")

if is_saved_status:
    st.sidebar.markdown('<div class="status-saved">🟢 تم حفظ البيانات</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-unsaved">🔴 لم يتم الحفظ</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "انتقل إلى الصفحة المطلوب العمل عليها:",
    ["الصفحة الأولى: تقديم الشكوى", "الصفحة الثانية: إدارة المدرسة", "الصفحة الثالثة: التقارير الصادرة"]
)

# ===================================================================
# الصفحة الأولى: تقديم الشكوى (للطالب وولي الأمر)
# ===================================================================
if page == "الصفحة الأولى: تقديم الشكوى":
    st.subheader("📩 تقديم شكوى جديدة")
    
    search_type = st.radio(
        "اختر طريقة تحديد الطالب:",
        ["القوائم المنسدلة (الصف ⬅️ الفصل ⬅️ الاسم)", "البحث بالاسم أو الهوية الوطنية"]
    )
    
    cursor = conn.cursor()
    selected_student = None
    
    if search_type == "القوائم المنسدلة (الصف ⬅️ الفصل ⬅️ الاسم)":
        c1, c2, c3 = st.columns(3)
        with c1:
            grade_sel = st.selectbox("اختر الصف الدراسي:", ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط"])
        with c2:
            sec_sel = st.selectbox("اختر الفصل:", ["1", "2", "3"])
        with c3:
            cursor.execute("SELECT national_id, name, phone FROM school_students WHERE grade=? AND section=? ORDER BY name ASC", (grade_sel, sec_sel))
            s_rows = cursor.fetchall()
            if s_rows:
                s_dict = {r[1]: (r[0], r[2]) for r in s_rows}
                chosen_name = st.selectbox("اختر اسم الطالب:", list(s_dict.keys()))
                if chosen_name:
                    selected_student = {
                        "name": chosen_name,
                        "national_id": s_dict[chosen_name][0],
                        "grade": grade_sel,
                        "section": sec_sel,
                        "phone": s_dict[chosen_name][1]
                    }
            else:
                st.warning("لا يوجد طلاب مسجلون في هذا الفصل حالياً.")
    else:
        q = st.text_input("🔍 ابحث عن اسم الطالب أو برقم الهوية الوطنية:")
        if q.strip():
            cursor.execute("SELECT national_id, name, grade, section, phone FROM school_students WHERE name LIKE ? OR national_id LIKE ? ORDER BY name ASC", (f'%{q.strip()}%', f'%{q.strip()}%'))
            res = cursor.fetchall()
            if res:
                r_dict = {f"{r[1]} (هوية: {r[0]} - صف {r[2]}/{r[3]})": r for r in res}
                chosen_q = st.selectbox("اختر الطالب من نتائج البحث:", list(r_dict.keys()))
                r_val = r_dict[chosen_q]
                selected_student = {
                    "national_id": r_val[0],
                    "name": r_val[1],
                    "grade": r_val[2],
                    "section": r_val[3],
                    "phone": r_val[4]
                }
            else:
                st.error("لم يتم العثور على طالب مطابق لبيانات البحث.")

    if selected_student:
        st.success(f"📌 الطالب المحدد: **{selected_student['name']}** | الهوية: `{selected_student['national_id']}` | الصف: {selected_student['grade']} (فصل {selected_student['section']})")
        
        with st.form(key="complaint_submission_form", clear_on_submit=True):
            complaint_val = st.text_area(
                "نص الشكوى",
                height=150,
                placeholder="اكتب نص الشكوى هنا بكل سرية..."
            )
            submit_btn = st.form_submit_button("📤 ارسال الشكوى لإدارة المدرسة", type="primary", use_container_width=True)
            
        if submit_btn:
            if complaint_val.strip():
                cursor.execute("""
                    INSERT INTO student_complaints (student_id, student_name, grade, section, phone, complaint_text, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'pending')
                """, (selected_student['national_id'], selected_student['name'], selected_student['grade'], selected_student['section'], selected_student['phone'], complaint_val.strip()))
                conn.commit()
                
                if supabase_client:
                    try:
                        supabase_client.table("student_complaints").insert({
                            "student_id": selected_student['national_id'],
                            "student_name": selected_student['name'],
                            "grade": selected_student['grade'],
                            "section": selected_student['section'],
                            "phone": selected_student['phone'],
                            "complaint_text": complaint_val.strip(),
                            "status": "pending"
                        }).execute()
                    except Exception:
                        pass
                
                st.balloons()
                st.success("✅ تم إرسال الشكوى بنجاح إلى إدارة المدرسة وتفريغ مربع النص.")
            else:
                st.error("يرجى كتابة نص الشكوى أولاً قبل الإرسال.")

# ===================================================================
# الصفحة الثانية: إدارة المدرسة (محمية بكلمة سر 000999)
# ===================================================================
elif page == "الصفحة الثانية: إدارة المدرسة":
    st.subheader("🔐 صفحة إدارة المدرسة (المدير / الوكيل)")
    
    if not st.session_state["admin_logged_in"]:
        pwd = st.text_input("أدخل كلمة السر للدخول (000999):", type="password", key="pwd_admin_input")
        if st.button("🔓 دخول لوحة الإدارة", type="primary"):
            if pwd == "000999":
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("كلمة السر غير صحيحة!")
    else:
        col_hdr_a, col_logout_a = st.columns([4, 1])
        with col_hdr_a:
            st.success("مرحباً بكم في لوحة إدارة الشكاوى وسجلات الطلاب.")
        with col_logout_a:
            if st.button("🔒 تسجيل الخروج", key="logout_admin_btn"):
                st.session_state["admin_logged_in"] = False
                st.rerun()
                
        tab1, tab2 = st.tabs(["📥 الشكاوى المرسلة والقرارات", "⚙️ إدارة الطلاب (إضافة / حذف / تحديث)"])
        cursor = conn.cursor()
        
        with tab1:
            cursor.execute("SELECT id, student_id, student_name, grade, section, phone, complaint_text, created_at FROM student_complaints WHERE status='pending' ORDER BY id DESC")
            pending_complaints = cursor.fetchall()
            
            if pending_complaints:
                st.info(f"يوجد ({len(pending_complaints)}) شكوى جديدة بانتظار اتخاذ الإجراء.")
                comp_map = {f"شكوى رقم #{c[0]} - الطالب: {c[2]} ({c[3]}/{c[4]})": c for c in pending_complaints}
                selected_comp_label = st.selectbox("اختر الشكوى للبدء بالمعالجة:", list(comp_map.keys()))
                c_info = comp_map[selected_comp_label]
                
                card_html = clean_html(f"""
                <div class="report-card">
                    <h4 style="color:#005A2B; margin-top:0;">تفاصيل الشكوى #{c_info[0]}</h4>
                    <p style="margin:5px 0;"><b>الطالب:</b> {c_info[2]} | <b>الهوية:</b> {c_info[1]} | <b>الصف:</b> {c_info[3]} (فصل {c_info[4]})</p>
                    <p style="margin:5px 0;"><b>جوال ولي الأمر:</b> <code>{c_info[5]}</code> | <b>تاريخ الإرسال:</b> {c_info[7]}</p>
                    <hr style="margin:12px 0;">
                    <p style="font-weight:bold; color:#1E293B; margin-bottom:5px;">📝 نص الشكوى المقدمة:</p>
                    <div style="background:#FFF9E6; border-right:5px solid #D4AF37; padding:15px; border-radius:8px; color:#453200;">{c_info[6]}</div>
                </div>
                """)
                st.markdown(card_html, unsafe_allow_html=True)
                
                action_text = st.text_area("الإدراءات المتخذة من إدارة المدرسة", height=120, placeholder="اكتب الإجراءات المتخذة من مدير / وكيل المدرسة هنا...")
                
                col_act1, col_act2 = st.columns([3, 1])
                with col_act1:
                    if st.button("✅ تم اتخاذ القرار", type="primary", use_container_width=True):
                        if action_text.strip():
                            cursor.execute("UPDATE student_complaints SET action_taken=?, status='resolved' WHERE id=?", (action_text.strip(), c_info[0]))
                            conn.commit()
                            
                            if supabase_client:
                                try:
                                    supabase_client.table("student_complaints").update({"action_taken": action_text.strip(), "status": "resolved"}).eq("id", c_info[0]).execute()
                                except Exception:
                                    pass
                                    
                            st.success("تم تسديد الشكوى بنجاح ونقل التقرير لصفحة التقارير الرسمية!")
                            st.rerun()
                        else:
                            st.error("يرجى تدوين الإجراءات المتخذة قبل الضغط على الزر.")
                
                with col_act2:
                    if st.button("🗑️ حذف الشكوى", type="secondary", use_container_width=True):
                        cursor.execute("DELETE FROM student_complaints WHERE id=?", (c_info[0],))
                        conn.commit()
                        if supabase_client:
                            try:
                                supabase_client.table("student_complaints").delete().eq("id", c_info[0]).execute()
                            except Exception:
                                pass
                        st.success(f"تم حذف الشكوى #{c_info[0]} بنجاح.")
                        st.rerun()
            else:
                st.success("لا توجد شكاوى معلقة حالياً.")
                
        with tab2:
            st.markdown("#### 🛠️ عمليات أمان السجلات")
            sub_action = st.radio("اختر العملية المطلوب تنفيذها:", ["إضافة طالب", "حذف طالب", "تحديث رقم جوال"])
            
            if sub_action == "إضافة طالب":
                with st.form("add_student_form"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        in_id = st.text_input("رقم الهوية الوطنية:")
                        in_name = st.text_input("اسم الطالب الرباعي:")
                    with col_b:
                        in_grade = st.selectbox("الصف الدراسي:", ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط"])
                        in_sec = st.selectbox("الفصل:", ["1", "2", "3"])
                        in_phone = st.text_input("رقم الجوال (مثلاً 966500000000):", value="9665")
                    
                    if st.form_submit_button("إضافة طالب جديد"):
                        if in_id and in_name and in_phone:
                            try:
                                cursor.execute("INSERT INTO school_students VALUES (?,?,?,?,?)", (in_id, in_name, in_grade, in_sec, in_phone))
                                conn.commit()
                                if supabase_client:
                                    try:
                                        supabase_client.table("school_students").insert({"national_id": in_id, "name": in_name, "grade": in_grade, "section": in_sec, "phone": in_phone}).execute()
                                    except Exception:
                                        pass
                                st.success(f"تمت إضافة الطالب {in_name} بنجاح.")
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error("رقم الهوية الوطنية موجود بالفعل بالسجل.")
                        else:
                            st.error("جميع البيانات مطلوبة.")
                            
            elif sub_action == "حذف طالب":
                cursor.execute("SELECT national_id, name FROM school_students ORDER BY name ASC")
                students_data = cursor.fetchall()
                if students_data:
                    del_map = {f"{s[1]} (هوية: {s[0]})": s[0] for s in students_data}
                    del_target = st.selectbox("اختر الطالب المراد حذفه نهائياً:", list(del_map.keys()))
                    if st.button("🗑️ حذف طالب", type="secondary"):
                        cursor.execute("DELETE FROM school_students WHERE national_id=?", (del_map[del_target],))
                        conn.commit()
                        if supabase_client:
                            try:
                                supabase_client.table("school_students").delete().eq("national_id", del_map[del_target]).execute()
                            except Exception:
                                pass
                        st.success("تم حذف الطالب من القاعدة بنجاح.")
                        st.rerun()
                        
            elif sub_action == "تحديث رقم جوال":
                cursor.execute("SELECT national_id, name, phone FROM school_students ORDER BY name ASC")
                all_st = cursor.fetchall()
                if all_st:
                    phone_map = {f"{s[1]} (الجوال الحالي: {s[2]})": (s[0], s[2]) for s in all_st}
                    chosen_up = st.selectbox("اختر الطالب لتحديث رقمه:", list(phone_map.keys()))
                    new_ph = st.text_input("رقم الجوال الجديد:", value=phone_map[chosen_up][1])
                    if st.button("🔄 تحديث رقم جوال"):
                        cursor.execute("UPDATE school_students SET phone=? WHERE national_id=?", (new_ph, phone_map[chosen_up][0]))
                        conn.commit()
                        if supabase_client:
                            try:
                                supabase_client.table("school_students").update({"phone": new_ph}).eq("national_id", phone_map[chosen_up][0]).execute()
                            except Exception:
                                pass
                        st.success("تم تحديث رقم الجوال بنجاح.")
                        st.rerun()

# ===================================================================
# الصفحة الثالثة: التقارير الصادرة (محمية بكلمة سر 000999)
# ===================================================================
elif page == "الصفحة الثالثة: التقارير الصادرة":
    st.subheader("📊 التقارير الصادرة والقرارات الإدارية")
    
    if not st.session_state["reports_logged_in"]:
        pwd_rep = st.text_input("أدخل كلمة السر للوصول للتقارير (000999):", type="password", key="pwd_rep_input")
        if st.button("🔓 دخول صفحة التقارير", type="primary"):
            if pwd_rep == "000999":
                st.session_state["reports_logged_in"] = True
                st.rerun()
            else:
                st.error("كلمة السر غير صحيحة!")
    else:
        col_hdr_r, col_logout_r = st.columns([4, 1])
        with col_hdr_r:
            st.success("تم الوصول لصفحة التقارير الإدارية والقرارات الرسمية.")
        with col_logout_r:
            if st.button("🔒 تسجيل الخروج", key="logout_rep_btn"):
                st.session_state["reports_logged_in"] = False
                st.rerun()

        cursor = conn.cursor()
        cursor.execute("SELECT id, student_id, student_name, grade, section, phone, complaint_text, action_taken, created_at FROM student_complaints WHERE status='resolved' ORDER BY id DESC")
        reports = cursor.fetchall()
        
        if reports:
            st.info(f"إجمالي التقارير الإدارية الصادرة: ({len(reports)}) تقرير رسمي.")
            for r in reports:
                r_id, s_id, s_name, grade, sec, phone, comp_text, action_taken, created_at = r
                
                wa_text = f"""📋 *تقرير إداري - متوسطة الثغر النموذجية الأهلية بالرياض*
----------------------------------------
👤 *اسم الطالب:* {s_name}
🪪 *الهوية الوطنية:* {s_id}
📚 *الصف الدراسي:* {grade} (فصل {sec})
🗓️ *تاريخ القرار:* {created_at}

📝 *نص الشكوى:*
{comp_text}

✅ *الإجراءات المتخذة من إدارة المدرسة:*
{action_taken}

----------------------------------------
👨‍💼 *وكيل شؤون الطلاب:* صالح بن عبدالله الدعجاني
👨‍💼 *وكيل شؤون المعلمين:* محمد مبروك السيد
👨‍💼 *مدير المدرسة:* إبراهيم بن موسى التميمي"""

                encoded_wa = urllib.parse.quote(wa_text)
                clean_phone = str(phone).replace("+", "").replace(" ", "").strip()
                wa_url = f"https://wa.me/{clean_phone}?text={encoded_wa}"
                
                report_html = clean_html(f"""
                <div class="report-card" id="report-{r_id}" style="direction: rtl !important; text-align: right !important;">
                    <div class="report-official-header">
                        <h2>المملكة العربية السعودية</h2>
                        <p>وزارة التعليم | الإدارة العامة للتعليم بمنطقة الرياض</p>
                        <p style="color:#005A2B; font-weight:800; font-size:16px; margin-top:5px;">متوسطة الثغر النموذجية الأهلية (بنين)</p>
                        <h3 style="color:#D4AF37; margin-top:10px; font-weight:800;">📋 تقرير قرار إداري سرّي رقم #{r_id}</h3>
                    </div>
                    
                    <div style="background:#F8FAFC; padding:15px; border-radius:10px; margin-bottom:15px; border:1px solid #E2E8F0; direction: rtl !important; text-align: right !important;">
                        <p style="margin:5px 0;"><b>اسم الطالب:</b> {s_name} &nbsp;|&nbsp; <b>الهوية الوطنية:</b> <code>{s_id}</code></p>
                        <p style="margin:5px 0;"><b>الصف الدراسي:</b> {grade} (فصل {sec}) &nbsp;|&nbsp; <b>جوال ولي الأمر:</b> <code>{phone}</code></p>
                        <p style="margin:5px 0;"><b>تاريخ التقرير:</b> {created_at}</p>
                    </div>

                    <div style="margin-bottom:15px;">
                        <p style="font-weight:bold; color:#1E293B; margin-bottom:5px;">📝 نص الشكوى المقدمة:</p>
                        <div style="background:#FFF9E6; border-right:5px solid #D4AF37; padding:12px 15px; border-radius:8px; color:#453200; direction: rtl !important; text-align: right !important;">
                            {comp_text}
                        </div>
                    </div>

                    <div style="margin-bottom:20px;">
                        <p style="font-weight:bold; color:#005A2B; margin-bottom:5px;">✅ الإجراءات المتخذة من إدارة المدرسة:</p>
                        <div style="background:#E6F4EA; border-right:5px solid #28a745; padding:12px 15px; border-radius:8px; font-weight:bold; color:#064E3B; direction: rtl !important; text-align: right !important;">
                            {action_taken}
                        </div>
                    </div>

                    <div class="signatures-block">
                        <div class="sig-item">
                            <span style="color:#64748B;">وكيل شؤون الطلاب</span><br>
                            <b style="color:#005A2B;">صالح بن عبدالله الدعجاني</b>
                        </div>
                        <div class="sig-item">
                            <span style="color:#64748B;">وكيل شؤون المعلمين</span><br>
                            <b style="color:#005A2B;">محمد مبروك السيد</b>
                        </div>
                        <div class="sig-item">
                            <span style="color:#64748B;">مدير المدرسة</span><br>
                            <b style="color:#005A2B;">إبراهيم بن موسى التميمي</b>
                        </div>
                    </div>
                </div>
                """)
                
                st.markdown(report_html, unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
                
                with col_btn1:
                    wa_btn_html = clean_html(f"""
                    <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                        <div style="background-color:#25D366; color:white; padding:10px 15px; border-radius:10px; text-align:center; font-weight:bold; box-shadow:0 3px 8px rgba(37,211,102,0.3); font-size:14px;">
                            📱 إرسال للواتساب ({phone})
                        </div>
                    </a>
                    """)
                    st.markdown(wa_btn_html, unsafe_allow_html=True)
                
                with col_btn2:
                    printable_doc = clean_html(f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="utf-8">
    <title>تقرير_إداري_{s_name}</title>
    <style>
        body {{ font-family: 'Cairo', sans-serif; padding: 30px; direction: rtl !important; text-align: right !important; background: #fff; color: #1e293b; }}
        .card {{ border: 2px solid #005A2B; padding: 30px; border-radius: 12px; direction: rtl !important; text-align: right !important; }}
        .header {{ text-align: right !important; border-bottom: 2px solid #D4AF37; border-right: 5px solid #005A2B; padding-right: 15px; padding-bottom: 15px; margin-bottom: 20px; direction: rtl !important; }}
        .header h2, .header h3, .header h4 {{ color: #005A2B; margin: 0; text-align: right !important; direction: rtl !important; }}
        .section {{ margin-bottom: 18px; padding: 15px; border-radius: 8px; text-align: right !important; direction: rtl !important; }}
        p, div, b, span {{ text-align: right !important; direction: rtl !important; }}
        .sigs {{ display: flex; justify-content: space-between; margin-top: 40px; text-align: right; border-top: 2px dashed #ccc; padding-top: 20px; }}
    </style>
</head>
<body onload="window.print()">
    <div class="card">
        <div class="header">
            <h2>المملكة العربية السعودية - وزارة التعليم</h2>
            <h3>متوسطة الثغر النموذجية الأهلية بالرياض</h3>
            <h4 style="color: #D4AF37;">تقرير قرار إداري سرّي رقم #{r_id}</h4>
        </div>
        <p><b>اسم الطالب:</b> {s_name} &nbsp;|&nbsp; <b>الهوية الوطنية:</b> {s_id} &nbsp;|&nbsp; <b>الصف:</b> {grade} (فصل {sec})</p>
        <p><b>تاريخ القرار:</b> {created_at} &nbsp;|&nbsp; <b>جوال ولي الأمر:</b> {phone}</p>
        <hr>
        <div class="section" style="background:#fff9e6; border-right: 4px solid #D4AF37;">
            <b>نص الشكوى المقدمة:</b><br>{comp_text}
        </div>
        <div class="section" style="background:#e6f4ea; border-right: 4px solid #28a745;">
            <b>الإجراء المتخذ من إدارة المدرسة:</b><br>{action_taken}
        </div>
        <div class="sigs">
            <div><b>وكيل شؤون الطلاب</b><br>صالح بن عبدالله الدعجاني</div>
            <div><b>وكيل شؤون المعلمين</b><br>محمد مبروك السيد</div>
            <div><b>مدير المدرسة</b><br>إبراهيم بن موسى التميمي</div>
        </div>
    </div>
</body>
</html>""")
                    st.download_button(
                        label="📄 طباعة / تصدير التقرير كـ PDF",
                        data=printable_doc,
                        file_name=f"تقرير_شكوى_{s_name}_{r_id}.html",
                        mime="text/html",
                        key=f"dl_rep_{r_id}",
                        use_container_width=True
                    )
                    
                with col_btn3:
                    if st.button(f"🗑️ حذف التقرير", key=f"del_rep_btn_{r_id}", type="secondary", use_container_width=True):
                        cursor.execute("DELETE FROM student_complaints WHERE id=?", (r_id,))
                        conn.commit()
                        if supabase_client:
                            try:
                                supabase_client.table("student_complaints").delete().eq("id", r_id).execute()
                            except Exception:
                                pass
                        st.success(f"تم حذف التقرير رقم #{r_id} بنجاح.")
                        st.rerun()

                st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)
        else:
            st.warning("لا توجد تقارير صادرة حتى الآن.")

# ===================================================================
# 6. حقوق التطوير والتوقيع النهائي
# ===================================================================
footer_html = clean_html("""
<div class="dev-footer">
    تصميم وتطوير: <b>محمد سامي السعيد</b>
</div>
""")
st.markdown(footer_html, unsafe_allow_html=True)
