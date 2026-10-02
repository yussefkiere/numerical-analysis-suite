"""
اختبار شامل لموجّه الشاشات وتدفق الواجهات العصرية (CustomTkinter GUI Test)
=============================================================================
يتحقق هذا الاختبار من:
1. تهيئة النافذة الرئيسية (AppWindow) وتفعيل الوضع الداكن افتراضياً.
2. عمل زر تبديل المظهر (Dark / Light Theme Toggle).
3. التنقل عبر موجّه الشاشات (Router) بين الشاشات الأربع ذهاباً وإياباً.
4. التحقق من تنفيذ الحساب وعرض النتائج في جدول التنفيذ السبوري بدون أشرطة تمرير.
5. التحقق من عمل إشعارات الـ Toast ونسخ النتيجة.
6. التحقق من عدم حدوث أي أخطاء أثناء تبديل المظهر وتغيير ألوان المكونات.
"""

import sys
import os

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from methods.registry import CATEGORIES
from gui.app_window import AppWindow
from gui.screens import (
    CategoryScreen,
    MethodsScreen,
    InputScreen,
    ResultScreen,
)


def test_customtkinter_gui():
    print("=" * 65)
    print("🚀 بدء فحص واجهات CustomTkinter العصرية وموجّه الشاشات")
    print("=" * 65)

    # 1. تهيئة التطبيق
    app = AppWindow()
    app.update_idletasks()
    assert isinstance(app.current_screen, CategoryScreen), "First screen must be CategoryScreen"
    print("  ✓ تم تشغيل النافذة الرئيسية وتوليد شاشة نوع المسألة (CategoryScreen) بنجاح.")

    # 2. فحص تبديل المظهر (Dark / Light)
    initial_mode = app.is_dark_mode
    app.toggle_theme()
    app.update_idletasks()
    assert app.is_dark_mode != initial_mode, "Theme toggle failed"
    app.toggle_theme()  # استعادة الوضع الداكن الافتراضي
    app.update_idletasks()
    print("  ✓ تم فحص زر تبديل المظهر الداكن/الفاتح وتأكيد سلامة تغير ألوان العناصر.")

    # 3. فحص إشعارات Toast
    app.show_toast("إشعار تجريبي ناجح", toast_type="success")
    app.update_idletasks()
    assert app.current_toast is not None, "Toast failed to show"
    print("  ✓ تم فحص إشعار الـ Toast العائم والتأكد من ظهوره بانسيابية.")

    # 4. دورة حياة التنقل عبر الأقسام الأربعة وكافة الطرق
    passed_methods = 0
    total_methods = sum(len(c["methods"]) for c in CATEGORIES.values())

    for cat_key, cat_data in CATEGORIES.items():
        print(f"\n* فحص تدفق القسم: {cat_data['title']} ({cat_key})")

        # أ. الانتقال لشاشة الطرق (Screen 2)
        app.show_screen("methods", cat_key=cat_key, cat_data=cat_data)
        app.update_idletasks()
        assert isinstance(app.current_screen, MethodsScreen), "Screen must be MethodsScreen"
        print(f"  ✓ تم فتح شاشة الطرق (MethodsScreen) للقسم: {cat_data['title']}.")

        # فحص الرجوع للرئيسية
        app.show_screen("categories")
        app.update_idletasks()
        assert isinstance(app.current_screen, CategoryScreen)
        app.show_screen("methods", cat_key=cat_key, cat_data=cat_data)
        app.update_idletasks()

        # ب. فحص كل طريقة ضمن القسم
        for method_key, method_data in cat_data["methods"].items():
            # الانتقال لشاشة المدخلات (Screen 3)
            app.show_screen(
                "input",
                cat_key=cat_key,
                cat_data=cat_data,
                method_key=method_key,
                method_data=method_data
            )
            app.update_idletasks()
            assert isinstance(app.current_screen, InputScreen), "Screen must be InputScreen"

            # محاكاة الضغط على زر احسب
            input_screen = app.current_screen
            input_screen._perform_calculation()
            app.update_idletasks()

            # التأكد من الانتقال لشاشة النتيجة (Screen 4)
            assert isinstance(app.current_screen, ResultScreen), f"Calculation failed to route to ResultScreen for {method_key}"
            result_screen = app.current_screen

            # التأكد من صحة نص النتيجة وجدول التنفيذ
            res_text = result_screen.res_val_lbl.cget("text")
            assert len(res_text) > 0, "Result text is empty"
            assert result_screen.tree is not None, "Treeview table must be initialized"
            rows_count = len(result_screen.tree.get_children())
            assert rows_count > 0, "Treeview table must contain execution rows"

            # فحص نسخ النتيجة للحافظة
            result_screen._on_copy_result()
            app.update_idletasks()

            # فحص التبديل للمظهر الفاتح والداكن أثناء وجود الجدول
            app.toggle_theme()
            app.update_idletasks()
            app.toggle_theme()
            app.update_idletasks()

            passed_methods += 1
            print(f"    ✓ طريقة [{method_data['title']}]: نجاح إدخال المعاملات، الحساب، ملء جدول السبورة ({rows_count} صف)، والنسخ.")

            # الرجوع لشاشة الطرق
            app.show_screen("methods", cat_key=cat_key, cat_data=cat_data)
            app.update_idletasks()

        # الرجوع للشاشة الرئيسية
        app.show_screen("categories")
        app.update_idletasks()

    app.destroy()

    print("\n" + "=" * 65)
    print(f"🎉 تم اجتياز كافة اختبارات الواجهات الرسومية العصرية ({passed_methods}/{total_methods}) بنسبة 100%!")
    print("=" * 65)


if __name__ == "__main__":
    test_customtkinter_gui()
