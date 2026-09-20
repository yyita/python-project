from keyboard import add_hotkey, wait
from pyautogui import move as move_cursor

remove_hotkey_up = add_hotkey('up', move_cursor, (0, -1), suppress=True, trigger_on_release=True)
remove_hotkey_down = add_hotkey('down', move_cursor, (0, 1), suppress=True, trigger_on_release=True)
remove_hotkey_left = add_hotkey('left', move_cursor, (-1, 0), suppress=True, trigger_on_release=True)
remove_hotkey_right = add_hotkey('right', move_cursor, (1, 0), suppress=True, trigger_on_release=True)

print("| Move: ↑↓←→ | Exit: Esc |", flush=True)

try:
    wait("esc")
finally:
    remove_hotkey_up()
    remove_hotkey_down()
    remove_hotkey_left()
    remove_hotkey_right()