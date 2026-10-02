# -*- coding: utf-8 -*-
"""
أداة استعراض منظومة التحليل العددي الشاملة
=========================================
تتيح الوصول السريع لجميع أدوات المذاكرة والاختبارات والتطبيق المكتبي وأكواد الماتلاب:
1. المذكرة الشاملة الأصلية المعتمدة (29 صفحة - شرح كامل ومباشر)
2. بطاقات المذاكرة التفاعلية والحفظ النشط (Interactive Cards & Active Recall)
3. منصة وبنك الامتحانات الشاملة ونماذج الأسئلة (38 صفحة)
4. التطبيق المكتبي المستقل (NumericalAnalysis.exe) المنفذ لجميع الـ 12 خوارزمية
5. مجلد خوارزميات ماتلاب المستقل (matlab) بصيغة .m للمعادلات الخطية وغير الخطية
"""

import os
import sys
import webbrowser
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. المذكرة الأصلية المعتمدة
    orig_guide_html = os.path.join(base_dir, "Numerical_Analysis_Study_Guide.html")
    orig_guide_pdf = os.path.join(base_dir, "Numerical_Analysis_Study_Guide.pdf")
    
    # 2. بطاقات المذاكرة التفاعلية والحفظ النشط
    cards_html = os.path.join(base_dir, "Numerical_Analysis_Interactive_Cards.html")
    cards_pdf = os.path.join(base_dir, "Numerical_Analysis_Interactive_Cards.pdf")
    
    # 3. بنك الامتحانات الشاملة
    exams_html = os.path.join(base_dir, "Numerical_Analysis_Comprehensive_Exams.html")
    exams_pdf = os.path.join(base_dir, "Numerical_Analysis_Comprehensive_Exams.pdf")

    # 4. التطبيق التنفيذي EXE
    exe_path = os.path.join(base_dir, "NumericalAnalysis.exe")
    if not os.path.exists(exe_path):
        exe_path = os.path.join(base_dir, "project", "NumericalAnalysis.exe")

    # 5. مجلد الماتلاب
    matlab_dir = os.path.join(base_dir, "matlab")

    print("=" * 75)
    print("🎓 منظومة التحليل العددي الشاملة (Numerical Analysis Learning Suite)")
    print("=" * 75)
    print("📖 [المجموعة الأولى: المذكرة الأصلية المعتمدة - 29 صفحة - شرح كامل]")
    print("  1. فتح المذكرة الأصلية (HTML في المتصفح)")
    print("  2. فتح المذكرة الأصلية (PDF كتاب كامل جاهز للطباعة)")
    print("")
    print("🧠 [المجموعة الثانية: بطاقات المذاكرة التفاعلية والحفظ النشط - ملف مستقل]")
    print("  3. فتح بطاقات المذاكرة التفاعلية (HTML في المتصفح - إخفاء وكشف لاختبار النفس)")
    print("  4. فتح بطاقات المذاكرة (PDF)")
    print("")
    print("📝 [المجموعة الثالثة: منصة وبنك الامتحانات الشاملة - 38 صفحة]")
    print("  5. فتح منصة الامتحانات التفاعلية (HTML - تفاعلي مع حلول تدريجية ودرجات)")
    print("  6. فتح بنك الامتحانات الشامل (PDF)")
    print("")
    print("💻 [المجموعة الرابعة: المنصة والتطبيق التنفيذي المكتبي المنفذ للخوارزميات]")
    print("  7. 🚀 تشغيل التطبيق المكتبي (NumericalAnalysis.exe بالتحديثات الأخيرة)")
    print("")
    print("📊 [المجموعة الخامسة: خوارزميات MATLAB المستقلة بصيغة .m]")
    print("  8. 📁 فتح مجلد خوارزميات ماتلاب (ملفات .m للأنظمة الخطية وغير الخطية)")
    print("")
    print("⚡ 9. فتح جميع المنصات التفاعلية معاً في المتصفح")
    print("❌ 10. خروج")
    print("-" * 75)

    try:
        choice = input("اختر رقم الخيار (الافتراضي 1): ").strip()
    except Exception:
        choice = "1"

    if choice == "1" or choice == "":
        if os.path.exists(orig_guide_html):
            print(f"جاري فتح المذكرة الأصلية HTML: {orig_guide_html}")
            webbrowser.open(f"file:///{orig_guide_html.replace(os.sep, '/')}")
        else:
            print("الملف غير موجود!")
    elif choice == "2":
        if os.path.exists(orig_guide_pdf):
            print(f"جاري فتح المذكرة الأصلية PDF: {orig_guide_pdf}")
            os.startfile(orig_guide_pdf)
        else:
            print("ملف المذكرة PDF غير موجود!")
    elif choice == "3":
        if os.path.exists(cards_html):
            print(f"جاري فتح بطاقات المذاكرة التفاعلية HTML: {cards_html}")
            webbrowser.open(f"file:///{cards_html.replace(os.sep, '/')}")
        else:
            print("ملف بطاقات المذاكرة HTML غير موجود!")
    elif choice == "4":
        if os.path.exists(cards_pdf):
            print(f"جاري فتح بطاقات المذاكرة PDF: {cards_pdf}")
            os.startfile(cards_pdf)
        else:
            print("ملف بطاقات المذاكرة PDF غير موجود!")
    elif choice == "5":
        if os.path.exists(exams_html):
            print(f"جاري فتح منصة الامتحانات HTML: {exams_html}")
            webbrowser.open(f"file:///{exams_html.replace(os.sep, '/')}")
        else:
            print("ملف الامتحانات HTML غير موجود!")
    elif choice == "6":
        if os.path.exists(exams_pdf):
            print(f"جاري فتح بنك الامتحانات PDF: {exams_pdf}")
            os.startfile(exams_pdf)
        else:
            print("ملف الامتحانات PDF غير موجود!")
    elif choice == "7":
        if os.path.exists(exe_path):
            print(f"جاري تشغيل تطبيق المنصة: {exe_path}")
            subprocess.Popen([exe_path])
        else:
            print(f"ملف التطبيق غير موجود في المسار: {exe_path}")
    elif choice == "8":
        if os.path.exists(matlab_dir):
            print(f"جاري فتح مجلد خوارزميات ماتلاب: {matlab_dir}")
            os.startfile(matlab_dir)
        else:
            print(f"مجلد ماتلاب غير موجود في المسار: {matlab_dir}")
    elif choice == "9":
        print("جاري فتح جميع المنصات في المتصفح...")
        for p in [orig_guide_html, cards_html, exams_html]:
            if os.path.exists(p):
                webbrowser.open(f"file:///{p.replace(os.sep, '/')}")
    elif choice == "10":
        print("مع السلامة وبالتوفيق والنجاح بأعلى الدرجات بإذن الله!")
    else:
        print("خيار غير معروف.")

if __name__ == "__main__":
    main()
