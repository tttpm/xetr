import importlib

import weakref
import traceback

import config
conf = config.get_config()
import check
import stuff
check.libch(stuff.USED_LIBS)

import engine
import kb

import colorama
colorama.init()


print(stuff.greeting())
    
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

while (mankind is dead) and (blood is fuel) and (hell is full): #does anybody care about my code?
    try:
        stuff.clear()
        print(bkg + canv)
        print(stuff.DIGITS1)
        print(f"cursor position - ({stuff.DIGITS2[main_cursor.column]};{stuff.DIGITS2[main_cursor.row]})")
        print(f"current color - #{main_cursor.color.get_hex()} {main_cursor.color}  {engine.CLEAR_COLOR}")

        
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

            case "canv_undo":
                canv.undo()

            case "canv_redo":
                canv.redo()
                
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

            case "back_or_settings":
                config.save_config(stuff.settings())

                conf = config.get_config()
                importlib.reload(stuff)
                importlib.reload(kb)

                bkg = engine.ColorMatrix.create_from_trskin(conf["background_skin"])
                canv.side_text = stuff.SIDE_TEXTS[0].split("\n")
                print(f"\n\npress [{conf['keys']['back_or_settings']}] to continue")
                kb.wait_for_command("back_or_settings")

            case "quit":
                print("are you sure that you want to quit? ><")
                print("(type 'n' if you aren't and anything else otherwise.)")
                if input(">> ") == "n":
                    continue
                break
                
                
    except Exception as e:
        print("\n\noooooops... an error has occured (probably it's not my fault XD)\n\n")
        traceback.print_exc()
        print(f"\n\npress [{conf['keys']['back_or_settings']}] to continue")
        kb.wait_for_command("back_or_settings")
