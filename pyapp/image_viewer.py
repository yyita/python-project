# todo
import tkinter
import sys
import os
from PIL import Image, ImageTk
import typing

if len(sys.argv) != 2:
    exit(1)

arg_1 = sys.argv[1]
if not os.path.exists(arg_1):
    exit(1)

def size_auto(size_1: typing.Sequence[int], size_2: typing.Sequence[int]) -> tuple[int, int]:
    scale = min(size_2[0] / size_1[0], size_2[1] / size_1[1])
    return (int(size_1[0] * scale), int(size_1[1] * scale))

def resize(width: int, height: int):
    global id_task_resize
    image_pillow_autosize = image_pillow_original.resize(size_auto(size_image_pillow_original, (width, height)))
    image_tk = ImageTk.PhotoImage(image_pillow_autosize)
    image.image = image_tk
    image.configure(image=image_tk)
    id_task_resize = None

width_window = 640
height_window = 480
interval_resize = 50

image_pillow_original = Image.open(arg_1)
size_image_pillow_original = (image_pillow_original.width, image_pillow_original.height)

root = tkinter.Tk()
root.wm_geometry(f"{width_window}x{height_window}")
root.wm_title("Image Viewer")

id_task_resize = None
image__is_enter = False

def image__when_enter(event: tkinter.Event):
    global image__is_enter
    image__is_enter = True

def image__when_leave(event: tkinter.Event):
    global image__is_enter
    image__is_enter = False

image = tkinter.Label(root)
image.pack_configure(fill="both", expand=True)
image.bind("<Enter>", image__when_enter)
image.bind("<Leave>", image__when_leave)

def root__when_configure(event: tkinter.Event):
    global id_task_resize
    if id_task_resize is not None:
        root.after_cancel(id_task_resize)
    id_task_resize = root.after(interval_resize, resize, event.width, event.height)

def root__when_mousewheel(event: tkinter.Event):
    if not image__is_enter:
        return
    mouse_x = event.x
    mouse_y = event.y
    

root.bind("<Configure>", root__when_configure)
root.bind("<MouseWheel>", root__when_mousewheel)

resize(width_window, height_window)

root.mainloop()