"""
الشاشة 2: قائمة الخوارزميات المعتمدة للقسم المختار (Methods Screen)
===================================================================
المرحلة الثانية في التسلسل الهرمي:
- تعرض قائمة مرقمة بالطرق العددية الخاصة بالقسم المختار.
- بطاقات عصرية في شبكة متجاوبة مع ترقيم ملون داخل دوائر وشارة كود الماتلاب.
- ترتيب البطاقات يبدأ من اليمين (RTL).
- ترويسة AppHeader مع مسار تنقل تفاعلي مفصول.
"""

import customtkinter as ctk
from typing import Dict, Any

from ..theme import (
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_SECTION,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_SMALL,
    FONT_SMALL_BOLD,
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_SURFACE_HOVER,
    COLOR_BORDER,
    COLOR_BORDER_HOVER,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    RADIUS_CARD,
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
from ..components import AppHeader, NoScrollbarFrame


class MethodItemCard(ctk.CTkFrame):
    """
    بطاقة طريقة متجاوبة تضم رقم الطريقة بدائرة ملونة على اليمين وشارة الماتلاب على اليسار.
    """
    def __init__(self, master, method_id: int, method_key: str, method_data: Dict[str, Any], on_click, **kwargs):
        super().__init__(
            master=master,
            corner_radius=RADIUS_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE,
            cursor="hand2",
            **kwargs
        )
        self.method_id = method_id
        self.method_key = method_key
        self.method_data = method_data
        self.on_click = on_click
        self._is_hovered = False

        self._build_ui(method_id, method_data)
        self._bind_events()

    def _build_ui(self, method_id: int, method_data: Dict[str, Any]):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=18, pady=16)

        # الصف العلوي: رقم الطريقة بدائرة ملونة في اليمين + شارة الماتلاب في اليسار
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 10))

        # رقم الطريقة داخل دائرة ملونة على اليمين
        num_circle = ctk.CTkLabel(
            top_row,
            text=str(method_id),
            font=FONT_BODY_BOLD,
            text_color="#FFFFFF",
            fg_color=COLOR_PRIMARY,
            corner_radius=18,
            width=36,
            height=36
        )
        num_circle.pack(side=side_start())

        # شارة الماتلاب على اليسار
        matlab_ref = method_data.get("matlab_ref")
        if matlab_ref:
            badge_text = f"⚙️ {matlab_ref}"
            badge_fg = ("#D1FAE5", "#064E3B")
            badge_tc = ("#065F46", "#34D399")
        else:
            badge_text = "🐍 بايثون مباشر"
            badge_fg = ("#F1F5F9", "#1E293B")
            badge_tc = COLOR_TEXT_MUTED

        matlab_badge = ctk.CTkLabel(
            top_row,
            text=ar(badge_text),
            font=FONT_SMALL_BOLD,
            text_color=badge_tc,
            fg_color=badge_fg,
            corner_radius=RADIUS_BADGE,
            padx=10,
            pady=3
        )
        matlab_badge.pack(side=side_end())

        # عنوان الطريقة بمحاذاة يمينية
        self.title_lbl = ctk.CTkLabel(
            content,
            text=ar(method_data["title"]),
            font=FONT_SUBTITLE,
            text_color=COLOR_TEXT_PRIMARY,
            anchor=anchor_start(),
            justify=justify_start()
        )
        self.title_lbl.pack(fill="x", pady=(0, 2))

        # العنوان بالإنجليزية
        en_title = method_data.get("title_en", "")
        if en_title:
            en_lbl = ctk.CTkLabel(
                content,
                text=en_title,
                font=FONT_SMALL,
                text_color=COLOR_TEXT_MUTED,
                anchor=anchor_start(),
                justify=justify_start()
            )
            en_lbl.pack(fill="x", pady=(0, 8))

        # وصف الطريقة بمحاذاة يمينية
        desc_lbl = ctk.CTkLabel(
            content,
            text=ar(method_data.get("desc", "")),
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor=anchor_start(),
            justify=justify_start(),
            wraplength=340
        )
        desc_lbl.pack(fill="both", expand=True, pady=(0, 10))

        # زر اختيار الطريقة
        select_lbl = ctk.CTkLabel(
            content,
            text=ar("اختيار الطريقة ←"),
            font=FONT_SMALL_BOLD,
            text_color=COLOR_PRIMARY,
            anchor=anchor_end()
        )
        select_lbl.pack(anchor=anchor_end())

    def _bind_events(self):
        widgets = [self] + self.winfo_children()
        for w in self.winfo_children():
            widgets.extend(w.winfo_children())

        for w in widgets:
            w.bind("<Enter>", self._on_enter, add="+")
            w.bind("<Leave>", self._on_leave, add="+")
            if self.on_click:
                w.bind("<Button-1>", lambda e: self.on_click(), add="+")

    def _on_enter(self, event=None):
        if not self._is_hovered:
            self._is_hovered = True
            self.configure(fg_color=COLOR_SURFACE_HOVER, border_color=COLOR_BORDER_HOVER, border_width=2)
            self.title_lbl.configure(text_color=COLOR_PRIMARY)

    def _on_leave(self, event=None):
        x, y = self.winfo_pointerxy()
        wx = self.winfo_rootx()
        wy = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()

        if wx <= x <= wx + w and wy <= y <= wy + h:
            return

        if self._is_hovered:
            self._is_hovered = False
            self.configure(fg_color=COLOR_SURFACE, border_color=COLOR_BORDER, border_width=1)
            self.title_lbl.configure(text_color=COLOR_TEXT_PRIMARY)


class MethodsScreen(ctk.CTkFrame):
    """
    الشاشة الثانية: قائمة الطرق المتاحة للقسم المحدد بالاتجاه العربي (RTL).
    """
    def __init__(self, master, router, cat_key: str, cat_data: Dict[str, Any], **kwargs):
        super().__init__(master=master, fg_color="transparent", **kwargs)
        self.router = router
        self.cat_key = cat_key
        self.cat_data = cat_data

        self._build_ui()

    def _build_ui(self):
        # 1. الشريط العلوي مع مسار تنقل تفاعلي مفصول
        header = AppHeader(
            self,
            title=self.cat_data["title"],
            breadcrumbs=[
                ("الرئيسية", lambda: self.router.show_screen("categories")),
                (self.cat_data["title"], None)
            ],
            on_back=lambda: self.router.show_screen("categories"),
            on_toggle_theme=self.router.toggle_theme,
            is_dark_mode=self.router.is_dark_mode
        )
        header.pack(fill="x", padx=30, pady=(16, 10))

        # 2. الحاوية القابلة للتمرير دون scrollbar
        scroll_container = NoScrollbarFrame(self)
        scroll_container.pack(fill="both", expand=True)

        content = scroll_container.inner_frame

        # وصف توضيحي للقسم بمحاذاة يمينية
        desc_box = ctk.CTkFrame(content, fg_color="transparent")
        desc_box.pack(fill="x", padx=30, pady=(0, 16))

        tk_lbl = ctk.CTkLabel(
            desc_box,
            text=ar(f"اختر الخوارزمية المطلوبة لحل المسألة ({self.cat_data['desc']}):"),
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor=anchor_start(),
            justify=justify_start()
        )
        tk_lbl.pack(anchor=anchor_start(), fill="x")

        # 3. شبكة البطاقات (ترتيب يبدأ من أقصى اليمين)
        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        methods_dict = self.cat_data.get("methods", {})
        count = len(methods_dict)
        num_cols = 2 if count <= 4 else 3

        for c in range(num_cols):
            grid.grid_columnconfigure(c, weight=1, uniform="method_col")

        for idx, (method_key, method_data) in enumerate(methods_dict.items()):
            card = MethodItemCard(
                grid,
                method_id=method_data["id"],
                method_key=method_key,
                method_data=method_data,
                on_click=lambda k=method_key, d=method_data: self._on_select_method(k, d)
            )

            row = idx // num_cols
            col = rtl_col(idx, num_cols)  # أول بطاقة في أقصى اليمين
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _on_select_method(self, method_key: str, method_data: Dict[str, Any]):
        """الانتقال لشاشة إدخال المعاملات."""
        self.router.show_screen(
            "input",
            cat_key=self.cat_key,
            cat_data=self.cat_data,
            method_key=method_key,
            method_data=method_data
        )
