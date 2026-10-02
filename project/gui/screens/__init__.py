"""
شاشات التطبيق الأربع (Application Screens)
===========================================
1. CategoryScreen: اختيار نوع المسألة (2x2 Card Grid)
2. MethodsScreen: قائمة الطرق للقسم المختار (Responsive Cards)
3. InputScreen: إدخال المعاملات والمصفوفات والتحقق اللحظي
4. ResultScreen: النتيجة البارزة وبطاقات الإحصاء وجدول التنفيذ
"""

from .category_screen import CategoryScreen
from .methods_screen import MethodsScreen
from .input_screen import InputScreen
from .result_screen import ResultScreen

__all__ = [
    "CategoryScreen",
    "MethodsScreen",
    "InputScreen",
    "ResultScreen"
]
