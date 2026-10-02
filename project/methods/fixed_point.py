"""
=============================================================================
خوارزمية طريقة النقطة الثابتة (Fixed Point Iteration)
=============================================================================
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
=============================================================================
"""

from typing import Callable, List, Dict, Any, Tuple


def fixed_point_method(
    g: Callable[[float], float],
    x0: float,
    tol: float = 1e-4,
    max_iter: int = 50
) -> Tuple[List[Dict[str, Any]], float]:
    """
    حساب جذر المعادلة بطريقة النقطة الثابتة بالصيغة x = g(x).

    المعاملات:
        g (Callable): دالة التكرار g(x)
        x0 (float): القيمة الابتدائية
        tol (float): مستوى الخطأ المسموح به
        max_iter (int): أقصى عدد للتكرارات

    المخرجات:
        Tuple[List[Dict], float]: (جدول التكرارات كقائمة قواميس، قيمة الجذر)
    """
    table = []
    curr_x = x0
    i = 0

    while i <= max_iter:
        try:
            next_x = g(curr_x)
        except Exception as exc:
            raise ValueError(f"خطأ أثناء حساب g({curr_x:.4f}): {exc}")

        # التحقق من تباعد القيم (Divergence Check)
        if abs(next_x) > 1e12:
            raise ValueError(
                f"فشل التقارب: الدالة تتباعد عند التكرار {i} (القيمة وصلت {next_x:.2e}).\n"
                "تأكد من اختيار صيغة مناسبة لـ g(x) تحقق شرط التقارب |g'(x)| < 1."
            )

        error = abs(next_x - curr_x)

        table.append({
            "n": i,
            "x_n": curr_x,
            "g_xn": next_x,
            "error": error
        })

        if error <= tol:
            return table, next_x

        curr_x = next_x
        i += 1

    return table, curr_x
