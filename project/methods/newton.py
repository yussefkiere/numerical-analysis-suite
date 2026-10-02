"""
=============================================================================
خوارزمية طريقة نيوتن - رافسون (Newton-Raphson Method)
=============================================================================
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
=============================================================================
"""

from typing import Callable, List, Dict, Any, Tuple


def newton_method(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-4,
    max_iter: int = 50
) -> Tuple[List[Dict[str, Any]], float]:
    """
    حساب جذر المعادلة بطريقة نيوتن - رافسون باستخدام الدالة ومشتقتها.

    المعاملات:
        f (Callable): دالة المعادلة f(x)
        df (Callable): مشتقة الدالة f'(x)
        x0 (float): النقطة الابتدائية
        tol (float): مستوى الخطأ المسموح به
        max_iter (int): أقصى عدد للتكرارات

    المخرجات:
        Tuple[List[Dict], float]: (جدول التكرارات كقائمة قواميس، قيمة الجذر)
    """
    table = []
    curr_x = x0
    i = 0

    while i <= max_iter:
        fx = f(curr_x)
        dfx = df(curr_x)

        if abs(dfx) < 1e-15:
            raise ValueError(
                f"فشل في التكرار {i}: المشتقة f'({curr_x:.4f}) تساوي صفراً.\n"
                "لا يمكن القسمة على الصفر في طريقة نيوتن (المماس يوازي محور السينات)."
            )

        # حساب النقطة التالية x_{i+1}
        next_x = curr_x - (fx / dfx)
        error = abs(next_x - curr_x)

        table.append({
            "n": i,
            "x_n": curr_x,
            "f_xn": fx,
            "df_xn": dfx,
            "x_next": next_x,
            "error": error
        })

        if abs(fx) < 1e-14 or error <= tol:
            return table, next_x

        curr_x = next_x
        i += 1

    return table, curr_x
