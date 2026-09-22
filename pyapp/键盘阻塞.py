import keyboard

unhook = keyboard.hook(lambda event: None, suppress=True)

print("Keyboard input has been blocked.")

try:
    keyboard.wait()
finally:
    unhook()