import tkinter as _tk
from tkinter import font as _tkFont
from _tkinter import (
    Tcl_Obj as _TclObject,
)

def widgets_configure(*widgets: _tk.Misc, **config):
    [widget.configure(config) for widget in widgets]

def center_to_window(
    window_1: _tk.Tk | _tk.Toplevel,
    window_2: _tk.Tk | _tk.Toplevel,
):
    window_1.update_idletasks()
    w_window_1 = window_1.winfo_width()
    h_window_1 = window_1.winfo_height()
    window_2.update_idletasks()
    w_window_2 = window_2.winfo_width()
    h_window_2 = window_2.winfo_height()
    x_window_2 = window_2.winfo_x()
    y_window_2 = window_2.winfo_y()
    x = x_window_2 + abs(w_window_2 - w_window_1) // 2
    y = y_window_2 + abs(h_window_2 - h_window_1) // 2
    window_1.wm_geometry(f"+{x}+{y}")

def center_to_screen(window: _tk.Tk | _tk.Toplevel):
    window.update_idletasks()
    w_window = window.winfo_width()
    h_window = window.winfo_height()
    w_screen = window.winfo_screenwidth()
    h_screen = window.winfo_screenheight()
    x = abs(w_screen - w_window) // 2
    y = abs(h_screen - h_window) // 2
    window.wm_geometry(f"+{x}+{y}")

def clipboard_sget(widget: _tk.Widget) -> str | None:
    try:
        return widget.clipboard_get()
    except _tk.TclError:
        return None

def ask_font(
    parent: _tk.Misc,
    *,
    font_initial: str | _TclObject | _tkFont.Font = None,
    language: dict[str, str] = None
):

    familys_available = sorted(_tkFont.families())
    if font_initial is not None:
        if isinstance(font_initial, _TclObject):
            font = _tkFont.Font(parent, font=font_initial.string)
        elif isinstance(font_initial, str):
            font = _tkFont.Font(parent, font=font_initial)
        else:
            font = font_initial
        if (family := font.cget("family")) not in set(familys_available):
            raise _tk.TclError
        index_initial = familys_available.index(family)
    else:
        index_initial = 0

    if language is None:
        language = {
            "title": "Font Settings",
            "size": "Size",
            "bold": "Bold",
            "italic": "Italic",
            "underline": "Underline",
            "overstrike": "Strikethrough",
            "ok": "Ok",
            "cancel": "Cancel",
        }

    dialog = _tk.Toplevel(parent)
    dialog.wm_withdraw()
    dialog.wm_title(language["title"])
    dialog.wm_transient(parent)

    frame_left = _tk.Frame(dialog)
    frame_right = _tk.Frame(dialog)
    frame_button = _tk.Frame(dialog)

    listbox_family = _tk.Listbox(frame_left, width=0, height=15, selectmode=_tk.SINGLE, exportselection=False)
    scrollbar_x = _tk.Scrollbar(frame_left, orient=_tk.HORIZONTAL, command=listbox_family.xview)
    scrollbar_y = _tk.Scrollbar(frame_left, orient=_tk.VERTICAL, command=listbox_family.yview)
    listbox_family.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    var_size = _tk.IntVar(frame_right, value=font.cget("size"))
    var_weight = _tk.BooleanVar(frame_right, value=font.cget("weight") == "bold")
    var_slant = _tk.BooleanVar(frame_right, value=font.cget("slant") == "italic")
    var_underline = _tk.BooleanVar(frame_right, value=font.cget("underline"))
    var_overstrike = _tk.BooleanVar(frame_right, value=font.cget("overstrike"))

    label_size = _tk.Label(frame_right, text=language["size"], width=4)
    spinbox_size = _tk.Spinbox(frame_right, width=3, textvariable=var_size, from_=1, to=99, state="readonly")
    checkbutton_weight = _tk.Checkbutton(frame_right, text=language["bold"], variable=var_weight)
    checkbutton_slant = _tk.Checkbutton(frame_right, text=language["italic"], variable=var_slant)
    checkbutton_underline = _tk.Checkbutton(frame_right, text=language["underline"], variable=var_underline)
    checkbutton_overstrike = _tk.Checkbutton(frame_right, text=language["overstrike"], variable=var_overstrike)

    is_ok = False
    family_current = None
    size_current = None
    weight_current = None
    slant_current = None
    underline_current = None
    overstrike_current = None

    def on_ok():
        nonlocal is_ok, family_current, size_current, weight_current, slant_current, underline_current, overstrike_current
        is_ok = True
        family_current = listbox_family.get(listbox_family.curselection()[0])
        size_current = var_size.get()
        if var_weight.get():
            weight_current = "bold"
        else:
            weight_current = "normal"
        if var_slant.get():
            slant_current = "italic"
        else:
            slant_current = "roman"
        underline_current = var_underline.get()
        overstrike_current = var_overstrike.get()
        dialog.destroy()

    button_text_ok = language["ok"]
    button_text_cancel = language["cancel"]
    width_button = max(len(button_text_ok), len(button_text_cancel))
    button_ok = _tk.Button(frame_button, text=button_text_ok, width=width_button, command=on_ok)
    button_cancel = _tk.Button(frame_button, text=button_text_cancel, width=width_button, command=dialog.destroy)

    # 设置布局权重
    dialog.grid_rowconfigure(0, weight=1)
    dialog.grid_columnconfigure(0, weight=1)
    frame_left.grid_rowconfigure(0, weight=1)
    frame_left.grid_columnconfigure(0, weight=1)
    frame_right.grid_columnconfigure((0, 1), weight=1)
    frame_button.grid_rowconfigure(0, weight=1)
    frame_button.grid_columnconfigure(0, weight=1)

    # 放置控件
    frame_left.grid_configure(row=0, column=0, padx=(16, 0), pady=(16, 0), sticky="nsew")
    frame_right.grid_configure(row=0, column=1, padx=(0, 16), pady=(16, 0), sticky="ns")
    frame_button.grid_configure(row=1, column=0, columnspan=2, padx=16, pady=16, sticky="ew")

    listbox_family.grid_configure(row=0, column=0, sticky="nsew")
    scrollbar_x.grid_configure(row=1, column=0, sticky="ew")
    scrollbar_y.grid_configure(row=0, column=1, sticky="ns")

    label_size.grid_configure(row=0, column=0, pady=(0, 8))
    spinbox_size.grid_configure(row=0, column=1, pady=(0, 8))
    checkbutton_weight.grid_configure(row=1, column=0, columnspan=2, sticky="w")
    checkbutton_slant.grid_configure(row=2, column=0, columnspan=2, sticky="w")
    checkbutton_underline.grid_configure(row=3, column=0, columnspan=2, sticky="w")
    checkbutton_overstrike.grid_configure(row=4, column=0, columnspan=2, sticky="w")

    button_ok.grid_configure(row=0, column=0, padx=8, sticky="e")
    button_cancel.grid_configure(row=0, column=1, padx=(0, 4), sticky="e")

    # 插入字体家族
    listbox_family.insert(_tk.END, *familys_available)
    # 选中初始的字体家族
    listbox_family.selection_set(index_initial)
    listbox_family.see(index_initial)

    # 锁定自适应的尺寸
    dialog.update_idletasks()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    dialog.minsize(dialog_width, dialog_height)
    # 移动到屏幕中心
    center_to_screen(dialog)
    # 显示并设置焦点
    dialog.wm_deiconify()
    dialog.focus_set()

    # 等待窗口销毁
    parent.wait_window(dialog)

    if is_ok:
        return _tkFont.Font(
            parent,
            family = family_current,
            size = size_current,
            weight = weight_current,
            slant = slant_current,
            underline = underline_current,
            overstrike = overstrike_current
        )
    return None

class Textbox(_tk.Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<KeyPress-Tab>", lambda event: (self.write("    "), "break")[1])

    def write(self, chars, *args):
        self.tk.call((self._w, 'insert', _tk.INSERT, chars) + args)

    def append(self, chars, *args):
        self.tk.call((self._w, 'insert', _tk.END, chars) + args)

    def selection_ranges(self):
        try:
            return (self.index("sel.first"), self.index("sel.last"))
        except _tk.TclError:
            return ()

    def insertline_ranges(self):
        return (self.index("insert linestart"), self.index("insert lineend"))

    def cut(self):
        # 获取文本（选区文本 / 当前插入位置所在行文本）
        head_position, tail_position = self.selection_ranges() or self.insertline_ranges()
        text = self.get(head_position, tail_position)
        # 复制文本
        self.clipboard_clear()
        self.clipboard_append(text)
        # 删除文本
        self.delete(head_position, tail_position)
        # 跳转视图
        self.see(f"insert +{len(text)}c")
        # 阻止事件传播
        return "break"

    def copy(self):
        # 获取文本（选区文本 / 当前插入位置所在行文本）
        head_position, tail_position = self.selection_ranges() or self.insertline_ranges()
        text = self.get(head_position, tail_position)
        # 复制文本
        self.clipboard_clear()
        self.clipboard_append(text)
        # 阻止事件传播
        return "break"

    def paste(self):
        # 获取文本（剪贴板文本）
        if text := clipboard_sget(self):
            # 若存在选区，替换选区文本
            if selection_position := self.tag_ranges("sel"):
                head_position, tail_position = selection_position
                self.delete(head_position, tail_position)
            # 插入文本
            self.write(text)
            # 跳转视图
            self.see("insert")
        # 阻止事件传播
        return "break"

class Listbox(_tk.Listbox):

    def find(self, text: str):
        for index in range(self.size()):
            if self.get(index) == text:
                return index
        return None