import streamlit as st
import pandas as pd
import sqlite3
import datetime
import urllib.parse

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

# ===================================================================
# 2. تنسيقات CSS بالهوية الوطنية السعودية وتصميم أنيق للجوال
# ===================================================================
st.markdown("""
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
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
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
    
    /* اخفاء القائمة الجانبية تلقائياً في الجوال عند الاختيار */
    @media (max-width: 768px) {
        .saudi-header h1 { font-size: 20px; }
        .saudi-header h3 { font-size: 14px; }
        .signatures-block { flex-direction: column; gap: 12px; }
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# 3. إعداد وقواعد البيانات (Supabase + SQLite المحلية الاحتياطية)
# ===================================================================
# القيم المباشرة مع القراءة التلقائية من st.secrets في Streamlit
SUPABASE_URL = "https://yathpzoxjfpgahkbjzgz.supabase.co"
SUPABASE_KEY = "sb_publishable_4Igw4yxTyqcZzSvXei6TEg_cuxhLKcE"

try:
    if "supabase" in st.secrets:
        SUPABASE_URL = st.secrets["supabase"].get("url", SUPABASE_URL)
        SUPABASE_KEY = st.secrets["supabase"].get("key", SUPABASE_KEY)
except Exception:
    pass

def init_db():
    conn = sqlite3.connect("school_complaints.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            national_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT NOT NULL,
            section TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
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
    
    # تعبئة النظام ببيانات حقيقية نموذجية من سجلات طلاب متوسطة الثغر
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        sample_students = [
            ('1167628468', 'إبراهيم بن محمد بن علي الوهيبي', 'الأول المتوسط', '1', '966504158122'),
            ('2395664317', 'بلال عبدالرزاق عيسى العيسى', 'الأول المتوسط', '1', '966507448712'),
            ('1170348286', 'الوليد بن خالد بن فهد العتيبي', 'الأول المتوسط', '2', '966558522229'),
            ('1163760935', 'أحمد بن سامي بن أحمد العمران', 'الثاني المتوسط', '1', '966551501503'),
            ('1165495258', 'عبدالله سامي سعد الحوشاني', 'الثاني المتوسط', '2', '966555219086'),
            ('1166911709', 'ثامر عمر إبراهيم عثمان', 'الثاني المتوسط', '3', '966538384444'),
            ('1163525544', 'ثامر وليد بن عبدالعزيز الطليحي', 'الثالث المتوسط', '3', '966504437710'),
            ('1158966166', 'أصيل ناصر محمد مذكور', 'الثالث المتوسط', '1', '966552149044')
        ]
        cursor.executemany("INSERT INTO students VALUES (?,?,?,?,?)", sample_students)
        conn.commit()
    return conn

conn = init_db()

# فحص حالة الحفظ والاتصال بقاعدة البيانات
supabase_client = None
is_saved_status = False

if HAS_SUPABASE and SUPABASE_KEY and SUPABASE_KEY != "YOUR_SUPABASE_ANON_KEY":
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        is_saved_status = True
    except Exception:
        is_saved_status = False
else:
    # الاعتماد على قاعدة البيانات المحلية لضمان حفظ البيانات
    is_saved_status = True

# ===================================================================
# 4. الترويسة والتنبيه الأمني للسرية
# ===================================================================
st.markdown("""
<div class="saudi-header">
    <h1>🏛️ منصة سرية لشكاوى الطلاب</h1>
    <h3>متوسطة الثغر النموذجية الأهلية بالرياض</h3>
</div>
<div class="notice-box">
    <span style="font-size:24px;">⚠️</span>
    <span>تنبيه: عزيزي ولي الأمر / عزيزي الطالب هذه المنصة سرية لايطلع على شكواك غير إدارة المدرسة من مدير - وكيل.</span>
</div>
""", unsafe_allow_html=True)

# ===================================================================
# 5. القائمة الجانبية ولوحة التحكم
# ===================================================================
st.sidebar.markdown("### 🎛️ لوحة التحكم")

# إظهار زر حالة حفظ البيانات بلون أخضر أو أحمر
if is_saved_status:
    st.sidebar.markdown('<div class="status-saved">🟢 تم حفظ البيانات</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-unsaved">🔴 لم يتم الحفظ</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

# اختيار الصفحة من لوحة التحكم
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
            cursor.execute("SELECT national_id, name, phone FROM students WHERE grade=? AND section=?", (grade_sel, sec_sel))
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
            cursor.execute("SELECT national_id, name, grade, section, phone FROM students WHERE name LIKE ? OR national_id LIKE ?", (f'%{q.strip()}%', f'%{q.strip()}%'))
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

    # ظهور مربع نص الشكوى عند اختيار الطالب
    if selected_student:
        st.success(f"📌 الطالب المحدد: **{selected_student['name']}** | الهوية: `{selected_student['national_id']}` | الصف: {selected_student['grade']} (فصل {selected_student['section']})")
        
        # إدارة حالة نص الشكوى للتفريغ التلقائي عقب الإرسال
        if "complaint_text_key" not in st.session_state:
            st.session_state["complaint_text_key"] = ""
            
        complaint_val = st.text_area(
            "نص الشكوى",
            value=st.session_state["complaint_text_key"],
            height=150,
            placeholder="اكتب نص الشكوى هنا بكل سرية..."
        )
        
        if st.button("📤 ارسال الشكوى لإدارة المدرسة", type="primary", use_container_width=True):
            if complaint_val.strip():
                # حفظ الشكوى في SQLite المحلية
                cursor.execute("""
                    INSERT INTO complaints (student_id, student_name, grade, section, phone, complaint_text, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'pending')
                """, (selected_student['national_id'], selected_student['name'], selected_student['grade'], selected_student['section'], selected_student['phone'], complaint_val.strip()))
                conn.commit()
                
                # حفظ الشكوى في Supabase إن أمكن
                if supabase_client:
                    try:
                        supabase_client.table("complaints").insert({
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
                
                # تفريغ مربع النص
                st.session_state["complaint_text_key"] = ""
                st.balloons()
                st.success("✅ تم إرسال الشكوى بنجاح إلى إدارة المدرسة وتفريغ مربع النص.")
                st.rerun()
            else:
                st.error("يرجى كتابة نص الشكوى أولاً قبل الإرسال.")

# ===================================================================
# الصفحة الثانية: إدارة المدرسة (محمية بكلمة سر 000999)
# ===================================================================
elif page == "الصفحة الثانية: إدارة المدرسة":
    st.subheader("🔐 صفحة إدارة المدرسة (المدير / الوكيل)")
    
    pwd = st.text_input("أدخل كلمة السر للدخول:", type="password")
    
    if pwd == "000999":
        st.success("مرحباً بكم في لوحة إدارة الشكاوى وسجلات الطلاب.")
        
        tab1, tab2 = st.tabs(["📥 الشكاوى المرسلة والقرارات", "⚙️ إدارة الطلاب (إضافة / حذف / تحديث)"])
        cursor = conn.cursor()
        
        with tab1:
            cursor.execute("SELECT id, student_name, grade, section, phone, complaint_text, created_at FROM complaints WHERE status='pending' ORDER BY id DESC")
            pending_complaints = cursor.fetchall()
            
            if pending_complaints:
                st.info(f"يوجد ({len(pending_complaints)}) شكوى جديدة بانتظار اتخاذ الإجراء.")
                comp_map = {f"شكوى رقم #{c[0]} - الطالب: {c[1]} ({c[2]}/{c[3]})": c for c in pending_complaints}
                selected_comp_label = st.selectbox("اختر الشكوى للبدء بالمعالجة:", list(comp_map.keys()))
                c_info = comp_map[selected_comp_label]
                
                st.markdown(f"""
                <div class="report-card">
                    <h4 style="color:#005A2B;">تفاصيل الشكوى #{c_info[0]}</h4>
                    <p><b>الطالب:</b> {c_info[1]} | <b>الصف:</b> {c_info[2]} (فصل {c_info[3]}) | <b>جوال ولي الأمر:</b> {c_info[4]}</p>
                    <p><b>تاريخ الإرسال:</b> {c_info[6]}</p>
                    <hr>
                    <p><b>نص الشكوى المقدمة:</b></p>
                    <div style="background:#F8FAFC; padding:15px; border-radius:8px; border-right:4px solid #005A2B;">{c_info[5]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                action_text = st.text_area("الإدراءات المتخذة من إدارة المدرسة", height=120, placeholder="اكتب الإجراءات المتخذة من مدير / وكيل المدرسة هنا...")
                
                if st.button("تم اتخاذ القرار", type="primary"):
                    if action_text.strip():
                        cursor.execute("UPDATE complaints SET action_taken=?, status='resolved' WHERE id=?", (action_text.strip(), c_info[0]))
                        conn.commit()
                        
                        if supabase_client:
                            try:
                                supabase_client.table("complaints").update({"action_taken": action_text.strip(), "status": "resolved"}).eq("id", c_info[0]).execute()
                            except Exception:
                                pass
                                
                        st.success("تم تسديد الشكوى بنجاح ونقل التقرير لصفحة التقارير الرسمية!")
                        st.rerun()
                    else:
                        st.error("يرجى تدوين الإجراءات المتخذة قبل الضغط على الزر.")
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
                        in_phone = st.text_input("رقم الجوال (بالصيغة الدولية مثلاً 966500000000):", value="9665")
                    
                    if st.form_submit_button("إضافة طالب جديد"):
                        if in_id and in_name and in_phone:
                            try:
                                cursor.execute("INSERT INTO students VALUES (?,?,?,?,?)", (in_id, in_name, in_grade, in_sec, in_phone))
                                conn.commit()
                                st.success(f"تمت إضافة الطالب {in_name} بنجاح.")
                            except sqlite3.IntegrityError:
                                st.error("رقم الهوية الوطنية موجود بالفعل بالسجل.")
                        else:
                            st.error("جميع البيانات مطلوبة.")
                            
            elif sub_action == "حذف طالب":
                cursor.execute("SELECT national_id, name FROM students")
                students_data = cursor.fetchall()
                if students_data:
                    del_map = {f"{s[1]} (هوية: {s[0]})": s[0] for s in students_data}
                    del_target = st.selectbox("اختر الطالب المراد حذفه نهائياً:", list(del_map.keys()))
                    if st.button("حذف طالب", type="secondary"):
                        cursor.execute("DELETE FROM students WHERE national_id=?", (del_map[del_target],))
                        conn.commit()
                        st.success("تم حذف الطالب من القاعدة بنجاح.")
                        st.rerun()
                        
            elif sub_action == "تحديث رقم جوال":
                cursor.execute("SELECT national_id, name, phone FROM students")
                all_st = cursor.fetchall()
                if all_st:
                    phone_map = {f"{s[1]} (الجوال الحالي: {s[2]})": (s[0], s[2]) for s in all_st}
                    chosen_up = st.selectbox("اختر الطالب لتحديث رقمه:", list(phone_map.keys()))
                    new_ph = st.text_input("رقم الجوال الجديد:", value=phone_map[chosen_up][1])
                    if st.button("تحديث رقم جوال"):
                        cursor.execute("UPDATE students SET phone=? WHERE national_id=?", (new_ph, phone_map[chosen_up][0]))
                        conn.commit()
                        st.success("تم تحديث رقم الجوال بنجاح.")
                        st.rerun()

    elif pwd:
        st.error("كلمة السر غير صحيحة!")

# ===================================================================
# الصفحة الثالثة: التقارير الصادرة (محمية بكلمة سر 000999)
# ===================================================================
elif page == "الصفحة الثالثة: التقارير الصادرة":
    st.subheader("📊 التقارير الصادرة والقرارات الإدارية")
    
    pwd_rep = st.text_input("أدخل كلمة السر للوصول للتقارير:", type="password")
    
    if pwd_rep == "000999":
        cursor = conn.cursor()
        cursor.execute("SELECT id, student_name, grade, section, phone, complaint_text, action_taken, created_at FROM complaints WHERE status='resolved' ORDER BY id DESC")
        reports = cursor.fetchall()
        
        if reports:
            st.info(f"إجمالي التقارير الإدارية الصادرة: ({len(reports)}) تقارير.")
            for r in reports:
                # إنشاء رابط واتساب لإرسال التقرير للطالب
                wa_msg = f"تقرير إداري من متوسطة الثغر النموذجية الأهلية\nالطالب: {r[1]}\nالصف: {r[2]} / فصل {r[3]}\nنص الشكوى: {r[5]}\nالإجراء المتخذ: {r[6]}"
                wa_url = f"https://wa.me/{r[4]}?text={urllib.parse.quote(wa_msg)}"
                
                st.markdown(f"""
                <div class="report-card">
                    <h3 style="color:#005A2B; text-align:center; margin-bottom:4px;">📋 تقرير إداري مفصل #{r[0]}</h3>
                    <p style="text-align:center; color:#64748B; font-weight:bold;">متوسطة الثغر النموذجية الأهلية بالرياض</p>
                    <hr>
                    <p><b>اسم الطالب:</b> {r[1]} &nbsp;|&nbsp; <b>الصف:</b> {r[2]} (فصل {r[3]}) &nbsp;|&nbsp; <b>تاريخ التقرير:</b> {r[7]}</p>

                    <p><b>نص الشكوى المقدمة:</b></p>
                    <div style="background:#F1F5F9; padding:12px; border-radius:8px; margin-bottom:12px;">{r[5]}</div>

                    <p><b>الإدراءات المتخذة من إدارة المدرسة:</b></p>
                    <div style="background:#E6F4EA; border-right:5px solid #28a745; padding:12px; border-radius:8px; font-weight:bold; color:#064E3B; margin-bottom:15px;">{r[6]}</div>

                    <div style="text-align:center; margin-top:15px;">
                        <a href="{wa_url}" target="_blank" style="background-color:#25D366; color:white; padding:10px 22px; border-radius:30px; text-decoration:none; font-weight:bold; display:inline-block; box-shadow:0 3px 8px rgba(37,211,102,0.3);">
                            📱 إرسال التقرير إلى واتساب الطالب ({r[4]})
                        </a>
                    </div>

                    <div class="signatures-block">
                        <div class="sig-item">
                            <b>وكيل شؤون الطلاب</b><br>
                            صالح بن عبدالله الدعجاني
                        </div>
                        <div class="sig-item">
                            <b>وكيل شؤون المعلمين</b><br>
                            محمد مبروك السيد
                        </div>
                        <div class="sig-item">
                            <b>مدير المدرسة</b><br>
                            إبراهيم بن موسى التميمي
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("لا توجد تقارير صادرة حتى الآن.")
            
    elif pwd_rep:
        st.error("كلمة السر غير صحيحة!")

# ===================================================================
# 6. حقوق التطوير والتوقيع النهائي
# ===================================================================
st.markdown("""
<div class="dev-footer">
    تصميم وتطوير: <b>محمد سامي السعيد</b>
</div>
""", unsafe_allow_html=True)
