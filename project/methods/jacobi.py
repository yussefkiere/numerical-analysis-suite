"""
=============================================================================
خوارزمية طريقة جاكوبي التكرارية (Jacobi Iterative Method)
=============================================================================
المقابل في كود الماتلاب: jacobi.m
- اسم الدالة في الماتلاب: function jacobi(A, B, n, e)
- جدول مطابقة الأسطر:
  ماتلاب: فحص السيادة القطرية: abs(A(i,i)) > sum(abs(A(i,:))) - abs(A(i,i))
  ماتلاب: التكرار: x_new(i) = (B(i) - sum_{j~=i} A(i,j)*x_old(j)) / A(i,i)
  ماتلاب: شرط التوقف: norm(x_new - x_old) <= e
=============================================================================
"""

from typing import List, Tuple, Dict, Any, Optional


def check_diagonal_dominance(A: List[List[float]]) -> Tuple[bool, str]:
    """
    التحقق من شرط السيادة القطرية الصارمة للمصفوفة A.
    """
    n = len(A)
    violations = []
    for i in range(n):
        diag = abs(A[i][i])
        off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diag <= off_diag_sum:
            violations.append(
                f"الصف {i+1}: |{A[i][i]}| لا تتجاوز مجموع باقي العناصر {off_diag_sum}"
            )

    if violations:
        msg = (
            "⚠️ تنبيه: المصفوفة لا تحقق شرط السيادة القطرية الصارمة تماماً:\n"
            + "\n".join(violations[:3]) +
            "\nقد تتباعد طريقة جاكوبي أو تستغرق تكرارات أكثر للتقارب."
        )
        return False, msg
    return True, "المصفوفة مهيمنة قطرياً بشكل صارم؛ التقارب مضمون رياضياً."


def jacobi_method(
    A: List[List[float]],
    B: List[float],
    X0: Optional[List[float]] = None,
    tol: float = 1e-4,
    max_iter: int = 50
) -> Tuple[List[Dict[str, Any]], str, str]:
    """
    حل النظام الخطي AX = B تكرارياً بطريقة جاكوبي.

    المخرجات:
        Tuple[List[Dict], str, str]: (جدول التكرارات، نص الحل النهائي، رسالة التحذير إن وجدت)
    """
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("يجب أن تكون مصفوفة المعاملات A مربعة (n x n).")
    if len(B) != n:
        raise ValueError("طول متجه الثوابت B يجب أن يطابق عدد صفوف A.")

    # التحقق من عدم وجود عناصر قطرية صفرية
    for i in range(n):
        if abs(A[i][i]) < 1e-14:
            raise ValueError(f"العنصر القطري a({i+1},{i+1}) يساوي صفراً؛ لا يمكن القسمة عليه في جاكوبي.")

    # فحص السيادة القطرية
    is_dominant, dominance_msg = check_diagonal_dominance(A)

    # التخمين الأولي الافتراضي (أصفار)
    if X0 is None or len(X0) != n:
        curr_X = [0.0] * n
    else:
        curr_X = [float(x) for x in X0]

    table = []
    # تسجيل التكرار الأولي k=0
    init_row = {"n": 0}
    for j in range(n):
        init_row[f"x{j+1}"] = curr_X[j]
    init_row["error"] = "-"
    table.append(init_row)

    k = 1
    while k <= max_iter:
        next_X = [0.0] * n
        for i in range(n):
            s = sum(A[i][j] * curr_X[j] for j in range(n) if j != i)
            next_X[i] = (B[i] - s) / A[i][i]

        # فحص تباعد الأرقام
        if any(abs(val) > 1e12 for val in next_X):
            raise ValueError(f"فشل التقارب في جاكوبي: تباعدت القيم عند التكرار {k}.")

        # حساب أقصى خطأ مطلق بين التكرارين
        err = max(abs(next_X[i] - curr_X[i]) for i in range(n))

        row_dict = {"n": k}
        for j in range(n):
            row_dict[f"x{j+1}"] = next_X[j]
        row_dict["error"] = err
        table.append(row_dict)

        if err <= tol:
            curr_X = next_X
            break

        curr_X = next_X
        k += 1

    sol_parts = [f"x{i+1} = {curr_X[i]:.6f}" for i in range(n)]
    result_str = " ، ".join(sol_parts)

    return table, result_str
