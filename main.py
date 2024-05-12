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
    print("checking version...")
    check.verch(stuff.VERSION)

print("press any key to continue...")
kb.read_key()


H = engine.LOOPER_HEIGHT
W = engine.LOOPER_WIDTH

bkg = engine.ColorMatrix.create_from_trskin(conf["background_skin"])
main_cursor = engine.Cursor(H//2, W//2, H, W, engine.Color(0,0,0))                      
canv = engine.ColorMatrix(W, H, engine.Color(0,0,0,0), weakref.ref(main_cursor)())

hide_background = False
show_cursor_position = False

while True:
    try:
        stuff.clear()
        if show_cursor_position:
            cross_overlay = stuff.cross(canv.width, canv.height, main_cursor.row, main_cursor.column, st=stuff.SIDE_TEXTS[0])
        else:
            cross_overlay = engine.ColorMatrix(canv.width, canv.height, engine.Color(0, 0, 0, 0.0), side_text=stuff.SIDE_TEXTS[0])
        print(bkg + canv + cross_overlay)
        print(stuff.DIGITS1)
        print(f"current color - #{main_cursor.color.get_hex()} {engine.Color(255, 255, 255) + main_cursor.color} {engine.Color(191, 191, 191) + main_cursor.color} {engine.CLEAR_COLOR}")
        print(f"selected pixel - ({stuff.DIGITS2[main_cursor.column % 26]};{stuff.DIGITS2[main_cursor.row % 26]}) #{canv[main_cursor.row][main_cursor.column].get_hex()} {engine.Color(255, 255, 255) + canv[main_cursor.row][main_cursor.column]} {engine.Color(191, 191, 191) + canv[main_cursor.row][main_cursor.column]} {engine.CLEAR_COLOR}")      
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

            case "crs_click_pipette":
                main_cursor.color = canv[main_cursor.row][main_cursor.column]
            
            case "crs_click_replace":
                canv.replace()

            case "crs_color_change":
                main_cursor.color = engine.Color.create_from_hex(input("Type the new color's HEX\n>> "))

            case "canv_undo":
                canv.undo()

            case "canv_redo":
                canv.redo()

            case "canv_hide_background":
                if hide_background:
                    hide_background = False
                    bkg = engine.ColorMatrix.create_from_trskin(conf["background_skin"])
                else:
                    hide_background = True
                    bkg = engine.ColorMatrix(engine.LOOPER_WIDTH, engine.LOOPER_HEIGHT, engine.Color(0, 0, 0, 0))
                
            case "canv_show_cursor_position":
                show_cursor_position = not show_cursor_position
                
            case "canv_skin_export":
                print(f"here your skin is:\n{canv.get_trskin()}")
                print("type 'img' to save it as PNG file, anything else otherwise")
                
                if input(">> ").lower() == "img":
                    canv.get_img(input("type the path to the image\n>> "))
                    
            case "canv_skin_import":
                q = input("and new skin is? (type 'img' if you wanna load skin from PNG image, the skin itself otherwise)\n>> ")
                oldcanv = canv
                if q.lower() == "img":
                    canv = engine.ColorMatrix.create_from_img(input("type the path to the image\n>> "), weakref.ref(main_cursor)(), stuff.SIDE_TEXTS[0])
                else:
                    canv = engine.ColorMatrix.create_from_trskin(q, weakref.ref(main_cursor)(), stuff.SIDE_TEXTS[0])
                canv.prepend_history_from(oldcanv)
            case "back_or_settings":
                config.save_config(stuff.settings())

                conf = config.get_config()
                importlib.reload(stuff)
                importlib.reload(kb)

                bkg = engine.ColorMatrix.create_from_trskin(conf["background_skin"])
                canv.side_text = stuff.SIDE_TEXTS[0].strip('\n').split("\n")
                print(f"\n\npress [{conf['keys']['back_or_settings']}] to continue")
                kb.wait_for_command("back_or_settings")

            case "quit":
                print("are you sure that you want to quit? ><")
                print("(type 'n' if you aren't and anything else otherwise.)")
                if input(">> ") == "n":
                    continue
                break
                
                
    except Exception as e:
        print("\n\noooooops... an error has occured (probably it's not my fault, but if u think it is, tell me about that)\n\n")
        traceback.print_exc()
        print(f"\n\npress [{conf['keys']['back_or_settings']}] to continue")
        kb.wait_for_command("back_or_settings")
