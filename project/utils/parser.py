"""
وحدة معالجة وتحليل الدوال الرياضية (Expression Parser)
======================================================
تحويل النصوص الرياضية المدخلة من المستخدم إلى دوال بايثون عددية قابلة للحساب.
تعتمد على مكتبة SymPy للتحليل الرمزي والتفاضل التلقائي.
"""

from typing import Callable
import sympy
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

# قاموس المعرفات الرياضية المسموح بها في الدوال
MATH_SYMBOLS = {
    'e': sympy.E,
    'E': sympy.E,
    'pi': sympy.pi,
    'sin': sympy.sin,
    'cos': sympy.cos,
    'tan': sympy.tan,
    'exp': sympy.exp,
    'log': sympy.log,
    'ln': sympy.log,
    'sqrt': sympy.sqrt,
    'abs': sympy.Abs,
}

# قواعد التحويل لتحليل النص الرياضي (دعم ^ كرفع للأس، ودعم الضرب الضمني مثل 3x)
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def _parse_to_sympy_expr(expr_str: str) -> tuple[sympy.Expr, sympy.Symbol]:
    """
    دالة مساعدة داخلية لتحليل النص الرياضي والتأكد من صحته ورموزه.

    المعاملات:
        expr_str (str): نص الدالة المدخلة من المستخدم (مثال: 'x^3 - x - 2').

    المخرجات:
        tuple[sympy.Expr, sympy.Symbol]: التعبير الرمزي والمتغير x.

    الأخطاء:
        ValueError: إذا كان النص فارغاً أو به خطأ في الصياغة أو يحتوي على متغيرات غير x.
    """
    if not isinstance(expr_str, str) or not expr_str.strip():
        raise ValueError("صيغة الدالة فارغة، يرجى إدخال معادلة رياضية صحيحة (مثال: x^3 - x - 2).")

    # تنظيف النص واستبدال الرفع بالأس للتوافق التام
    clean_str = expr_str.strip().replace('^', '**')

    try:
        sym_expr = parse_expr(
            clean_str,
            transformations=TRANSFORMATIONS,
            local_dict=MATH_SYMBOLS,
        )
    except Exception as exc:
        raise ValueError(
            f"خطأ في صياغة الدالة: '{expr_str}'. "
            "تأكد من كتابة الأقواس والعمليات الرياضية بشكل سليم."
        ) from exc

    x = sympy.Symbol('x')
    # التحقق من أن المتغير الوحيد هو x
    unknown_vars = [sym for sym in sym_expr.free_symbols if sym != x]
    if unknown_vars:
        vars_names = ", ".join(str(s) for s in unknown_vars)
        raise ValueError(
            f"المتغير المدعوم في الدالة هو (x) فقط. تم العثور على متغيرات غير معروفة: {vars_names}"
        )

    return sym_expr, x


def make_function(expr_str: str) -> Callable[[float], float]:
    """
    تحويل نص دالة رياضية إلى دالة بايثون عددية.

    تقبل نصوصاً بصيغ رياضية متنوعة مثل:
      - 'x**3 - x - 2'
      - 'x^3 - x - 2'
      - 'cos(x) - x'
      - 'e^x - 3x'

    المعاملات:
        expr_str (str): صيغة الدالة كنص.

    المخرجات:
        Callable[[float], float]: دالة تستقبل x وتعيد قيمة float.

    الأخطاء:
        ValueError: رسالة عربية واضحة عند وجود خطأ في الصياغة أو التعويض.
    """
    sym_expr, x = _parse_to_sympy_expr(expr_str)

    # إنشاء دالة عددية سريعة باستخدام lambdify
    raw_callable = sympy.lambdify(x, sym_expr, modules=['math', 'sympy'])

    def numerical_function(val: float) -> float:
        try:
            result = raw_callable(float(val))
            # في حال أعاد الحساب عدداً مركباً (تخيلياً)
            if isinstance(result, complex):
                if abs(result.imag) < 1e-12:
                    return float(result.real)
                raise ValueError(
                    f"التعويض بالقيمة x = {val} أنتج عدداً تخيلياً غير حقيقي."
                )
            return float(result)
        except ZeroDivisionError:
            raise ValueError(f"قسمة على الصفر حدثت عند التعويض بالقيمة x = {val}")
        except ValueError:
            raise
        except Exception as err:
            raise ValueError(f"خطأ حسابي عند التعويض بالقيمة x = {val}: {err}")

    return numerical_function


def derivative(expr_str: str) -> Callable[[float], float]:
    """
    اشتقاق الدالة رمزياً وإرجاع دالة المشتقة الأولى f'(x) كدالة عددية.
    (تستخدم خاصة في طريقة نيوتن - رافسون).

    المعاملات:
        expr_str (str): صيغة الدالة الأصلية f(x).

    المخرجات:
        Callable[[float], float]: دالة المشتقة f'(x) تقبل x وتعيد float.
    """
    sym_expr, x = _parse_to_sympy_expr(expr_str)
    # التفاضل الرمزي بالنسبة لـ x
    diff_expr = sym_expr.diff(x)

    raw_diff_callable = sympy.lambdify(x, diff_expr, modules=['math', 'sympy'])

    def numerical_derivative(val: float) -> float:
        try:
            result = raw_diff_callable(float(val))
            if isinstance(result, complex):
                if abs(result.imag) < 1e-12:
                    return float(result.real)
                raise ValueError(
                    f"حساب المشتقة عند x = {val} أنتج عدداً تخيلياً."
                )
            return float(result)
        except ZeroDivisionError:
            raise ValueError(f"قسمة على الصفر في المشتقة عند x = {val}")
        except ValueError:
            raise
        except Exception as err:
            raise ValueError(f"خطأ أثناء حساب المشتقة عند x = {val}: {err}")

    return numerical_derivative


