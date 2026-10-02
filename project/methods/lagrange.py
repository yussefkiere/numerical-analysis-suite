"""
=============================================================================
خوارزمية استيفاء كثيرات حدود لاجرانج (Lagrange Interpolating Polynomial)
=============================================================================
المقابل في كود الماتلاب: lagrang.m
- اسم الدالة في الماتلاب: function lagrang(s, f)
- جدول مطابقة الأسطر:
  ماتلاب السطور 1-3:   n = length(s); syms x; P = 0;
  ماتلاب السطور 4-10:  حساب حدود الأساس L وجداء الأقواس:
                       L = L * (x - s(j)) / (s(i) - s(j));
                       P = P + L * f(i);
  ماتلاب السطر 11:     disp(simplify(P));
=============================================================================
"""

from typing import List, Tuple, Dict, Any
import sympy


def lagrange_interpolation_method(
    x_points: List[float],
    y_points: List[float],
    x_eval: float
) -> Tuple[List[Dict[str, Any]], str]:
    """
    حساب كثيرات حدود لاجرانج وتقدير قيمة الدالة عند نقطة معينة.

    المعاملات:
        x_points: إحداثيات النقاط السينية [x0, x1, ...]
        y_points: إحداثيات النقاط الصادية [y0, y1, ...]
        x_eval: القيمة المراد تقدير صورتها P(x)

    المخرجات:
        Tuple[List[Dict], str]: (جدول حدود الأساس والتعويض، نص النتيجة وصيغة P(x))
    """
    n = len(x_points)
    if n != len(y_points):
        raise ValueError("عدد نقاط x يجب أن يساوي تماماً عدد نقاط y.")
    if n < 2:
        raise ValueError("يلزم على الأقل نقطتان لحساب استيفاء لاجرانج.")

    # التحقق من أن جميع نقاط x متمايزة (Distinct Points)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(x_points[i] - x_points[j]) < 1e-12:
                raise ValueError(
                    f"النقاط السينية يجب أن تكون متمايزة تماماً؛ تم تكرار القيمة x = {x_points[i]}."
                )

    table = []
    p_eval = 0.0

    # إعداد الرمز x لحساب كثيرة الحدود الرمزية المبسطة بـ SymPy
    x_sym = sympy.Symbol('x')
    poly_sym = sympy.sympify(0)

    for i in range(n):
        xi = x_points[i]
        yi = y_points[i]

        # 1. حساب القيمة العددية لـ Li(x_eval)
        li_val = 1.0
        # 2. حساب الحد الرمزي لـ Li(x)
        li_sym = sympy.sympify(1)

        for j in range(n):
            if i != j:
                xj = x_points[j]
                denom = xi - xj
                li_val *= (x_eval - xj) / denom
                li_sym *= (x_sym - xj) / denom

        term_val = yi * li_val
        p_eval += term_val
        poly_sym += yi * li_sym

        table.append({
            "i": i,
            "xi": xi,
            "yi": yi,
            "li_val": li_val,
            "term_val": term_val
        })

    # تبسيط كثيرة الحدود الرمزية
    simplified_poly = sympy.simplify(poly_sym)

    result_str = (
        f"P({x_eval:.4f}) = {p_eval:.6f}\n\n"
        f"صيغة كثيرة حدود لاجرانج المبسطة:\n"
        f"P(x) = {simplified_poly}"
    )

    return table, result_str
