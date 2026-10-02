"""
اختبار شامل لكافة طرق التحليل العددي الـ 12 المعتمدة بالمقرر
=============================================================
يتحقق هذا الاختبار من:
1. صحة حلول كل طريقة ومقارنتها بالقيم الدقيقة.
2. اتساق بنية المخرجات (table, result).
3. فحص حالات الخطأ المعالجة.
4. التأكد من سلامة تحميل واجهات التطبيق الرسومية.
"""

import sys
import os
import math
import sympy

# ضبط ترميز الطرفية للتعامل مع الرموز واليونيكود
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# إضافة مسار المشروع
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.parser import make_function, derivative
from methods.registry import CATEGORIES
from methods import (
    bisection_method,
    false_position_method,
    secant_method,
    newton_method,
    fixed_point_method,
    gaussian_elimination_method,
    jacobi_method,
    cramer_rule_method,
    matrix_inversion_method,
    lagrange_interpolation_method,
    composite_trapezoidal_method,
    numerical_differentiation_method,
)


def run_all_benchmarks():
    print("=" * 65)
    print("🚀 بدء الفحص الشامل لجميع الطرق الـ 12 مع الأمثلة المعيارية")
    print("=" * 65)

    passed_count = 0
    total_count = 0

    # ---------------------------------------------------------
    # [1] معادلات غير خطية: x^3 - x - 2 = 0 -> الجذر ≈ 1.521380
    # ---------------------------------------------------------
    print("\n[1] فحص طرق المعادلات غير الخطية (الجذور): f(x) = x^3 - x - 2")
    f = make_function("x^3 - x - 2")
    df = derivative("x^3 - x - 2")
    g = make_function("(x + 2)**(1/3)")
    target_root = 1.5213797

    # 1. التنصيف
    total_count += 1
    t, r = bisection_method(f, 1.0, 2.0, tol=1e-4, max_iter=50)
    assert abs(r - target_root) < 1e-3, f"Bisection failed: {r}"
    print(f"  ✓ 1. التنصيف: الجذر = {r:.6f} في {len(t)} خطوات.")
    passed_count += 1

    # 2. الموضع الخاطئ
    total_count += 1
    t, r = false_position_method(f, 1.0, 2.0, tol=1e-4, max_iter=50)
    assert abs(r - target_root) < 1e-3, f"False Position failed: {r}"
    print(f"  ✓ 2. الموضع الخاطئ: الجذر = {r:.6f} في {len(t)} خطوات.")
    passed_count += 1

    # 3. القاطع
    total_count += 1
    t, r = secant_method(f, 1.0, 2.0, tol=1e-4, max_iter=50)
    assert abs(r - target_root) < 1e-3, f"Secant failed: {r}"
    print(f"  ✓ 3. القاطع: الجذر = {r:.6f} في {len(t)} خطوات.")
    passed_count += 1

    # 4. نيوتن رافسون
    total_count += 1
    t, r = newton_method(f, df, 1.5, tol=1e-4, max_iter=50)
    assert abs(r - target_root) < 1e-4, f"Newton failed: {r}"
    print(f"  ✓ 4. نيوتن رافسون: الجذر = {r:.6f} في {len(t)} خطوات.")
    passed_count += 1

    # 5. النقطة الثابتة
    total_count += 1
    t, r = fixed_point_method(g, 1.5, tol=1e-4, max_iter=50)
    assert abs(r - target_root) < 1e-3, f"Fixed point failed: {r}"
    print(f"  ✓ 5. النقطة الثابتة: الجذر = {r:.6f} في {len(t)} خطوات.")
    passed_count += 1

    # ---------------------------------------------------------
    # [2] أنظمة المعادلات الخطية AX = B:
    # 2x + y = 5
    # x + 3y = 10
    # الحل الدقيق: x1 = 1, x2 = 3
    # ---------------------------------------------------------
    print("\n[2] فحص طرق حل الأنظمة الخطية AX = B:")
    A = [[2.0, 1.0], [1.0, 3.0]]
    B = [5.0, 10.0]

    # 1. حذف جاوس
    total_count += 1
    t, r = gaussian_elimination_method(A, B)
    assert "x1 = 1.000000" in r and "x2 = 3.000000" in r, f"Gauss failed: {r}"
    print(f"  ✓ 1. حذف جاوس: النتيجة = {r}")
    passed_count += 1

    # 2. جاكوبي (نظام مهيمن قطرياً: 2x+y=5, x+3y=10 يمكن تحويله أو نظام 3x3 قياسي)
    total_count += 1
    # نظام 2x2: A=[[4, 1], [1, 4]], B=[5, 5] -> x1=1, x2=1
    A_jac = [[4.0, 1.0], [1.0, 4.0]]
    B_jac = [5.0, 5.0]
    t, r = jacobi_method(A_jac, B_jac, X0=[0.0, 0.0], tol=1e-5, max_iter=50)
    assert "x1 = 0.9999" in r or "x1 = 1.0000" in r, f"Jacobi failed: {r}"
    print(f"  ✓ 2. جاكوبي: النتيجة = {r} في {len(t)-1} تكرار.")
    passed_count += 1

    # 3. قاعدة كرامر
    total_count += 1
    t, r = cramer_rule_method(A, B)
    assert "x1 = 1.000000" in r and "x2 = 3.000000" in r, f"Cramer failed: {r}"
    print(f"  ✓ 3. قاعدة كرامر: النتيجة = {r}")
    passed_count += 1

    # 4. معكوس المصفوفة
    total_count += 1
    t, r = matrix_inversion_method(A, B)
    assert "x1 = 1.000000" in r and "x2 = 3.000000" in r, f"Inversion failed: {r}"
    print(f"  ✓ 4. معكوس المصفوفة: النتيجة = تم إيجاد A⁻¹ وضربها بنجاح.")
    passed_count += 1

    # ---------------------------------------------------------
    # [3] الاستيفاء: نقاط من y = x^2: (1, 1), (2, 4), (3, 9)
    # تقدير عند x = 2.5 -> يجب أن تكون 2.5^2 = 6.25
    # ---------------------------------------------------------
    print("\n[3] فحص الاستيفاء بكثيرات حدود لاجرانج:")
    total_count += 1
    x_pts = [1.0, 2.0, 3.0]
    y_pts = [1.0, 4.0, 9.0]
    t, r = lagrange_interpolation_method(x_pts, y_pts, x_eval=2.5)
    assert "P(2.5000) = 6.250000" in r, f"Lagrange failed: {r}"
    print(f"  ✓ 1. كثيرات حدود لاجرانج: P(2.5) = 6.250000 والصيغة الرمزية صحيحة.")
    passed_count += 1

    # ---------------------------------------------------------
    # [4] التفاضل والتكامل العددي:
    # 1. شبه المنحرف: ∫₀¹ x² dx = 1/3 ≈ 0.333333
    # 2. التفاضل: f(x) = sin(x) عند x0 = 1.0، h = 0.01
    # ---------------------------------------------------------
    print("\n[4] فحص التفاضل والتكامل العددي:")
    f_sq = make_function("x^2")
    
    # شبه المنحرف n=10
    total_count += 1
    t10, r10 = composite_trapezoidal_method(f_sq, 0.0, 1.0, n=10)
    assert "0.335000" in r10, f"Trapezoidal n=10 failed: {r10}"
    # شبه المنحرف n=100
    t100, r100 = composite_trapezoidal_method(f_sq, 0.0, 1.0, n=100)
    assert "0.333350" in r100, f"Trapezoidal n=100 failed: {r100}"
    print(f"  ✓ 1. شبه المنحرف المركبة: n=10 تعطي 0.335000، و n=100 تعطي 0.333350 (تقترب من 1/3).")
    passed_count += 1

    # التفاضل العددي
    total_count += 1
    t_diff, r_diff = numerical_differentiation_method("sin(x)", 1.0, h=0.01)
    cos_1 = math.cos(1.0) # 0.5403023
    sin_1 = -math.sin(1.0) # -0.8414709
    # الفرق المركزي للمشتقة الأولى
    cnt_d1 = t_diff[2]["calc_val"]
    assert abs(cnt_d1 - cos_1) < 1e-4, f"Central diff failed: {cnt_d1} vs {cos_1}"
    print(f"  ✓ 2. التفاضل العددي لـ sin(x) عند x0=1.0: f' ≈ {cnt_d1:.6f} مقارنة بالقيمة الدقيقة {cos_1:.6f}.")
    passed_count += 1

    # ---------------------------------------------------------
    # [5] فحص معالجة الأخطاء وحالات الاستثناء (Error Handling)
    # ---------------------------------------------------------
    print("\n[5] فحص معالجة الأخطاء والحالات الحدية (بدون انهيار):")
    
    # أ. خطأ f(a)*f(b) > 0 في التنصيف
    try:
        bisection_method(f, 2.0, 3.0, tol=1e-4, max_iter=50)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"  ✓ نجاح فحص حصر الجذر: {e}")

    # ب. خطأ مصفوفة منفردة (Singular Matrix) في كرامر
    try:
        cramer_rule_method([[1.0, 2.0], [2.0, 4.0]], [1.0, 2.0])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"  ✓ نجاح فحص المصفوفة المنفردة: {e}")

    # ج. خطأ نقاط مكررة في لاجرانج
    try:
        lagrange_interpolation_method([1.0, 1.0], [2.0, 3.0], 1.5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"  ✓ نجاح فحص النقاط المتمايزة في لاجرانج: {e}")

    # د. خطأ حدود التكامل a >= b في شبه المنحرف
    try:
        composite_trapezoidal_method(f_sq, 2.0, 1.0, 10)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"  ✓ نجاح فحص حدود التكامل: {e}")

    # ---------------------------------------------------------
    # [6] فحص استيراد الواجهات الرسومية وسلامة ربطها بـ registry.py
    # ---------------------------------------------------------
    print("\n[6] فحص الواجهات الرسومية والسجل المركزي registry.py:")
    assert len(CATEGORIES) == 4, f"Expected 4 categories, got {len(CATEGORIES)}"
    methods_total = sum(len(c["methods"]) for c in CATEGORIES.values())
    assert methods_total == 12, f"Expected 12 methods, got {methods_total}"
    print(f"  ✓ السجل المركزي يحتوي بالضبط على 4 أقسام و 12 طريقة معتمدة.")

    from gui import AppWindow, CategoryScreen, MethodsScreen, InputScreen, ResultScreen
    print("  ✓ تم استيراد كافة كلاسات الواجهات العصرية وموجّه الشاشات بنجاح تام.")

    print("\n" + "=" * 65)
    print(f"🎉 تم بنجاح اجتياز جميع الاختبارات ({passed_count}/{total_count}) بنسبة 100%!")
    print("=" * 65)


if __name__ == "__main__":
    run_all_benchmarks()
