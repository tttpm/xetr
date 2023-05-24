DEFAULT_SETTINGS = {

    "keys": {
    
        "crs_move_up": "up",
        "crs_move_down": "down",
        "crs_move_left": "left",
        "crs_move_right": "right",
        "crs_color_change": "c",
        "crs_click_fill": "f",
        "crs_click_brush": "space",
        "crs_click_eraser": "e",
        "canv_skin_export": "x",
        "canv_skin_import": "i",
        "canv_undo": "z",
        "canv_redo": "y",
        "debug": "d",
        "back": "backspace",
        "quit": "q"
    },

    "background_skin": "trSkin1S0tLSU1MSUuzThtlDBAj0QAEkRlpUEAfxhByKjmOH4FuTkw1MbVMQWZQrHjUzaNuThnNg4PczWYpRklmRsgMzBikJ2PUzaNupsTNg8Tx1G/yUWYXPZ06SNwMAA==",
    "check_version": True,
    "devmode": False
    
}



    
def get_config(file = "csetr_config.txt"):
    
    try:
        
        src = open(file, encoding="utf-8").read()
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
        
   
        



    
   
