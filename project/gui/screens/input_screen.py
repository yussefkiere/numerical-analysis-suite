"""
الشاشة 3: إدخال معاملات المسألة والتحقق اللحظي (Input Screen)
==============================================================
المرحلة الثالثة في التسلسل الهرمي:
بطاقة نموذج مركزية ديناميكية:
- حقول إدخال بعنوان فوق كل حقل مع تحقق لحظي وتحول الحدود للأحمر عند الخطأ.
- شبكة مصفوفة مرتبة متساوية الخلايا مع تنقل كامل بأسهم لوحة المفاتيح وTab.
- جدول نقاط استيفاء تفاعلي بإمكانية إضافة وحذف النقاط.
- زر "احسب" يتحول فورياً إلى "جارٍ الحساب..." قبل الانتقال لشاشة النتائج.
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, Any, List, Optional

from utils.parser import make_function, derivative
from methods.jacobi import check_diagonal_dominance
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
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_BORDER,
    COLOR_BORDER_HOVER,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_PRIMARY_CONTAINER,
    COLOR_SECONDARY,
    COLOR_SUCCESS,
    COLOR_ERROR,
    COLOR_WARNING,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    RADIUS_CARD,
    RADIUS_INPUT,
    RADIUS_BUTTON,
    RADIUS_BADGE,
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


class ValidatedInputField(ctk.CTkFrame):
    """
    حقل إدخال متطور بعنوان أعلاه وتحقق لحظي مع رسالة خطأ ملونة أسفله.
    """
    def __init__(
        self,
        master,
        label: str,
        default_val: str = "",
        hint: str = "",
        is_numeric: bool = True,
        width: int = 240,
        **kwargs
    ):
        super().__init__(master=master, fg_color="transparent", **kwargs)
        self.is_numeric = is_numeric

        # عنوان الحقل بمحاذاة يمينية
        self.label_widget = ctk.CTkLabel(
            self,
            text=ar(label),
            font=FONT_SMALL_BOLD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor=anchor_start(),
            justify=justify_start()
        )
        self.label_widget.pack(fill="x", pady=(0, 4))

        # خانة الإدخال LTR لسهولة كتابة المعادلات والأرقام
        placeholder = hint if (hint and not default_val) else ""
        self.entry = ctk.CTkEntry(
            self,
            font=FONT_BODY,
            corner_radius=RADIUS_INPUT,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE,
            text_color=COLOR_TEXT_PRIMARY,
            width=width,
            height=40,
            justify="left",
            placeholder_text=placeholder
        )
        self.entry.pack(fill="x", pady=(0, 2))
        self.entry.insert(0, default_val)

        # رسالة الخطأ اللحظي (فارغة افتراضياً ولا تظهر إلا عند وجود خطأ)
        self.info_lbl = ctk.CTkLabel(
            self,
            text="",
            font=FONT_TINY,
            text_color=COLOR_ERROR,
            anchor=anchor_start(),
            justify=justify_start()
        )
        self.info_lbl.pack(fill="x")

        # ربط أحداث التحقق اللحظي
        self.entry.bind("<KeyRelease>", self._on_validate)
        self.entry.bind("<FocusOut>", self._on_validate)

    def _on_validate(self, event=None):
        val = self.entry.get().strip()
        if not val:
            self.set_error("هذا الحقل مطلوب")
            return False
        if self.is_numeric:
            try:
                float(val)
                self.clear_error()
                return True
            except ValueError:
                self.set_error("يجب إدخال قيمة عددية صحيحة")
                return False
        self.clear_error()
        return True

    def set_error(self, message: str):
        self.entry.configure(border_color=COLOR_ERROR, border_width=2)
        self.info_lbl.configure(text=ar(f"⚠️ {message}"), text_color=COLOR_ERROR)

    def clear_error(self):
        self.entry.configure(border_color=COLOR_BORDER, border_width=1)
        self.info_lbl.configure(text="", text_color=COLOR_TEXT_MUTED)

    def get(self) -> str:
        return self.entry.get().strip()

    def set(self, val: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, val)
        self.clear_error()


class InputScreen(ctk.CTkFrame):
    """
    الشاشة الثالثة: النموذج المركزي للمدخلات بحسب نوع الخوارزمية.
    """
    def __init__(
        self,
        master,
        router,
        cat_key: str,
        cat_data: Dict[str, Any],
        method_key: str,
        method_data: Dict[str, Any],
        **kwargs
    ):
        super().__init__(master=master, fg_color="transparent", **kwargs)
        self.router = router
        self.cat_key = cat_key
        self.cat_data = cat_data
        self.method_key = method_key
        self.method_data = method_data

        # مراجع الحقول
        self.param_fields: Dict[str, ValidatedInputField] = {}
        self.func_field: Optional[ValidatedInputField] = None
        
        # مصفوفات النظام الخطي
        self.n_var = tk.IntVar(value=self.method_data.get("default_n", 2))
        self.matrix_a_cells: List[List[ctk.CTkEntry]] = []
        self.vector_b_cells: List[ctk.CTkEntry] = []
        self.x0_cells: List[ctk.CTkEntry] = []
        self.matrix_grid_container = None

        # نقاط الاستيفاء
        self.points_rows: List[tuple[ctk.CTkFrame, ctk.CTkEntry, ctk.CTkEntry]] = []
        self.points_container = None
        self.x_eval_field: Optional[ValidatedInputField] = None

        self._build_ui()

    def _build_ui(self):
        # 1. الشريط العلوي مع مسار تنقل تفاعلي مفصول
        header = AppHeader(
            self,
            title=self.method_data["title"],
            breadcrumbs=[
                ("الرئيسية", lambda: self.router.show_screen("categories")),
                (self.cat_data["title"], lambda: self.router.show_screen("methods", cat_key=self.cat_key, cat_data=self.cat_data)),
                (self.method_data["title"], None)
            ],
            on_back=lambda: self.router.show_screen("methods", cat_key=self.cat_key, cat_data=self.cat_data),
            on_toggle_theme=self.router.toggle_theme,
            is_dark_mode=self.router.is_dark_mode
        )
        header.pack(fill="x", padx=30, pady=(16, 8))

        # 2. الحاوية القابلة للتمرير دون scrollbar
        self.scroll_container = NoScrollbarFrame(self)
        self.scroll_container.pack(fill="both", expand=True)

        content = self.scroll_container.inner_frame

        # 3. البطاقة المركزية للنموذج (Central Form Card)
        form_card = ctk.CTkFrame(
            content,
            corner_radius=RADIUS_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE
        )
        form_card.pack(fill="both", expand=True, padx=40, pady=(0, 24))

        form_inner = ctk.CTkFrame(form_card, fg_color="transparent")
        form_inner.pack(fill="both", expand=True, padx=30, pady=24)

        # بناء حقول النموذج حسب نوع المسألة
        cat_type = self.cat_data.get("type")
        if cat_type == "nonlinear":
            self._build_nonlinear_form(form_inner)
        elif cat_type == "linear_systems":
            self._build_linear_systems_form(form_inner)
        elif cat_type == "interpolation":
            self._build_interpolation_form(form_inner)
        elif cat_type == "calculus":
            self._build_calculus_form(form_inner)

        # 4. أزرار الإجراء (احسب أولاً على اليمين ثم رجوع لليسار)
        action_box = ctk.CTkFrame(form_inner, fg_color="transparent")
        action_box.pack(fill="x", pady=(24, 8))

        self.calc_btn = PrimaryButton(
            action_box,
            text="احسب 🖩",
            command=self._on_click_calculate,
            height=48
        )
        self.calc_btn.pack(side=side_start(), fill="x", expand=True, padx=(8, 0))

        back_btn = GhostButton(
            action_box,
            text="→ رجوع",
            command=lambda: self.router.show_screen("methods", cat_key=self.cat_key, cat_data=self.cat_data),
            height=48,
            width=130
        )
        back_btn.pack(side=side_start(), padx=(0, 8))

    # =============================================================
    # [1] نموذج المعادلات غير الخطية
    # =============================================================
    def _build_nonlinear_form(self, parent: ctk.CTkFrame):
        is_g = self.method_data.get("is_g_func", False)
        f_label = "الدالة g(x) المعاد صياغتها (حيث x = g(x)):" if is_g else "الدالة الرياضية f(x):"
        hint = "مثال: (x + 2)**(1/3)" if is_g else "أمثلة مقبولة: x^3 - x - 2  أو  cos(x) - x  أو  e^x - 3x"

        # حقل الدالة
        self.func_field = ValidatedInputField(
            parent,
            label=f_label,
            default_val=self.method_data.get("default_f", "x^3 - x - 2"),
            hint=hint,
            is_numeric=False,
            width=380
        )
        self.func_field.pack(fill="x", pady=(0, 14))

        # شبكة المعاملات
        params_grid = ctk.CTkFrame(parent, fg_color="transparent")
        params_grid.pack(fill="x", pady=(0, 10))
        params_grid.grid_columnconfigure((0, 1), weight=1, uniform="param_col")

        inputs = self.method_data.get("inputs", [])
        row = 0
        col = 1
        for key, label_txt, default_val, desc_txt in inputs:
            field = ValidatedInputField(
                params_grid,
                label=label_txt,
                default_val=default_val,
                hint=desc_txt,
                is_numeric=True
            )
            field.grid(row=row, column=col, padx=8, pady=6, sticky="ew")
            self.param_fields[key] = field

            col -= 1
            if col < 0:
                col = 1
                row += 1

        if self.method_key == "newton":
            note_box = ctk.CTkFrame(parent, fg_color=COLOR_PRIMARY_CONTAINER, corner_radius=RADIUS_INPUT)
            note_box.pack(fill="x", pady=(8, 0), padx=8)
            ctk.CTkLabel(
                note_box,
                text=ar("💡 المشتقة الأولى f'(x) تُحسب تلقائياً دون الحاجة لكتابتها."),
                font=FONT_SMALL,
                text_color=COLOR_PRIMARY,
                anchor="e"
            ).pack(fill="x", padx=14, pady=8)

    # =============================================================
    # [2] نموذج أنظمة المعادلات الخطية AX = B
    # =============================================================
    def _build_linear_systems_form(self, parent: ctk.CTkFrame):
        # صف اختيار الحجم n
        size_bar = ctk.CTkFrame(parent, fg_color="transparent")
        size_bar.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(
            size_bar,
            text=ar("رتبة النظام الخطي (عدد المعادلات والمجاهيل n):"),
            font=FONT_SMALL_BOLD,
            text_color=COLOR_TEXT_PRIMARY
        ).pack(side="right", padx=(10, 0))

        # أزرار اختيار الرتبة من 2 إلى 6
        seg_btn = ctk.CTkSegmentedButton(
            size_bar,
            values=["2", "3", "4", "5", "6"],
            command=self._on_change_matrix_size,
            corner_radius=RADIUS_BUTTON,
            font=FONT_BODY_BOLD,
            selected_color=COLOR_PRIMARY,
            selected_hover_color=COLOR_PRIMARY_HOVER
        )
        seg_btn.set(str(self.n_var.get()))
        seg_btn.pack(side="right", padx=10)

        ctk.CTkLabel(
            size_bar,
            text=ar("(التنقل بالأسهم ← ↑ ↓ → و Tab متاح بين خلايا المصفوفة)"),
            font=FONT_TINY,
            text_color=COLOR_TEXT_MUTED
        ).pack(side="left")

        # حاوية شبكة المصفوفة
        self.matrix_grid_container = ctk.CTkFrame(
            parent,
            fg_color=COLOR_BG,
            corner_radius=RADIUS_INPUT,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.matrix_grid_container.pack(fill="both", expand=True, pady=10, padx=4)

        self._render_matrix_grid()

        # إذا كانت جاكوبي: مدخلات التخمين الأولي وشروط التوقف
        if self.method_key == "jacobi":
            self.jacobi_box = ctk.CTkFrame(parent, fg_color="transparent")
            self.jacobi_box.pack(fill="x", pady=(14, 0))

            self._render_jacobi_x0()

            # tol و max_iter
            iter_row = ctk.CTkFrame(self.jacobi_box, fg_color="transparent")
            iter_row.pack(fill="x", pady=(8, 0))
            iter_row.grid_columnconfigure((0, 1), weight=1)

            self.param_fields["tol"] = ValidatedInputField(
                iter_row,
                label="الدقة المطلوبة (ε):",
                default_val="0.0001",
                hint="شرط التوقف عند الخطأ"
            )
            self.param_fields["tol"].grid(row=0, column=1, padx=8, sticky="ew")

            self.param_fields["max_iter"] = ValidatedInputField(
                iter_row,
                label="أقصى تكرارات (N):",
                default_val="50",
                hint="حماية التكرار اللانهائي"
            )
            self.param_fields["max_iter"].grid(row=0, column=0, padx=8, sticky="ew")

    def _render_matrix_grid(self):
        """رسم شبكة مصفوفة المعاملات A ومتجه الثوابت B بالترتيب من اليمين لليسار [A | B]."""
        for child in self.matrix_grid_container.winfo_children():
            child.destroy()

        n = self.n_var.get()
        self.matrix_a_cells = []
        self.vector_b_cells = []

        def_A = self.method_data.get("default_A")
        def_B = self.method_data.get("default_B")
        has_default = (def_A and len(def_A) == n and def_B and len(def_B) == n)

        inner = ctk.CTkFrame(self.matrix_grid_container, fg_color="transparent")
        inner.pack(padx=20, pady=16)

        # ترويسة الأعمدة من اليمين لليسار: x1, x2, ..., xn | B
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x", pady=(0, 6))

        for j in range(n):
            ctk.CTkLabel(
                header,
                text=f"x{j+1}",
                font=FONT_SMALL_BOLD,
                text_color=COLOR_TEXT_PRIMARY,
                width=64,
                anchor="center"
            ).pack(side=side_start(), padx=3)

        ctk.CTkLabel(header, text="|", font=FONT_SECTION, text_color=COLOR_BORDER, width=16).pack(side=side_start())

        ctk.CTkLabel(
            header,
            text=ar("B (الثوابت)"),
            font=FONT_SMALL_BOLD,
            text_color=COLOR_PRIMARY,
            width=76,
            anchor="center"
        ).pack(side=side_start(), padx=4)

        # خلايا كل صف
        for i in range(n):
            row_frame = ctk.CTkFrame(inner, fg_color="transparent")
            row_frame.pack(fill="x", pady=3)

            a_row = []
            for j in range(n):
                a_cell = ctk.CTkEntry(
                    row_frame,
                    font=FONT_MONO,
                    width=64,
                    height=36,
                    justify="left",
                    corner_radius=RADIUS_BADGE,
                    border_width=1,
                    border_color=COLOR_BORDER,
                    fg_color=COLOR_SURFACE
                )
                a_cell.pack(side=side_start(), padx=3)
                if has_default:
                    a_val = str(def_A[i][j])
                else:
                    a_val = "4.0" if i == j else "1.0"
                a_cell.insert(0, a_val)
                a_row.append(a_cell)
            self.matrix_a_cells.append(a_row)

            ctk.CTkLabel(row_frame, text="|", font=FONT_SECTION, text_color=COLOR_BORDER, width=16).pack(side=side_start())

            # خلية المتجه B
            b_cell = ctk.CTkEntry(
                row_frame,
                font=FONT_MONO,
                width=76,
                height=36,
                justify="left",
                corner_radius=RADIUS_BADGE,
                border_width=1,
                border_color=COLOR_BORDER,
                fg_color=COLOR_SURFACE
            )
            b_cell.pack(side=side_start(), padx=4)
            b_val = str(def_B[i]) if has_default else ("1.0" if i == 0 else "0.0")
            b_cell.insert(0, b_val)
            self.vector_b_cells.append(b_cell)

        # ربط أحداث التنقل بالأسهم بين كافة الخلايا
        self._bind_matrix_keyboard_navigation(n)

    def _bind_matrix_keyboard_navigation(self, n: int):
        """ربط مفاتيح الأسهم للتنقل السلس والذكي بين خلايا المصفوفة والمتجه."""
        for i in range(n):
            for j in range(n):
                cell = self.matrix_a_cells[i][j]
                cell.bind("<Up>", lambda e, r=i, c=j: self._move_focus(r - 1, c, "a"))
                cell.bind("<Down>", lambda e, r=i, c=j: self._move_focus(r + 1, c, "a"))
                # في الترتيب من اليمين لليسار: السهم لليمين يتحرك نحو البداية (j - 1)، والسهم لليسار نحو B (j + 1)
                cell.bind("<Right>", lambda e, r=i, c=j: self._move_focus(r, c - 1, "a"))
                cell.bind("<Left>", lambda e, r=i, c=j: self._move_focus(r, c + 1, "a"))

            b_cell = self.vector_b_cells[i]
            b_cell.bind("<Up>", lambda e, r=i: self._move_focus(r - 1, 0, "b"))
            b_cell.bind("<Down>", lambda e, r=i: self._move_focus(r + 1, 0, "b"))
            b_cell.bind("<Right>", lambda e, r=i: self._move_focus(r, n - 1, "a"))

    def _move_focus(self, target_row: int, target_col: int, target_type: str):
        n = self.n_var.get()
        if target_type == "b":
            if 0 <= target_row < n:
                self.vector_b_cells[target_row].focus_set()
        else:
            if target_col >= n:
                if 0 <= target_row < n:
                    self.vector_b_cells[target_row].focus_set()
            elif target_col >= 0 and 0 <= target_row < n:
                self.matrix_a_cells[target_row][target_col].focus_set()

    def _render_jacobi_x0(self):
        """رسم خلايا التخمين الأولي لطريقة جاكوبي من اليمين إلى اليسار."""
        if not hasattr(self, "jacobi_box"):
            return

        for child in self.jacobi_box.winfo_children():
            child.destroy()

        n = self.n_var.get()
        self.x0_cells = []

        title_lbl = ctk.CTkLabel(
            self.jacobi_box,
            text=ar("التخمين الأولي X0 للمجاهيل:"),
            font=FONT_SMALL_BOLD,
            text_color=COLOR_TEXT_PRIMARY,
            anchor=anchor_start(),
            justify=justify_start()
        )
        title_lbl.pack(fill="x", pady=(0, 4))

        row = ctk.CTkFrame(self.jacobi_box, fg_color="transparent")
        row.pack(fill="x")

        for j in range(n):
            col_box = ctk.CTkFrame(row, fg_color="transparent")
            col_box.pack(side=side_start(), padx=4)

            ctk.CTkLabel(col_box, text=f"x{j+1}⁽⁰⁾", font=FONT_TINY, text_color=COLOR_TEXT_MUTED).pack(side="top")
            x0_ent = ctk.CTkEntry(
                col_box,
                font=FONT_MONO,
                width=64,
                height=34,
                justify="left",
                corner_radius=RADIUS_BADGE,
                border_width=1,
                border_color=COLOR_BORDER,
                fg_color=COLOR_SURFACE
            )
            x0_ent.pack(side="top")
            x0_ent.insert(0, "0.0")
            self.x0_cells.append(x0_ent)

    def _on_change_matrix_size(self, choice: str):
        try:
            val = int(choice)
            if 2 <= val <= 6:
                self.n_var.set(val)
                self._render_matrix_grid()
                if self.method_key == "jacobi":
                    self._render_jacobi_x0()
        except Exception:
            pass

    # =============================================================
    # [3] نموذج استيفاء لاجرانج مع إضافة وحذف النقاط ديناميكياً
    # =============================================================
    def _build_interpolation_form(self, parent: ctk.CTkFrame):
        # شريط أزرار التحكم بالنقاط
        ctrl_bar = ctk.CTkFrame(parent, fg_color="transparent")
        ctrl_bar.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            ctrl_bar,
            text=ar("جدول النقاط المعلومة (xi , yi):"),
            font=FONT_SMALL_BOLD,
            text_color=COLOR_TEXT_PRIMARY
        ).pack(side="right", padx=(10, 0))

        # أزرار الإضافة والحذف
        add_btn = GhostButton(
            ctrl_bar,
            text="+ إضافة نقطة",
            command=self._on_add_point,
            width=110,
            height=32
        )
        add_btn.pack(side="right", padx=6)

        remove_btn = GhostButton(
            ctrl_bar,
            text="− حذف آخر نقطة",
            command=self._on_remove_point,
            width=110,
            height=32
        )
        remove_btn.pack(side="right")

        # حاوية جدول النقاط
        self.points_container = ctk.CTkFrame(
            parent,
            fg_color=COLOR_BG,
            corner_radius=RADIUS_INPUT,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.points_container.pack(fill="x", pady=6, padx=4)

        # الترويسة
        header = ctk.CTkFrame(self.points_container, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(12, 6))

        ctk.CTkLabel(header, text=ar("رقم النقطة"), font=FONT_SMALL_BOLD, text_color=COLOR_TEXT_MUTED, width=80).pack(side="right", padx=6)
        ctk.CTkLabel(header, text=ar("xi (الإحداثي السيني)"), font=FONT_SMALL_BOLD, text_color=COLOR_PRIMARY, width=140).pack(side="right", padx=6)
        ctk.CTkLabel(header, text=ar("yi = f(xi)"), font=FONT_SMALL_BOLD, text_color=COLOR_SECONDARY, width=140).pack(side="right", padx=6)

        # الحاوية التي تحمل صفوف النقاط
        self.points_rows_frame = ctk.CTkFrame(self.points_container, fg_color="transparent")
        self.points_rows_frame.pack(fill="x", padx=16, pady=(0, 12))

        # ملء النقاط الافتراضية
        def_pts = self.method_data.get("default_points", [(1.0, 1.0), (2.0, 4.0), (3.0, 9.0)])
        self.points_rows = []
        for xi, yi in def_pts:
            self._create_point_row(xi, yi)

        # حقل قيمة x المراد تقديرها
        eval_bar = ctk.CTkFrame(parent, fg_color="transparent")
        eval_bar.pack(fill="x", pady=(14, 0))

        self.x_eval_field = ValidatedInputField(
            eval_bar,
            label="قيمة x المطلوب تقدير قيمة الدالة عندها P(x):",
            default_val=str(self.method_data.get("default_x_eval", 2.5)),
            hint="القيمة النقطية المراد تعويضها في كثيرة حدود لاجرانج",
            is_numeric=True
        )
        self.x_eval_field.pack(fill="x")

    def _create_point_row(self, xi: float, yi: float):
        idx = len(self.points_rows)
        row_frame = ctk.CTkFrame(self.points_rows_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=3)

        lbl = ctk.CTkLabel(
            row_frame,
            text=f"النقطة {idx}",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_SECONDARY,
            width=80
        )
        lbl.pack(side="right", padx=6)

        x_entry = ctk.CTkEntry(
            row_frame,
            font=FONT_MONO,
            width=140,
            height=34,
            justify="left",
            corner_radius=RADIUS_BADGE,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE
        )
        x_entry.pack(side=side_start(), padx=6)
        x_entry.insert(0, str(xi))

        y_entry = ctk.CTkEntry(
            row_frame,
            font=FONT_MONO,
            width=140,
            height=34,
            justify="left",
            corner_radius=RADIUS_BADGE,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE
        )
        y_entry.pack(side=side_start(), padx=6)
        y_entry.insert(0, str(yi))

        self.points_rows.append((row_frame, x_entry, y_entry))

    def _on_add_point(self):
        idx = len(self.points_rows)
        if idx >= 10:
            self.router.show_toast("الحد الأقصى للنقاط هو 10 نقاط", toast_type="warning")
            return
        next_x = float(idx + 1)
        next_y = float((idx + 1) ** 2)
        self._create_point_row(next_x, next_y)

    def _on_remove_point(self):
        if len(self.points_rows) <= 2:
            self.router.show_toast("يلزم وجود نقطتين على الأقل لاستيفاء لاجرانج", toast_type="warning")
            return
        last_row, _, _ = self.points_rows.pop()
        last_row.destroy()

    # =============================================================
    # [4] نموذج التفاضل والتكامل العددي
    # =============================================================
    def _build_calculus_form(self, parent: ctk.CTkFrame):
        self.func_field = ValidatedInputField(
            parent,
            label="الدالة الرياضية f(x):",
            default_val=self.method_data.get("default_f", "x^2"),
            hint="أمثلة:  x^2  أو  sin(x)  أو  exp(x)  أو  1 / (1 + x^2)",
            is_numeric=False
        )
        self.func_field.pack(fill="x", pady=(0, 14))

        params_grid = ctk.CTkFrame(parent, fg_color="transparent")
        params_grid.pack(fill="x", pady=(0, 10))
        params_grid.grid_columnconfigure((0, 1), weight=1, uniform="calc_param")

        inputs = self.method_data.get("inputs", [])
        row = 0
        col = 1
        for key, label_txt, default_val, desc_txt in inputs:
            field = ValidatedInputField(
                params_grid,
                label=label_txt,
                default_val=default_val,
                hint=desc_txt,
                is_numeric=True
            )
            field.grid(row=row, column=col, padx=8, pady=6, sticky="ew")
            self.param_fields[key] = field

            col -= 1
            if col < 0:
                col = 1
                row += 1

    # =============================================================
    # تشغيل الحساب (Calculate Action)
    # =============================================================
    def _on_click_calculate(self):
        # تغيير حالة الزر فورياً إلى "جارٍ الحساب..."
        self.calc_btn.configure(text=ar("جارٍ الحساب... ⏳"), state="disabled")
        self.update_idletasks()

        # تأخير قصير جداً (50ms) لإعطاء إحساس بصري سلس بالمعالجة
        self.after(50, self._perform_calculation)

    def _perform_calculation(self):
        try:
            cat_type = self.cat_data.get("type")
            calc_func = self.method_data["func"]

            # 1. معادلات غير خطية
            if cat_type == "nonlinear":
                f_str = self.func_field.get()
                if not f_str:
                    raise ValueError("يرجى إدخال الدالة الرياضية.")

                if self.method_key == "fixed_point":
                    g_func = make_function(f_str)
                    x0 = float(self.param_fields["x0"].get())
                    tol = float(self.param_fields["tol"].get())
                    max_iter = int(self.param_fields["max_iter"].get())
                    table, result = calc_func(g_func, x0, tol, max_iter)
                elif self.method_key == "newton":
                    f_func = make_function(f_str)
                    df_func = derivative(f_str)
                    x0 = float(self.param_fields["x0"].get())
                    tol = float(self.param_fields["tol"].get())
                    max_iter = int(self.param_fields["max_iter"].get())
                    table, result = calc_func(f_func, df_func, x0, tol, max_iter)
                elif self.method_key in ["bisection", "false_position"]:
                    f_func = make_function(f_str)
                    a = float(self.param_fields["a"].get())
                    b = float(self.param_fields["b"].get())
                    tol = float(self.param_fields["tol"].get())
                    max_iter = int(self.param_fields["max_iter"].get())
                    table, result = calc_func(f_func, a, b, tol, max_iter)
                elif self.method_key == "secant":
                    f_func = make_function(f_str)
                    x0 = float(self.param_fields["x0"].get())
                    x1 = float(self.param_fields["x1"].get())
                    tol = float(self.param_fields["tol"].get())
                    max_iter = int(self.param_fields["max_iter"].get())
                    table, result = calc_func(f_func, x0, x1, tol, max_iter)

            # 2. أنظمة خطية
            elif cat_type == "linear_systems":
                n = self.n_var.get()
                A = []
                for i in range(n):
                    row_vals = []
                    for j in range(n):
                        val_str = self.matrix_a_cells[i][j].get().strip()
                        if not val_str:
                            raise ValueError(f"العنصر a({i+1},{j+1}) فارغ؛ يرجى ملء كافة خلايا المصفوفة.")
                        row_vals.append(float(val_str))
                    A.append(row_vals)

                B = []
                for i in range(n):
                    b_str = self.vector_b_cells[i].get().strip()
                    if not b_str:
                        raise ValueError(f"العنصر b({i+1}) فارغ.")
                    B.append(float(b_str))

                if self.method_key == "jacobi":
                    # فحص السيادة القطرية
                    is_dom, dom_msg = check_diagonal_dominance(A)
                    if not is_dom:
                        self.router.show_toast(
                            "تنبيه: المصفوفة ليست مهيمنة قطرياً؛ جاري الحساب مع احتمالية بطء التقارب",
                            toast_type="warning"
                        )

                    X0 = [float(cell.get().strip() or "0.0") for cell in self.x0_cells]
                    tol = float(self.param_fields["tol"].get() or "0.0001")
                    max_iter = int(self.param_fields["max_iter"].get() or "50")
                    table, result = calc_func(A, B, X0, tol, max_iter)
                else:
                    table, result = calc_func(A, B)

            # 3. استيفاء لاجرانج
            elif cat_type == "interpolation":
                x_pts = []
                y_pts = []
                for _, x_ent, y_ent in self.points_rows:
                    xs = x_ent.get().strip()
                    ys = y_ent.get().strip()
                    if not xs or not ys:
                        raise ValueError("يرجى ملء جميع إحداثيات النقاط المعطاة.")
                    x_pts.append(float(xs))
                    y_pts.append(float(ys))

                x_eval_str = self.x_eval_field.get()
                if not x_eval_str:
                    raise ValueError("يرجى إدخال قيمة x المطلوب تقديرها.")
                x_eval = float(x_eval_str)

                table, result = calc_func(x_pts, y_pts, x_eval)

            # 4. تفاضل وتكامل عددي
            elif cat_type == "calculus":
                f_str = self.func_field.get()
                if not f_str:
                    raise ValueError("يرجى إدخال الدالة الرياضية.")

                if self.method_key == "trapezoidal":
                    f_func = make_function(f_str)
                    a = float(self.param_fields["a"].get())
                    b = float(self.param_fields["b"].get())
                    n = int(self.param_fields["n"].get())
                    table, result = calc_func(f_func, a, b, n)
                elif self.method_key == "numerical_diff":
                    x0 = float(self.param_fields["x0"].get())
                    h = float(self.param_fields["h"].get())
                    table, result = calc_func(f_str, x0, h)

            # نجاح الحساب: الانتقال إلى شاشة النتائج
            self.router.show_screen(
                "result",
                cat_key=self.cat_key,
                cat_data=self.cat_data,
                method_key=self.method_key,
                method_data=self.method_data,
                table=table,
                result=result
            )

        except ValueError as e:
            err_msg = str(e)
            if "could not convert" in err_msg or "invalid literal" in err_msg:
                err_msg = "يرجى التأكد من إدخال أرقام صحيحة في جميع الحقول المطلوبة."
            self.router.show_toast(err_msg, toast_type="error")
        except ZeroDivisionError:
            self.router.show_toast("حدثت قسمة على صفر؛ يرجى مراجعة معاملات المسألة لتجنب انعدام المقام.", toast_type="error")
        except Exception:
            self.router.show_toast("صيغة الدالة الرياضية غير صحيحة، يرجى كتابتها بصيغة مقبولة (مثال: x^3 - x - 2).", toast_type="error")
        finally:
            # استعادة زر الحساب فقط في حال لم تُدمر الشاشة بعد
            try:
                if self.winfo_exists() and hasattr(self, "calc_btn") and self.calc_btn.winfo_exists():
                    self.calc_btn.configure(text=ar("احسب 🖩"), state="normal")
            except Exception:
                pass
