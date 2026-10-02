"""
=============================================================================
خوارزمية طريقة معكوس المصفوفة (Matrix Inversion Method via Gauss-Jordan)
=============================================================================
ملاحظة الماتلاب:
لا يوجد كود ماتلاب مقابل، كُتبت مباشرة بالبايثون.
تعتمد على إيجاد معكوس المصفوفة A^-1 بتطبيق حذف جاوس-جوردان على
المصفوفة الموسعة مع مصفوفة الوحدة [A | I]， ثم حساب حل النظام: X = A^-1 * B.
=============================================================================
"""

import copy
from typing import List, Tuple, Dict, Any


def matrix_inversion_method(
    A: List[List[float]],
    B: List[float]
) -> Tuple[List[Dict[str, Any]], str]:
    """
    حل النظام الخطي AX = B عن طريق إيجاد المعكوس A^-1 بجاوس-جوردان ثم ضربه في B.

    المخرجات:
        Tuple[List[Dict], str]: (جدول مراحل إيجاد المعكوس والضرب، نص الحل والمعكوس)
    """
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("يجب أن تكون مصفوفة المعاملات A مربعة (n x n).")
    if len(B) != n:
        raise ValueError("طول متجه الثوابت B يجب أن يطابق عدد صفوف المصفوفة A.")

    # 1. بناء المصفوفة الموسعة [A | I]
    aug = []
    for i in range(n):
        row = [float(x) for x in A[i]]
        # إضافة صف مصفوفة الوحدة I
        identity_part = [1.0 if j == i else 0.0 for j in range(n)]
        aug.append(row + identity_part)

    table = []

    # 2. تطبيق جاوس-جوردان لتحويل [A | I] إلى [I | A^-1]
    for k in range(n):
        # البحث عن أكبر عنصر ارتكاز في العمود k
        max_row = k
        for r in range(k + 1, n):
            if abs(aug[r][k]) > abs(aug[max_row][k]):
                max_row = r

        if abs(aug[max_row][k]) < 1e-12:
            raise ValueError(
                f"المصفوفة منفردة (غير قابلة للعكس)؛ عنصر الارتكاز في العمود {k+1} يساوي صفراً."
            )

        # تبديل الصفوف إن لزم
        if max_row != k:
            aug[k], aug[max_row] = aug[max_row], aug[k]
            table.append({
                "step": f"تبديل k={k+1}",
                "operation": f"تبديل الصف R{k+1} مع R{max_row+1}",
                "row_preview": f"عنصر الارتكاز = {aug[k][k]:.4f}",
                "result_info": "تبديل الصفوف"
            })

        # قسمة الصف k على عنصر الارتكاز ليصبح العنصر القطري = 1
        pivot = aug[k][k]
        for c in range(2 * n):
            aug[k][c] /= pivot

        table.append({
            "step": f"توحيد القطر k={k+1}",
            "operation": f"قسمة R{k+1} على {pivot:.4f} لجعل القطر = 1",
            "row_preview": " ، ".join(f"{aug[k][c]:.3f}" for c in range(n)),
            "result_info": "عنصر القطر أصبح 1.0"
        })

        # تصفير باقي عناصر العمود k في جميع الصفوف الأخرى
        for r in range(n):
            if r != k:
                factor = aug[r][k]
                if abs(factor) > 1e-15:
                    for c in range(2 * n):
                        aug[r][c] -= factor * aug[k][c]
                    aug[r][k] = 0.0

                    table.append({
                        "step": f"تصفير العمود {k+1}",
                        "operation": f"R{r+1} - ({factor:.3f}) R{k+1} -> R{r+1}",
                        "row_preview": " ، ".join(f"{aug[r][c]:.3f}" for c in range(n)),
                        "result_info": f"تصفير a({r+1},{k+1})"
                    })

    # استخراج مصفوفة المعكوس A^-1 من النصف الأيمن
    inv_A = []
    for i in range(n):
        inv_A.append(aug[i][n: 2 * n])

    # 3. حساب حل النظام: X = A^-1 * B
    X = [0.0] * n
    for i in range(n):
        X[i] = sum(inv_A[i][j] * B[j] for j in range(n))
        table.append({
            "step": f"ضرب X[{i+1}]",
            "operation": f"الصف {i+1} من المعكوس ضرب المتجه B",
            "row_preview": f"x{i+1} = {X[i]:.6f}",
            "result_info": f"المجهول x{i+1}"
        })

    # تجهيز عرض نص المعكوس والحل
    inv_lines = []
    for r in range(n):
        line = "   ".join(f"{val:9.4f}" for val in inv_A[r])
        inv_lines.append(f"[ {line} ]")
    inv_str = "\n".join(inv_lines)

    sol_parts = [f"x{i+1} = {X[i]:.6f}" for i in range(n)]
    result_str = (
        "مصفوفة المعكوس A⁻¹:\n" + inv_str +
        "\n\nمتجه الحل النهائي:  " + " ، ".join(sol_parts)
    )

    return table, result_str
