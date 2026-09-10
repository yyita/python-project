# todo
import tkinter
from PIL import ImageGrab, ImageTk
原始屏幕快照PIL = ImageGrab.grab()
root = tkinter.Tk()
root.withdraw()
原始屏幕快照Tk = ImageTk.PhotoImage(原始屏幕快照PIL)
label = tkinter.Label(root, image=原始屏幕快照Tk)
label.image = 原始屏幕快照Tk
label.pack(fill="both", expand=True)
def when_escape_keypress(event: tkinter.Event):
    root.destroy()
root.bind("<KeyPress-Escape>", when_escape_keypress)
root.attributes("-fullscreen", True)
root.deiconify()
root.mainloop()