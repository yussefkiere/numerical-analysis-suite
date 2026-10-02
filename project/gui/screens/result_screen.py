"""
الشاشة 4: عرض النتائج وجدول التنفيذ (Result Screen)
=====================================================
المرحلة الرابعة في التسلسل الهرمي:
- بطاقة نتيجة بارزة في الأعلى بخط كبير ولون النجاح الأخضر (Emerald).
- بطاقات إحصاء صغيرة: عدد التكرارات/الخطوات، الخطأ النهائي، الطريقة المستخدمة.
- بطاقة جدول التنفيذ السبوري (ttk.Treeview مُنسّق تماماً مع المظهر الحالي،
  بدون أي شريط تمرير، مع دعم التمرير الرأسي بعجلة الفأرة والتمرير الأفقي بـ Shift+العجلة).
- تمييز الصف الأخير (الحل النهائي) بلون مميز وصفوف متبادلة الألوان (Zebra).
- أزرار: نسخ النتيجة، حساب جديد، القائمة الرئيسية.
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Dict, Any, List

from ..theme import (
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_SECTION,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_SMALL,
    FONT_SMALL_BOLD,
    FONT_TINY,
    FONT_MONO,
    FONT_MONO_BOLD,
    FONT_RESULT_HERO,
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_BORDER,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_SUCCESS,
    COLOR_SUCCESS_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    RADIUS_CARD,
    RADIUS_BUTTON,
    RADIUS_BADGE,
    apply_treeview_theme,
    side_start,
    side_end,
    anchor_start,
    anchor_end,
    justify_start,
    justify_end,
    rtl_col,
    ar,
)
from ..components import AppHeader, PrimaryButton, GhostButton, NoScrollbarFrame


class ResultScreen(ctk.CTkFrame):
    """
    الشاشة الرابعة: لوحة النتائج الإحصائية وجدول خطوات الحل السبوري.
    """
    def __init__(
        self,
        master,
        router,
        cat_key: str,
        cat_data: Dict[str, Any],
        method_key: str,
        method_data: Dict[str, Any],
        table: List[Dict[str, Any]],
        result: Any,
        **kwargs
    ):
        super().__init__(master=master, fg_color="transparent", **kwargs)
        self.router = router
        self.cat_key = cat_key
        self.cat_data = cat_data
        self.method_key = method_key
        self.method_data = method_data
        self.table = table
        self.result = result

        self.tree = None
        self.tree_style = None

        self._build_ui()

    def _build_ui(self):
        # 1. الشريط العلوي مع مسار تنقل تفاعلي مفصول
        header = AppHeader(
            self,
            title=f"نتيجة {self.method_data['title']}",
            breadcrumbs=[
                ("الرئيسية", lambda: self.router.show_screen("categories")),
                (self.cat_data["title"], lambda: self.router.show_screen("methods", cat_key=self.cat_key, cat_data=self.cat_data)),
                (self.method_data["title"], lambda: self.router.show_screen(
                    "input",
                    cat_key=self.cat_key,
                    cat_data=self.cat_data,
                    method_key=self.method_key,
                    method_data=self.method_data
                )),
                ("النتيجة", None)
            ],
            on_back=lambda: self.router.show_screen(
                "input",
                cat_key=self.cat_key,
                cat_data=self.cat_data,
                method_key=self.method_key,
                method_data=self.method_data
            ),
            on_toggle_theme=self._on_toggle_theme_internal,
            is_dark_mode=self.router.is_dark_mode
        )
        header.pack(fill="x", padx=30, pady=(16, 8))

        # 2. الحاوية القابلة للتمرير دون scrollbar
        scroll_container = NoScrollbarFrame(self)
        scroll_container.pack(fill="both", expand=True)

        content = scroll_container.inner_frame

        # ---------------------------------------------------------
        # 3. بطاقة النتيجة البارزة في الأعلى (Hero Result Card)
        # ---------------------------------------------------------
        hero_card = ctk.CTkFrame(
            content,
            corner_radius=RADIUS_CARD,
            border_width=2,
            border_color=COLOR_SUCCESS,
            fg_color=COLOR_SUCCESS_BG
        )
        hero_card.pack(fill="x", padx=30, pady=(0, 14))

        hero_inner = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_inner.pack(fill="both", expand=True, padx=24, pady=16)

        # سطر النتيجة الواضح والمباشر
        formatted_res = self._format_result_string()
        self.res_val_lbl = ctk.CTkLabel(
            hero_inner,
            text=ar(formatted_res),
            font=FONT_RESULT_HERO,
            text_color=COLOR_SUCCESS,
            anchor=anchor_start(),
            justify=justify_start(),
            wraplength=820
        )
        self.res_val_lbl.pack(fill="x", padx=6, pady=6)

        # ---------------------------------------------------------
        # 4. بطاقات الإحصاء: تظهر فقط للطرق التكرارية (عدد التكرارات والخطأ النهائي)
        # ---------------------------------------------------------
        is_iterative = self.method_data.get("is_iterative", False)
        if is_iterative:
            stats_box = ctk.CTkFrame(content, fg_color="transparent")
            stats_box.pack(fill="x", padx=30, pady=(0, 14))
            stats_box.grid_columnconfigure((0, 1), weight=1, uniform="stat_col")

            # 1. عدد التكرارات
            steps_count = len(self.table)
            self._create_stat_card(stats_box, title="عدد التكرارات", val=f"{steps_count} تكرار", col=rtl_col(0, 2))

            # 2. الخطأ النهائي
            last_error = "-"
            if self.table and "error" in self.table[-1]:
                err_val = self.table[-1]["error"]
                if isinstance(err_val, float):
                    last_error = f"{err_val:.2e}"
                else:
                    last_error = str(err_val)
            self._create_stat_card(stats_box, title="الخطأ النهائي", val=last_error, col=rtl_col(1, 2))

        # ---------------------------------------------------------
        # 5. بطاقة جدول التنفيذ السبوري (Treeview Table Card)
        # ---------------------------------------------------------
        table_card = ctk.CTkFrame(
            content,
            corner_radius=RADIUS_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE
        )
        table_card.pack(fill="both", expand=True, padx=30, pady=(0, 14))

        table_header = ctk.CTkFrame(table_card, fg_color="transparent")
        table_header.pack(fill="x", padx=20, pady=(16, 10))

        ctk.CTkLabel(
            table_header,
            text=ar("جدول خطوات التنفيذ المنهجي (كما على السبورة):"),
            font=FONT_SECTION,
            text_color=COLOR_TEXT_PRIMARY,
            anchor=anchor_start(),
            justify=justify_start()
        ).pack(side=side_start())

        ctk.CTkLabel(
            table_header,
            text=ar("(التمرير بعجلة الفأرة، والأفقي بـ Shift + العجلة)"),
            font=FONT_TINY,
            text_color=COLOR_TEXT_MUTED,
            anchor=anchor_end()
        ).pack(side=side_end())

        # بناء الجدول بـ ttk.Treeview
        self._build_treeview(table_card)

        # ---------------------------------------------------------
        # 6. أزرار الإجراءات السفلية (من اليمين لليسار: نسخ النتيجة وحساب جديد فقط)
        # ---------------------------------------------------------
        action_bar = ctk.CTkFrame(content, fg_color="transparent")
        action_bar.pack(fill="x", padx=30, pady=(0, 24))

        # نسخ النتيجة على اليمين
        copy_btn = PrimaryButton(
            action_bar,
            text="📋 نسخ النتيجة",
            command=self._on_copy_result,
            width=150
        )
        copy_btn.pack(side=side_start(), padx=(0, 10))

        # حساب جديد إلى يساره
        new_calc_btn = GhostButton(
            action_bar,
            text="🔄 حساب جديد",
            command=self._on_new_calc,
            width=150
        )
        new_calc_btn.pack(side=side_start())

    def _create_stat_card(self, parent: ctk.CTkFrame, title: str, val: str, col: int):
        card = ctk.CTkFrame(
            parent,
            corner_radius=RADIUS_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE,
            height=70
        )
        card.grid(row=0, column=col, padx=6, sticky="ew")

        ctk.CTkLabel(
            card,
            text=ar(title),
            font=FONT_TINY,
            text_color=COLOR_TEXT_MUTED,
            anchor=anchor_start(),
            justify=justify_start()
        ).pack(fill="x", padx=14, pady=(10, 0))

        ctk.CTkLabel(
            card,
            text=val,
            font=FONT_BODY_BOLD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor=anchor_start(),
            justify=justify_start()
        ).pack(fill="x", padx=14, pady=(2, 10))

    def _build_treeview(self, parent: ctk.CTkFrame):
        """بناء وتنسيق جدول Treeview بدون أي scrollbar ظاهرة مع دعم التمرير."""
        tree_container = ctk.CTkFrame(parent, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        cols_cfg = self._prepare_columns()
        col_ids = [c[0] for c in cols_cfg]

        self.tree_style = ttk.Style(self)
        self.theme_colors = apply_treeview_theme(self.tree_style, self.router.is_dark_mode)

        self.tree = ttk.Treeview(
            tree_container,
            columns=col_ids,
            show="headings",
            selectmode="browse",
            style="Modern.Treeview",
            height=min(12, max(6, len(self.table)))
        )
        self.tree.pack(fill="both", expand=True)

        # ضبط عناوين وعرض الأعمدة
        for cid, chead, cwidth in cols_cfg:
            self.tree.heading(cid, text=chead, anchor="center")
            self.tree.column(cid, width=cwidth, minwidth=60, anchor="center")

        # إدراج الصفوف مع تمييز الصف الأخير بلون النجاح
        total_rows = len(self.table)
        for idx, row_dict in enumerate(self.table):
            row_values = []
            for cid in col_ids:
                val = row_dict.get(cid, "-")
                row_values.append(self._format_cell(val))

            is_last = (idx == total_rows - 1) and (total_rows > 1)
            tag = "last_row" if is_last else ("even_row" if idx % 2 == 0 else "odd_row")
            self.tree.insert("", "end", values=row_values, tags=(tag,))

        # ألوان الصفوف المتبادلة والصف الأخير
        self.tree.tag_configure("even_row", background=self.theme_colors["even_row"])
        self.tree.tag_configure("odd_row", background=self.theme_colors["odd_row"])
        self.tree.tag_configure(
            "last_row",
            background=self.theme_colors["last_row"],
            foreground=self.theme_colors["last_fg"]
        )

        # ربط أحداث التمرير بعجلة الفأرة على الجدول (رأسي وأفقي) دون أشرطة تمرير
        self.tree.bind("<MouseWheel>", self._on_tree_mousewheel)
        self.tree.bind("<Shift-MouseWheel>", self._on_tree_shift_mousewheel)
        self.tree.bind("<Button-4>", lambda e: self.tree.yview_scroll(-2, "units"))
        self.tree.bind("<Button-5>", lambda e: self.tree.yview_scroll(2, "units"))

    def _on_tree_mousewheel(self, event):
        delta = -1 * int(event.delta / 120)
        self.tree.yview_scroll(delta, "units")
        return "break"

    def _on_tree_shift_mousewheel(self, event):
        delta = -1 * int(event.delta / 120)
        self.tree.xview_scroll(delta, "units")
        return "break"

    def _prepare_columns(self) -> List[tuple]:
        base_cols = self.method_data.get("table_columns", [])
        if not self.table:
            return base_cols

        first_keys = list(self.table[0].keys())
        base_ids = [c[0] for c in base_cols]

        if all(k in base_ids for k in first_keys) and len(first_keys) <= len(base_ids):
            return base_cols

        prepared = []
        for k in first_keys:
            found = False
            for cid, chead, cwidth in base_cols:
                if cid == k:
                    prepared.append((cid, chead, cwidth))
                    found = True
                    break
            if not found:
                label = f"x{k[1:]}" if k.startswith("x") else str(k)
                prepared.append((k, label, 100))
        return prepared

    def _format_cell(self, val: Any) -> str:
        if val is None:
            return "-"
        if isinstance(val, float):
            return f"{val:.6f}"
        if isinstance(val, int):
            return str(val)
        if isinstance(val, (list, tuple)):
            return " ، ".join(f"{x:.4f}" if isinstance(x, float) else str(x) for x in val)
        return str(val)

    def _format_result_string(self) -> str:
        cat_type = self.cat_data.get("type")
        if cat_type == "nonlinear":
            if isinstance(self.result, float):
                return f"الجذر هو  x = {self.result:.6f}"
            return f"الجذر هو  {self.result}"
        elif cat_type == "linear_systems":
            if isinstance(self.result, (list, tuple)):
                parts = [f"x{i+1} = {x:.6f}" if isinstance(x, float) else str(x) for i, x in enumerate(self.result)]
                return "الحل:  " + "  ،  ".join(parts)
            return f"الحل:  {self.result}"
        elif self.method_key == "trapezoidal":
            if isinstance(self.result, float):
                return f"قيمة التكامل = {self.result:.6f}"
            return f"قيمة التكامل = {self.result}"
        elif self.method_key == "lagrange":
            if isinstance(self.result, dict):
                x_eval = self.result.get("x_eval", "x")
                eval_val = self.result.get("eval", 0.0)
                return f"P({x_eval}) = {eval_val:.6f}"
            return f"P(x) = {self.result}"
        elif self.method_key == "numerical_diff":
            if isinstance(self.result, dict):
                f_p = self.result.get("f_prime", 0.0)
                x0 = self.result.get("x0", "x0")
                return f"المشتقة:  f'({x0}) = {f_p:.6f}"
            return f"المشتقة = {self.result}"
        if isinstance(self.result, float):
            return f"{self.result:.6f}"
        return str(self.result)

    def _on_copy_result(self):
        """نسخ نص النتيجة للحافظة مع إظهار إشعار Toast بنجاح النسخ."""
        try:
            self.clipboard_clear()
            self.clipboard_append(self._format_result_string())
            self.router.show_toast("تم نسخ النتيجة بنجاح إلى الحافظة 📋", toast_type="success")
        except Exception:
            self.router.show_toast("تعذر نسخ النتيجة إلى الحافظة", toast_type="error")

    def _on_new_calc(self):
        """العودة لشاشة المدخلات لتعديل القيم."""
        self.router.show_screen(
            "input",
            cat_key=self.cat_key,
            cat_data=self.cat_data,
            method_key=self.method_key,
            method_data=self.method_data
        )

    def _on_toggle_theme_internal(self):
        """تبديل المظهر وإعادة ضبط ألوان الـ Treeview."""
        self.router.toggle_theme()
        if self.tree and self.tree_style:
            self.theme_colors = apply_treeview_theme(self.tree_style, self.router.is_dark_mode)
            self.tree.tag_configure("even_row", background=self.theme_colors["even_row"])
            self.tree.tag_configure("odd_row", background=self.theme_colors["odd_row"])
            self.tree.tag_configure(
                "last_row",
                background=self.theme_colors["last_row"],
                foreground=self.theme_colors["last_fg"]
            )
