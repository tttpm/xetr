DEFAULT_SETTINGS = {

    "keys": {
    
        "crs_move_up": "arrow_up",
        "crs_move_down": "arrow_down",
        "crs_move_left": "arrow_left",
        "crs_move_right": "arrow_right",
        "crs_click_fill": "f",
        "crs_click_brush": "space",
        "crs_click_eraser": "e",
        "crs_click_pipette": "p",
        "crs_click_replace": "r",
        "canv_skin_export": "x",
        "canv_skin_import": "i",
        "canv_undo": "z",
        "canv_redo": "y",
        "canv_hide_background": "b",
        "canv_show_cursor_position": "g",
        "clrpckr_open": "c",
        "back_or_settings": "backspace",
        "quit": "q"
    },

    "colorpicker_keys": {
        "decrease_hue": "q",
        "increase_hue": "w",
        "decrease_saturation": "a",
        "increase_saturation": "s",
        "decrease_value": "z",
        "increase_value": "x",
        "decrease_alpha": "f",
        "increase_alpha": "g",
        "set_hue": "1",
        "set_saturation": "2",
        "set_value": "3",
        "set_alpha": "4",
        "set_hex": "5",
        "submit": "enter",
        "close": "backspace",
    },

    "background_skin": "trSkin1S0tLSU1MSUuzThtlDBAj0QAEkRlpUEAfxhByKjmOH4FuTkw1MbVMQWZQrHjUzaNuThnNg4PczWYpRklmRsgMzBikJ2PUzaNupsTNg8Tx1G/yUWYXPZ06SNwMAA==",
    "check_version": True
    
}



    
def get_config(filename = "csetr_config.txt"):
    
    try:
        with open(filename, encoding="utf-8") as file:
            src = file.read()
        src = eval(src)
        res = {}
        
        for k in DEFAULT_SETTINGS:

            if k == "keys":
                
                res[k] = {}
                
                for key in DEFAULT_SETTINGS[k]:
                    
                    res[k][key] = src[k].get(key, DEFAULT_SETTINGS[k][key])

                    
            else:
                
                res[k] = src.get(k, DEFAULT_SETTINGS[k])
                

        return res

    except:
        return DEFAULT_SETTINGS




def save_config(conf: dict, file = "csetr_config.txt"):
    
    try:
        
        with open(file, "w", encoding="utf-8") as f:
            
            f.write("{\n")

            for k in conf:

                if k == "keys":

                    f.write("'keys': {\n")
                    
                    for key in conf[k]:
                        f.write(f"    {repr(key)}: {repr(conf[k][key])},\n")
                        
                    f.write("    },\n")
                    
                else:
                    f.write(f"{repr(k)}: {repr(conf[k])},\n")

            f.write("}")
            
        return 1
    
    except:
        
        return 0
