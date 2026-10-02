"""
الشاشة 1: اختيار نوع المسألة (Category Selection Screen)
==========================================================
المرحلة الأولى في التسلسل الهرمي:
تعرض عنواناً ترحيبياً وأربع بطاقات تفاعلية كبيرة في شبكة 2×2:
1. معادلات غير خطية
2. أنظمة معادلات خطية
3. الاستيفاء
4. التفاضل والتكامل العددي

تُقرأ البيانات ديناميكياً من قاموس CATEGORIES في registry.py.
"""

import customtkinter as ctk
from typing import Dict, Any

from methods.registry import CATEGORIES
from ..theme import (
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_SMALL,
    FONT_SMALL_BOLD,
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    RADIUS_CARD,
    side_start,
    side_end,
    anchor_start,
    justify_start,
    rtl_col,
    ar,
)
from ..components import Card, AppHeader, NoScrollbarFrame


class CategoryScreen(ctk.CTkFrame):
    """
    الشاشة الأولى: اختيار تصنيف المسألة في شبكة 2×2 متجاوبة بالاتجاه العربي (RTL).
    """
    def __init__(self, master, router, **kwargs):
        super().__init__(master=master, fg_color="transparent", **kwargs)
        self.router = router

        self._build_ui()

    def _build_ui(self):
        # 1. الشريط العلوي الموحد (عنوان المنصة وزر تبديل المظهر على اليسار)
        header = AppHeader(
            self,
            title="منصة التحليل العددي الشاملة",
            breadcrumbs=[("الرئيسية", None)],
            on_toggle_theme=self.router.toggle_theme,
            is_dark_mode=self.router.is_dark_mode
        )
        header.pack(fill="x", padx=30, pady=(16, 4))

        # 2. حاوية قابلة للتمرير دون ظهور أي Scrollbar
        scroll_container = NoScrollbarFrame(self)
        scroll_container.pack(fill="both", expand=True)

        content = scroll_container.inner_frame

        # رسالة الترحيب الإرشادية
        hero_box = ctk.CTkFrame(content, fg_color="transparent")
        hero_box.pack(fill="x", padx=30, pady=(10, 16))

        subtitle_lbl = ctk.CTkLabel(
            hero_box,
            text=ar("اختر تصنيف المسألة الرياضية للانتقال إلى قائمة الخوارزميات المعتمدة بالمقرر:"),
            font=FONT_SUBTITLE,
            text_color=COLOR_TEXT_SECONDARY,
            anchor=anchor_start(),
            justify=justify_start()
        )
        subtitle_lbl.pack(anchor=anchor_start(), fill="x")

        # 3. شبكة البطاقات الكبيرة 2×2 مرتبة من اليمين إلى اليسار (RTL)
        grid_container = ctk.CTkFrame(content, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        grid_container.grid_columnconfigure((0, 1), weight=1, uniform="category_col")
        grid_container.grid_rowconfigure((0, 1), weight=1)

        # أيقونات ورموز الرياضيات لكل تصنيف
        category_meta = {
            "nonlinear": {"icon": "🎯", "en": "Nonlinear Equations (Roots)"},
            "linear_systems": {"icon": "⚡", "en": "Linear Systems (AX = B)"},
            "interpolation": {"icon": "📈", "en": "Interpolation & Fitting"},
            "calculus": {"icon": "📐", "en": "Numerical Calculus (∫ / d)"}
        }

        for idx, (cat_key, cat_data) in enumerate(CATEGORIES.items()):
            meta = category_meta.get(cat_key, {"icon": "⚡", "en": cat_data.get("title_en", "")})
            methods_count = len(cat_data.get("methods", {}))
            count_str = f"{methods_count} طرق معتمدة"

            card = Card(
                grid_container,
                title=cat_data["title"],
                desc=cat_data["desc"],
                icon=meta["icon"],
                badge=count_str,
                on_click=lambda k=cat_key, d=cat_data: self._on_select_category(k, d),
                height=190
            )

            row = idx // 2
            col = rtl_col(idx, 2)  # العمود 1 في اليمين للبطاقة الأولى ثم 0 لليسار
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        # ---------------------------------------------------------
        # 3. تذييل الشاشة
        # ---------------------------------------------------------
        footer_box = ctk.CTkFrame(content, fg_color="transparent")
        footer_box.pack(fill="x", padx=30, pady=(10, 20))

        footer_lbl = ctk.CTkLabel(
            footer_box,
            text=ar("مشروع مقرر التحليل العددي • مطابقة تامة بين بايثون وأكواد الماتلاب الأصلية"),
            font=FONT_SMALL,
            text_color=COLOR_TEXT_MUTED,
            anchor="center"
        )
        footer_lbl.pack(fill="x")

    def _on_select_category(self, cat_key: str, cat_data: Dict[str, Any]):
        """الانتقال إلى شاشة قائمة الطرق للقسم المختار."""
        self.router.show_screen("methods", cat_key=cat_key, cat_data=cat_data)
