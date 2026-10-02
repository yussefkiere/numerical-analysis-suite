"""
=============================================================================
خوارزمية قاعدة كرامر لحل الأنظمة الخطية (Cramer's Rule)
=============================================================================
ملاحظة الماتلاب:
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
تعتمد على حساب محدد مصفوفة المعاملات الرئيسي det(A)، ثم استبدال
كل عمود i بمتجه الثوابت B وحساب det(Ai)، وتطبيق x_i = det(Ai) / det(A).
=============================================================================
"""

import copy
from typing import List, Tuple, Dict, Any


def determinant(matrix: List[List[float]]) -> float:
    """
    حساب محدد المصفوفة المربعة بطريقة الحذف الغوسي السريعة والدقيقة.
    """
    n = len(matrix)
    M = [row[:] for row in matrix]
    det = 1.0

    for i in range(n):
        # البحث عن أكبر عنصر في العمود الحالي (Partial Pivoting)
        pivot = i
        for r in range(i + 1, n):
            if abs(M[r][i]) > abs(M[pivot][i]):
                pivot = r

        if abs(M[pivot][i]) < 1e-15:
            return 0.0

        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
            det = -det

        det *= M[i][i]
        diag = M[i][i]

        for r in range(i + 1, n):
            factor = M[r][i] / diag
            for c in range(i + 1, n):
                M[r][c] -= factor * M[i][c]

    return det


def cramer_rule_method(
    A: List[List[float]],
    B: List[float]
) -> Tuple[List[Dict[str, Any]], str]:
    """
    حل النظام الخطي AX = B بقاعدة كرامر.

    المخرجات:
        Tuple[List[Dict], str]: (جدول المحددات والقسمة، نص الحل النهائي)
    """
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("يجب أن تكون مصفوفة المعاملات A مربعة (n x n).")
    if len(B) != n:
        raise ValueError("طول متجه الثوابت B يجب أن يطابق عدد صفوف المصفوفة A.")

    # 1. حساب المحدد العام det(A)
    det_A = determinant(A)

    table = []
    table.append({
        "var": "det(A)",
        "matrix_desc": "محدد مصفوفة المعاملات الأساسية |A|",
        "det_value": det_A,
        "calculation": "المحدد العام",
        "root_value": "-"
    })

    if abs(det_A) < 1e-12:
        raise ValueError(
            f"محدد المصفوفة det(A) = {det_A:.6f} مساوٍ للصفر؛ النظام ليس له حل وحيد (المصفوفة منفردة)."
        )

    # 2. حساب المحددات الفرعية det(A_i) لكل متغير
    X = []
    for i in range(n):
        # استبدال العمود i بالمتجه B
        A_sub = [row[:] for row in A]
        for r in range(n):
            A_sub[r][i] = B[r]

        det_Ai = determinant(A_sub)
        xi = det_Ai / det_A
        X.append(xi)

        table.append({
            "var": f"x{i+1}",
            "matrix_desc": f"محدد det(A{i+1}) بعد استبدال العمود {i+1} بـ B",
            "det_value": det_Ai,
            "calculation": f"det(A{i+1}) / det(A) = {det_Ai:.4f} / {det_A:.4f}",
            "root_value": f"{xi:.6f}"
        })

    sol_parts = [f"x{i+1} = {X[i]:.6f}" for i in range(n)]
    result_str = " ، ".join(sol_parts)

    return table, result_str
