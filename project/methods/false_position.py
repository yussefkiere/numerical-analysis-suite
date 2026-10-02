"""
=============================================================================
خوارزمية طريقة الموضع الخاطئ (False Position Method / Regula Falsi)
=============================================================================
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
=============================================================================
"""

from typing import Callable, List, Dict, Any, Tuple


def false_position_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-4,
    max_iter: int = 50
) -> Tuple[List[Dict[str, Any]], float]:
    """
    حساب جذر المعادلة بطريقة الموضع الخاطئ مع تسجيل خطوات الحل.

    المعاملات:
        f (Callable): دالة المعادلة f(x)
        a (float): بداية فترة الحصر
        b (float): نهاية فترة الحصر
        tol (float): مستوى الخطأ المسموح به
        max_iter (int): أقصى عدد للتكرارات

    المخرجات:
        Tuple[List[Dict], float]: (جدول التكرارات كقائمة قواميس، قيمة الجذر)
    """
    if a >= b:
        raise ValueError("يجب أن تكون بداية الفترة (a) أصغر من نهايتها (b).")

    fa = f(a)
    fb = f(b)

    if abs(fa) < 1e-14:
        return ([{"i": 1, "a": a, "b": b, "p": a, "f_a": fa, "f_b": fb, "f_p": fa, "error": 0.0}], a)
    if abs(fb) < 1e-14:
        return ([{"i": 1, "a": a, "b": b, "p": b, "f_a": fa, "f_b": fb, "f_p": fb, "error": 0.0}], b)

    if fa * fb > 0:
        raise ValueError(
            f"شرط الحصر غير محقق:\n"
            f"f(a) = {fa:.5f} و f(b) = {fb:.5f} لهما نفس الإشارة.\n"
            f"يجب أن يكون f(a) * f(b) < 0 لوجود جذر محصور."
        )

    table = []
    i = 1
    p = a
    p_prev = None

    while i <= max_iter:
        fa = f(a)
        fb = f(b)

        denom = fb - fa
        if abs(denom) < 1e-15:
            raise ValueError(f"قسمة على الصفر في المقام [f(b) - f(a)] عند التكرار {i}.")

        # قانون الموضع الخاطئ (الوتر المتقاطع مع محور x)
        p = b - (fb * (b - a)) / denom
        fp = f(p)

        error = abs(b - a) if p_prev is None else abs(p - p_prev)

        table.append({
            "n": i,
            "a": a,
            "b": b,
            "c": p,
            "f_a": fa,
            "f_b": fb,
            "f_c": fp,
            "error": error
        })

        if abs(fp) < 1e-14 or (p_prev is not None and error <= tol):
            break

        if fa * fp < 0:
            b = p
        else:
            a = p

        p_prev = p
        i += 1

    return table, p
