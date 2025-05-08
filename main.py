import ctypes
import time

# 定义 Windows API 所需结构和常量
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ('wVk', ctypes.c_ushort),
        ('wScan', ctypes.c_ushort),
        ('dwFlags', ctypes.c_ulong),
        ('time', ctypes.c_ulong),
        ('dwExtraInfo', PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [('uMsg', ctypes.c_ulong),
                ('wParamL', ctypes.c_short),
                ('wParamH', ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [('dx', ctypes.c_long),
                ('dy', ctypes.c_long),
                ('mouseData', ctypes.c_ulong),
                ('dwFlags', ctypes.c_ulong),
                ('time', ctypes.c_ulong),
                ('dwExtraInfo', PUL)]

class Input_I(ctypes.Union):
    _fields_ = [('ki', KeyBdInput),
                ('mi', MouseInput),
                ('hi', HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [('type', ctypes.c_ulong),
                ('ii', Input_I)]

# 常量
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002
INPUT_KEYBOARD = 1
VK_RETURN = 0x0D

def send_unicode_char(char):
    ucode = ord(char)
    ki = KeyBdInput(0, ucode, KEYEVENTF_UNICODE, 0, None)
    x = Input(INPUT_KEYBOARD, Input_I(ki))
    ctypes.windll.user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

    # Key up
    ki2 = KeyBdInput(0, ucode, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, None)
    x2 = Input(INPUT_KEYBOARD, Input_I(ki2))
    ctypes.windll.user32.SendInput(1, ctypes.byref(x2), ctypes.sizeof(x2))

def send_enter_key():
    ki_down = KeyBdInput(VK_RETURN, 0, 0, 0, None)
    ki_up = KeyBdInput(VK_RETURN, 0, KEYEVENTF_KEYUP, 0, None)
    x_down = Input(INPUT_KEYBOARD, Input_I(ki_down))
    x_up = Input(INPUT_KEYBOARD, Input_I(ki_up))
    ctypes.windll.user32.SendInput(1, ctypes.byref(x_down), ctypes.sizeof(x_down))
    ctypes.windll.user32.SendInput(1, ctypes.byref(x_up), ctypes.sizeof(x_up))


def type_text_unicode(text, delay=0.05):
    print("请在5秒内将焦点切换到目标输入框...")
    time.sleep(5)
    for char in text:
        if char == '\n':
            send_enter_key()
        else:
            send_unicode_char(char)
        time.sleep(delay)

if __name__ == "__main__":
    with open('text.txt', 'r', encoding='utf-8') as file:
        text_to_type = file.read()
    type_text_unicode(text_to_type, delay=0.01)
