import config as cfg

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
        

SUNCAT = 'trSkin17ZZBCoAwDAS/VFCk4qmt5v9P8iBIsTVuYqwIelq0ZidhJTq3XZODBdFRiF43r8NbLF0InnKhMLWqA1rMQ1pSzMWZaVUo6hiiMqaMENVRwEu9rERL5jIJusM/8yeYd5F8H8aYi+eYy0ci5hIVgWcImTNlZRy+Ol6kC4YQuXPJjGxPEBVJCzJwxXjV2RCFpEE29k/YnJBZJVbZQPayuVBkg+mrpbj/U0r0gmgAf7NBxH0F'
CSETR_DUDE = 'trSkin1MzCAAGuDUcYAMRwNQNDNDcFwgwJ6MIaQU8lz/Ah0s6OriamlCzKDQsWjbh518wC6ebTcINLNZi5GTmZGQMVwBmYM0pMx6uZRN1Pi5kHieOo3+Sizi55OHSRuBgA='



USED_LIBS = {'colorama': 'colorama',
             'readchar': 'readchar',
             'PIL':'Pillow',
             'requests': 'requests'}

k = cfg.get_config()['keys']
SIDE_TEXTS = [
    f'''
    cursor movement:
        up - [{k["crs_move_up"]}]
        down - [{k["crs_move_down"]}]
        right - [{k["crs_move_right"]}]
        left - [{k["crs_move_left"]}]
        
    drawing:
        paint one pixel - [{k["crs_click_brush"]}]
        erase one pixel - [{k["crs_click_eraser"]}]
        fill an area - [{k["crs_click_fill"]}] 
        change color - [{k["crs_color_change"]}]

    misc:
        import skin - [{k["canv_skin_import"]}]
        export skin - [{k["canv_skin_export"]}]
    16
    17
    18
    lmao this line won't be displayed
    and this
    this too
    and this as well
    :D
    '''
]
   











