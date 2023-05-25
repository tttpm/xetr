import config as cfg
import kb

import sys
import time

VERSION = "0.1"

def clear():
    import os, sys
    os.system('cls' if sys.platform == 'win32' else 'clear')

def logo():
    w, b = '\033[38;2;255;255;255m\033[48;2;255;255;255m##', '\033[38;2;0;0;0m\033[48;2;0;0;0m##'
    x = '\033[38;2;0;0;0m\033[48;2;255;255;255mX '
    e = '\033[38;2;0;0;0m\033[48;2;255;255;255mE '
    return (

        w + w + w + w + w + w + w + w + w + '\n' +
        w + b + b + b + w + b + b + b + w + '\n' +
        w + w + b + w + w + b + w + b + w + '\n' +
        w + w + b + w + w + b + b + w + w + '\n' +
        w + w + b + w + w + b + w + b + w + '\n' +
        w + w + b + w + w + b + w + b + w + '\n' +
        w + w + w + w + w + w + w + w + w + '\n' +
        w + w + w + w + x + e + w + w + w + '\n' +
        w + w + w + w + w + w + w + w + w + '\n' +

        '\033[0m')
        
def greeting():
    y = "\033[38;2;255;255;0m"
    o = "\033[38;2;255;102;0m"
    c = "\033[0m"
    return (logo() +
            y + "eXtremely new console skin Editor for Team Run " +
            c + f"v{VERSION} by " +
            o + "Tipim" +
            c)

    
SUNCAT = 'trSkin17ZZBCoAwDAS/VFCk4qmt5v9P8iBIsTVuYqwIelq0ZidhJTq3XZODBdFRiF43r8NbLF0InnKhMLWqA1rMQ1pSzMWZaVUo6hiiMqaMENVRwEu9rERL5jIJusM/8yeYd5F8H8aYi+eYy0ci5hIVgWcImTNlZRy+Ol6kC4YQuXPJjGxPEBVJCzJwxXjV2RCFpEE29k/YnJBZJVbZQPayuVBkg+mrpbj/U0r0gmgAf7NBxH0F'
CSETR_DUDE = 'trSkin1MzCAAGuDUcYAMRwNQNDNDcFwgwJ6MIaQU8lz/Ah0s6OriamlCzKDQsWjbh518wC6ebTcINLNZi5GTmZGQMVwBmYM0pMx6uZRN1Pi5kHieOo3+Sizi55OHSRuBgA='
CSETR_DUDE_WITH_BACKGROUND = 'trSkin1S0tLSU1MSUuzThtlDBAj0QAEkRlpUEAfxhByKjmOH4FuTkw1MbVMQWZQrHjUzaNuThnNg4PczWYpRklmRsgMzBikJ2PUzaNupsTNg8Tx1G/yUWYXPZ06SNwMAA=='


USED_LIBS = {'colorama': 'colorama',
             'readchar': 'readchar',
             'PIL':'Pillow',
             'requests': 'requests'}
            
k = cfg.get_config()['keys']
SIDE_TEXTS = [
    f'''
 0  | cursor movement:
 1  |     up - [{k["crs_move_up"]}]
 2  |     down - [{k["crs_move_down"]}]
 3  |     right - [{k["crs_move_right"]}]
 4  |     left - [{k["crs_move_left"]}]
 5  |
 6  | drawing:
 7  |     paint one pixel - [{k["crs_click_brush"]}]
 8  |     erase one pixel - [{k["crs_click_eraser"]}]
 9  |     fill an area - [{k["crs_click_fill"]}] 
 A  |     change color - [{k["crs_color_change"]}]
 B  |
 C  | misc:
 D  |     import skin - [{k["canv_skin_import"]}]
 E  |     export skin - [{k["canv_skin_export"]}]
 F  |     undo - [{k["canv_undo"]}]
 G  |     redo - [{k["canv_redo"]}]
 H  |     settings - [{k["back_or_settings"]}]
        
lmao this line won't be displayed
and this
this too
and this as well
:D
    '''
]   
     
DIGITS1 = "   0 1 2 3 4 5 6 7 8 9 A B C D E F G H I J\n"
DIGITS2 = "0123456789ABCDEFGHIJ"



def ask(question="", no="n", yes="Y"):
    while True:
        answer = input(question)
        if answer != no and answer != yes:
            print(f"it's not {yes} nor {no}, try again!")
            continue
        return answer == yes
    
def settings():
    print("\nyou've entered the settings menu!!!!")
    new_conf = {"keys":{}}
    print("\nfirst of all, do u wanna adjust keys?")
    
    if ask("(Y/n) >> "):
        print("\nokay! i recommend you use english letters [a]-[z], [A]-[Z] (case counts!), digits [0]-[9], arrow keys, [enter], [space]")
        print("but you can choose other languages' letters and funny keys like [insert] as well")
        print("\nso, let's begin!")
        while True:
            used_keys = set()
            for command in cfg.DEFAULT_SETTINGS["keys"]:
                why = True
                while why:
                    print(f"new key for '{command}': ", end='')
                    sys.stdout.flush()
                    
                    new_key = kb.read_key()
                    
                    if new_key in used_keys:
                        print(f"hey, you've choosed [{new_key}] before for other command!")
                        continue
                    
                    used_keys.add(new_key)
                    new_conf["keys"][command] = new_key
                    print(f"[{new_key}]")
                    
                    why = False
                    time.sleep(0.1)
                    
                
            if ask("done?\n(Y/n) >> "):
                break
    print("\nalright, let's proceed")      
    new_conf["check_version"] = ask("check version on launch?\n(Y/n) >> ")
    print("roger that.")
    if ask("\nlastly, do you want to change the skin on background?\n(Y/n) >> "):
        new_conf["background_skin"] = input("and new background skin is?\n>> ")
    print("\nthank you for using XETR!")
    return new_conf
        
    





