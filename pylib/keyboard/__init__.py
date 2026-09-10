class KeyName:
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    e = "e"
    f = "f"
    g = "g"
    h = "h"
    i = "i"
    j = "j"
    k = "k"
    l = "l"
    m = "m"
    n = "n"
    o = "o"
    p = "p"
    q = "q"
    r = "r"
    s = "s"
    t = "t"
    u = "u"
    v = "v"
    w = "w"
    x = "x"
    y = "y"
    z = "z"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    K0 = "0"
    K1 = "1"
    K2 = "2"
    K3 = "3"
    K4 = "4"
    K5 = "5"
    K6 = "6"
    K7 = "7"
    K8 = "8"
    K9 = "9"
    PARENTHESE_RIGHT=PARENTHESE_CLOSE = ")"
    EXCLAMATION_MARK=BANG = "!"
    AT_SIGN = "@"
    HASH_SIGN = "#"
    DOLLAR_SIGN = "$"
    PERCENT_SIGN=MOD = "%"
    CARET=CIRCUMFLEX = "^"
    AMPERSAND=AND = "&"
    ASTERISK=MULTIPLY = "*"
    PARENTHESE_LEFT=PARENTHESE_OPEN = "("
    BACKQUOTE=GRAVE_ACCENT = "`"
    TILDE = "~"
    MINUS=HYPHEN = "-"
    UNDERSCORE=UNDERLINE = "_"
    EQUALS = "="
    PLUS = "+"
    BRACKET_LEFT=BRACKET_OPEN = "["
    BRACE_LEFT=BRACE_OPEN = "{"
    BRACKET_RIGHT=BRACKET_CLOSE = "]"
    BRACE_RIGHT=BRACE_CLOSE = "}"
    BACKSLASH = "\\"
    PIPE = "|"
    SEMICOLON = ";"
    COLON = ":"
    APOSTROPHE=SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'
    COMMA =","
    LESS=ANGLE_BRACKET_LEFT=ANGLE_BRACKET_OPEN = "<"
    DOT=PERIOD=POINT = "."
    GREATER=ANGLE_BRACKET_RIGHT=ANGLE_BRACKET_CLOSE = ">"
    DIVIDE=SLASH = "/"
    QUESTION_MARK = "?"
    TAB = "tab"
    SHIFT_LEFT = "shift"
    SHIFT_RIGHT = "right shift"
    CTRL_LEFT = "ctrl"
    CTRL_RIGHT = "right ctrl"
    ALT_LEFT = "alt"
    ALT_RIGHT = "right alt"
    SPACE = "space"
    ENTER = "enter"
    BACKSPACE = "backspace"
    WINDOWS_LEFT = "left windows"
    WINDOWS_RIGHT = "right windows"
    MENU = "menu"
    ESCAPE = "esc"
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"
    F10 = "f10"
    F11 = "f11"
    F12 = "f12"
    INSERT = "insert"
    DELETE = "delete"
    HOME = "home"
    END = "end"
    PAGE_UP = "page up"
    PAGE_DOWN = "page down"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    CAPSLOCK = "caps lock"
    NUMLOCK = "num lock"
    SCROLL_LOCK = "scroll lock"
    PRINT_SCREEN = "print screen"
    PAUSE_BREAK = "pause"
    SEARCH = "browser search key"
    PREVIOUS_TRACK = "previous track"
    PLAY_PAUSE_MEDIA = "play/pause media"
    NEXT_TRACK = "next track"
    VOLUME_MUTE = "volume mute"
    VOLUME_UP = "volume up"
    VOLUME_DOWN = "volume down"

class ScanCode:
    # 主键盘区 (Main Keyboard)
    KEY_A = 30
    KEY_B = 48
    KEY_C = 46
    KEY_D = 32
    KEY_E = 18
    KEY_F = 33
    KEY_G = 34
    KEY_H = 35
    KEY_I = 23
    KEY_J = 36
    KEY_K = 37
    KEY_L = 38
    KEY_M = 50
    KEY_N = 49
    KEY_O = 24
    KEY_P = 25
    KEY_Q = 16
    KEY_R = 19
    KEY_S = 31
    KEY_T = 20
    KEY_U = 22
    KEY_V = 47
    KEY_W = 17
    KEY_X = 45
    KEY_Y = 21
    KEY_Z = 44
    #0 #)
    KEY_0 = KEY_PARENTHESE_RIGHT=KEY_PARENTHESE_CLOSE = 11
    #1 #!
    KEY_1 = KEY_EXCLAMATION_MARK=KEY_BANG = 2
    #2 #@
    KEY_2 = KEY_AT_SIGN = 3
    #3 ##
    KEY_3 = KEY_HASH_SIGN = 4
    #4 #$
    KEY_4 = KEY_DOLLAR_SIGN = 5
    #5 #%
    KEY_5 = KEY_PERCENT_SIGN=KEY_MOD = 6
    #6 #^
    KEY_6 = KEY_CARET=KEY_CIRCUMFLEX = 7
    #7 #&
    KEY_7 = KEY_AMPERSAND=KEY_AND = 8
    #8 #*
    KEY_8 = KEY_ASTERISK=KEY_MULTIPLY = 9
    #9 #(
    KEY_9 = KEY_LEFT_PARENTHESE=KEY_OPEN_PARENTHESE = 10
    #` #~
    KEY_BACKQUOTE=KEY_GRAVE_ACCENT = KEY_TILDE = 41
    #- #_
    KEY_MINUS=KEY_HYPHEN = KEY_UNDERSCORE=KEY_UNDERLINE = 12
    #= #+
    KEY_EQUALS = KEY_PLUS = 13
    #[ #{
    KEY_BRACKET_LEFT=KEY_BRACKET_OPEN = KEY_BRACE_LEFT=KEY_BRACE_OPEN = 26
    #] #}
    KEY_BRACKET_RIGHT=KEY_BRACKET_CLOSE = KEY_BRACE_RIGHT=KEY_BRACE_CLOSE = 27
    #\ #|
    KEY_BACKSLASH = KEY_PIPE = 43
    #; #:
    KEY_SEMICOLON = KEY_COLON = 39
    #' #"
    KEY_APOSTROPHE=KEY_SINGLE_QUOTE = KEY_DOUBLE_QUOTE = 40
    #, #<
    KEY_COMMA = KEY_LESS=KEY_ANGLE_BRACKET_LEFT=KEY_ANGLE_BRACKET_OPEN = 51
    #. #>
    KEY_DOT=KEY_PERIOD=KEY_POINT = KEY_GREATER=KEY_ANGLE_BRACKET_RIGHT=KEY_ANGLE_BRACKET_CLOSE = 52
    #/ #?
    KEY_SLASH=KEY_DIVIDE = KEY_QUESTION_MARK = 53
    KEY_TAB = 15
    KEY_CAPSLOCK = 58      # 大写锁定
    KEY_LEFT_SHIFT = 42    # 上档
    KEY_RIGHT_SHIFT = 54   # 上档
    KEY_CONTROL = 29       # 控制
    KEY_ALT = 56           # 换档
    KEY_SPACE = 57         # 空格
    KEY_ENTER = 28         # 回车
    KEY_BACKSPACE = 14     # 回格
    KEY_WINDOWS = 91       # Windows
    KEY_MENU = 93          # 菜单

    # 功能键区 (Function Keys)
    KEY_ESCAPE = 1  # 退出
    KEY_F1 = 59
    KEY_F2 = 60
    KEY_F3 = 61
    KEY_F4 = 62
    KEY_F5 = 63
    KEY_F6 = 64
    KEY_F7 = 65
    KEY_F8 = 66
    KEY_F9 = 67
    KEY_F10 = 68
    KEY_F11 = 87
    KEY_F12 = 88

    # 编辑键区 (Editing Keys)
    KEY_INSERT = 82        # 插入
    KEY_DELETE = 83        # 删除
    KEY_HOME = 71          # 起始
    KEY_END = 79           # 结束
    KEY_PAGE_UP = 73       # 上页
    KEY_PAGE_DOWN = 81     # 下页

    # 方向键区 (Arrow Keys)
    KEY_UP = 72
    KEY_DOWN = 80
    KEY_LEFT = 75
    KEY_RIGHT = 77

    # 小键盘区 (Keypad)
    NUMLOCK = 69       # 数码锁定
    KEYPAD_0 = 82
    KEYPAD_1 = 79
    KEYPAD_2 = 80
    KEYPAD_3 = 81
    KEYPAD_4 = 75
    KEYPAD_5 = 76
    KEYPAD_6 = 77
    KEYPAD_7 = 71
    KEYPAD_8 = 72
    KEYPAD_9 = 73
    #+
    KEYPAD_PLUS = 78
    #-
    KEYPAD_MINUS=KEYPAD_HYPHEN = 74
    #*
    KEYPAD_MULTIPLY=KEYPAD_ASTERISK = 55
    #/
    KEYPAD_DIVIDE=KEYPAD_SLASH = 53
    #.
    KEYPAD_DOT=KEYPAD_PERIOD=KEYPAD_POINT = 83

    # 其他特殊键
    KEY_PRINT_SCREEN = 55        # 打印屏幕
    KEY_SCROLL_LOCK = 70         # 滚动锁定
    KEY_PAUSE_BREAK = 69         # 暂停中断
    KEY_SEARCH = -170            # 搜索
    KEY_PREVIOUS_TRACK = -177    # 上一首
    KEY_PLAY_PAUSE_MEDIA = -179  # 播放/暂停
    KEY_NEXT_TRACK = -176        # 下一首
    KEY_VOLUME_MUTE = -173       # 静音
    KEY_VOLUME_UP = -174         # 放大音量
    KEY_VOLUME_DOWN = -175       # 缩小音量