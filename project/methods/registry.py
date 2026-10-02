"""
السجل المركزي لتعريف الطرق والأقسام (Methods Registry)
======================================================
الملف المركزي الموحد الذي يصف كافة تصنيفات وطرق المقرر:
- معادلات غير خطية (nonlinear)
- أنظمة معادلات خطية (linear_systems)
- استيفاء وتوفيق منحنيات (interpolation)
- تفاضل وتكامل عددي (calculus)

تُبنى كافة واجهات التطبيق الرسومية ديناميكياً من هذا القاموس،
مما يتيح إضافة أو تعديل أي طريقة بسهولة فائقة دون تغيير كود الواجهات.
"""

from typing import Dict, Any

from .bisection import bisection_method
from .false_position import false_position_method
from .secant import secant_method
from .newton import newton_method
from .fixed_point import fixed_point_method
from .gauss import gaussian_elimination_method
from .jacobi import jacobi_method
from .cramer import cramer_rule_method
from .matrix_inversion import matrix_inversion_method
from .lagrange import lagrange_interpolation_method
from .trapezoidal import composite_trapezoidal_method
from .numerical_diff import numerical_differentiation_method

CATEGORIES: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------
    # [1] قسم المعادلات غير الخطية (Nonlinear Equations - Roots)
    # -------------------------------------------------------------
    "nonlinear": {
        "id": 1,
        "title": "معادلات غير خطية",
        "title_en": "Nonlinear Equations (Root Finding)",
        "badge": "1",
        "desc": "إيجاد جذور المعادلات f(x) = 0 بالطرق الحاصرة والمفتوحة",
        "type": "nonlinear",
        "methods": {
            "bisection": {
                "id": 1,
                "title": "طريقة التنصيف",
                "title_en": "Bisection Method",
                "matlab_ref": None,
                "desc": "حصر الجذر في فترة [a, b] وتنصيفها تكرارياً",
                "func": bisection_method,
                "needs_function": True,
                "needs_derivative": False,
                "is_iterative": True,
                "default_f": "x^3 - x - 2",
                "inputs": [
                    ("a", "بداية الفترة (a):", "1.0", "الحد الأدنى لفترة الحصر"),
                    ("b", "نهاية الفترة (b):", "2.0", "الحد الأقصى لفترة الحصر"),
                    ("tol", "الدقة المطلوبة (ε):", "0.0001", "شرط التوقف عند الخطأ"),
                    ("max_iter", "أقصى تكرارات (N):", "50", "حماية التكرار اللانهائي"),
                ],
                "table_columns": [
                    ("n", "n (التكرار)", 70),
                    ("a", "a", 105),
                    ("b", "b", 105),
                    ("c", "c = (a+b)/2", 115),
                    ("f_a", "f(a)", 105),
                    ("f_b", "f(b)", 105),
                    ("f_c", "f(c)", 105),
                    ("error", "الخطأ", 115),
                ],
                "result_label": "الجذر هو:"
            },
            "false_position": {
                "id": 2,
                "title": "طريقة الموضع الخاطئ",
                "title_en": "False Position Method (Regula Falsi)",
                "matlab_ref": None,
                "desc": "حصر الجذر بوتر خطي بين طرفي الفترة للتقارب السريع",
                "func": false_position_method,
                "needs_function": True,
                "needs_derivative": False,
                "is_iterative": True,
                "default_f": "x^3 - x - 2",
                "inputs": [
                    ("a", "بداية الفترة (a):", "1.0", "الحد الأدنى للفترة"),
                    ("b", "نهاية الفترة (b):", "2.0", "الحد الأقصى للفترة"),
                    ("tol", "الدقة المطلوبة (ε):", "0.0001", "شرط التوقف"),
                    ("max_iter", "أقصى تكرارات (N):", "50", "أقصى حد للخطوات"),
                ],
                "table_columns": [
                    ("n", "n (التكرار)", 70),
                    ("a", "a", 105),
                    ("b", "b", 105),
                    ("c", "c (الموضع الخاطئ)", 115),
                    ("f_a", "f(a)", 105),
                    ("f_b", "f(b)", 105),
                    ("f_c", "f(c)", 105),
                    ("error", "الخطأ", 115),
                ],
                "result_label": "الجذر هو:"
            },
            "secant": {
                "id": 3,
                "title": "طريقة القاطع",
                "title_en": "Secant Method",
                "matlab_ref": None,
                "desc": "تقريب المشتقة بميل القاطع عبر نقطتين ابتدائيتين",
                "func": secant_method,
                "needs_function": True,
                "needs_derivative": False,
                "is_iterative": True,
                "default_f": "x^3 - x - 2",
                "inputs": [
                    ("x0", "النقطة الأولى (x0):", "1.0", "النقطة الابتدائية الأولى"),
                    ("x1", "النقطة الثانية (x1):", "2.0", "النقطة الابتدائية الثانية"),
                    ("tol", "الدقة المطلوبة (ε):", "0.0001", "شرط التوقف"),
                    ("max_iter", "أقصى تكرارات (N):", "50", "أقصى حد للخطوات"),
                ],
                "table_columns": [
                    ("n", "n (التكرار)", 70),
                    ("x_prev", "x(n-1)", 115),
                    ("x_curr", "x(n)", 115),
                    ("f_x_prev", "f(x(n-1))", 115),
                    ("f_x_curr", "f(x(n))", 115),
                    ("x_next", "x(n+1)", 125),
                    ("error", "الخطأ", 115),
                ],
                "result_label": "الجذر هو:"
            },
            "newton": {
                "id": 4,
                "title": "طريقة نيوتن رافسون",
                "title_en": "Newton-Raphson Method",
                "matlab_ref": None,
                "desc": "التقارب السريع بمماس المنحنى وحساب المشتقة تلقائياً",
                "func": newton_method,
                "needs_function": True,
                "needs_derivative": True,
                "is_iterative": True,
                "default_f": "x^3 - x - 2",
                "inputs": [
                    ("x0", "النقطة الابتدائية (x0):", "1.5", "نقطة البداية للمماس"),
                    ("tol", "الدقة المطلوبة (ε):", "0.0001", "شرط التوقف"),
                    ("max_iter", "أقصى تكرارات (N):", "50", "أقصى حد للخطوات"),
                ],
                "table_columns": [
                    ("n", "n (التكرار)", 70),
                    ("x_n", "x(n)", 125),
                    ("f_xn", "f(x(n))", 125),
                    ("df_xn", "f'(x(n))", 125),
                    ("x_next", "x(n+1)", 135),
                    ("error", "الخطأ", 120),
                ],
                "result_label": "الجذر هو:"
            },
            "fixed_point": {
                "id": 5,
                "title": "طريقة النقطة الثابتة",
                "title_en": "Fixed Point Iteration",
                "matlab_ref": None,
                "desc": "صياغة المعادلة كـ x = g(x) وتكرار التعويض",
                "func": fixed_point_method,
                "needs_function": True,
                "needs_derivative": False,
                "is_iterative": True,
                "is_g_func": True,
                "default_f": "(x + 2)^(1/3)",
                "inputs": [
                    ("x0", "النقطة الابتدائية (x0):", "1.5", "نقطة البداية للتكرار"),
                    ("tol", "الدقة المطلوبة (ε):", "0.0001", "شرط التوقف"),
                    ("max_iter", "أقصى تكرارات (N):", "50", "أقصى حد للخطوات"),
                ],
                "table_columns": [
                    ("n", "n (التكرار)", 80),
                    ("x_n", "x(n)", 180),
                    ("g_xn", "g(x(n))", 200),
                    ("error", "الخطأ", 160),
                ],
                "result_label": "الجذر هو:"
            }
        }
    },

    # -------------------------------------------------------------
    # [2] قسم أنظمة المعادلات الخطية AX = B (Linear Systems)
    # -------------------------------------------------------------
    "linear_systems": {
        "id": 2,
        "title": "أنظمة معادلات خطية",
        "title_en": "Linear Systems (AX = B)",
        "badge": "2",
        "desc": "حل أنظمة المعادلات الخطية بالطرق المباشرة والتكرارية",
        "type": "linear_systems",
        "methods": {
            "gauss": {
                "id": 1,
                "title": "طريقة حذف جاوس",
                "title_en": "Gaussian Elimination",
                "matlab_ref": "gauss.m",
                "desc": "تحويل المصفوفة الموسعة [A|B] لمثلثية عليا ثم التعويض العكسي",
                "func": gaussian_elimination_method,
                "is_iterative": False,
                "default_n": 2,
                "default_A": [[2.0, 1.0], [1.0, 3.0]],
                "default_B": [5.0, 10.0],
                "table_columns": [
                    ("step", "المرحلة / الخطوة", 110),
                    ("operation", "العملية ومعامل الضرب", 240),
                    ("augmented_row", "الصف أو المجهول الناتج", 260),
                    ("state", "البيان التوضيحي", 180),
                ],
                "result_label": "حل النظام الخطي X:"
            },
            "jacobi": {
                "id": 2,
                "title": "طريقة جاكوبي التكرارية",
                "title_en": "Jacobi Iterative Method",
                "matlab_ref": "jacobi.m",
                "desc": "حل النظام تكرارياً ابتداءً من X0 مع فحص السيادة القطرية",
                "func": jacobi_method,
                "is_iterative": True,
                "default_n": 3,
                "default_A": [[8.0, 1.0, 1.0], [3.0, 5.0, -1.0], [1.0, -1.0, 5.0]],
                "default_B": [26.0, 7.0, 7.0],
                "default_X0": [0.0, 0.0, 0.0],
                "default_tol": 0.0001,
                "default_max_iter": 50,
                "table_columns": [
                    ("n", "k (التكرار)", 80),
                    ("x1", "x1", 120),
                    ("x2", "x2", 120),
                    ("x3", "x3", 120),
                    ("error", "الخطأ", 120),
                ],
                "result_label": "الحل التقريبي بنظام جاكوبي:"
            },
            "cramer": {
                "id": 3,
                "title": "طريقة قاعدة كرامر",
                "title_en": "Cramer's Rule",
                "matlab_ref": None,
                "desc": "حل النظام باستخدام المحددات العامة والمحددات البديلة det(Ai)",
                "func": cramer_rule_method,
                "is_iterative": False,
                "default_n": 2,
                "default_A": [[2.0, 1.0], [1.0, 3.0]],
                "default_B": [5.0, 10.0],
                "table_columns": [
                    ("var", "المتغير / المحدد", 110),
                    ("matrix_desc", "وصف المصفوفة", 250),
                    ("det_value", "قيمة المحدد", 140),
                    ("calculation", "صيغة الحساب", 200),
                    ("root_value", "قيمة المجهول", 120),
                ],
                "result_label": "حل النظام بقاعدة كرامر:"
            },
            "matrix_inversion": {
                "id": 4,
                "title": "طريقة معكوس المصفوفة",
                "title_en": "Matrix Inversion Method (A⁻¹)",
                "matlab_ref": None,
                "desc": "إيجاد A⁻¹ بحذف جاوس-جوردان على [A|I] ثم الحل X = A⁻¹B",
                "func": matrix_inversion_method,
                "is_iterative": False,
                "default_n": 2,
                "default_A": [[2.0, 1.0], [1.0, 3.0]],
                "default_B": [5.0, 10.0],
                "table_columns": [
                    ("step", "المرحلة", 120),
                    ("operation", "العملية", 260),
                    ("row_preview", "القيم الناتجة", 240),
                    ("result_info", "البيان", 160),
                ],
                "result_label": "معكوس المصفوفة وحل النظام:"
            }
        }
    },

    # -------------------------------------------------------------
    # [3] قسم الاستيفاء وتوفيق المنحنيات (Interpolation)
    # -------------------------------------------------------------
    "interpolation": {
        "id": 3,
        "title": "الاستيفاء",
        "title_en": "Interpolation",
        "badge": "3",
        "desc": "إيجاد دالة كثيرة حدود تمر بمجموعة نقاط معلومة وتقدير القيم بينها",
        "type": "interpolation",
        "methods": {
            "lagrange": {
                "id": 1,
                "title": "كثيرات حدود لاجرانج",
                "title_en": "Lagrange Polynomials",
                "matlab_ref": "lagrang.m",
                "desc": "استيفاء جدول نقاط (xi, yi) وحساب صيغة P(x) وتقدير نقطة",
                "func": lagrange_interpolation_method,
                "is_iterative": False,
                "default_points": [(1.0, 1.0), (2.0, 4.0), (3.0, 9.0)],
                "default_x_eval": 2.5,
                "table_columns": [
                    ("i", "i", 70),
                    ("xi", "xi", 120),
                    ("yi", "yi", 120),
                    ("li_val", "Li(x)", 180),
                    ("term_val", "yi · Li(x)", 180),
                ],
                "result_label": "قيمة وصيغة كثيرة حدود لاجرانج:"
            }
        }
    },

    # -------------------------------------------------------------
    # [4] قسم التفاضل والتكامل العددي (Numerical Calculus)
    # -------------------------------------------------------------
    "calculus": {
        "id": 4,
        "title": "التفاضل والتكامل العددي",
        "title_en": "Numerical Calculus",
        "badge": "4",
        "desc": "تقريب التكاملات المحددة وحساب المشتقات بالفروق المنتهية لتايلور",
        "type": "calculus",
        "methods": {
            "trapezoidal": {
                "id": 1,
                "title": "قاعدة شبه المنحرف المركبة",
                "title_en": "Composite Trapezoidal Rule",
                "matlab_ref": None,
                "desc": "تقسيم المساحة إلى n شريحة وحساب التكامل المحدد بالتقريب",
                "func": composite_trapezoidal_method,
                "is_iterative": False,
                "default_f": "x^2",
                "inputs": [
                    ("a", "بداية التكامل (a):", "0.0", "الحد الأدنى للتكامل"),
                    ("b", "نهاية التكامل (b):", "1.0", "الحد الأعلى للتكامل"),
                    ("n", "عدد التقسيمات (n):", "10", "عدد الشرائح"),
                ],
                "table_columns": [
                    ("i", "i (القسم)", 70),
                    ("xi", "xi", 120),
                    ("f_xi", "f(xi)", 140),
                    ("weight", "المعامل (w)", 100),
                    ("weighted_val", "المعامل × f(xi)", 160),
                ],
                "result_label": "قيمة التكامل العددي:"
            },
            "numerical_diff": {
                "id": 2,
                "title": "التفاضل العددي (صيغ تايلور)",
                "title_en": "Numerical Differentiation",
                "matlab_ref": None,
                "desc": "حساب المشتقة الأولى والثانية بصيغ الفروق ومقارنتها بالدقيقة",
                "func": numerical_differentiation_method,
                "is_iterative": False,
                "default_f": "sin(x)",
                "inputs": [
                    ("x0", "النقطة المطلوب عندها (x0):", "1.0", "قيمة x لحساب المشتقة"),
                    ("h", "مقدار الخطوة التفاضلية (h):", "0.01", "عرض الخطوة h"),
                ],
                "table_columns": [
                    ("formula_name", "صيغة الفرق", 210),
                    ("rule", "القانون المستخدم", 220),
                    ("calc_val", "القيمة المحسوبة", 130),
                    ("exact_val", "القيمة الدقيقة", 140),
                    ("error", "الخطأ المطلق", 120),
                ],
                "result_label": "المشتقات العددية المحسوبة:"
            }
        }
    }
}
