"""
=============================================================================
خوارزمية قاعدة شبه المنحرف المركبة (Composite Trapezoidal Rule)
=============================================================================
ملاحظة الماتلاب:
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
تقسم المساحة تحت منحنى الدالة f(x) على الفترة [a, b] إلى n من الشرائح
المتساوية بعرض h = (b - a) / n، وتطبق القاعدة:
I ≈ (h / 2) * [ f(x0) + 2*f(x1) + 2*f(x2) + ... + 2*f(xn-1) + f(xn) ]
=============================================================================
"""

from typing import Callable, List, Tuple, Dict, Any


def composite_trapezoidal_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    n: int
) -> Tuple[List[Dict[str, Any]], str]:
    """
    حساب التكامل المحدد عددياً بقاعدة شبه المنحرف المركبة.

    المعاملات:
        f: دالة التكامل f(x)
        a: الحد الأدنى للتكامل
        b: الحد الأعلى للتكامل
        n: عدد الشرائح (التقسيمات)

    المخرجات:
        Tuple[List[Dict], str]: (جدول النقاط والمعاملات، نص النتيجة وقيمة التكامل)
    """
    if a >= b:
        raise ValueError("يجب أن يكون الحد الأدنى للتكامل a أصغر من الحد الأعلى b.")
    if n < 1:
        raise ValueError("عدد التقسيمات n يجب أن يكون عدداً صحيحاً أكبر من أو يساوي 1.")

    h = (b - a) / float(n)
    table = []
    total_weighted_sum = 0.0

    for i in range(n + 1):
        xi = a + i * h
        try:
            f_xi = f(xi)
        except Exception as exc:
            raise ValueError(f"خطأ أثناء حساب قيمة الدالة عند x = {xi:.4f}: {exc}")

        # المعامل: 1 عند الطرفين (الأول والأخير) و 2 لجميع النقاط الوسطى
        weight = 1 if (i == 0 or i == n) else 2
        weighted_val = weight * f_xi
        total_weighted_sum += weighted_val

        table.append({
            "i": i,
            "xi": xi,
            "f_xi": f_xi,
            "weight": weight,
            "weighted_val": weighted_val
        })

    integral_val = (h / 2.0) * total_weighted_sum

    result_str = (
        f"عرض الشريحة:  h = ({b} - {a}) / {n} = {h:.6f}\n"
        f"مجموع الحدود:  Σ = {total_weighted_sum:.6f}\n\n"
        f"قيمة التكامل = (h / 2) · Σ = ({h:.6f} / 2) · {total_weighted_sum:.6f} = {integral_val:.6f}"
    )

    return table, result_str
