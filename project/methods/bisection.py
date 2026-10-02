"""
=============================================================================
خوارزمية طريقة التنصيف (Bisection Method)
=============================================================================
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
=============================================================================
"""

from typing import Callable, List, Dict, Any, Tuple


def bisection_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-4,
    max_iter: int = 50
) -> Tuple[List[Dict[str, Any]], float]:
    """
    حساب جذر المعادلة بطريقة التنصيف مع حفظ خطوات الحل في جدول.

    المعاملات:
        f (Callable): دالة المعادلة f(x)
        a (float): بداية فترة الحصر
        b (float): نهاية فترة الحصر
        tol (float): الدقة المطلوبة (مستوى الخطأ المسموح به)
        max_iter (int): أقصى عدد للتكرارات

    المخرجات:
        Tuple[List[Dict], float]: (جدول التكرارات كقائمة قواميس، قيمة الجذر التقريبي)

    الأخطاء:
        ValueError: إذا كان شرط الانغلاق f(a)*f(b) < 0 غير متحقق أو المدخلات غير سليمة.
    """
    # 1. التحقق من صحة الفترة
    if a >= b:
        raise ValueError("يجب أن تكون بداية الفترة (a) أصغر من نهايتها (b).")

    fa = f(a)
    fb = f(b)

    # التحقق من أن أحد الطرفين هو الجذر مباشرة
    if abs(fa) < 1e-14:
        return ([{"i": 1, "a": a, "b": b, "p": a, "f_a": fa, "f_p": fa, "error": 0.0}], a)
    if abs(fb) < 1e-14:
        return ([{"i": 1, "a": a, "b": b, "p": b, "f_a": fb, "f_p": fb, "error": 0.0}], b)

    # 2. شرط نظرية القيمة المتوسطة (حصر الجذر)
    if fa * fb > 0:
        raise ValueError(
            f"شرط الحصر غير محقق:\n"
            f"f(a) = {fa:.5f} و f(b) = {fb:.5f} لهما نفس الإشارة.\n"
            f"يجب أن تكون الدالة مختلفة الإشارة عند طرفي الفترة [f(a) * f(b) < 0]."
        )

    table = []
    i = 1
    p = a
    p_prev = None

    # 3. حلقة التكرار (مطابقة لكود الماتلاب)
    while i <= max_iter:
        p = (a + b) / 2.0
        fp = f(p)
        fa = f(a)

        # حساب الخطأ: إما نصف طول الفترة |b - a| / 2 أو الفرق بين تقريبين
        error = abs(b - a) / 2.0 if p_prev is None else abs(p - p_prev)

        table.append({
            "n": i,
            "a": a,
            "b": b,
            "c": p,
            "f_a": fa,
            "f_b": f(b),
            "f_c": fp,
            "error": error
        })

        # شرط التوقف إذا وصلنا للجذر بدقة تامة أو تحققت الدقة المطلوبة
        if abs(fp) < 1e-14 or error <= tol:
            break

        # تحديث حدود الفترة بحسب إشارة f(a) * f(p)
        if fa * fp < 0:
            b = p
        else:
            a = p

        p_prev = p
        i += 1

    return table, p
