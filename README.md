# 🎓 منظومة التحليل العددي الحديثة والمتكاملة
### Modern Numerical Analysis Learning & Computational Suite

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-0284c7)
![MATLAB](https://img.shields.io/badge/MATLAB-R2016b%20--%20R2024b%20%7C%20Octave-orange?logo=mathworks)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed%20%26%20Verified-success)

منظومة برمجية وتعليمية شاملة تجمع بين **الواجهات الرسومية العصرية (Desktop GUI)**، و**المكتبة الرياضية بلغة MATLAB (.m)**، و**المراجع الأكاديمية التفاعلية وبنك الامتحانات (HTML / PDF)** لكافة مقررات التحليل العددي في كليات الهندسة والحاسبات والعلوم.

---

## 🌟 المكونات الأساسية للمنظومة

```
📁 منظومة التحليل العددي
├── 🖥️ [1] تطبيق الواجهات الرسومية الحديث (Python & CustomTkinter)
├── 📊 [2] مكتبة خوارزميات ماتلاب المستقلة (MATLAB .m Scripts & Functions)
├── 📖 [3] المذكرة الأكاديمية الشاملة المعتمدة (29 صفحة - HTML & PDF)
├── 🧠 [4] بطاقات المذاكرة التفاعلية والحفظ النشط (15 صفحة - HTML & PDF)
├── 📝 [5] منصة وبنك الامتحانات ونماذج الأسئلة (38 صفحة - HTML & PDF)
└── ⚡ [6] أداة التشغيل الموحدة (open_exams.py)
```

---

## 📋 الخوارزميات الـ 12 المعتمدة في المنظومة

| # | الطريقة (Method) | التصنيف | ملف البايثون | ملف الماتلاب | الصيغة الأساسية |
|---|---|---|---|---|---|
| **1** | **طريقة التنصيف** (Bisection) | معادلات غير خطية | `methods/bisection.py` | `matlab/bisection.m` | $p = \frac{a+b}{2} \quad [f(a) \cdot f(b) < 0]$ |
| **2** | **طريقة الموضع الخاطئ** (False Position) | معادلات غير خطية | `methods/false_position.py` | `matlab/false_position.m` | $p = b - \frac{f(b)(b-a)}{f(b)-f(a)}$ |
| **3** | **طريقة القاطع** (Secant) | معادلات غير خطية | `methods/secant.py` | `matlab/secant.m` | $x_{n+1} = x_n - \frac{f(x_n)(x_n-x_{n-1})}{f(x_n)-f(x_{n-1})}$ |
| **4** | **طريقة نيوتن رافسون** (Newton-Raphson) | معادلات غير خطية | `methods/newton.py` | `matlab/newton_raphson.m` | $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$ |
| **5** | **طريقة النقطة الثابتة** (Fixed Point) | معادلات غير خطية | `methods/fixed_point.py` | `matlab/fixed_point.m` | $x_{n+1} = g(x_n) \quad [\|g'(x)\| < 1]$ |
| **6** | **حذف جاوس** (Gaussian Elimination) | أنظمة خطية | `methods/gauss.py` | `matlab/gauss_elimination.m` | $[A \mid b] \xrightarrow{\text{Elimination}} [U \mid c] \xrightarrow{\text{Back-Sub}} x$ |
| **7** | **طريقة جاكوبي التكرارية** (Jacobi Iteration) | أنظمة خطية | `methods/jacobi.py` | `matlab/jacobi.m` | $x_i^{(k+1)} = \frac{b_i - \sum_{j \ne i} a_{ij} x_j^{(k)}}{a_{ii}}$ |
| **8** | **قاعدة كرامر** (Cramer's Rule) | أنظمة خطية | `methods/cramer.py` | `matlab/cramer_rule.m` | $x_i = \frac{\det(A_i)}{\det(A)}$ |
| **9** | **معكوس المصفوفة** (Matrix Inversion) | أنظمة خطية | `methods/matrix_inversion.py` | `matlab/matrix_inversion.m` | $X = A^{-1} B = \frac{\text{adj}(A)}{\det(A)} B$ |
| **10** | **استيفاء لاجرانج** (Lagrange Interpolation) | استيفاء وتوفيق | `methods/lagrange.py` | `matlab/lagrange_interpolation.m` | $P_n(x) = \sum_{i=0}^n y_i \prod_{j \ne i} \frac{x-x_j}{x_i-x_j}$ |
| **11** | **قاعدة شبه المنحرف المركبة** (Trapezoidal) | تكامل عددي | `methods/trapezoidal.py` | `matlab/trapezoidal_rule.m` | $\int_a^b f(x) dx \approx \frac{h}{2}[y_0 + 2\sum y_i + y_n]$ |
| **12** | **التفاضل العددي** (Taylor Numerical Diff) | تفاضل عددي | `methods/numerical_diff.py` | `matlab/numerical_differentiation.m` | $f'(x_0) \approx \frac{f(x_0+h)-f(x_0-h)}{2h}$ |

---

## 🚀 التشغيل السريع (Quickstart)

### 1. تثبيت المتطلبات (Prerequisites)
تأكد من وجود بايثون (3.10 فما فوق):
```bash
git clone <repository-url>
cd "Numerical-Analysis"
pip install -r requirements.txt
```

### 2. تشغيل أداة التوجيه الموحدة (Unified Launcher)
```bash
python open_exams.py
```
ستظهر لك قائمة تفاعلية مرقمة تتيح بضغطة زر:
* فتح تطبيق الواجهات الرسومية (GUI App).
* فتح المذكرة الأكاديمية الشاملة (HTML أو PDF).
* فتح بطاقات المذاكرة التفاعلية (Active Recall Cards).
* فتح منصة وبنك الامتحانات (Interactive Exams).
* فتح مجلد أكواد ماتلاب المستقلة.

### 3. تشغيل تطبيق الواجهات الرسومية مباشرة (Desktop App)
```bash
python project/main.py
```

### 4. تشغيل خوارزميات ماتلاب (MATLAB Suite)
افتح مجلد `matlab/` داخل بيئة **MATLAB** أو **GNU Octave**، واكتب:
```matlab
run_all_algorithms
```
أو شغّل أي خوارزمية مستقلة كدالة أو كسكربت مباشر:
```matlab
[root, table] = newton_raphson(@(x) x.^3 - x - 2, @(x) 3*x.^2 - 1, 1.5, 1e-4, 50);
```

---

## 📂 شجرة هيكل المشروع (Project Directory Tree)

```text
├── .gitignore                                 # ملف استبعاد المخلفات والملفات المؤقتة
├── LICENSE                                    # رخصة MIT المفتوحة
├── README.md                                  # التوثيق الرئيسي للمستودع
├── requirements.txt                           # متطلبات تشغيل بيئة البايثون
├── open_exams.py                              # أداة التوجيه والتشغيل السريع
│
├── Numerical_Analysis_Study_Guide.html        # المذكرة الشاملة المعتمدة (29 صفحة)
├── Numerical_Analysis_Study_Guide.pdf         # المذكرة بصيغة PDF للطباعة
├── Numerical_Analysis_Interactive_Cards.html  # بطاقات المذاكرة التفاعلية والحفظ النشط
├── Numerical_Analysis_Interactive_Cards.pdf   # بطاقات المذاكرة بصيغة PDF
├── Numerical_Analysis_Comprehensive_Exams.html# منصة وبنك الامتحانات الشامل (38 صفحة)
├── Numerical_Analysis_Comprehensive_Exams.pdf # بنك الامتحانات بصيغة PDF
│
├── matlab/                                    # حزمة خوارزميات الماتلاب المستقلة
│   ├── README.md                              # دليل استخدام خوارزميات ماتلاب
│   ├── bisection.m                            # طريقة التنصيف
│   ├── false_position.m                       # طريقة الموضع الخاطئ
│   ├── secant.m                               # طريقة القاطع
│   ├── newton_raphson.m                       # طريقة نيوتن رافسون
│   ├── fixed_point.m                          # طريقة النقطة الثابتة
│   ├── gauss_elimination.m                    # طريقة حذف جاوس
│   ├── jacobi.m                               # طريقة جاكوبي التكرارية
│   ├── cramer_rule.m                          # قاعدة كرامر بالمحددات
│   ├── matrix_inversion.m                     # طريقة معكوس المصفوفة
│   ├── lagrange_interpolation.m               # استيفاء كثيرات حدود لاجرانج
│   ├── trapezoidal_rule.m                     # قاعدة شبه المنحرف المركبة
│   ├── numerical_differentiation.m            # صيغ التفاضل العددي
│   └── run_all_algorithms.m                   # سكربت تشغيل واختبار جميع الخوارزميات
│
└── project/                                   # الكود المصدري لتطبيق البايثون (CustomTkinter)
    ├── main.py                                # نقطة انطلاق التطبيق
    ├── NumericalAnalysis.spec                 # ملف بناء التطبيق التنفيذي (PyInstaller)
    ├── gui/                                   # واجهات المستخدم وتخطيط الشاشات والمكونات
    ├── methods/                               # الخوارزميات الرياضية وسجل الطرق (registry.py)
    ├── utils/                                 # أدوات التحليل الرياضي ومحلل الدوال (SymPy)
    ├── test_all_methods.py                    # الفحص الشامل لجميع الخوارزميات الـ 12
    └── test_gui_flow.py                       # فحص تدفق الشاشات التفاعلية بنسبة 100%
```

---

## 🛠️ المميزات التقنية للمنظومة

1. **تصميم عصري ونظام ألوان متناسق (Modern Design System):**
   * دعم كامل للتبديل الفوري بين المظهرين الداكن (Dark Mode) والفاتح (Light Mode).
   * بطاقات إحصائية بارزة، شبكات مصفوفات تفاعلية، وجداول سبورية مرقمة بدون أي أشرطة تمرير معقدة.
2. **محرك رياضي متقدم (SymPy Integration):**
   * دعم التعابير الرياضية الطبيعية مثل `x^3 - x - 2`, `sin(x)`, `exp(x)`, والضرب الضمني `2x`.
3. **معالجة قوية للأخطاء والاستثناءات:**
   * تنبيهات ذكية لشرط حصر الجذر، المصفوفات المنفردة، انعدام المشتقة، وفحص الهيمنة القطرية الصارمة قبل التنفيذ.
4. **تصدير النتائج والحلول:**
   * زر نسخ فوري للحل النهائي، وجداول التكرارات مع إشعارات عائمة (Floating Toasts).
5. **جاهزية كاملة للبناء المستقل:**
   * إمكانية تحويل التطبيق لملف تنفيذي مستقل بدون بايثون باستخدام `PyInstaller`.

---

## 📜 الترخيص (License)
هذا المشروع مرخص بموجب رخصة **[MIT License](LICENSE)** - يحق لك الاستخدام والتعديل والتطوير بحرية تامة.
