"""
مكوّنات واجهة المستخدم القابلة لإعادة الاستخدام (Reusable UI Components)
========================================================================
تحتوي على:
1. Card: بطاقة تفاعلية بحواف دائرية وتأثير Hover ناعم.
2. PrimaryButton / GhostButton: أزرار أساسية وثانوية بتصميم راقٍ.
3. AppHeader: شريط علوي موحد مع Breadcrumb وزر رجوع وتبديل المظهر.
4. Toast: إشعارات منبثقة غير حاجبة (تختفي تلقائياً بعد 3 ثوانٍ).
5. NoScrollbarFrame: حاوية قابلة للتمرير بعجلة الفأرة والأسهم دون ظهور أي Scrollbar.
"""

import sys
import tkinter as tk
from typing import Callable, Optional, Dict, Any, List

import customtkinter as ctk

from .theme import (
    FONT_FAMILY,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_SECTION,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_SMALL,
    FONT_SMALL_BOLD,
    FONT_TINY,
    COLOR_BG,
    COLOR_SURFACE,
    COLOR_SURFACE_HOVER,
    COLOR_BORDER,
    COLOR_BORDER_HOVER,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_SECONDARY,
    COLOR_SUCCESS,
    COLOR_SUCCESS_BG,
    COLOR_ERROR,
    COLOR_ERROR_BG,
    COLOR_WARNING,
    COLOR_WARNING_BG,
    COLOR_INFO,
    COLOR_INFO_BG,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    COLOR_ON_PRIMARY,
    RADIUS_CARD,
    RADIUS_BUTTON,
    RADIUS_INPUT,
    RADIUS_BADGE,
    RADIUS_TOAST,
    RTL,
    side_start,
    side_end,
    anchor_start,
    anchor_end,
    justify_start,
    justify_end,
    rtl_col,
    ar,
)


# =============================================================
# 1. زر أساسي وزر ثانوي (PrimaryButton & GhostButton)
# =============================================================
class PrimaryButton(ctk.CTkButton):
    """زر رئيسي بلون العلامة وحواف دائرية."""
    def __init__(self, master, text: str, command: Optional[Callable] = None, **kwargs):
        font = kwargs.pop("font", FONT_BODY_BOLD)
        height = kwargs.pop("height", 44)
        super().__init__(
            master=master,
            text=ar(text),
            command=command,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_ON_PRIMARY,
            corner_radius=RADIUS_BUTTON,
            font=font,
            height=height,
            cursor="hand2",
            **kwargs
        )


class GhostButton(ctk.CTkButton):
    """زر شفاف بحدود ناعمة وتأثير مرور خفيف."""
    def __init__(self, master, text: str, command: Optional[Callable] = None, **kwargs):
        font = kwargs.pop("font", FONT_BODY)
        height = kwargs.pop("height", 40)
        super().__init__(
            master=master,
            text=ar(text),
            command=command,
            fg_color="transparent",
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT_PRIMARY,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=RADIUS_BUTTON,
            font=font,
            height=height,
            cursor="hand2",
            **kwargs
        )


# =============================================================
# 2. بطاقة تفاعلية مع تأثير Hover ناعم (Card)
# =============================================================
class Card(ctk.CTkFrame):
    """
    بطاقة عصرية بحواف دائرية (18px) وظل خفيف وتأثير Hover ناعم.
    تقبل أيقونة رمزية، عنواناً، وصفاً، وشارة ترقيم، ودالة تنفيذ عند النقر.
    """
    def __init__(
        self,
        master,
        title: str,
        desc: str = "",
        icon: str = "⚡",
        badge: str = "",
        on_click: Optional[Callable] = None,
        width: int = 280,
        height: int = 180,
        **kwargs
    ):
        super().__init__(
            master=master,
            corner_radius=RADIUS_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE,
            width=width,
            height=height,
            cursor="hand2" if on_click else "arrow",
            **kwargs
        )
        self.on_click = on_click
        self._is_hovered = False

        self._build_card_ui(title, desc, icon, badge)
        self._bind_events()

    def _build_card_ui(self, title: str, desc: str, icon: str, badge: str):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. الصف العلوي: الأيقونة على اليمين والشارة على اليسار
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", padx=18, pady=(16, 6))

        # الأيقونة على اليمين
        icon_lbl = ctk.CTkLabel(
            top_row,
            text=icon,
            font=(FONT_FAMILY, 24, "bold"),
            text_color=COLOR_PRIMARY
        )
        icon_lbl.pack(side=side_start())

        # الشارة على اليسار
        if badge:
            badge_lbl = ctk.CTkLabel(
                top_row,
                text=ar(badge),
                font=FONT_SMALL_BOLD,
                text_color=COLOR_PRIMARY,
                fg_color=COLOR_BG,
                corner_radius=RADIUS_BADGE,
                padx=10,
                pady=3
            )
            badge_lbl.pack(side=side_end())

        # 2. عنوان البطاقة
        self.title_lbl = ctk.CTkLabel(
            self,
            text=ar(title),
            font=FONT_SUBTITLE,
            text_color=COLOR_TEXT_PRIMARY,
            anchor=anchor_start(),
            justify=justify_start()
        )
        self.title_lbl.pack(fill="x", padx=18, pady=(2, 4))

        # 3. وصف البطاقة
        if desc:
            self.desc_lbl = ctk.CTkLabel(
                self,
                text=ar(desc),
                font=FONT_SMALL,
                text_color=COLOR_TEXT_SECONDARY,
                anchor=anchor_start(),
                justify=justify_start(),
                wraplength=260
            )
            self.desc_lbl.pack(fill="x", padx=18, pady=(0, 14))

    def _bind_events(self):
        """ربط أحداث المرور والنقر بكافة عناصر البطاقة وأبنائها."""
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
        # التحقق مما إذا كان المؤشر لا يزال داخل حدود البطاقة
        x, y = self.winfo_pointerxy()
        wx = self.winfo_rootx()
        wy = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()

        if wx <= x <= wx + w and wy <= y <= wy + h:
            return  # ما زال فوق عنصر ابن داخل البطاقة

        if self._is_hovered:
            self._is_hovered = False
            self.configure(fg_color=COLOR_SURFACE, border_color=COLOR_BORDER, border_width=1)
            self.title_lbl.configure(text_color=COLOR_TEXT_PRIMARY)


# =============================================================
# 3. شريط التنقل العلوي الموحد (AppHeader) - متوافق 100% مع RTL
# =============================================================
class AppHeader(ctk.CTkFrame):
    """
    شريط علوي يحتوي على عناصر مرتبة من اليمين إلى اليسار (RTL):
    1. على أقصى اليمين: زر الرجوع مع سهم يشير لليمين (→).
    2. بجانبه إلى اليسار: عنوان الشاشة بمحاذاة يمينية.
    3. بعده: مسار التنقل (Breadcrumb) كعناصر منفصلة تبدأ من الرئيسية على اليمين مع فواصل ‹.
    4. على أقصى اليسار: زر تبديل المظهر (☀️ / 🌙).
    """
    def __init__(
        self,
        master,
        title: str,
        breadcrumbs: Optional[List[tuple]] = None,
        breadcrumb: Optional[str] = None,
        on_back: Optional[Callable] = None,
        on_toggle_theme: Optional[Callable] = None,
        is_dark_mode: bool = True,
        **kwargs
    ):
        super().__init__(master=master, fg_color="transparent", height=70, **kwargs)
        self.title_text = title
        self.breadcrumbs = breadcrumbs or []
        self.breadcrumb_str = breadcrumb
        self.on_back = on_back
        self.on_toggle_theme = on_toggle_theme
        self.is_dark_mode = is_dark_mode

        self._build_header()

    def _build_header(self):
        # 1. على أقصى اليسار: زر تبديل المظهر (☀ / 🌙)
        theme_box = ctk.CTkFrame(self, fg_color="transparent")
        theme_box.pack(side=side_end(), fill="y", padx=(10, 0), pady=12)

        theme_icon = "☀️ فاتح" if self.is_dark_mode else "🌙 داكن"
        self.theme_btn = GhostButton(
            theme_box,
            text=theme_icon,
            command=self._handle_toggle_theme,
            width=90,
            height=38,
            font=FONT_SMALL_BOLD
        )
        self.theme_btn.pack(side=side_end(), pady=2)

        # 2. على أقصى اليمين: زر الرجوع مع سهم يشير لليمين (→)
        if self.on_back:
            back_btn = GhostButton(
                self,
                text="→ رجوع",
                command=self.on_back,
                width=84,
                height=38,
                font=FONT_SMALL_BOLD
            )
            back_btn.pack(side=side_start(), padx=(0, 14), pady=12)

        # 3. بجانبه إلى اليسار: عنوان الشاشة بمحاذاة يمينية
        self.title_lbl = ctk.CTkLabel(
            self,
            text=ar(self.title_text),
            font=FONT_SUBTITLE,
            text_color=COLOR_TEXT_PRIMARY,
            anchor=anchor_start(),
            justify=justify_start()
        )
        self.title_lbl.pack(side=side_start(), padx=(0, 14), pady=12)

        # 4. بعده: مسار التنقل (Breadcrumb) عناصر منفصلة من اليمين إلى اليسار
        items = self._get_breadcrumb_items()
        if items:
            div = ctk.CTkLabel(
                self,
                text="|",
                font=FONT_SECTION,
                text_color=COLOR_BORDER,
                width=10
            )
            div.pack(side=side_start(), padx=(0, 10), pady=12)

            bc_container = ctk.CTkFrame(self, fg_color="transparent")
            bc_container.pack(side=side_start(), fill="y", pady=12)

            for i, item in enumerate(items):
                name = item[0]
                cmd = item[1] if len(item) > 1 else None
                is_last = (i == len(items) - 1)

                if is_last or cmd is None:
                    lbl = ctk.CTkLabel(
                        bc_container,
                        text=ar(name),
                        font=FONT_SMALL_BOLD if is_last else FONT_SMALL,
                        text_color=COLOR_PRIMARY if is_last else COLOR_TEXT_MUTED,
                        anchor=anchor_start()
                    )
                    lbl.pack(side=side_start(), padx=2)
                else:
                    lbl = ctk.CTkLabel(
                        bc_container,
                        text=ar(name),
                        font=FONT_SMALL,
                        text_color=COLOR_TEXT_MUTED,
                        cursor="hand2",
                        anchor=anchor_start()
                    )
                    lbl.pack(side=side_start(), padx=2)
                    lbl.bind("<Button-1>", lambda e, c=cmd: c())
                    lbl.bind("<Enter>", lambda e, w=lbl: w.configure(text_color=COLOR_PRIMARY))
                    lbl.bind("<Leave>", lambda e, w=lbl: w.configure(text_color=COLOR_TEXT_MUTED))

                if not is_last:
                    sep = ctk.CTkLabel(
                        bc_container,
                        text="‹",
                        font=FONT_SMALL_BOLD,
                        text_color=COLOR_BORDER_HOVER,
                        padx=3
                    )
                    sep.pack(side=side_start())

    def _get_breadcrumb_items(self) -> List[tuple]:
        if self.breadcrumbs:
            return self.breadcrumbs
        if not self.breadcrumb_str:
            return []
        parts = [p.strip() for p in self.breadcrumb_str.replace("›", "‹").split("‹") if p.strip()]
        return [(p, None) for p in parts]

    def _handle_toggle_theme(self):
        if self.on_toggle_theme:
            self.on_toggle_theme()
            self.is_dark_mode = not self.is_dark_mode
            self.theme_btn.configure(text="☀️ فاتح" if self.is_dark_mode else "🌙 داكن")


# =============================================================
# 4. إشعار منبثق أنيق وغير حاجب (Toast)
# =============================================================
class Toast(ctk.CTkFrame):
    """
    إشعار عائم في أعلى النافذة يظهر بانسيابية ويختفي تلقائياً بعد 3 ثوانٍ.
    يدعم 4 حالات: error, warning, success, info.
    """
    def __init__(self, master, message: str, toast_type: str = "info", duration_ms: int = 3200):
        # اختيار الألوان حسب نوع الإشعار
        if toast_type == "error":
            fg_col = COLOR_ERROR_BG
            text_col = COLOR_ERROR
            icon = "❌"
            border_col = COLOR_ERROR
        elif toast_type == "warning":
            fg_col = COLOR_WARNING_BG
            text_col = COLOR_WARNING
            icon = "⚠️"
            border_col = COLOR_WARNING
        elif toast_type == "success":
            fg_col = COLOR_SUCCESS_BG
            text_col = COLOR_SUCCESS
            icon = "✅"
            border_col = COLOR_SUCCESS
        else:
            fg_col = COLOR_INFO_BG
            text_col = COLOR_INFO
            icon = "ℹ️"
            border_col = COLOR_INFO

        super().__init__(
            master=master,
            corner_radius=RADIUS_TOAST,
            border_width=1,
            border_color=border_col,
            fg_color=fg_col,
            height=46
        )

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=8)

        lbl = ctk.CTkLabel(
            content,
            text=f"{icon}  {ar(message)}",
            font=FONT_BODY_BOLD,
            text_color=text_col,
            anchor=anchor_start(),
            justify=justify_start()
        )
        lbl.pack(side=side_start())

        # إغلاق سريع عند النقر
        self.bind("<Button-1>", lambda e: self.dismiss())
        lbl.bind("<Button-1>", lambda e: self.dismiss())

        # توقيت الإخفاء التلقائي
        self.after(duration_ms, self.dismiss)

    def dismiss(self):
        try:
            self.destroy()
        except Exception:
            pass


# =============================================================
# 5. حاوية قابلة للتمرير دون ظهور أي Scrollbar (NoScrollbarFrame)
# =============================================================
class NoScrollbarFrame(ctk.CTkFrame):
    """
    حاوية متطورة توفر تجربة تمرير فائقة السلاسة عبر:
    - عجلة الفأرة (MouseWheel)
    - لوحة اللمس (Touchpad)
    - أزرار الأسهم و PageUp / PageDown
    - Shift + عجلة الفأرة للتمرير الأفقي
    دون إظهار أي شريط تمرير (Scrollbar) على الإطلاق!
    """
    def __init__(self, master, **kwargs):
        super().__init__(master=master, fg_color="transparent", **kwargs)

        # قماش Tkinter بدون شريط تمرير
        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            bd=0,
            bg=self._get_canvas_bg()
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # الحاوية الداخلية الحاملة للعناصر
        self.inner_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.window_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # ضبط اتساع القماش ومطابقة المحتوى
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # ربط أحداث التمرير بعجلة الفأرة عند وجود المؤشر فوق الحاوية
        self._bind_mouse_scroll(self)
        self._bind_mouse_scroll(self.inner_frame)

    def _get_canvas_bg(self) -> str:
        """جلب لون الخلفية الحالي بناء على مظهر CustomTkinter."""
        mode = ctk.get_appearance_mode()
        return COLOR_BG[1] if mode == "Dark" else COLOR_BG[0]

    def update_canvas_bg(self):
        """تحديث لون خلفية الـ Canvas عند تبديل المظهر."""
        self.canvas.configure(bg=self._get_canvas_bg())

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # ضمان تمدد الإطار الداخلي ليطابق عرض النافذة
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _bind_mouse_scroll(self, widget):
        """ربط عجلة الفأرة وأزرار التمرير لجميع العناصر الداخلية."""
        widget.bind("<Enter>", self._activate_scroll, add="+")
        widget.bind("<Leave>", self._deactivate_scroll, add="+")

    def _activate_scroll(self, event=None):
        # Windows & macOS Mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)
        # Linux Mousewheel
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_down)
        # Keyboard Navigation
        self.canvas.bind_all("<Prior>", lambda e: self.canvas.yview_scroll(-5, "units"))
        self.canvas.bind_all("<Next>", lambda e: self.canvas.yview_scroll(5, "units"))
        self.canvas.bind_all("<Up>", lambda e: self.canvas.yview_scroll(-2, "units"))
        self.canvas.bind_all("<Down>", lambda e: self.canvas.yview_scroll(2, "units"))

    def _deactivate_scroll(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Shift-MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        self.canvas.unbind_all("<Prior>")
        self.canvas.unbind_all("<Next>")
        self.canvas.unbind_all("<Up>")
        self.canvas.unbind_all("<Down>")

    def _on_mousewheel(self, event):
        # في ويندوز event.delta يكون موجباً للأعلى وسالباً للأسفل
        delta = -1 * int(event.delta / 120)
        self.canvas.yview_scroll(delta, "units")

    def _on_shift_mousewheel(self, event):
        # التمرير الأفقي بواسطة Shift + عجلة الفأرة
        delta = -1 * int(event.delta / 120)
        self.canvas.xview_scroll(delta, "units")

    def _on_mousewheel_up(self, event):
        self.canvas.yview_scroll(-2, "units")

    def _on_mousewheel_down(self, event):
        self.canvas.yview_scroll(2, "units")

    def scroll_to_top(self):
        """إعادة التمرير إلى أعلى الصفحة."""
        self.canvas.yview_moveto(0.0)
