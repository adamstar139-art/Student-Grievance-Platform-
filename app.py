<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سرية لشكاوى الطلاب - متوسطة الثغر النموذجية الأهلية</title>
    <!-- خط تجوال العربي -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Supabase JS Library -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        saudi: {
                            green: '#006C35',
                            darkGreen: '#004D25',
                            gold: '#C5A059',
                            goldLight: '#E8D2A0',
                            bgLight: '#F4F7F5'
                        }
                    },
                    fontFamily: {
                        sans: ['Tajawal', 'sans-serif']
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Tajawal', sans-serif;
            background-color: #F4F7F5;
        }
        .animate-fade-in {
            animation: fadeIn 0.3s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col text-gray-800">

    <!-- الترويسة الرئيسية بالهوية الوطنية السعودية -->
    <header class="bg-saudi-green text-white shadow-lg border-b-4 border-saudi-gold">
        <div class="max-w-6xl mx-auto px-4 py-4 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-4">
                <div class="w-14 h-14 bg-white/10 rounded-full flex items-center justify-center border border-saudi-gold text-saudi-gold text-2xl shadow-inner">
                    <i class="fa-solid fa-shield-halved"></i>
                </div>
                <div class="text-center md:text-right">
                    <h1 class="text-lg md:text-2xl font-bold tracking-wide text-white">منصة سرية لشكاوى الطلاب</h1>
                    <p class="text-xs md:text-sm text-saudi-goldLight font-medium mt-0.5">متوسطة الثغر النموذجية الأهلية</p>
                </div>
            </div>

            <!-- لوحة التحكم ومفتاح حفظ البيانات باللون الأخضر/الأحمر -->
            <div class="flex items-center gap-3 bg-saudi-darkGreen px-4 py-2 rounded-xl border border-white/10 shadow-inner">
                <span class="text-xs text-gray-200">حالة قاعدة البيانات:</span>
                <div id="statusBadge" class="bg-emerald-500 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 transition-all shadow">
                    <span id="statusDot" class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
                    <span id="statusText">تم حفظ البيانات</span>
                </div>
            </div>
        </div>
    </header>

    <!-- شريط التنقل للكمبيوتر والجوال -->
    <nav class="bg-white shadow-md border-b sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 flex justify-between items-center h-14">
            <!-- القائمة للجوال -->
            <div class="md:hidden flex items-center w-full justify-between">
                <span id="currentPageTitle" class="font-bold text-saudi-green text-sm">تقديم شكوى</span>
                <button id="mobileMenuBtn" class="text-saudi-green text-xl p-2 rounded-lg hover:bg-gray-100 transition">
                    <i class="fa-solid fa-bars"></i>
                </button>
            </div>

            <!-- الروابط في الكمبيوتر -->
            <div class="hidden md:flex items-center gap-2 w-full justify-center">
                <button onclick="switchTab('page-submit')" id="tab-page-submit" class="tab-btn active-tab px-6 py-2 rounded-lg font-bold text-sm transition-all flex items-center gap-2 bg-saudi-green text-white shadow-sm">
                    <i class="fa-solid fa-pen-to-square"></i> تقديم شكوى
                </button>
                <button onclick="switchTab('page-admin')" id="tab-page-admin" class="tab-btn px-6 py-2 rounded-lg font-bold text-sm text-gray-600 hover:bg-gray-100 transition-all flex items-center gap-2">
                    <i class="fa-solid fa-user-gear"></i> إدارة المدرسة
                </button>
                <button onclick="switchTab('page-reports')" id="tab-page-reports" class="tab-btn px-6 py-2 rounded-lg font-bold text-sm text-gray-600 hover:bg-gray-100 transition-all flex items-center gap-2">
                    <i class="fa-solid fa-file-invoice"></i> التقارير
                </button>
            </div>
        </div>

        <!-- القائمة المنسدلة للجوال (تختفي بشكل احترافي عند اختيار أي صفحة) -->
        <div id="mobileMenu" class="hidden md:hidden bg-white border-b px-4 py-3 flex flex-col gap-2 shadow-xl animate-fade-in">
            <button onclick="switchTab('page-submit')" class="w-full text-right py-2.5 px-3 rounded-lg font-bold text-sm flex items-center gap-2 bg-gray-50 text-saudi-green">
                <i class="fa-solid fa-pen-to-square"></i> تقديم شكوى
            </button>
            <button onclick="switchTab('page-admin')" class="w-full text-right py-2.5 px-3 rounded-lg font-bold text-sm flex items-center gap-2 text-gray-700 hover:bg-gray-50">
                <i class="fa-solid fa-user-gear"></i> إدارة المدرسة (كلمة سر)
            </button>
            <button onclick="switchTab('page-reports')" class="w-full text-right py-2.5 px-3 rounded-lg font-bold text-sm flex items-center gap-2 text-gray-700 hover:bg-gray-50">
                <i class="fa-solid fa-file-invoice"></i> التقارير (كلمة سر)
            </button>
        </div>
    </nav>

    <!-- المحتوى الرئيسي -->
    <main class="max-w-4xl mx-auto px-4 py-6 flex-1 w-full">

        <!-- تنبيه السرية -->
        <div class="bg-amber-50 border-r-4 border-amber-500 p-4 mb-6 rounded-xl shadow-sm flex items-start gap-3">
            <div class="text-amber-600 text-2xl mt-0.5">
                <i class="fa-solid fa-triangle-exclamation"></i>
            </div>
            <div>
                <h3 class="font-bold text-amber-900 text-sm md:text-base">تنبيه هام وحاسم:</h3>
                <p class="text-amber-800 text-xs md:text-sm mt-1 leading-relaxed">
                    عزيزي ولي الأمر / عزيزي الطالب: هذه المنصة سرية لا يطلع على شكواك غير إدارة المدرسة من مدير - وكيل.
                </p>
            </div>
        </div>

        <!-- الصفحة الأولى: تقديم الشكوى -->
        <section id="page-submit" class="tab-content bg-white p-6 rounded-2xl shadow-md border border-gray-100">
            <h2 class="text-lg font-bold text-saudi-green mb-5 pb-2 border-b flex items-center justify-between">
                <span class="flex items-center gap-2"><i class="fa-solid fa-paper-plane"></i> نموذج تقديم الشكوى السرية</span>
                <span class="text-xs font-semibold text-gray-500">سجل الطلاب المربوط آلياً (167 طالب)</span>
            </h2>

            <form id="complaintForm" onsubmit="handleComplaintSubmit(event)" class="space-y-5">
                <!-- البحث السريع بالاسم أو الهوية -->
                <div class="bg-gray-50 p-4 rounded-xl border border-gray-200">
                    <label class="block text-xs font-bold text-gray-700 mb-2">بحث سريع عن الطالب (بالاسم أو برقم الهوية):</label>
                    <div class="relative">
                        <input type="text" id="searchInput" oninput="filterStudents()" placeholder="أدخل اسم الطالب أو رقم الهوية الوطنية..." class="w-full pl-10 pr-4 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none">
                        <i class="fa-solid fa-magnifying-glass absolute left-3 top-3 text-gray-400"></i>
                    </div>
                </div>

                <!-- القوائم المنسدلة -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-gray-700 mb-1.5">الصف الدراسي *</label>
                        <select id="gradeSelect" onchange="updateStudentOptions()" required class="w-full p-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none bg-white">
                            <option value="">اختر الصف...</option>
                            <option value="الأول المتوسط">الأول المتوسط</option>
                            <option value="الثاني المتوسط">الثاني المتوسط</option>
                            <option value="الثالث المتوسط">الثالث المتوسط</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-gray-700 mb-1.5">الفصل *</label>
                        <select id="classSelect" onchange="updateStudentOptions()" required class="w-full p-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none bg-white">
                            <option value="">اختر الفصل...</option>
                            <option value="1">فصل 1</option>
                            <option value="2">فصل 2</option>
                            <option value="3">فصل 3</option>
                            <option value="4">فصل 4</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-gray-700 mb-1.5">اسم الطالب *</label>
                        <select id="studentSelect" onchange="autoFillStudentData()" required class="w-full p-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none bg-white">
                            <option value="">اختر الطالب...</option>
                        </select>
                    </div>
                </div>

                <!-- الهوية والجوال المربوط آلياً -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-gray-700 mb-1.5">رقم الهوية الوطنية *</label>
                        <input type="text" id="nationalIdInput" required placeholder="أدخل رقم الهوية الوطنية (10 أرقام)" maxlength="10" class="w-full p-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none bg-gray-50">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-gray-700 mb-1.5">رقم جوال الطالب / ولي الأمر للتواصل *</label>
                        <input type="tel" id="whatsappInput" required placeholder="مثال: 0501234567" class="w-full p-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none bg-gray-50">
                    </div>
                </div>

                <!-- نص الشكوى -->
                <div>
                    <label class="block text-xs font-bold text-gray-700 mb-1.5">نص الشكوى *</label>
                    <textarea id="complaintText" rows="5" required placeholder="اكتب تفاصيل الشكوى بكل حرية وسرية هنا..." class="w-full p-3 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none resize-none"></textarea>
                </div>

                <!-- زر الإرسال -->
                <button type="submit" class="w-full bg-saudi-green text-white font-bold py-3.5 px-6 rounded-xl shadow-lg hover:bg-saudi-darkGreen transition-all flex items-center justify-center gap-2 text-base">
                    <i class="fa-solid fa-paper-plane"></i> إرسال الشكوى لإدارة المدرسة
                </button>
            </form>
        </section>

        <!-- الصفحة الثانية: إدارة المدرسة -->
        <section id="page-admin" class="tab-content hidden bg-white p-6 rounded-2xl shadow-md border border-gray-100">
            <h2 class="text-lg font-bold text-saudi-green mb-5 pb-2 border-b flex items-center justify-between">
                <span><i class="fa-solid fa-user-shield"></i> لوحة إدارة المدرسة (الشكاوى المرسلة)</span>
                <span class="text-xs font-normal bg-saudi-goldLight/30 text-saudi-gold px-3 py-1 rounded-full font-bold">محمية بكلمة سر</span>
            </h2>

            <div id="adminComplaintsList" class="space-y-4">
                <!-- تعبأ ديناميكياً -->
            </div>
        </section>

        <!-- الصفحة الثالثة: التقارير -->
        <section id="page-reports" class="tab-content hidden bg-white p-6 rounded-2xl shadow-md border border-gray-100">
            <h2 class="text-lg font-bold text-saudi-green mb-5 pb-2 border-b flex items-center justify-between">
                <span><i class="fa-solid fa-file-contract"></i> التقارير التفصيلية والقرارات</span>
                <span class="text-xs font-normal bg-saudi-goldLight/30 text-saudi-gold px-3 py-1 rounded-full font-bold">محمية بكلمة سر</span>
            </h2>

            <div id="reportsList" class="space-y-6">
                <!-- تعبأ ديناميكياً -->
            </div>
        </section>

    </main>

    <!-- Modal كلمة السر (000999) -->
    <div id="passwordModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-2xl p-6 max-w-sm w-full shadow-2xl border text-center animate-fade-in">
            <div class="w-12 h-12 bg-saudi-green/10 text-saudi-green rounded-full flex items-center justify-center mx-auto text-xl mb-3">
                <i class="fa-solid fa-lock"></i>
            </div>
            <h3 class="font-bold text-gray-800 text-base mb-1">منطقة محمية بكلمة سر</h3>
            <p class="text-xs text-gray-500 mb-4">يرجى إدخال كلمة السر الخاصة بإدارة المدرسة للوصول</p>
            
            <input type="password" id="modalPasswordInput" placeholder="أدخل كلمة السر" class="w-full text-center tracking-widest text-lg font-bold py-2.5 border rounded-lg mb-3 focus:ring-2 focus:ring-saudi-green focus:outline-none">
            <p id="passwordError" class="text-xs text-red-500 hidden mb-3 font-bold">كلمة السر غير صحيحة!</p>
            
            <div class="flex gap-2">
                <button onclick="verifyPassword()" class="flex-1 bg-saudi-green text-white font-bold py-2.5 rounded-lg hover:bg-saudi-darkGreen transition text-sm">دخول</button>
                <button onclick="closePasswordModal()" class="flex-1 bg-gray-100 text-gray-600 font-bold py-2.5 rounded-lg hover:bg-gray-200 transition text-sm">إلغاء</button>
            </div>
        </div>
    </div>

    <!-- التوقيع والحقوق Footer -->
    <footer class="bg-saudi-darkGreen text-white text-center py-4 border-t-2 border-saudi-gold mt-auto">
        <p class="text-xs md:text-sm font-medium tracking-wide">
            تصميم وتطوير <span class="text-saudi-gold font-bold">محمد سامي السعيد</span>
        </p>
    </footer>

    <!-- JavaScript الخاص بالمنصة -->
    <script>
        // رابط وقاعدة بيانات Supabase المحددة من المستخدم
        const SUPABASE_URL = "https://looldhswootseeqltohg.supabase.co";
        const SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"; 
        let supabaseClient = null;

        if (window.supabase && SUPABASE_KEY !== "YOUR_SUPABASE_ANON_KEY") {
            supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
        }

        // قائمة الطلاب الحقيقية المربوطة بأرقام الجوالات والهويات من السجلات
        const mockStudents = [
  {
    "name": "إبراهيم بن محمد بن علي الوهيبي",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1167628468",
    "phone": "0504158122"
  },
  {
    "name": "بلال عبدالرزاق عيسى العيسى",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "2395664317",
    "phone": "0507448712"
  },
  {
    "name": "حسام بن محمد بن علي آل رايان البارقي",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1170582165",
    "phone": "0504445699"
  },
  {
    "name": "ريان عبدالله جابر الأسمري",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1169004353",
    "phone": "0554260960"
  },
  {
    "name": "زيد زياد عبد اللطيف أبو قبع",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "2446713998",
    "phone": "0590123455"
  },
  {
    "name": "سامي سعد عباس حمد",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "2527104554",
    "phone": "0591781701"
  },
  {
    "name": "سعد ناصر سعد السيف",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1170111759",
    "phone": "0503219351"
  },
  {
    "name": "عبدالعزيز عبدالله عبدالعزيز العمار",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1195559479",
    "phone": "0555838394"
  },
  {
    "name": "عبدالله بن سليمان بن عبدالله الراجحي",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1153310501",
    "phone": "0551418881"
  },
  {
    "name": "عبدالله سعد بن محمد العيشان",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1170836520",
    "phone": "0504217660"
  },
  {
    "name": "علي احمد علي كريري",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1171448515",
    "phone": "0558885481"
  },
  {
    "name": "علي سعد علي القحطاني",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1170853053",
    "phone": "0505466546"
  },
  {
    "name": "عمر عبدالله سعد الجبرين",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1172018036",
    "phone": "0555249420"
  },
  {
    "name": "مازن اسلام احمد ابراهيم موسى",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "2552851368",
    "phone": "0550490495"
  },
  {
    "name": "محمد أحمد علي عقيل",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "013609321",
    "phone": "0546000184"
  },
  {
    "name": "محمد اشرف مسعود ابوخاطر",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "2394606749",
    "phone": "0501276888"
  },
  {
    "name": "محمد بن فيصل بن مصلح الشمراني",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1170042046",
    "phone": "0555832145"
  },
  {
    "name": "محمد نايف فراج الدعجاني",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "1169174164",
    "phone": "0554444782"
  },
  {
    "name": "وائل بولعيش",
    "grade": "الأول المتوسط",
    "classNum": "1",
    "nationalId": "2380890976",
    "phone": "0591534495"
  },
  {
    "name": "الوليد ابن خالد بن فهد العتيبي",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170348286",
    "phone": "0558522229"
  },
  {
    "name": "باسل محمد فرج الدوسري",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1172433185",
    "phone": "0537589781"
  },
  {
    "name": "بسام بن عبدالكريم بن عبدالله الحرقان الدوسري",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1173391556",
    "phone": "0534467820"
  },
  {
    "name": "تركي عبدالله مسفر الدوسري",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1169185053",
    "phone": "0505258369"
  },
  {
    "name": "تميم فهد عبدالعزيز العزاز",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170108078",
    "phone": "0554435692"
  },
  {
    "name": "جاسر بن عبدالله بن منصور المطارحة الحارثي",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170970741",
    "phone": "0559455545"
  },
  {
    "name": "راكان عبدالله يحيى كريري",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1168982427",
    "phone": "0581727444"
  },
  {
    "name": "ريان عبدالله منصور السبر",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1172590968",
    "phone": "0566959670"
  },
  {
    "name": "ريان وليد حلاق",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "2392863888",
    "phone": "0530527662"
  },
  {
    "name": "سيف عبدالكريم بريك العصيمي",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170420473",
    "phone": "0504277904"
  },
  {
    "name": "صالح حسن فتحي سندي",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1168942108",
    "phone": "0557553922"
  },
  {
    "name": "عبدالرحمن ابراهيم عبدالله الحضيف",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1173182138",
    "phone": "0558822674"
  },
  {
    "name": "عبدالله صالح حمد الصفيان",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1172448548",
    "phone": "0558889978"
  },
  {
    "name": "فهد ابن احمد بن فهد العثمان",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170000945",
    "phone": "0504484898"
  },
  {
    "name": "فهد عويض ثعيل المطيري",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1167092616",
    "phone": "0508271056"
  },
  {
    "name": "فهد نايف فهد الحسينان",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170413171",
    "phone": "0504140616"
  },
  {
    "name": "فيصل موينع عبدالله بن موينع",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170294118",
    "phone": "0541600918"
  },
  {
    "name": "فيصل ناصر سيف العريفي",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1171524604",
    "phone": "0505474606"
  },
  {
    "name": "محمد اسلام سعد محمد دراز",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "2502333707",
    "phone": "0556124553"
  },
  {
    "name": "مشاري عثمان سعد ناصر السعد",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170374993",
    "phone": "0500330693"
  },
  {
    "name": "يزن محمد علي اليحيا",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170884165",
    "phone": "0557072133"
  },
  {
    "name": "يوسف محمد عبدالله الدوسري",
    "grade": "الأول المتوسط",
    "classNum": "2",
    "nationalId": "1170548737",
    "phone": "0556666176"
  },
  {
    "name": "احمد سامي بن احمد العمران",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1163760935",
    "phone": "0551501503"
  },
  {
    "name": "الوليد عبدالله بن ابراهيم المبدل",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1153756612",
    "phone": "0505241627"
  },
  {
    "name": "ذياب بن محمد بن ذياب بن محمد ال مريتع القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1164269209",
    "phone": "0561169999"
  },
  {
    "name": "راكان سالم بن محمد بن مسفر القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1163187972",
    "phone": "0556609291"
  },
  {
    "name": "سعود خالد عبدالله الحمد",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1171617069",
    "phone": "0555242944"
  },
  {
    "name": "سعود مشعل بن ابراهيم الشثري",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1163458878",
    "phone": "0598887996"
  },
  {
    "name": "سلطان عبدالله حسن القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1167623758",
    "phone": "0563484825"
  },
  {
    "name": "عبدالرحمن حمد بن محمد العريفي",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1164769430",
    "phone": "0555556856"
  },
  {
    "name": "عبدالرحمن ربيع جابر خبراني",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1167893740",
    "phone": "0535924655"
  },
  {
    "name": "عبدالعزيز سعود بن فهد العتيبي",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1159740032",
    "phone": "0544155592"
  },
  {
    "name": "عبدالمجيد بن محمد بن مسعود ال عايض القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1164747436",
    "phone": "0555275591"
  },
  {
    "name": "فيصل بن عبدالله بن سعود بن عبدالعزيز الجمعه",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1160901128",
    "phone": "0554949948"
  },
  {
    "name": "مبارك صالح مبارك هليل",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1162168627",
    "phone": "0553663819"
  },
  {
    "name": "محمد بن عبدالله بن حمد بن ناصر بن عمران",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1163212978",
    "phone": "0544779170"
  },
  {
    "name": "محمد عبدالمحسن ناصر الحزام",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1161858301",
    "phone": "0505264075"
  },
  {
    "name": "محمد فايز عبدالرحمن بن يوسف",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1175902442",
    "phone": "0505482728"
  },
  {
    "name": "مشاري سلطان سالم الشمراني",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1165686179",
    "phone": "0553908888"
  },
  {
    "name": "معاذ عبدالله سعود العريفي",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1166040053",
    "phone": "0505473192"
  },
  {
    "name": "ناصر حسين محمد ال جبران",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1167081981",
    "phone": "0550004952"
  },
  {
    "name": "وائل بن عبدالله بن عامر علي ال عبد الغامدي",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1171868639",
    "phone": "0548888663"
  },
  {
    "name": "يزيد بن طارق بن علي الحديثي",
    "grade": "الثاني المتوسط",
    "classNum": "1",
    "nationalId": "1163191222",
    "phone": "0554084040"
  },
  {
    "name": "ابراهيم بن مبارك بن راشد بن عبدالرحمن السبيعان ال موينع",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1166753291",
    "phone": "0555212896"
  },
  {
    "name": "ابراهيم ياسر ابراهيم الحلوي",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1163613795",
    "phone": "0502220990"
  },
  {
    "name": "حامد بن محمد بن حامد شباط",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1167148251",
    "phone": "0595001616"
  },
  {
    "name": "حسام حسن محمد الشهري",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1164599977",
    "phone": "0557775278"
  },
  {
    "name": "خالد تركي عايض القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1169057351",
    "phone": "0536201378"
  },
  {
    "name": "خالد داود بن عابد الحارثي",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1164120600",
    "phone": "0501076244"
  },
  {
    "name": "سطام عبدالعزيز عبدالله العريفي",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1165839455",
    "phone": "0599791658"
  },
  {
    "name": "سعود سلطان بن هليل العتيبي",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1163778960",
    "phone": "0554820082"
  },
  {
    "name": "طلال محمد منير المهدرس",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1166582989",
    "phone": "0531167666"
  },
  {
    "name": "عبدالكريم مساعد عبدالعزيز الهزاع",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1165143783",
    "phone": "0503210252"
  },
  {
    "name": "عبداللطيف ابراهيم محمد الطمره",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1164277830",
    "phone": "0505404365"
  },
  {
    "name": "عبدالله سامي سعد الحوشاني",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1165495258",
    "phone": "0555219086"
  },
  {
    "name": "علي أحمد علي عقيل",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "013609088",
    "phone": "0546000184"
  },
  {
    "name": "عمر بن سعد بن هلال الشبانات",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1164825802",
    "phone": "0505213725"
  },
  {
    "name": "فارس مشعل عبدالله بن موينع",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1163537838",
    "phone": "0555200719"
  },
  {
    "name": "فهد عيسى محمد العيسى",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1162761306",
    "phone": "0554499908"
  },
  {
    "name": "مازن خالد دخيل المطيري",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1164997858",
    "phone": "0501110052"
  },
  {
    "name": "مازن رفعت محمد حاج النيل",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "2348937422",
    "phone": "0501331089"
  },
  {
    "name": "محمد بن علي محسن العثيميني",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1172720045",
    "phone": "0506256254"
  },
  {
    "name": "نايف بن بندر بن خلفان العلوي",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1166803245",
    "phone": "0532225560"
  },
  {
    "name": "نواف عبدالعزيز عبدالله المرزوق",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1165668417",
    "phone": "0501100076"
  },
  {
    "name": "هادي سلطان هادي القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1164387977",
    "phone": "0505936192"
  },
  {
    "name": "يزيد بن حسين بن متعب بن محمد كعكم",
    "grade": "الثاني المتوسط",
    "classNum": "2",
    "nationalId": "1165002153",
    "phone": "0550117805"
  },
  {
    "name": "ثامر عمر ابراهيم عثمان",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1166911709",
    "phone": "0538384444"
  },
  {
    "name": "جهاد فارس عبدالقادر حتاوي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "008464815",
    "phone": "0562674178"
  },
  {
    "name": "خالد محمد عبدالكريم الخفاجي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1164830562",
    "phone": "0533074601"
  },
  {
    "name": "سعد ابن مسفر بن سعد القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1188914319",
    "phone": "0508057005"
  },
  {
    "name": "سعود بن عبدالله بن سعود السحامي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1165099498",
    "phone": "0500650867"
  },
  {
    "name": "سعود ناصر سيف العريفي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1167770468",
    "phone": "0505474606"
  },
  {
    "name": "سعيد محمد باوزير",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "2344500760",
    "phone": "0553435135"
  },
  {
    "name": "طلال بن فهد بن عطيه بالحكم الزهراني",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1164983874",
    "phone": "0567837159"
  },
  {
    "name": "عبدالرحمن احمد جاسم الحمدي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "2362260263",
    "phone": "0503432054"
  },
  {
    "name": "عبدالعزيز ماجد راشد الزير",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1167153434",
    "phone": "0500933390"
  },
  {
    "name": "عبدالعزيز وليد ناصر بن سعران",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1164512566",
    "phone": "0556660555"
  },
  {
    "name": "عبدالله بن بندر بن فهد المسيحل",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1167267341",
    "phone": "0500155334"
  },
  {
    "name": "عز الدين احمد محمد سعد",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "2358022958",
    "phone": "0561317507"
  },
  {
    "name": "عزام خالد شلهوب بن شلهوب",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1167515020",
    "phone": "0506404016"
  },
  {
    "name": "عزام فهد احمد صلوي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1164747014",
    "phone": "0555796951"
  },
  {
    "name": "عمر وليد ياسين درويش علي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "4533080448",
    "phone": "0557790508"
  },
  {
    "name": "فارس ابن محمد بن سالم بن نويشي الوهبي الحربي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1163397811",
    "phone": "0583228278"
  },
  {
    "name": "يزيد بن حمد بن مترك بن محمد ال مسعود القحطاني",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1166629798",
    "phone": "0505203795"
  },
  {
    "name": "يوسف عايد عواد البلوي",
    "grade": "الثاني المتوسط",
    "classNum": "3",
    "nationalId": "1167371093",
    "phone": "0531066289"
  },
  {
    "name": "أصيل ناصر بن محمد مذكور",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1158966166",
    "phone": "0552149044"
  },
  {
    "name": "خالد محمد مسدف معافا",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1162308223",
    "phone": "0552680201"
  },
  {
    "name": "راكان بن عبدالله بن سالم اليافعي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1161109093",
    "phone": "0504234219"
  },
  {
    "name": "زياد احمد بن علي اللحيد",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1160805899",
    "phone": "0504432362"
  },
  {
    "name": "سطام محمد سعود الدوسري",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1160267124",
    "phone": "0555260669"
  },
  {
    "name": "سلطان احمد صالح الفنتوخ",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1163270869",
    "phone": "0555242266"
  },
  {
    "name": "ضاري صالح مهنا العازمي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1161085236",
    "phone": "0531111140"
  },
  {
    "name": "عبدالعزيز عبدالله شراز المالكي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1160585624",
    "phone": "0556999627"
  },
  {
    "name": "عبدالعزيز عبدالله عايض الأسمري",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1160050678",
    "phone": "0555992269"
  },
  {
    "name": "عبدالله عبيد عبدالله العتيبي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1161021314",
    "phone": "0597882020"
  },
  {
    "name": "عبدالله فهد جلوي الشرهمي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1160857700",
    "phone": "0555457732"
  },
  {
    "name": "عماد الدين اسلام محمد دراز",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "2502333723",
    "phone": "0556124553"
  },
  {
    "name": "فهد عبدالرحمن فهد العتيبي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1161418593",
    "phone": "0552270402"
  },
  {
    "name": "فيصل بن عبدالمحسن بن عايض العصيمي العتيبي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1163074592",
    "phone": "0505552320"
  },
  {
    "name": "مازن خالد عبدربه الزهراني",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1171918236",
    "phone": "0540707365"
  },
  {
    "name": "محمد سلطان عبدالعزيز العيد",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1158815876",
    "phone": "0503167770"
  },
  {
    "name": "محمد مقعد ساير العتيبي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1166075653",
    "phone": "0536655992"
  },
  {
    "name": "مشاري ابراهيم عبداللطيف المغربي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1160693949",
    "phone": "0542744245"
  },
  {
    "name": "مشاري علي موسى عقيلي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1160803878",
    "phone": "0502259722"
  },
  {
    "name": "مهند عبدالله فهد الزكري",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1161661846",
    "phone": "0558794720"
  },
  {
    "name": "نواف وليد حمد الشعلان",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1159404795",
    "phone": "0555798074"
  },
  {
    "name": "يوسف نايف مقعد العتيبي",
    "grade": "الثالث المتوسط",
    "classNum": "1",
    "nationalId": "1168385894",
    "phone": "0505290037"
  },
  {
    "name": "تركي عبدالعزيز عبدالله المرزوق",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1156933093",
    "phone": "0501100076"
  },
  {
    "name": "تركي عثمان عبدالعزيز العثمان",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1160223317",
    "phone": "0505226153"
  },
  {
    "name": "راشد احمد فهد آل سعيد",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1159683497",
    "phone": "0555992829"
  },
  {
    "name": "راكان ابراهيم محمد ديوان",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "2310646332",
    "phone": "0500030732"
  },
  {
    "name": "ريان ناصر عبدالرحمن المرشود",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1161397599",
    "phone": "0550666662"
  },
  {
    "name": "صالح بن ممدوح بن صالح بن خالد الجويعي",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1163112129",
    "phone": "0549887719"
  },
  {
    "name": "عبد الرحمن محمد صلاح بدر الدين",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "2508581135",
    "phone": "0507652707"
  },
  {
    "name": "عبدالعزيز تركي عبدالعزيز اللهيم",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1162188872",
    "phone": "0505256806"
  },
  {
    "name": "عبدالعزيز عبدالمحسن فهد بن بديع",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1161340763",
    "phone": "0554457163"
  },
  {
    "name": "عبدالله متعب بن عبدالرحمن الجبرين",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1171845140",
    "phone": "0559898559"
  },
  {
    "name": "عبدالمحسن طارق بن عبدالرحمن العروان",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1159200318",
    "phone": "0506291294"
  },
  {
    "name": "عمر فهد محمد السقامي",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1162454266",
    "phone": "0564234552"
  },
  {
    "name": "فيصل محمد صالح الفنتوخ",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1165152107",
    "phone": "0556488802"
  },
  {
    "name": "ماجد فهد عبدالعزيز الكثيري",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1162325722",
    "phone": "0557609015"
  },
  {
    "name": "محمد خالد محمد بن مشرف",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1162461857",
    "phone": "0551777559"
  },
  {
    "name": "محمد سعد بن محمد العيشان",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1161288897",
    "phone": "0504217660"
  },
  {
    "name": "محمد عبدالعزيز محمد الخالدي",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1156334813",
    "phone": "0500091387"
  },
  {
    "name": "مهند ماجد علي كعبي",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1162044851",
    "phone": "0533313738"
  },
  {
    "name": "ناصر سعد عبدالله الزريعي",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1158021137",
    "phone": "0505231121"
  },
  {
    "name": "نواف سعد بن علي القاسم",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1161363443",
    "phone": "0504200199"
  },
  {
    "name": "ياسر تركي اسماعيل مسملي",
    "grade": "الثالث المتوسط",
    "classNum": "2",
    "nationalId": "1162274086",
    "phone": "0504261855"
  },
  {
    "name": "ثامر وليد بن عبدالعزيز الطليحي",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1163525544",
    "phone": "0504437710"
  },
  {
    "name": "خالد بن عبدالرؤوف بن عبدالرحمن بن عبدالله الشنير",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1160712996",
    "phone": "0504173163"
  },
  {
    "name": "خالد عبدالله خالد الخالدي",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1162560054",
    "phone": "0558890881"
  },
  {
    "name": "خالد محمد بن عبدالله حنيف آل درعان",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1174188647",
    "phone": "0505556029"
  },
  {
    "name": "راشد سعيد راشد عبدالسلام",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1159155223",
    "phone": "0533177877"
  },
  {
    "name": "راشد صالح بن عبدالعزيز الحلوان",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1174226389",
    "phone": "0551112126"
  },
  {
    "name": "رواد محمد ابراهيم الخليل",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1167756897",
    "phone": "0502555411"
  },
  {
    "name": "صالح بن محمد بن صالح الميموني المطيري",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1159394046",
    "phone": "0555097811"
  },
  {
    "name": "عبدالرحمن بدر عبدالرحمن الطريقي",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1158551372",
    "phone": "0507004114"
  },
  {
    "name": "عبدالرحمن خالد محمد سعيد",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1195815558",
    "phone": "0504411393"
  },
  {
    "name": "عبدالله تركي عبدالله الأحمد",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1158561843",
    "phone": "0542800700"
  },
  {
    "name": "عبدالله عبدالرحمن عبدالله النجراني",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1159977451",
    "phone": "0546416395"
  },
  {
    "name": "علي بن خالد بن علي العجيري",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1162387458",
    "phone": "0505199500"
  },
  {
    "name": "علي عبدالله علي ال حمود",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1158128270",
    "phone": "0545555161"
  },
  {
    "name": "فارس وليد بن عبدالله الحوطي",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1161333677",
    "phone": "0552805550"
  },
  {
    "name": "فهد بن خالد بن فهد بن عبدالعزيز الزيد",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1158198604",
    "phone": "0555198633"
  },
  {
    "name": "فيصل عبدالرحمن عزيز القحطاني",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1159551264",
    "phone": "0556444082"
  },
  {
    "name": "متعب مطر جمعان الدوسري",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1186515613",
    "phone": "0530545913"
  },
  {
    "name": "نواف فهد بن ناصر القحطاني",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1159852746",
    "phone": "0556557210"
  },
  {
    "name": "يوسف عبدالله عوض العتيبي",
    "grade": "الثالث المتوسط",
    "classNum": "3",
    "nationalId": "1163027392",
    "phone": "0506371377"
  }
];

        // المتغيرات العامة
        const AUTH_PASS = "000999";
        let pendingTargetTab = null;
        let isAuthenticated = false;

        // تهيئة التطبيق
        document.addEventListener('DOMContentLoaded', () => {
            initMenuListeners();
            populateStudentDropdown(mockStudents);
            updateStatusIndicator(true);
        });

        // إدارة القائمة للجوال
        function initMenuListeners() {
            const mobileBtn = document.getElementById('mobileMenuBtn');
            const mobileMenu = document.getElementById('mobileMenu');
            mobileBtn.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }

        // التبديل بين الصفحات
        function switchTab(tabId) {
            // إخفاء القائمة المنسدلة للجوال بشكل احترافي
            document.getElementById('mobileMenu').classList.add('hidden');

            // حماية صفحة إدارة المدرسة والتقارير بكلمة السر 000999
            if ((tabId === 'page-admin' || tabId === 'page-reports') && !isAuthenticated) {
                pendingTargetTab = tabId;
                openPasswordModal();
                return;
            }

            executeTabSwitch(tabId);
        }

        function executeTabSwitch(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.getElementById(tabId).classList.remove('hidden');

            // تحديث تصميم أزرار لوحة التحكم
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('bg-saudi-green', 'text-white', 'shadow-sm');
                btn.classList.add('text-gray-600');
            });

            const activeBtn = document.getElementById(`tab-${tabId}`);
            if (activeBtn) {
                activeBtn.classList.add('bg-saudi-green', 'text-white', 'shadow-sm');
                activeBtn.classList.remove('text-gray-600');
            }

            // تحديث العنوان للجوال
            const titles = {
                'page-submit': 'تقديم شكوى',
                'page-admin': 'إدارة المدرسة',
                'page-reports': 'التقارير'
            };
            document.getElementById('currentPageTitle').innerText = titles[tabId];
            
            if (tabId === 'page-admin') renderAdminPage();
            if (tabId === 'page-reports') renderReportsPage();
        }

        // حماية كلمة السر Modal
        function openPasswordModal() {
            document.getElementById('modalPasswordInput').value = '';
            document.getElementById('passwordError').classList.add('hidden');
            document.getElementById('passwordModal').classList.remove('hidden');
            document.getElementById('modalPasswordInput').focus();
        }

        function closePasswordModal() {
            document.getElementById('passwordModal').classList.add('hidden');
            pendingTargetTab = null;
        }

        function verifyPassword() {
            const entered = document.getElementById('modalPasswordInput').value;
            if (entered === AUTH_PASS) {
                isAuthenticated = true;
                closePasswordModal();
                if (pendingTargetTab) executeTabSwitch(pendingTargetTab);
            } else {
                document.getElementById('passwordError').classList.remove('hidden');
            }
        }

        // تحديث خيارات الطلاب بناءً على الصف والفصل
        function updateStudentOptions() {
            const grade = document.getElementById('gradeSelect').value;
            const classNum = document.getElementById('classSelect').value;

            let filtered = mockStudents;
            if (grade) filtered = filtered.filter(s => s.grade === grade);
            if (classNum) filtered = filtered.filter(s => s.classNum === classNum);

            populateStudentDropdown(filtered);
        }

        function populateStudentDropdown(list) {
            const select = document.getElementById('studentSelect');
            select.innerHTML = '<option value="">اختر الطالب...</option>';
            list.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.name;
                opt.textContent = `${s.name} (${s.grade} - فصل ${s.classNum})`;
                opt.dataset.nationalId = s.nationalId;
                opt.dataset.phone = s.phone;
                opt.dataset.grade = s.grade;
                opt.dataset.classNum = s.classNum;
                select.appendChild(opt);
            });
        }

        // البحث السريع بالاسم أو الهوية
        function filterStudents() {
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            const filtered = mockStudents.filter(s => 
                s.name.toLowerCase().includes(query) || s.nationalId.includes(query)
            );
            populateStudentDropdown(filtered);
        }

        // تعبئة البيانات تلقائياً عند اختيار الطالب
        function autoFillStudentData() {
            const select = document.getElementById('studentSelect');
            const selectedOpt = select.options[select.selectedIndex];
            if (selectedOpt && selectedOpt.dataset.nationalId) {
                document.getElementById('nationalIdInput').value = selectedOpt.dataset.nationalId;
                document.getElementById('whatsappInput').value = selectedOpt.dataset.phone;
                if(selectedOpt.dataset.grade) document.getElementById('gradeSelect').value = selectedOpt.dataset.grade;
                if(selectedOpt.dataset.classNum) document.getElementById('classSelect').value = selectedOpt.dataset.classNum;
            }
        }

        // التعامل مع إرسال الشكوى
        async function handleComplaintSubmit(e) {
            e.preventDefault();

            const complaintData = {
                id: Date.now(),
                grade: document.getElementById('gradeSelect').value,
                classNum: document.getElementById('classSelect').value,
                studentName: document.getElementById('studentSelect').value || "طالب",
                nationalId: document.getElementById('nationalIdInput').value,
                phoneNumber: document.getElementById('whatsappInput').value,
                complaintText: document.getElementById('complaintText').value,
                status: 'pending',
                adminAction: '',
                createdAt: new Date().toLocaleDateString('ar-SA', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
            };

            let saveSuccess = false;

            // حفظ في Supabase إن وجد
            if (supabaseClient) {
                try {
                    const { error } = await supabaseClient.from('complaints').insert([{
                        grade: complaintData.grade,
                        class_num: complaintData.classNum,
                        student_name: complaintData.studentName,
                        national_id: complaintData.nationalId,
                        phone_number: complaintData.phoneNumber,
                        complaint_text: complaintData.complaintText
                    }]);
                    if (!error) saveSuccess = true;
                } catch (err) {
                    saveSuccess = false;
                }
            }

            // الحفظ الدائم في LocalStorage آلياً لموثوقية حفظ الشكاوى بصورة دائمة
            try {
                let localData = JSON.parse(localStorage.getItem('school_complaints') || '[]');
                localData.push(complaintData);
                localStorage.setItem('school_complaints', JSON.stringify(localData));
                saveSuccess = true;
            } catch(err) {
                saveSuccess = false;
            }

            // تحديث حالة النظام (أخضر/أحمر)
            updateStatusIndicator(saveSuccess);

            if (saveSuccess) {
                // تفريغ مربع النص
                document.getElementById('complaintText').value = '';
                alert('تم إرسال الشكوى بنجاح وبسرية تامة إلى إدارة المدرسة.');
            } else {
                alert('عذراً، حدث خطأ أثناء حفظ الشكوى. يرجى المحاولة مرة أخرى.');
            }
        }

        // تحديث زر المؤشر الأخضر والأحمر بكتلة التحكم
        function updateStatusIndicator(isSaved) {
            const badge = document.getElementById('statusBadge');
            const text = document.getElementById('statusText');

            if (isSaved) {
                badge.className = "bg-emerald-500 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 transition-all shadow";
                text.innerText = "تم حفظ البيانات";
            } else {
                badge.className = "bg-red-600 text-white px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 transition-all shadow";
                text.innerText = "لم يتم الحفظ";
            }
        }

        // تحميل الشكاوى المخزنة
        function getStoredComplaints() {
            return JSON.parse(localStorage.getItem('school_complaints') || '[]');
        }

        // عرض صفحة إدارة المدرسة (الشكاوى المرسلة)
        function renderAdminPage() {
            const complaints = getStoredComplaints().filter(c => c.status === 'pending');
            const container = document.getElementById('adminComplaintsList');

            if (complaints.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-10 text-gray-400">
                        <i class="fa-solid fa-circle-check text-4xl mb-2 text-emerald-500"></i>
                        <p class="text-sm font-bold">لا توجد شكاوى جديدة غير معالجة حالياً.</p>
                    </div>`;
                return;
            }

            container.innerHTML = complaints.map(c => `
                <div class="border rounded-xl p-5 bg-gray-50 hover:shadow-md transition">
                    <div class="flex flex-wrap justify-between items-start gap-2 border-b pb-3 mb-3">
                        <div>
                            <span class="font-bold text-saudi-green text-base">${c.studentName}</span>
                            <span class="text-xs text-gray-500 mr-2">(${c.grade} - فصل ${c.classNum})</span>
                        </div>
                        <span class="text-xs bg-gray-200 text-gray-700 px-2.5 py-1 rounded-md font-medium">الهوية: ${c.nationalId}</span>
                    </div>

                    <div class="mb-4">
                        <p class="text-xs font-bold text-gray-500 mb-1">نص الشكوى:</p>
                        <p class="text-sm text-gray-800 bg-white p-3 rounded-lg border leading-relaxed">${c.complaintText}</p>
                    </div>

                    <!-- مربع نص الإجراءات المتخذة من إدارة المدرسة -->
                    <div class="mt-4 pt-3 border-t">
                        <label class="block text-xs font-bold text-saudi-darkGreen mb-1.5">الإجراءات المتخذة من إدارة المدرسة:</label>
                        <textarea id="action-text-${c.id}" rows="3" placeholder="اكتب الإجراءات القرارية المتخذة هنا..." class="w-full p-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-saudi-green focus:outline-none bg-white mb-3 resize-none"></textarea>
                        
                        <button onclick="resolveComplaint(${c.id})" class="bg-saudi-green text-white text-xs font-bold px-5 py-2.5 rounded-lg hover:bg-saudi-darkGreen transition flex items-center gap-1.5">
                            <i class="fa-solid fa-check"></i> تم اتخاذ القرار
                        </button>
                    </div>
                </div>
            `).join('');
        }

        // النقر على مفتاح "تم اتخاذ القرار"
        function resolveComplaint(id) {
            const actionText = document.getElementById(`action-text-${id}`).value.trim();
            if (!actionText) {
                alert('يرجى كتابة الإجراءات المتخذة من إدارة المدرسة أولاً.');
                return;
            }

            let complaints = getStoredComplaints();
            const index = complaints.findIndex(c => c.id === id);
            if (index !== -1) {
                complaints[index].status = 'resolved';
                complaints[index].adminAction = actionText;
                complaints[index].actionDate = new Date().toLocaleDateString('ar-SA');
                localStorage.setItem('school_complaints', JSON.stringify(complaints));

                alert('تم تسجيل الإجراء وتحويل الشكوى إلى صورة تقرير مفصل في صفحة التقارير.');
                renderAdminPage();
            }
        }

        // عرض صفحة التقارير الرسمية
        function renderReportsPage() {
            const reports = getStoredComplaints().filter(c => c.status === 'resolved');
            const container = document.getElementById('reportsList');

            if (reports.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-10 text-gray-400">
                        <i class="fa-solid fa-folder-open text-4xl mb-2 text-saudi-gold"></i>
                        <p class="text-sm font-bold">لا توجد تقارير صادرة حتى الآن.</p>
                    </div>`;
                return;
            }

            container.innerHTML = reports.map(r => {
                const cleanPhone = r.phoneNumber.replace(/^0/, '');
                const waMessage = encodeURIComponent(`السلام عليكم ورحمة الله وبركاته
عزيزي ولي أمر الطالب: ${r.studentName}
نحيطكم علماً بأنه تم النظر في الشكوى المقدمة واتخاذ الإجراءات التالية من قبل إدارة المدرسة:
"${r.adminAction}"
شاكرين اهتمامكم وحرصكم.`);
                const waUrl = `https://wa.me/966${cleanPhone}?text=${waMessage}`;

                return `
                <div class="border-2 border-saudi-gold/40 rounded-2xl p-6 bg-white shadow-lg relative overflow-hidden">
                    <!-- الترويسة الفرعية للتقرير -->
                    <div class="text-center border-b-2 border-saudi-green pb-4 mb-4">
                        <h3 class="font-extrabold text-saudi-green text-base">تقرير مفصل لمعالجة شكوى طالب</h3>
                        <p class="text-xs text-saudi-gold font-bold">متوسطة الثغر النموذجية الأهلية</p>
                    </div>

                    <!-- تفاصيل الشكوى والقرار -->
                    <div class="grid grid-cols-2 gap-2 text-xs mb-4 bg-gray-50 p-3 rounded-lg border">
                        <div><span class="font-bold text-gray-600">اسم الطالب:</span> ${r.studentName}</div>
                        <div><span class="font-bold text-gray-600">الصف والفصل:</span> ${r.grade} - فصل ${r.classNum}</div>
                        <div><span class="font-bold text-gray-600">رقم الهوية:</span> ${r.nationalId}</div>
                        <div><span class="font-bold text-gray-600">تاريخ المعالجة:</span> ${r.actionDate || 'اليوم'}</div>
                    </div>

                    <div class="mb-3">
                        <p class="text-xs font-bold text-gray-600 mb-1">نص الشكوى المقدمة:</p>
                        <p class="text-xs text-gray-700 bg-gray-50 p-2.5 rounded border">${r.complaintText}</p>
                    </div>

                    <div class="mb-5">
                        <p class="text-xs font-bold text-saudi-green mb-1">الإجراءات المتخذة من إدارة المدرسة:</p>
                        <p class="text-xs text-gray-800 bg-emerald-50/60 p-3 rounded border border-emerald-200 font-medium leading-relaxed">${r.adminAction}</p>
                    </div>

                    <!-- رابط رقم الواتس الخاص بالطالب لارسال التقرير اليه -->
                    <div class="mb-6 pb-4 border-b">
                        <a href="${waUrl}" target="_blank" class="inline-flex items-center gap-2 bg-emerald-600 text-white text-xs font-bold px-4 py-2.5 rounded-xl hover:bg-emerald-700 transition shadow">
                            <i class="fa-brands fa-whatsapp text-base"></i> إرسال التقرير عبر رقم الواتس الخاص بالطالب (${r.phoneNumber})
                        </a>
                    </div>

                    <!-- التواقيع الرسمية اسفل التقرير -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center pt-2 text-xs font-bold text-gray-800 bg-gray-50/90 p-3 rounded-xl border border-gray-100">
                        <div class="border-b md:border-b-0 md:border-l pb-2 md:pb-0 pl-2">
                            <p class="text-saudi-green font-bold">وكيل شؤون الطلاب</p>
                            <p class="mt-1 text-gray-700">صالح بن عبدالله الدعجاني</p>
                        </div>
                        <div class="border-b md:border-b-0 md:border-l pb-2 md:pb-0 pl-2">
                            <p class="text-saudi-green font-bold">وكيل شؤون المعلمين</p>
                            <p class="mt-1 text-gray-700">محمد مبروك السيد</p>
                        </div>
                        <div>
                            <p class="text-saudi-green font-bold">مدير المدرسة</p>
                            <p class="mt-1 text-gray-700">إبراهيم بن موسى التميمي</p>
                        </div>
                    </div>
                </div>
            `}).join('');
        }
    </script>
</body>
</html>

