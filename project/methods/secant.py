"""
=============================================================================
خوارزمية طريقة القاطع (Secant Method)
=============================================================================
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
=============================================================================
"""

from typing import Callable, List, Dict, Any, Tuple


def secant_method(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-4,
    max_iter: int = 50
) -> Tuple[List[Dict[str, Any]], float]:
    """
    حساب جذر المعادلة بطريقة القاطع باستخدام نقطتين ابتدائيتين.

    المعاملات:
        f (Callable): دالة المعادلة f(x)
        x0 (float): النقطة الابتدائية الأولى
        x1 (float): النقطة الابتدائية الثانية
        tol (float): الدقة المطلوبة
        max_iter (int): أقصى عدد للتكرارات

    المخرجات:
        Tuple[List[Dict], float]: (جدول التكرارات كقائمة قواميس، قيمة الجذر)
    """
    if abs(x1 - x0) < 1e-15:
        raise ValueError("يجب اختيار نقطتين ابتدائيتين مختلفتين (x0 != x1).")

    table = []
    i = 1

    curr_x0 = x0
    curr_x1 = x1

    while i <= max_iter:
        f0 = f(curr_x0)
        f1 = f(curr_x1)

        denom = f1 - f0
        if abs(denom) < 1e-15:
            raise ValueError(
                f"فشل في التكرار {i}: المشتقة التقريبية تساوي صفراً [f(x1) - f(x0) = 0] (قسمة على صفر)."
            )

        # حساب النقطة التالية باستخدام معادلة القاطع
        p = curr_x1 - (f1 * (curr_x1 - curr_x0)) / denom
        fp = f(p)
        error = abs(p - curr_x1)

        table.append({
            "n": i,
            "x_prev": curr_x0,
            "x_curr": curr_x1,
            "f_x_prev": f0,
            "f_x_curr": f1,
            "x_next": p,
            "error": error
        })

        if abs(fp) < 1e-14 or error <= tol:
            return table, p

        # تحديث النقطتين للتكرار التالي
        curr_x0 = curr_x1
        curr_x1 = p
        i += 1

    return table, curr_x1
