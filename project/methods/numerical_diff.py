"""
=============================================================================
خوارزمية التفاضل العددي بصيغ تايلور والفروق المنتهية (Numerical Differentiation)
=============================================================================
ملاحظة الماتلاب:
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
تعتمد على مفكوك متسلسلة تايلور لحساب المشتقات الأولى والثانية عددياً:
1. الفرق الأمامي للمشتقة الأولى: f'(x0) ≈ (f(x0 + h) - f(x0)) / h  [O(h)]
2. الفرق الخلفي للمشتقة الأولى: f'(x0) ≈ (f(x0) - f(x0 - h)) / h  [O(h)]
3. الفرق المركزي للمشتقة الأولى: f'(x0) ≈ (f(x0 + h) - f(x0 - h)) / (2h)  [O(h^2)]
4. الفرق المركزي للمشتقة الثانية: f''(x0) ≈ (f(x0 + h) - 2f(x0) + f(x0 - h)) / (h^2)
=============================================================================
"""

from typing import Callable, List, Tuple, Dict, Any
import sympy
from utils.parser import _parse_to_sympy_expr


def numerical_differentiation_method(
    func_str: str,
    x0: float,
    h: float = 0.01
) -> Tuple[List[Dict[str, Any]], str]:
    """
    حساب المشتقة الأولى والثانية عددياً ومقارنتها بالقيمة الدقيقة لـ SymPy.

    المعاملات:
        func_str: نص الدالة الرياضية f(x)
        x0: النقطة المراد حساب المشتقة عندها
        h: مقدار الخطوة التفاضلية

    المخرجات:
        Tuple[List[Dict], str]: (جدول الصيغ والقيم والخطأ، نص ملخص المشتقات)
    """
    if abs(h) < 1e-15:
        raise ValueError("مقدار الخطوة h يجب ألا يساوي صفراً.")

    # تحليل الدالة واستخراج المشتقات الرمزية الدقيقة
    sym_expr, x_sym = _parse_to_sympy_expr(func_str)
    diff1_sym = sym_expr.diff(x_sym)
    diff2_sym = diff1_sym.diff(x_sym)

    f_raw = sympy.lambdify(x_sym, sym_expr, modules=['math', 'sympy'])
    d1_raw = sympy.lambdify(x_sym, diff1_sym, modules=['math', 'sympy'])
    d2_raw = sympy.lambdify(x_sym, diff2_sym, modules=['math', 'sympy'])

    # حساب النقاط الثلاث: f(x0), f(x0 + h), f(x0 - h)
    f_x0 = float(f_raw(x0))
    f_plus = float(f_raw(x0 + h))
    f_minus = float(f_raw(x0 - h))

    # القيم التحليلية الدقيقة
    exact_d1 = float(d1_raw(x0))
    exact_d2 = float(d2_raw(x0))

    # 1. الفرق الأمامي للمشتقة الأولى
    fwd_d1 = (f_plus - f_x0) / h
    # 2. الفرق الخلفي للمشتقة الأولى
    bwd_d1 = (f_x0 - f_minus) / h
    # 3. الفرق المركزي للمشتقة الأولى
    cnt_d1 = (f_plus - f_minus) / (2.0 * h)
    # 4. الفرق المركزي للمشتقة الثانية
    cnt_d2 = (f_plus - 2.0 * f_x0 + f_minus) / (h ** 2)

    table = [
        {
            "formula_name": "الفرق الأمامي f'(x0)",
            "rule": "(f(x0+h) - f(x0)) / h",
            "calc_val": fwd_d1,
            "exact_val": exact_d1,
            "error": abs(fwd_d1 - exact_d1)
        },
        {
            "formula_name": "الفرق الخلفي f'(x0)",
            "rule": "(f(x0) - f(x0-h)) / h",
            "calc_val": bwd_d1,
            "exact_val": exact_d1,
            "error": abs(bwd_d1 - exact_d1)
        },
        {
            "formula_name": "الفرق المركزي f'(x0) [الأدق]",
            "rule": "(f(x0+h) - f(x0-h)) / (2h)",
            "calc_val": cnt_d1,
            "exact_val": exact_d1,
            "error": abs(cnt_d1 - exact_d1)
        },
        {
            "formula_name": "الفرق المركزي للمشتقة الثانية f''(x0)",
            "rule": "(f(x0+h) - 2f(x0) + f(x0-h)) / h²",
            "calc_val": cnt_d2,
            "exact_val": exact_d2,
            "error": abs(cnt_d2 - exact_d2)
        }
    ]

    result_str = (
        f"المشتقة الأولى بالفرق المركزي:  f'({x0}) ≈ {cnt_d1:.6f}   (الدقيقة: {exact_d1:.6f})\n"
        f"المشتقة الثانية بالفرق المركزي: f''({x0}) ≈ {cnt_d2:.6f}   (الدقيقة: {exact_d2:.6f})\n\n"
        f"معامل الخطوة المستخدم: h = {h}"
    )

    return table, result_str
