"""
نقطة انطلاق تطبيق التحليل العددي الحديث (Modern Numerical Analysis App)
======================================================================
مشروع مقرر التحليل العددي - الواجهات العصرية الحديثة (CustomTkinter):
1. شاشة نوع المسألة: اختيار القسم (معادلات غير خطية، أنظمة خطية، استيفاء، تفاضل وتكامل).
2. شاشة قائمة الطرق: تصفح الطرق المعتمدة في شبكة متجاوبة.
3. شاشة إدخال المعاملات: نموذج ذكي مع تحقق لحظي وشبكة مصفوفات تفاعلية.
4. شاشة النتائج: بطاقة الحل البارزة، بطاقات الإحصاء، وجدول التنفيذ السبوري بدون scrollbars.

جميع الخوارزميات مستقلة في methods/ ومربوطة بالسجل المركزي registry.py.
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gui.app_window import AppWindow


def main():
    """الدالة الرئيسية لتشغيل المنصة العصرية."""
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
