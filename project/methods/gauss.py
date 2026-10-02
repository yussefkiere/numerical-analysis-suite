"""
=============================================================================
خوارزمية حذف جاوس والتعويض العكسي (Gaussian Elimination)
=============================================================================
المقابل في كود الماتلاب: gauss.m
- اسم الدالة في الماتلاب: function gauss(A, B)
- جدول مطابقة الأسطر:
  ماتلاب السطور 1-2:   n = length(A);
  ماتلاب السطور 3-10:  حلقة k وحساب معامل الضرب وتحديث الصف:
                       L = -A(i, k) / A(k, k);
                       A(i, :) = A(i, :) + L * A(k, :);
                       B(i) = B(i) + L * B(k);
  ماتلاب السطور 11-17: مرحلة التعويض العكسي:
                       X(n) = B(n) / A(n, n);
                       X(i) = (B(i) - A(i, i+1:n) * X(i+1:n)) / A(i, i);
=============================================================================
"""

import copy
from typing import List, Tuple, Dict, Any


def gaussian_elimination_method(
    A: List[List[float]],
    B: List[float]
) -> Tuple[List[Dict[str, Any]], str]:
    """
    حل نظام المعادلات الخطية AX = B بحذف جاوس مع تسجيل خطوات السبورة.

    المعاملات:
        A: مصفوفة المعاملات (مربعة n x n)
        B: متجه الحدود المطلقة (الثوابت)

    المخرجات:
        Tuple[List[Dict], str]: (جدول خطوات الحذف والتعويض العكسي، نص الحل النهائي)
    """
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("يجب أن تكون مصفوفة المعاملات A مربعة (n x n).")
    if len(B) != n:
        raise ValueError("طول متجه الثوابت B يجب أن يطابق عدد صفوف المصفوفة A.")

    # نسخ مصفوفة المعاملات والمتجه لتجنب تعديل الأصل
    M = [row[:] for row in A]
    V = B[:]
    table = []

    # 1. مرحلة الحذف الأمامي (Forward Elimination)
    for k in range(n - 1):
        pivot = M[k][k]

        # فحص إذا كان عنصر الارتكاز صفراً والتبديل الجزئي (Partial Pivoting)
        if abs(pivot) < 1e-12:
            max_row = k
            for r in range(k + 1, n):
                if abs(M[r][k]) > abs(M[max_row][k]):
                    max_row = r
            if abs(M[max_row][k]) < 1e-12:
                raise ValueError(
                    f"عنصر الارتكاز في العمود {k+1} يساوي صفراً تماماً؛ النظام ليس له حل وحيد."
                )
            # تبديل الصفوف
            M[k], M[max_row] = M[max_row], M[k]
            V[k], V[max_row] = V[max_row], V[k]
            pivot = M[k][k]
            table.append({
                "step": f"المرحلة k={k+1}",
                "operation": f"تبديل الصف R{k+1} مع R{max_row+1}",
                "augmented_row": f"الارتكاز الجديد = {pivot:.6f}",
                "state": "تبديل لتفادي القسمة على صفر"
            })

        for i in range(k + 1, n):
            factor = M[i][k] / pivot
            # R_i = R_i - factor * R_k
            for j in range(k, n):
                M[i][j] -= factor * M[k][j]
            V[i] -= factor * V[k]
            M[i][k] = 0.0  # تصفير القيمة تحت القطر بدقة

            row_str = "  ".join(f"{val:9.4f}" for val in M[i])
            table.append({
                "step": f"حذف k={k+1}",
                "operation": f"R{i+1} - ({factor:.4f}) R{k+1} -> R{i+1}",
                "augmented_row": f"[ {row_str} | {V[i]:9.4f} ]",
                "state": f"تصفير العنصر a({i+1},{k+1})"
            })

    # التحقق من العنصر الأخير
    if abs(M[n - 1][n - 1]) < 1e-12:
        raise ValueError("المصفوفة منفردة (Singular Matrix)؛ النظام ليس له حل وحيد.")

    # 2. مرحلة التعويض العكسي (Back Substitution)
    X = [0.0] * n
    X[n - 1] = V[n - 1] / M[n - 1][n - 1]
    table.append({
        "step": "تعويض خلفي",
        "operation": f"x{n} = {V[n-1]:.4f} / {M[n-1][n-1]:.4f}",
        "augmented_row": f"x{n} = {X[n-1]:.6f}",
        "state": f"قيمة المجهول الأخير x{n}"
    })

    for i in range(n - 2, -1, -1):
        s = sum(M[i][j] * X[j] for j in range(i + 1, n))
        X[i] = (V[i] - s) / M[i][i]
        table.append({
            "step": "تعويض خلفي",
            "operation": f"x{i+1} = ({V[i]:.4f} - {s:.4f}) / {M[i][i]:.4f}",
            "augmented_row": f"x{i+1} = {X[i]:.6f}",
            "state": f"قيمة المجهول x{i+1}"
        })

    # صياغة نص النتيجة النهائية
    sol_parts = [f"x{i+1} = {X[i]:.6f}" for i in range(n)]
    result_str = " ، ".join(sol_parts)

    return table, result_str
