"""
نظام المظهر والتصميم الحديث (Modern Design System & Theme)
============================================================
تعريف مركزي موحد لكافة رموز التصميم (Design Tokens):
- لوحة الألوان للنمطين الداكن والفاتح (Dark / Light Tuples)
- مقاييس الخطوط (Cairo / Segoe UI)
- أنصاف الأقطار وهوامش الحواف
- دوال المساعدة للغة العربية وتنسيق الجداول
"""

import sys
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

# =============================================================
# 1. الخطوط واكتشاف الخط العربي الأنسب
# =============================================================
def _detect_best_arabic_font() -> str:
    """اكتشاف أفضل خط عربي متوفر في النظام بترتيب الأفضلية."""
    try:
        # إنشاء نافذة مؤقتة مخفية لاكتشاف الخطوط إن لم تكن هناك نافذة قائمة
        temp_root = None
        if not tk._default_root:
            temp_root = tk.Tk()
            temp_root.withdraw()
        families = [f.lower() for f in tkfont.families()]
        if temp_root:
            temp_root.destroy()

        if any("cairo" in f for f in families):
            return "Cairo"
        if any("tajawal" in f for f in families):
            return "Tajawal"
        if any("segoe ui" in f for f in families):
            return "Segoe UI"
        return "Tahoma"
    except Exception:
        return "Segoe UI"


FONT_FAMILY = _detect_best_arabic_font()
FONT_MONO_FAMILY = "Consolas"

# أحجام الخطوط المعتمدة بالمواصفات
FONT_TITLE = (FONT_FAMILY, 28, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 18, "bold")
FONT_SECTION = (FONT_FAMILY, 16, "bold")
FONT_BODY = (FONT_FAMILY, 14)
FONT_BODY_BOLD = (FONT_FAMILY, 14, "bold")
FONT_SMALL = (FONT_FAMILY, 12)
FONT_SMALL_BOLD = (FONT_FAMILY, 12, "bold")
FONT_TINY = (FONT_FAMILY, 10)
FONT_MONO = (FONT_MONO_FAMILY, 13)
FONT_MONO_BOLD = (FONT_MONO_FAMILY, 13, "bold")
FONT_RESULT_HERO = (FONT_FAMILY, 24, "bold")

# =============================================================
# 2. لوحة الألوان الموحدة (Dark / Light Tuples)
# كل لون بصيغة (Light_Color, Dark_Color) ليعمل مع CustomTkinter تلقائياً
# =============================================================
# خلفيات التطبيق والأسطح
COLOR_BG = ("#F8FAFC", "#0B0F19")                    # خلفية النافذة الرئيسية
COLOR_SURFACE = ("#FFFFFF", "#151C2C")               # سطح البطاقات والحاويات
COLOR_SURFACE_HOVER = ("#F1F5F9", "#1E293B")         # السطح عند مرور الفأرة
COLOR_SURFACE_ACTIVE = ("#E2E8F0", "#27354A")        # السطح عند الضغط

# الحدود والفواصل
COLOR_BORDER = ("#E2E8F0", "#26334D")                # الحدود العادية
COLOR_BORDER_HOVER = ("#6366F1", "#818CF8")          # الحدود عند المرور
COLOR_DIVIDER = ("#E2E8F0", "#1E293B")               # الفواصل الداخلية

# الألوان المميزة والعلامة التجارية (Primary Indigo Gradient)
COLOR_PRIMARY = ("#4F46E5", "#6366F1")               # اللون الأساسي البنفسجي/الأزرق
COLOR_PRIMARY_HOVER = ("#4338CA", "#4F46E5")         # الأساسي عند المرور
COLOR_PRIMARY_CONTAINER = ("#EEF2FF", "#1E1B4B")     # خلفية الحاويات الأساسية

# الألوان الثانوية والمساندة
COLOR_SECONDARY = ("#0284C7", "#38BDF8")             # أزرق سماوي ثانوي
COLOR_SECONDARY_HOVER = ("#0369A1", "#0284C7")
COLOR_SECONDARY_CONTAINER = ("#E0F2FE", "#082F49")

# حالات النجاح والتنبيه والخطأ
COLOR_SUCCESS = ("#059669", "#10B981")               # أخضر النجاح
COLOR_SUCCESS_BG = ("#ECFDF5", "#064E3B")
COLOR_ERROR = ("#DC2626", "#EF4444")                 # أحمر الخطأ
COLOR_ERROR_BG = ("#FEF2F2", "#450A0A")
COLOR_WARNING = ("#D97706", "#F59E0B")               # برتقالي التحذير
COLOR_WARNING_BG = ("#FFFBEB", "#451A03")
COLOR_INFO = ("#2563EB", "#60A5FA")                  # أزرق المعلومات
COLOR_INFO_BG = ("#EFF6FF", "#172554")

# ألوان النصوص
COLOR_TEXT_PRIMARY = ("#0F172A", "#F8FAFC")          # النص الرئيسي عالي التباين
COLOR_TEXT_SECONDARY = ("#475569", "#94A3B8")        # النص الفرعي والتوضيحي
COLOR_TEXT_MUTED = ("#94A3B8", "#64748B")            # النص الخافت والتلميحات
COLOR_ON_PRIMARY = "#FFFFFF"                         # النص فوق الأزرار الأساسية

# =============================================================
# 3. أنصاف أقطار الحواف الدائرية (Corner Radiuses)
# =============================================================
RADIUS_CARD = 18
RADIUS_BUTTON = 14
RADIUS_INPUT = 12
RADIUS_BADGE = 10
RADIUS_TOAST = 14

# =============================================================
# 4. محاذاة واتجاه الواجهات (RTL Direction System)
# =============================================================
RTL = True

def side_start() -> str:
    """إرجاع جهة بداية العناصر ('right' في RTL، و 'left' في LTR)."""
    return "right" if RTL else "left"

def side_end() -> str:
    """إرجاع جهة نهاية العناصر ('left' في RTL، و 'right' في LTR)."""
    return "left" if RTL else "right"

def anchor_start() -> str:
    """إرجاع محاذاة البداية ('e' في RTL، و 'w' في LTR)."""
    return "e" if RTL else "w"

def anchor_end() -> str:
    """إرجاع محاذاة النهاية ('w' في RTL، و 'e' في LTR)."""
    return "w" if RTL else "e"

def justify_start() -> str:
    """إرجاع ضبط اتجاه النص للبداية ('right' في RTL، و 'left' في LTR)."""
    return "right" if RTL else "left"

def justify_end() -> str:
    """إرجاع ضبط اتجاه النص للنهاية ('left' في RTL، و 'right' في LTR)."""
    return "left" if RTL else "right"

def rtl_col(col_idx: int, total_cols: int) -> int:
    """
    تحويل مؤشر العمود في الشبكة ليصبح الترتيب من اليمين لليسار.
    مثال في شبكة من عمودين: العنصر الأول (0) يوضع في العمود 1 (أقصى اليمين).
    """
    if RTL:
        return (total_cols - 1) - (col_idx % total_cols)
    return col_idx % total_cols

# =============================================================
# 5. دالة معالجة النصوص العربية ar()
# =============================================================
# في بيئة ويندوز يدعم Tkinter و CustomTkinter النص العربي الموصول تلقائياً.
# في حال ظهور الحروف مقطعة في أي بيئة، يمكن تفعيل ENABLE_RESHAPING = True.
ENABLE_RESHAPING = False

def ar(text: str) -> str:
    """
    معالجة النص العربي لضمان ظهوره بشكل سليم واتجاه صحيح.
    """
    if not text or not ENABLE_RESHAPING:
        return text
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text

# =============================================================
# 5. دالة تنسيق جدول Treeview ليتوافق مع الوضعين الداكن والفاتح
# =============================================================
def apply_treeview_theme(style: ttk.Style, is_dark: bool):
    """
    تطبيق أنماط الألوان والخطوط على جدول ttk.Treeview ليتناغم تماماً
    مع CustomTkinter بالوضع الداكن أو الفاتح بدون أشرطة تمرير ظاهرة.
    """
    if is_dark:
        bg_color = "#151C2C"
        fg_color = "#F8FAFC"
        header_bg = "#1E293B"
        header_fg = "#818CF8"
        even_row = "#151C2C"
        odd_row = "#182235"
        last_row = "#064E3B"
        last_fg = "#34D399"
        border_color = "#26334D"
    else:
        bg_color = "#FFFFFF"
        fg_color = "#0F172A"
        header_bg = "#EEF2FF"
        header_fg = "#4F46E5"
        even_row = "#FFFFFF"
        odd_row = "#F8FAFC"
        last_row = "#ECFDF5"
        last_fg = "#059669"
        border_color = "#E2E8F0"

    style.theme_use("clam")
    
    style.configure(
        "Modern.Treeview",
        background=bg_color,
        foreground=fg_color,
        fieldbackground=bg_color,
        rowheight=38,
        font=FONT_BODY,
        borderwidth=0,
        relief="flat"
    )
    style.configure(
        "Modern.Treeview.Heading",
        background=header_bg,
        foreground=header_fg,
        relief="flat",
        font=FONT_BODY_BOLD,
        padding=(10, 8)
    )
    style.map(
        "Modern.Treeview.Heading",
        background=[("active", header_bg)],
        foreground=[("active", header_fg)]
    )
    style.map(
        "Modern.Treeview",
        background=[("selected", "#4F46E5" if is_dark else "#6366F1")],
        foreground=[("selected", "#FFFFFF")]
    )

    return {
        "even_row": even_row,
        "odd_row": odd_row,
        "last_row": last_row,
        "last_fg": last_fg,
        "fg_color": fg_color,
        "border_color": border_color
    }
