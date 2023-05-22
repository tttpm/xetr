import weakref
import traceback

import config
conf = config.get_config()
import stuff
import check
check.libch(stuff.USED_LIBS)

import engine
import kb

import colorama
colorama.init()



print(stuff.logo())


print(f"eXtremely new console skin Editor for Team Run v{stuff.VERSION} by {engine.Color(255,102,0).get_ansi()}Tipim{engine.CLEAR_COLOR}")

if conf["check_version"]:
    check.verch(stuff.VERSION)

print("press any key to continue...")
kb.read_key()


H = engine.LOOPER_HEIGHT
W = engine.LOOPER_WIDTH

bkg = engine.ColorMatrix.create_from_trskin(conf["background_skin"])
main_cursor = engine.Cursor(H//2, W//2, H, W, engine.Color(0,0,0))                      
canv = engine.ColorMatrix(W, H, engine.Color(0,0,0,0), weakref.ref(main_cursor)(), stuff.SIDE_TEXTS[0])

mankind = dead = blood = fuel = hell = full = [69]
print(1)
while (mankind is dead) and (blood is fuel) and (hell is full): #does anybody care about my code?
    try:
        stuff.clear()
        print(bkg + canv)
        print(main_cursor.row, main_cursor.column)
        
        action = kb.get_command()
        
        match action:
      
            case "crs_move_up":
                main_cursor.up()

            case "crs_move_down":
                main_cursor.down()

            case "crs_move_right":
                main_cursor.right()

            case "crs_move_left":
                main_cursor.left()

            case "crs_click_brush":
                canv.paint()

            case "crs_click_eraser":
                canv.paint(new_color=engine.Color(0,0,0,0))

            case "crs_click_fill":
                canv.fill()

            case "crs_color_change":
                main_cursor.color = engine.Color.create_from_hex(input("Type the new color's HEX\n>> "))

            case "canv_skin_export":
                print(f"here your skin is:\n{canv.get_trskin()}")
                print("type 'img' to save it as PNG file, anything else otherwise")
                
                if input(">> ").lower() == "img":
                    canv.get_img(input("type the path to the image\n>> "))
                    
            case "canv_skin_import":
                q = input("and new skin is? (type 'img' if you wanna load skin from PNG image, the skin itself otherwise)\n>> ")
                if q.lower() == "img":
                    canv = engine.ColorMatrix.create_from_img(input("type the path to the image\n>> "), weakref.ref(main_cursor)(), stuff.SIDE_TEXTS[0])
                else:
                    canv = engine.ColorMatrix.create_from_trskin(q, weakref.ref(main_cursor)(), stuff.SIDE_TEXTS[0])

    except Exception as e:
        print("\n\noooooops... an error has occured (probably it's not my fault XD)\n\n")
        traceback.print_exc()
        print(f"\n\npress [{conf['keys']['back']}] to continue")
        kb.wait_for_command("back")
input()
