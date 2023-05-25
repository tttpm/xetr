import readchar
import readchar.key as rk

from config import get_config
keys = {v: k for k, v in get_config()["keys"].items()}

SPECIAL_KEYS = {
    
    rk.BACKSPACE: "backspace",
    rk.UP: "arrow_up",
    rk.DOWN: "arrow_down",
    rk.LEFT: "arrow_left",
    rk.RIGHT: "arrow_right",
    rk.F1: "f1",
    rk.F2: "f2",
    rk.F3: "f3",
    rk.F4: "f4",
    rk.F5: "f5",
    rk.F6: "f6",
    rk.F7: "f7",
    rk.F8: "f8",
    rk.F9: "f9",
    rk.F10: "f10",
    rk.F11: "f11",
    rk.F12:  "f12",
    rk.INSERT: "insert",
    rk.DELETE: "delete",
    rk.HOME: "home",
    rk.END: "end",
    rk.PAGE_UP: "pgup",
    rk.PAGE_DOWN: "pgdn",
    rk.ENTER: "enter",
    " ": "space",
}
    


def read_key():
    a = readchar.readkey()
    if a in SPECIAL_KEYS:
        a = SPECIAL_KEYS[a]
    return str(a)


def wait_for(key: str):
    while read_key() != key:
        pass


def get_command():

    pressed = read_key()
    while pressed not in keys:
        pressed = read_key()

    return keys[pressed]


def wait_for_command(command: str):
    while get_command() != command:
        pass
