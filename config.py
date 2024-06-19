import json

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
        "canv_layer_add": "A",
        "canv_layer_delete": "Q",
        "canv_layer_next": "W",
        "canv_layer_prev": "S",
        "canv_layer_swap_next": "E",
        "canv_layer_swap_prev": "D",
        "canv_layer_comb_next": "R",
        "canv_layer_comb_prev": "F",
        "canv_layer_hide": "H",
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


DEFAULT_CONFIG_FILE = "./xetr_config.json"
    
def get_config(filename = DEFAULT_CONFIG_FILE):
    
    try:
        with open(filename, encoding="utf-8") as file:
            src = json.load(file)

        res = {}
        
        for k in DEFAULT_SETTINGS:

            if type(DEFAULT_SETTINGS[k]) == dict:
                
                res[k] = {}
                
                for key in DEFAULT_SETTINGS[k]:
                    
                    res[k][key] = src[k].get(key, DEFAULT_SETTINGS[k][key])

                    
            else:
                
                res[k] = src.get(k, DEFAULT_SETTINGS[k])
                

        return res

    except:
        return DEFAULT_SETTINGS




def save_config(conf: dict, file = DEFAULT_CONFIG_FILE):
    try:
        with open(file, "w", encoding="utf-8") as f:
           f.write(json.dumps(conf, indent=4))    
        return 1
    except:
        return 0
