from pip import main as pip

def libch(libs: dict[str, str]):
    
    failed = {}
    
    for lib in libs.keys():

        try:
            exec('import ' + lib)
        except:
            failed[lib] = libs[lib]

    if failed:

        print('oops... looks like you need to install these libraries -> ', list(failed.values()))

        if input('do u wanna install them?(Y/n)\n>> ').lower() == 'y':
            for lib in failed.keys():
                pip(['install', failed[lib]])
                

def verch(current_version: str):
    try:
        from requests import get
        
        URL = "https://pastebin.com/raw/Z8jFRFr2"

        newest = get(URL).text

        if newest != current_version:

            print(f"\033[38;2;255;255;0mNew ({newest}) version is available!\033[0m (you can disable this prompt in settings)")
    except:
        print("\033[38;2;255;255;0mCouldn't check your version (maybe some problems with internet connection)\033[0m  (you can disable this prompt in settings)")
