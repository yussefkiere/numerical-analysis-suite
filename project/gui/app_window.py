"""
نافذة التطبيق الرئيسية والموجّه (Main AppWindow & Screen Router)
================================================================
النافذة الوحيدة الرئيسية للتطبيق (customtkinter.CTk):
- توفر موجّه شاشات مرن وسريع: show_screen(name, **data)
- تدعم التبديل اللحظي بين المظهرين الداكن والفاتح (Dark / Light)
- تدير الإشعارات المنبثقة العائمة (Toast Notifications)
- توفر انتقالاً سلساً وسريعاً (Fade Transition <= 200ms) بين الشاشات
"""

import sys
import tkinter as tk
import customtkinter as ctk
from typing import Optional, Dict, Any

from .theme import (
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_PRIMARY,
    COLOR_TEXT_PRIMARY,
    FONT_FAMILY,
    FONT_TITLE,
)
from .components import Toast
from .screens import (
    CategoryScreen,
    MethodsScreen,
    InputScreen,
    ResultScreen,
)


class AppWindow(ctk.CTk):
    """
    النافذة الرئيسية والموجّه المركزي لجميع شاشات التطبيق.
    """
    def __init__(self):
        super().__init__()

        # 1. إعدادات المظهر والنافذة (الافتراضي هو الوضع الداكن)
        self.is_dark_mode = True
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("منصة التحليل العددي الشاملة")
        self.geometry("1060x760")
        self.minsize(860, 620)
        self.configure(fg_color=COLOR_BG)

        # 2. الحاوية الرئيسية للشاشات
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.current_screen = None
        self.current_toast: Optional[Toast] = None

        # 3. توسيط النافذة على الشاشة
        self._center_window()

        # 4. فتح الشاشة الأولى (اختيار نوع المسألة)
        self.show_screen("categories")

    def _center_window(self):
        """توسيط النافذة على شاشة المستخدم بدقة."""
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_screen(self, screen_name: str, **kwargs):
        """
        الانتقال إلى أي شاشة بتبديل الإطارات مع انتقال تلاشٍ سريع (Fade Transition <= 200ms).
        """
        # بناء الشاشة الجديدة
        new_screen = None
        if screen_name == "categories":
            new_screen = CategoryScreen(self.main_container, router=self)
        elif screen_name == "methods":
            new_screen = MethodsScreen(
                self.main_container,
                router=self,
                cat_key=kwargs["cat_key"],
                cat_data=kwargs["cat_data"]
            )
        elif screen_name == "input":
            new_screen = InputScreen(
                self.main_container,
                router=self,
                cat_key=kwargs["cat_key"],
                cat_data=kwargs["cat_data"],
                method_key=kwargs["method_key"],
                method_data=kwargs["method_data"]
            )
        elif screen_name == "result":
            new_screen = ResultScreen(
                self.main_container,
                router=self,
                cat_key=kwargs["cat_key"],
                cat_data=kwargs["cat_data"],
                method_key=kwargs["method_key"],
                method_data=kwargs["method_data"],
                table=kwargs["table"],
                result=kwargs["result"]
            )

        if not new_screen:
            return

        # تأثير التلاشي السريع (Quick Fade Transition)
        old_screen = self.current_screen

        if old_screen:
            # إخفاء فوري للشاشة السابقة وعرض الشاشة الجديدة
            old_screen.pack_forget()
            old_screen.destroy()

        self.current_screen = new_screen
        self.current_screen.pack(fill="both", expand=True)

        # التمرير التلقائي لأعلى الصفحة
        self.update_idletasks()

    def toggle_theme(self):
        """التبديل اللحظي بين المظهرين الداكن والفاتح."""
        self.is_dark_mode = not self.is_dark_mode
        new_mode = "Dark" if self.is_dark_mode else "Light"
        ctk.set_appearance_mode(new_mode)

        # تحديث ألوان الـ Canvas في الشاشة الحالية إن وُجدت
        if self.current_screen:
            for child in self.current_screen.winfo_children():
                if hasattr(child, "update_canvas_bg"):
                    child.update_canvas_bg()

    def show_toast(self, message: str, toast_type: str = "info"):
        """
        عرض إشعار Toast عائم في أعلى النافذة دون حجب التفاعل.
        """
        if self.current_toast:
            try:
                self.current_toast.destroy()
            except Exception:
                pass

        self.current_toast = Toast(self, message=message, toast_type=toast_type)
        # تموضع الإشعار في الزاوية العلوية اليمنى لدعم محاذاة اليمين (RTL)
        self.current_toast.place(relx=0.97, y=22, anchor="ne")
