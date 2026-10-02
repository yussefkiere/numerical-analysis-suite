"""
حزمة واجهات المستخدم الرسومية الحديثة (Modern CustomTkinter GUI)
==================================================================
الواجهات مبنية وفق معايير Material Design 3 بواسطة CustomTkinter:
- AppWindow: النافذة الرئيسية الحاوية لموجّه الشاشات (Screen Router).
- Screen 1: CategoryScreen (اختيار نوع المسألة).
- Screen 2: MethodsScreen (قائمة الطرق).
- Screen 3: InputScreen (المدخلات والمصفوفات مع التحقق اللحظي).
- Screen 4: ResultScreen (النتيجة البارزة وجدول التنفيذ).
"""

from .app_window import AppWindow
from .screens import (
    CategoryScreen,
    MethodsScreen,
    InputScreen,
    ResultScreen,
)

# توجيه للتوافق مع أي استدعاء قديم
MainWindow = AppWindow
CategoryWindow = AppWindow

__all__ = [
    "AppWindow",
    "MainWindow",
    "CategoryWindow",
    "CategoryScreen",
    "MethodsScreen",
    "InputScreen",
    "ResultScreen",
]
