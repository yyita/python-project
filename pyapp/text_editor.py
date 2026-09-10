# done
import tkinter as tk
from tkinter import (
    filedialog as tkFileDialog,
    colorchooser as tkColorChooser,
    messagebox as tkMessagebox,
)
from pylib import tkinter2 as tk2
import itertools
import datetime
import functools
import typing
import os
import sys
import traceback
import time

def logging_when_call(call):

    @functools.wraps(call)
    def wrapper(*args, **kwargs):

        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        arg_parts = []
        if args:
            arg_parts.append(', '.join(map(repr, args)))
        if kwargs:
            arg_parts.append(kwargs)
        print(f"{timestamp} >>> {call.__name__}({', '.join(arg_parts)})")

        try:
            t1 = time.time()
            result = call(*args, **kwargs)
            t2 = time.time()
            print(f"{result!r} {type(result)} {t2 - t1}\n")
            return result
        except Exception:
            print(f"{traceback.format_exc()}\n")

    return wrapper

class AreaManager:

    def __init__(self, textbox: tk.Text, tag_name: str, **config):
        if not isinstance(textbox, tk.Text):
            raise TypeError

        self.textbox = textbox
        self.tag_name = tag_name
        self.position_head = None
        self.position_tail = None

        textbox.tag_configure(FindreplaceDialog.AREA, config)

    def area_exists(self):
        return self.position_head is not None

    def area_add(self, head: str, tail: str):
        if not isinstance(head, str):  raise TypeError
        if not isinstance(tail, str):  raise TypeError
        self.position_head = head
        self.position_tail = tail
        self.textbox.tag_remove(tk.SEL, head, tail)
        self.textbox.tag_add(self.tag_name, head, tail)

    def area_remove(self):
        if (head := self.position_head) is None:  raise Exception
        if (tail := self.position_tail) is None:  raise Exception
        self.textbox.tag_remove(self.tag_name, head, tail)
        self.textbox.tag_add(tk.SEL, head, tail)
        self.position_head = None
        self.position_tail = None

class FindreplaceDialog(tk.Toplevel):

    AREA = "findreplace.area"

    def __init__(
        self,
        master: tk.Misc = None,
        *,
        textbox: tk.Text,
        font_textbox = ("TkFixedFont", 14),
        font_button = ("TkDefaultFont", 10),
        font_label = ("TkDefaultFont", 12),
    ):

        super().__init__(master)
        self.wm_withdraw()
        self.wm_title("Find, and replace or not.")
        self.wm_transient(master)
        self.wm_protocol("WM_DELETE_WINDOW", self.on_exit)
        # self.wm_resizable(False, False)

        # 状态对照: True - normal | False - disabled
        status_options_find = False
        status_options_replace = False

        self.manager_area = AreaManager(
            textbox, tag_name=FindreplaceDialog.AREA,
            background="#cfefff", selectbackground=textbox.cget("selectbackground"),
        )

        @logging_when_call
        def textbox_find__when_modified(event):

            nonlocal status_options_find, status_options_replace

            if (status_textbox := (textbox_find.index("end -1c") != "1.0")) != status_options_find:

                if status_textbox:
                    state_new = tk.NORMAL
                    status_options_find = True
                    status_options_replace = True
                else:
                    state_new = tk.DISABLED
                    status_options_find = False
                    status_options_replace = False

                tk2.widgets_configure(
                    button_find_last, button_find_next, checkbutton_ignorecase,
                    button_replace, button_replace_all, checkbutton_preservecase,
                    state=state_new
                )

            textbox_find.edit_modified(False)

        @logging_when_call
        def on_find_last():

            text = textbox_find.get("1.0", "end -1c")
            offset = len(text)

            manager_area = self.manager_area
            if manager_area.area_exists():
                position_search_tail = manager_area.position_tail
            else:
                position_search_tail = None

            if position_head := textbox.search(
                text, f"insert -{offset}c", position_search_tail, backwards=True,
                nocase=var_ignorecase.get(),
            ):
                row_head, column_head = map(int, position_head.split("."))
                column_tail = column_head + offset
                position_tail = f"{row_head}.{column_tail}"
                textbox.tag_remove("sel", "1.0", tk.END)
                textbox.tag_add("sel", position_head, position_tail)
                textbox.mark_set("insert", position_tail)
                textbox.see(position_head)
            else:
                tkMessagebox.showinfo(parent=self, message="Not found")

        @logging_when_call
        def on_find_next():

            text = textbox_find.get("1.0", "end -1c")
            offset = len(text)

            manager_area = self.manager_area
            if manager_area.area_exists():
                position_search_tail = manager_area.position_tail
            else:
                position_search_tail = None

            if position_head := textbox.search(
                text, tk.INSERT, position_search_tail, forwards=True,
                nocase=var_ignorecase.get()
            ):
                row_head, column_head = map(int, position_head.split("."))
                column_tail = column_head + offset
                position_tail = f"{row_head}.{column_tail}"
                textbox.tag_remove("sel", "1.0", tk.END)
                textbox.tag_add("sel", position_head, position_tail)
                textbox.mark_set("insert", position_tail)
                textbox.see(position_head)
            else:
                tkMessagebox.showinfo(parent=self, message="Not found")

        @logging_when_call
        def on_inselection():
            manager_area = self.manager_area
            if manager_area.area_exists():
                manager_area.area_remove()
            else:
                manager_area.area_add(textbox.index("sel.first"), textbox.index("sel.last"))

        def on_replace():
            head, tail = textbox.tag_ranges("sel")
            textbox.replace(head, tail, self.textbox_replace.get("1.0", "end -1c"))

        def on_replace_all():

            text_find = textbox_find.get("1.0", "end -1c")
            text_replace = textbox_replace.get("1.0", "end -1c")
            offset_text_find = len(text_find)
            offset_text_replace = len(text_replace)

            manager_area = self.manager_area
            if manager_area.area_exists():
                position_head_search = manager_area.position_head
                position_tail_search = manager_area.position_tail
            else:
                position_head_search = "1.0"
                position_tail_search = None

            while position_head_find := textbox.search(
                text_find, position_head_search, position_tail_search, forwards=True,
                nocase=var_ignorecase.get()
            ):
                row_position_head_find, column_position_head_find = map(int, position_head_find.split("."))
                # 替换文本
                column_position_tail_find = column_position_head_find + offset_text_find
                textbox.replace(position_head_find, f"{row_position_head_find}.{column_position_tail_find}", text_replace)
                # 更新搜索起点
                column_position_tail_search = column_position_head_find + offset_text_replace
                position_head_search = f"{row_position_head_find}.{column_position_tail_search}"

        self.textbox = textbox
        self.panedwindow = panedwindow = tk.PanedWindow(self, orient=tk.VERTICAL, showhandle=False, sashrelief=tk.SUNKEN)

        frame_find = tk.Frame(panedwindow)
        label_find = tk.Label(frame_find, text="Find", font=font_label)
        self.textbox_find = textbox_find = tk2.Textbox(frame_find, font=font_textbox, width=30, height=1, bd=0)
        var_ignorecase = tk.BooleanVar(frame_find, value=False)
        checkbutton_ignorecase = tk.Checkbutton(frame_find, text="Ignore case", state=tk.DISABLED, anchor="w", width=13, font=font_button, variable=var_ignorecase)
        button_find_last = tk.Button(frame_find, text="↑", width=2, bd=1, font=font_button, state=tk.DISABLED, command=on_find_last)
        button_find_next = tk.Button(frame_find, text="↓", width=2, bd=1, font=font_button, state=tk.DISABLED, command=on_find_next)

        frame_replace = tk.Frame(panedwindow)
        label_replace = tk.Label(frame_replace, text="Replace As", font=font_label)
        self.textbox_replace = textbox_replace = tk2.Textbox(frame_replace, font=font_textbox, width=30, height=1, bd=0)
        var_preservecase = tk.BooleanVar(frame_replace, value=False)
        checkbutton_preservecase = tk.Checkbutton(frame_replace, text="Preserve case", state=tk.DISABLED, anchor="w", width=13, font=font_button, variable=var_preservecase)
        button_replace = tk.Button(frame_replace, text="↓", width=2, bd=1, font=font_button, state=tk.DISABLED, command=on_replace)
        button_replace_all = tk.Button(frame_replace, text="⇊", width=2, bd=1, font=font_button, state=tk.DISABLED, command=on_replace_all)

        frame_bottom = tk.Frame(self)
        self.var_inselection = var_inselection = tk.BooleanVar(frame_bottom, value=False)
        self.checkbutton_inselection = checkbutton_inselection = tk.Checkbutton(frame_bottom,
            text="In selection", font=font_button, anchor="w", width=13,
            variable=var_inselection, command=on_inselection, state=tk.DISABLED,
        )
        button_move = tk.Button(frame_bottom, text="✥", width=2, bd=1, font=font_button, cursor="fleur")
        button_exit = tk.Button(frame_bottom, text="✕", width=2, bd=1, font=font_button, command=self.on_exit)

        textbox_find.bind("<<Modified>>", textbox_find__when_modified)

        def start_move(event):
            self._dx = event.x_root - self.winfo_x()
            self._dy = event.y_root - self.winfo_y()

        def do_move(event):
            self.wm_geometry(f"+{event.x_root - self._dx}+{event.y_root - self._dy}")

        button_move.bind("<Button-1>", start_move)
        button_move.bind("<B1-Motion>", do_move)

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame_find.grid_rowconfigure(1, weight=1)
        frame_find.grid_columnconfigure(0, weight=1)

        frame_replace.grid_rowconfigure(1, weight=1)
        frame_replace.grid_columnconfigure(0, weight=1)

        frame_bottom.grid_rowconfigure(0, weight=1)
        frame_bottom.grid_columnconfigure(0, weight=1)

        panedwindow.grid_configure(row=0, column=0, padx=8, pady=(8, 4), sticky="nsew")
        panedwindow.add(frame_find, minsize=0, sticky="nsew")
        label_find.grid_configure(row=0, column=0, sticky="w")
        textbox_find.grid_configure(row=1, column=0, columnspan=4, sticky="nsew")
        checkbutton_ignorecase.grid_configure(row=0, column=1)
        button_find_last.grid_configure(row=0, column=2)
        button_find_next.grid_configure(row=0, column=3)

        panedwindow.add(frame_replace, minsize=0, sticky="nsew")
        label_replace.grid_configure(row=0, column=0, sticky="w")
        textbox_replace.grid_configure(row=1, column=0, columnspan=4, sticky="nsew")
        checkbutton_preservecase.grid_configure(row=0, column=1)
        button_replace.grid_configure(row=0, column=2)
        button_replace_all.grid_configure(row=0, column=3)

        frame_bottom.grid_configure(row=1, column=0, padx=8, pady=(4, 8), sticky="ew")
        checkbutton_inselection.grid_configure(row=0, column=1)
        button_move.grid_configure(row=0, column=2)
        button_exit.grid_configure(row=0, column=3)

    def on_exit(self):
        # 隐藏窗口
        self.wm_withdraw()
        # 重置部分配置
        var_inselection = self.var_inselection
        if var_inselection.get():
            var_inselection.set(False)
        # 清理标签（Tag）
        manager_area = self.manager_area
        if manager_area.area_exists():
            manager_area.area_remove()

    def show(self, mode: typing.Literal['find', 'replace']):

        textbox = self.textbox
        panedwindow = self.panedwindow
        textbox_find = self.textbox_find
        textbox_replace = self.textbox_replace

        # 存在选区时，自动设置“查找”输入框的内容为选区文本
        if position_selection := textbox.tag_ranges("sel"):
            position_head, position_tail = position_selection
            selection = textbox.get(position_head, position_tail)
            textbox_find.set(selection)

        # 仅在窗口未显示时进行居中+显示
        if not self.winfo_viewable():
            tk2.center_to_window(self, self.master)
            self.wm_deiconify()

        # · 根据模式选择是否隐藏“替换”相关控件。
        # · 让输入框获得焦点以等待输入。（应避免在窗口显示前进行，否则焦点会被切换）
        reqheight_panedwindow = panedwindow.winfo_reqheight()
        if mode == "find":
            panedwindow.sash_place(0, 0, reqheight_panedwindow)
            textbox_find.focus_set()
        else:
            panedwindow.sash_place(0, 0, reqheight_panedwindow // 2)
            textbox_replace.focus_set()

class TextEditor(tk.Toplevel):

    def __init__(self, master: tk.Tk):

        @logging_when_call
        def menu_file__on_load(event = None):
            if path_file := tkFileDialog.askopenfilename(parent=self):
                self.load(path_file)
            return "break"

        @logging_when_call
        def menu_file__on_save(event = None):
            if path_file := tkFileDialog.asksaveasfilename(parent=self):
                try:
                    with open(path_file, "w", encoding="UTF-8") as handle_file:
                        data = textbox.get("1.0", "end -1c")
                        handle_file.write(data)
                except Exception as error:
                    tkMessagebox.showinfo("Text Editor: Save failed", error)
            return "break"

        @logging_when_call
        def menu_edit__on_cut(event = None):
            return textbox.cut()

        @logging_when_call
        def menu_edit__on_copy(event = None):
            return textbox.copy()

        @logging_when_call
        def menu_edit__on_paste(event = None):
            return textbox.paste()

        @logging_when_call
        def menu_edit__on_undo(event = None):
            # Undo 栈不为空时 undo
            if textbox.edit("canundo"):
                textbox.edit_undo()
                # 启用 Redo 菜单（若已禁用）
                if str(menu_edit.entrycget("Redo", "state")) == "disabled":
                    menu_edit.entryconfigure("Redo", state="normal")
                    print("Enable 'Redo' entry.")
                # 禁用 Undo 菜单（若 Undo 栈已空）
                if not textbox.edit("canundo"):
                    menu_edit.entryconfigure("Undo", state="disabled")
                    print("Disable 'Undo' entry.")
            # 阻止事件传播
            return "break"

        @logging_when_call
        def menu_edit__on_redo(event = None):
            # Redo 栈不为空时 redo
            if textbox.edit("canredo"):
                textbox.edit_redo()
                # 启用 Undo 菜单（若已禁用）
                if str(menu_edit.entrycget("Undo", "state")) == "disabled":
                    menu_edit.entryconfigure("Undo", state="normal")
                    print("Enable 'Undo' entry.")
                # 禁用 Redo 菜单（若 Redo 栈已空）
                if not textbox.edit("canredo"):
                    menu_edit.entryconfigure("Redo", state="disabled")
                    print("Disable 'Redo' entry.")
            # 阻止事件传播
            return "break"

        @logging_when_call
        def menu_edit__on_find(event = None):
            findreplace_dialog.show('find')

        @logging_when_call
        def menu_edit__on_replace(event = None):
            findreplace_dialog.show('replace')

        @logging_when_call
        def menu_format__on_upper(event = None):
            # 获取文本（选区文本 / 当前插入位置所在行文本）
            head_position, tail_position = textbox.selection_ranges() or textbox.insertline_ranges()
            text = textbox.get(head_position, tail_position)
            # 获取插入位置
            insert_position = textbox.index("insert")
            # 修改文本
            textbox.replace(head_position, tail_position, text.upper())
            # 恢复选区和插入光标
            textbox.tag_add("sel", head_position, tail_position)
            textbox.mark_set("insert", insert_position)
            # 阻止事件传播
            return "break"

        @logging_when_call
        def menu_format__on_lower(event = None):
            # 获取文本（选区文本 / 当前插入位置所在行文本）
            head_position, tail_position = textbox.selection_ranges() or textbox.insertline_ranges()
            text = textbox.get(head_position, tail_position)
            # 获取插入位置
            insert_position = textbox.index("insert")
            # 修改文本
            textbox.replace(head_position, tail_position, text.lower())
            # 恢复选区和插入光标
            textbox.tag_add("sel", head_position, tail_position)
            textbox.mark_set("insert", insert_position)
            # 阻止事件传播
            return "break"

        @logging_when_call
        def menu_format__on_capitalize(event = None):
            # 获取文本（选区文本 / 当前插入位置所在行文本）
            head_position, tail_position = textbox.selection_ranges() or textbox.insertline_ranges()
            text = textbox.get(head_position, tail_position)
            # 获取插入位置
            insert_position = textbox.index("insert")
            # 修改文本
            textbox.replace(head_position, tail_position, text.capitalize())
            # 恢复选区和插入光标
            textbox.tag_add("sel", head_position, tail_position)
            textbox.mark_set("insert", insert_position)
            # 阻止事件传播
            return "break"

        @logging_when_call
        def int_position(position: str):
            return tuple(map(int, position.split(".")))

        @logging_when_call
        def count_leading_spaces(string: str):
            return sum(1 for _ in itertools.takewhile(str.isspace, string))

        @logging_when_call
        def menu_format__on_indent(event = None):
            # 获取行范围（选区行范围 / 当前插入位置所在行）
            (head_row, head_column), (tail_row, tail_column) = map(int_position, textbox.selection_ranges() or textbox.insertline_ranges())
            # 插入缩进
            for row in range(head_row, tail_row+1):
                text = textbox.get(f"{row}.0", f"{row}.0 lineend")
                space_count = count_leading_spaces(text)
                textbox.insert(f"{row}.0", (4 - space_count % 4) * " ")
            # 阻止事件传播
            return "break"

        @logging_when_call
        def menu_format__on_dedent(event = None):
            # 获取行范围（选区行范围 / 当前插入位置所在行）
            (head_row, head_column), (tail_row, tail_column) = map(int_position, textbox.selection_ranges() or textbox.insertline_ranges())
            # 移除缩进
            for row in range(head_row, tail_row+1):
                text = textbox.get(f"{row}.0", f"{row}.4")
                space_count = count_leading_spaces(text)
                textbox.delete(f"{row}.0", f"{row}.{space_count}")
            # 阻止事件传播
            return "break"

        def menu_wrap__toggle_wrap(wrap: typing.Literal["word", "char", "none"]):
            @logging_when_call
            def toggle(wrap = wrap):
                textbox.configure(wrap=wrap)
                if wrap == "none":
                    if not x_scrollbar.winfo_manager():
                        x_scrollbar.grid_configure(row=1, column=0, sticky="ew")
                else:
                    if x_scrollbar.winfo_manager():
                        x_scrollbar.grid_forget()
            return toggle

        def menu_textbox_color__setattr_callback(attr: str):
            @logging_when_call
            def configure(event = None):
                rgb, hex = tkColorChooser.askcolor(parent=self, initialcolor=textbox.cget(attr))
                if hex:
                    textbox.configure({attr: hex})
            return configure

        def menu_menu_color__setattr_callback(attr: str):
            @logging_when_call
            def configure(event = None):
                rgb, hex = tkColorChooser.askcolor(parent=self, initialcolor=menubar.cget(attr))
                if hex:
                    for menu in menus:
                        menu.configure({attr: hex})
            return configure

        @logging_when_call
        def menu_menu__on_font(event = None):
            if font := tk2.ask_font(self, font_initial=menubar.cget("font")):
                for menu in menus:
                    menu.configure(font=font)
            return "break"

        @logging_when_call
        def menu_textbox__on_font(event = None):
            if font := tk2.ask_font(self, font_initial=textbox.cget("font")):
                textbox.configure(font=font)
            return "break"

        @logging_when_call
        def menu_window__on_topmost(event = None):
            topmost_var.set(not topmost_var.get())
            self.wm_attributes("-topmost", not self.wm_attributes("-topmost"))

        @logging_when_call
        def menu_window__on_fullscreen(event = None):
            fullscreen_var.set(not fullscreen_var.get())
            self.wm_attributes("-fullscreen", not self.wm_attributes("-fullscreen"))

        def menu_transparency__toggle_callback(transparency: float):
            @logging_when_call
            def toggle(transparency = transparency):
                self.wm_attributes("-alpha", transparency)
            return toggle

        super().__init__(master)
        self.wm_title("Text Editor")
        self.wm_geometry("800x600")
        self.wm_withdraw()
        tk2.center_to_screen(self)

        menubar = tk.Menu(self, tearoff=False)
        menu_file = tk.Menu(menubar, tearoff=False)
        menu_edit = tk.Menu(menubar, tearoff=False)
        menu_format = tk.Menu(menubar, tearoff=False)
        menu_view = tk.Menu(menubar, tearoff=False)
        menu_menu = tk.Menu(menu_view, tearoff=False)
        menu_menu_font = tk.Menu(menu_menu, tearoff=False)
        menu_menu_fontfamily = tk.Menu(menu_menu_font, tearoff=False)
        menu_menu_fontsize = tk.Menu(menu_menu_font, tearoff=False)
        menu_menu_color = tk.Menu(menu_menu, tearoff=False)
        menu_textbox = tk.Menu(menu_view, tearoff=False)
        menu_wrap = tk.Menu(menu_textbox, tearoff=False)
        menu_textbox_font = tk.Menu(menu_textbox, tearoff=False)
        menu_textbox_color = tk.Menu(menu_textbox, tearoff=False)
        menu_textbox_fontfamily = tk.Menu(menu_textbox_font, tearoff=False)
        menu_textbox_fontsize = tk.Menu(menu_textbox_font, tearoff=False)
        menu_window = tk.Menu(menu_view, tearoff=False)
        menu_transparency = tk.Menu(menu_window, tearoff=False)
        menus = (
            menubar,
            menu_file,
            menu_edit,
            menu_format,
            menu_view, menu_menu, menu_menu_font, menu_menu_fontfamily, menu_menu_fontsize, menu_menu_color, menu_textbox, menu_wrap, menu_textbox_font, menu_textbox_color, menu_textbox_fontfamily, menu_textbox_fontsize, menu_window, menu_transparency,
        )

        menu_file.add_command(label="Load", command=menu_file__on_load, accelerator="Ctrl+L")
        menu_file.add_command(label="Save", command=menu_file__on_save, accelerator="Ctrl+S")

        menu_edit.add_command(label="Cut", command=menu_edit__on_cut, accelerator="Ctrl+X")
        menu_edit.add_command(label="Copy", command=menu_edit__on_copy, accelerator="Ctrl+C")
        menu_edit.add_command(label="Paste", command=menu_edit__on_paste, accelerator="Ctrl+V")
        menu_edit.add_separator()
        menu_edit.add_command(label="Undo", command=menu_edit__on_undo, accelerator="Ctrl+Z", state="disabled")
        menu_edit.add_command(label="Redo", command=menu_edit__on_redo, accelerator="Ctrl+Y", state="disabled")
        menu_edit.add_separator()
        menu_edit.add_command(label="Find", command=menu_edit__on_find, accelerator="Ctrl+F")
        menu_edit.add_command(label="Replace", command=menu_edit__on_replace, accelerator="Ctrl+R")

        menu_format.add_command(label="Upper", command=menu_format__on_upper, accelerator="Alt+U")
        menu_format.add_command(label="Lower", command=menu_format__on_lower, accelerator="Alt+L")
        menu_format.add_command(label="Capitalize", command=menu_format__on_capitalize, accelerator="Alt+C")
        menu_format.add_separator()
        menu_format.add_command(label="Indent", command=menu_format__on_indent, accelerator="Ctrl+]")
        menu_format.add_command(label="Dedent", command=menu_format__on_dedent, accelerator="Ctrl+[")

        menu_menu.add_command(label="Font", command=menu_menu__on_font)

        menu_menu_color.add_command(label="Background", command=menu_menu_color__setattr_callback("bg"))
        menu_menu_color.add_command(label="Foreground", command=menu_menu_color__setattr_callback("fg"))
        menu_menu_color.add_command(label="Selected", command=menu_menu_color__setattr_callback("selectcolor"))
        menu_menu_color.add_command(label="Activated Background", command=menu_menu_color__setattr_callback("activebackground"))
        menu_menu_color.add_command(label="Activated Foreground", command=menu_menu_color__setattr_callback("activeforeground"))
        menu_menu_color.add_command(label="Disabled Foreground", command=menu_menu_color__setattr_callback("disabledforeground"))

        menu_textbox.add_command(label="Font", command=menu_textbox__on_font)

        self.wrap_var = wrap_var = tk.StringVar(menu_wrap, value="none")
        menu_wrap.add_radiobutton(label="Word", value="word", variable=wrap_var, command=menu_wrap__toggle_wrap("word"))
        menu_wrap.add_radiobutton(label="Char", value="char", variable=wrap_var, command=menu_wrap__toggle_wrap("char"))
        menu_wrap.add_radiobutton(label="None", value="none", variable=wrap_var, command=menu_wrap__toggle_wrap("none"))

        menu_textbox_color.add_command(label="Insert", command=menu_textbox_color__setattr_callback("insertbackground"))
        menu_textbox_color.add_command(label="Background", command=menu_textbox_color__setattr_callback("bg"))
        menu_textbox_color.add_command(label="Foreground", command=menu_textbox_color__setattr_callback("fg"))
        menu_textbox_color.add_command(label="Selected Background", command=menu_textbox_color__setattr_callback("selectbackground"))
        menu_textbox_color.add_command(label="Selected Foreground", command=menu_textbox_color__setattr_callback("selectforeground"))

        self.topmost_var = topmost_var = tk.BooleanVar(menu_window, value=False)
        menu_window.add_checkbutton(label="Topmost", variable=topmost_var, command=menu_window__on_topmost, accelerator="Alt+T")
        self.fullscreen_var = fullscreen_var = tk.BooleanVar(menu_window, value=False)
        menu_window.add_checkbutton(label="Fullscreen", variable=fullscreen_var, command=menu_window__on_fullscreen, accelerator="F11")
        menu_window.add_cascade(label="Transparency", menu=menu_transparency)

        self.transparency_var = transparency_var = tk.DoubleVar(menu_transparency, value=1.0)
        for n in range(1, 11):
            transparency = n / 10
            menu_transparency.add_radiobutton(
                label=transparency,
                command=menu_transparency__toggle_callback(transparency),
                value=transparency,
                variable=transparency_var
            )

        menubar.add_cascade(label="File", menu=menu_file)
        menubar.add_cascade(label="Edit", menu=menu_edit)
        menubar.add_cascade(label="Format", menu=menu_format)
        menubar.add_cascade(label="View", menu=menu_view)
        menu_view.add_cascade(label="Menu", menu=menu_menu)
        menu_view.add_cascade(label="Textbox", menu=menu_textbox)
        menu_view.add_cascade(label="Window", menu=menu_window)
        menu_menu.add_cascade(label="Color", menu=menu_menu_color)
        menu_textbox.add_cascade(label="Wrap", menu=menu_wrap)
        menu_textbox.add_cascade(label="Color", menu=menu_textbox_color)

        self.configure(menu=menubar)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        textframe = tk.Frame(self)
        textframe.grid_rowconfigure(0, weight=1)
        textframe.grid_columnconfigure(0, weight=1)
        textframe.grid_configure(row=0, column=0, sticky="nsew")

        self.textbox = textbox = tk2.Textbox(textframe,
            width=0, height=0,  # 随权重拉伸尺寸
            undo=True, autoseparators=False,  # 支持“撤销”和“重做”
            wrap="none", font=("TkFixedFont", 12),  # 默认样式
            inactiveselectbackground="gray",
        )
        x_scrollbar = tk.Scrollbar(textframe, orient="horizontal", command=textbox.xview)
        y_scrollbar = tk.Scrollbar(textframe, orient="vertical", command=textbox.yview)
        textbox.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

        textbox.grid_configure(row=0, column=0, sticky="nsew")
        x_scrollbar.grid_configure(row=1, column=0, sticky="ew")
        y_scrollbar.grid_configure(row=0, column=1, sticky="ns")

        statusbar = tk.Frame(self)
        statusbar.grid_rowconfigure(0, weight=1)
        statusbar.grid_columnconfigure(4, weight=1)
        statusbar.grid_configure(row=1, column=0, sticky="ew")

        position_var = tk.StringVar(statusbar)
        selection_length_var = tk.IntVar(statusbar)

        position_title = tk.Label(statusbar, text="Position :")
        position_value = tk.Label(statusbar, textvariable=position_var)
        selection_length_title = tk.Label(statusbar, text="Selected :")
        selection_length_value = tk.Label(statusbar, textvariable=selection_length_var)

        position_title.grid_configure(row=0, column=0)
        position_value.grid_configure(row=0, column=1, padx=(0, 8))
        selection_length_title.grid_configure(row=0, column=2)
        selection_length_value.grid_configure(row=0, column=3)

        @logging_when_call
        def refresh_position():
            row, column = map(int, textbox.index("insert").split("."))
            position_var.set(f"{row}, {column+1}")

        @logging_when_call
        def refresh_selection_length():

            checkbutton_inselection = findreplace_dialog.checkbutton_inselection

            if position_selection := textbox.tag_ranges("sel"):

                position_head, position_tail = position_selection
                selection = textbox.get(position_head, position_tail)
                length = len(selection)

                selection_length_var.set(length)
                checkbutton_inselection.configure(state=tk.NORMAL)

            else:
                selection_length_var.set(0)
                checkbutton_inselection.configure(state=tk.DISABLED)

        @logging_when_call
        def textbox__when_focusin(event):
            textbox.after(0, refresh_position)

        @logging_when_call
        def textbox__when_focusout(event):
            textbox.after(0, refresh_position)

        @logging_when_call
        def textbox__when_modified(event):
            textbox.after(0, refresh_position)
            textbox.after(500, textbox.edit_separator)
            # 启用 Undo 菜单（若 Undo 已禁用 且 Undo 栈未空）
            if str(menu_edit.entrycget("Undo", "state")) == "disabled" and textbox.edit("canundo"):
                menu_edit.entryconfigure("Undo", state="normal")
                print("Enable 'Undo' entry.")
            textbox.edit_modified(False)

        @logging_when_call
        def textbox__when_keypress_up(event):
            textbox.after(0, refresh_position)

        @logging_when_call
        def textbox__when_keypress_down(event):
            textbox.after(0, refresh_position)

        @logging_when_call
        def textbox__when_keypress_left(event):
            textbox.after(0, refresh_position)

        @logging_when_call
        def textbox__when_keypress_right(event):
            textbox.after(0, refresh_position)

        @logging_when_call
        def textbox__when_keypress_backspace(event):
            # 部分修复 BUG#1（临时方案）
            # 步骤：
            #   1. 按下[Shift]和[→]选中最后一个换行符
            #   2. 按下[BackSpace]删除当前选区
            # 预期：选区字符数统计停留在 0 。
            # 实际：选区字符数统计停留在 1 。
            # 排除：
            #   · <<Selection>> 事件：尝试后无法修复。
            textbox.after(0, refresh_selection_length)

        @logging_when_call
        def textbox__when_buttonpress_left(event):
            textbox.after(0, refresh_position)

        @logging_when_call
        def textbox__when_buttonrelease_left(event):
            textbox.after(0, refresh_selection_length)

        @logging_when_call
        def textbox__when_buttondrag_left(event):
            textbox.after(0, refresh_selection_length)

        def textbox__when_keypress_home(event):
            textbox.mark_set("insert", "insert linestart")
            textbox.see("insert")

        def textbox__when_keypress_end(event):
            textbox.mark_set("insert", "insert lineend")
            textbox.see("insert")

        textbox.bind("<FocusIn>", textbox__when_focusin)
        textbox.bind("<FocusOut>", textbox__when_focusout)
        textbox.bind("<<Modified>>", textbox__when_modified)
        textbox.bind("<KeyPress-Up>", textbox__when_keypress_up)
        textbox.bind("<KeyPress-Down>", textbox__when_keypress_down)
        textbox.bind("<KeyPress-Left>", textbox__when_keypress_left)
        textbox.bind("<KeyPress-Right>", textbox__when_keypress_right)
        textbox.bind("<KeyPress-BackSpace>", textbox__when_keypress_backspace)
        textbox.bind("<KeyPress-Home>", textbox__when_keypress_home)
        textbox.bind("<KeyPress-End>", textbox__when_keypress_end)
        textbox.bind("<ButtonPress-1>", textbox__when_buttonpress_left)
        textbox.bind("<ButtonRelease-1>", textbox__when_buttonrelease_left)
        textbox.bind("<B1-Motion>", textbox__when_buttondrag_left)
        textbox.bind("<Control-l>", menu_file__on_load)
        textbox.bind("<Control-s>", menu_file__on_save)
        textbox.bind("<Control-x>", menu_edit__on_cut)
        textbox.bind("<Control-c>", menu_edit__on_copy)
        textbox.bind("<Control-v>", menu_edit__on_paste)
        textbox.bind("<Control-z>", menu_edit__on_undo)
        textbox.bind("<Control-y>", menu_edit__on_redo)
        textbox.bind("<Control-f>", menu_edit__on_find)
        textbox.bind("<Control-r>", menu_edit__on_replace)
        textbox.bind("<Alt-u>", menu_format__on_upper)
        textbox.bind("<Alt-l>", menu_format__on_lower)
        textbox.bind("<Control-]>", menu_format__on_indent)
        textbox.bind("<Control-[>", menu_format__on_dedent)
        textbox.bind("<Alt-c>", menu_format__on_capitalize)

        findreplace_dialog = FindreplaceDialog(self, textbox=textbox)

        self.bind("<KeyPress-F11>", menu_window__on_fullscreen)
        self.bind("<Alt-t>", menu_window__on_topmost)
        self.wm_deiconify()

        textbox.focus_set()

    def load(self, path_file: str):
        textbox = self.textbox
        textbox.delete("1.0", "end")
        try:
            with open(path_file, "r", encoding="UTF-8") as file_handle:
                while (data := file_handle.read(1024)):
                    textbox.append(data)
        except Exception as error:
            tkMessagebox.showinfo("Text Editor: Load failed", error)
        return self

root = tk.Tk()
root.wm_withdraw()

editor = TextEditor(root)

if len(sys.argv) == 2:
    arg_1 = sys.argv[1]
    if os.path.exists(arg_1) and os.path.isfile(arg_1):
        editor.load(arg_1)

root.wait_window(editor)