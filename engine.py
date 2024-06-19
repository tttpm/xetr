from base64 import b64encode, b64decode
from os import name
from zlib import decompress, compressobj, MAX_WBITS, DEFLATED
import copy


from PIL import Image, ImageColor, ImageDraw

CLEAR_COLOR = '\033[0m'
LOOPER_WIDTH = 20
LOOPER_HEIGHT = 18

class Color:
    
    '''literally color!!'''
    
    def __init__(self, red: int, green: int, blue: int, alpha = 255):
        
        '''create Color using red, green, and alpha values'''
        
        try:
            assert type(red) == int and 0 <= red <= 255
            self.red = red
            
        except:
            raise ValueError(f'invalid red value: {red}')

        try:
            assert type(green) == int and 0 <= green <= 255
            self.green = green
            
        except:
            raise ValueError(f'invalid green value: {green}')


        try:
            assert type(blue) == int and 0 <= blue <= 255
            self.blue = blue
            
        except:
            raise ValueError(f'invalid blue value: {blue}')
        
        try:
            if type(alpha) == int:
                alpha /= 255
            assert type(alpha) == float and 0 <= alpha <= 1
            self.alpha = alpha
            
        except:
            raise ValueError(f'invalid alpha value: {alpha}')
        

    @classmethod
    def transparent(cls):
        return Color(0, 0, 0, 0)

    @classmethod
    def black(cls):
        return Color(0, 0, 0)
        
    @classmethod
    def create_from_rgba(cls, r: int, g: int, b: int, a: int):
        
        '''create Color using red, green, blue and alpha values'''
        
        return Color(r, g, b, a)



    @classmethod
    def create_from_hex(cls, hex_: str):

        '''create Color using six- or eight-digit HEX'''
        
        hex_ = hex_.removeprefix("#")
        if len(hex_) == 3 or len(hex_) == 4:
            hex_ = "".join([c + c for c in hex_])
        try:
            
            r = int(hex_[:2], 16)
            g = int(hex_[2:4], 16)
            b = int(hex_[4:6], 16)
            a = 1.0
            if len(hex_) > 6: a = int(hex_[6:8], 16) / 255

            
        except:
            raise ValueError('invalid HEX')
        
        return Color(r, g, b, a)



    @classmethod
    def create_from_ansi(cls, ansi: str):

        '''create Color using ANSI code'''
        
        try:
            ansi = ansi.split(';') 
            r = int(ansi[2])
            g = int(ansi[3])
            b = int(ansi[4][:-1])
            
        except:
            raise ValueError('invalid ANSI code')
        
        return Color(r, g, b)

    @classmethod
    def create_from_hsva(cls, h: int, s: int, v: int, a: float = 1.0):
        h = h / 360.0
        s = s / 100.0
        v = v / 100.0
        if s:
            if h == 1.0: h = 0.0
            i = int(h*6.0); f = h*6.0 - i
            
            w = int(255*( v * (1.0 - s) ))
            q = int(255*( v * (1.0 - s * f) ))
            t = int(255*( v * (1.0 - s * (1.0 - f)) ))
            v = int(255*v)
            
            if i==0: return Color(v, t, w, a)
            if i==1: return Color(q, v, w, a)
            if i==2: return Color(w, v, t, a)
            if i==3: return Color(w, q, v, a)
            if i==4: return Color(t, w, v, a)
            if i==5: return Color(v, w, q, a)
        else: v = int(255*v); return Color(v, v, v, a)


    def get_hsva(self):
        r = self.red / 255
        g = self.green / 255
        b = self.blue / 255
        a = self.alpha
        cmin = min(r, g, b)
        cmax = max(r, g, b)
        d = cmax - cmin
        if cmax == 0.0:
            s = 0
        else:
            s = round(d / cmax * 100)
        v = round(cmax * 100)
        if d == 0:
            return (0, s, v, a)
        if cmax == r:
            return (round(60 * (((g - b) / d) % 6)), s, v, a)
        if cmax == g:
            return (round(60 * (((b - r) / d) + 2)), s, v, a)
        return (round(60 * (((r - g) / d) + 4)), s, v, a)


    def get_hex(self):

        '''get eight-digit HEX from Color'''
        
        return "{:02X}{:02X}{:02X}{:02X}".format(*self.values())

    def get_ansi(self, back: bool = False, fore: bool = True):
        
        '''get ANSI code from Color'''
        
        return ((f"\033[38;2;{self.red};{self.green};{self.blue}m" if fore else '') +
               (f"\033[48;2;{self.red};{self.green};{self.blue}m" if back else ''))



    def __eq__(self, other):
        if type(other) != Color or not(self.red == other.red and self.blue == other.blue and self.green == other.green and self.alpha == other.alpha):
            return False 
        return True



    def __str__(self):
        return self.get_ansi(back = True)


    def __add__(self, other):

        if type(other) == Color:
            
            a = other.alpha + self.alpha * (1 - other.alpha)

            if not a:
                return Color(0,0,0,0)
    
            r = round((other.alpha * other.red + self.alpha * self.red * (1 - other.alpha)) / a)
        
            g = round((other.alpha * other.green + self.alpha * self.green * (1 - other.alpha)) / a)
        
            b = round((other.alpha * other.blue + self.alpha * self.blue * (1 - other.alpha)) / a)
          
            return Color(r, g, b, a)

    def __iter__(self): 
        return iter(self.values(alpha255=False))
    
    def values(self, alpha255 = True):
        a = self.alpha
        if alpha255:
            a = round(a * 255)
        return (self.red, self.green, self.blue, a)
    
    def fvalues(self):
        return (self.red / 255, self.green / 255, self.blue / 255, self.alpha)

    def copy(self):
        return Color(*self.values())
  



class Cursor:

    def __init__(self, row: int, column: int, maxrow: int, maxcolumn: int, color: Color):
        
        self.row = row
        self.column = column
        self.maxrow = maxrow
        self.maxcolumn = maxcolumn 
        self.color = color

    def up(self): self.row -= (1 if self.row > 0 else 0)
    
    def left(self): self.column -= (1 if self.column > 0 else 0)
    
    def down(self): self.row += (1 if self.row < self.maxrow - 1 else 0)

    def right(self): self.column += (1 if self.column < self.maxcolumn - 1 else 0)

    def is_on(self, row: int, column: int) -> bool:
        return (self.row == row) and (self.column == column)




class ColorArray:
    
    '''array of Colors'''

    def __init__(self, size: int, color: Color, cursor = None, index = 0):

        self.size = size
        self.index = index
        self.cursor = cursor
        
        if type(color) != Color:
            raise ValueError('ColorArray can only contain Color objects')
        
        self.__content = [color] * size
        

    def __setitem__(self, index, value):
        
        if type(value) != Color:
            raise ValueError('ColorArray can only contain Color objects')
        
        self.__content[index] = value


        
    def __getitem__(self, index):
        return self.__content[index]



    def __str__(self):
        
        res = ''

        if self.index % 2 == 0:
            transparent = (Color(255, 255, 255), Color(191, 191, 191))
        else:
            transparent = (Color(191, 191, 191), Color(255, 255, 255))
        
        for i in range(self.size):
            
            c1, c2 = transparent
            
            c1 = c1 + self[i]
            c2 = c2 + self[i]

            if self.cursor != None and self.cursor.row == self.index and self.cursor.column == i:
                c1 += self.cursor.color
                c2 += self.cursor.color

            res += str(c1) + "#" + str(c2) + "#"

            
        return res + CLEAR_COLOR



    def __len__(self):
        return len(self.__content)







class ColorMatrix: 

    '''array of ColorArrays'''
    
    def __init__(self, width: int, height: int, color: Color = Color.transparent(), cursor = None, side_text: str = None, init_record = True):

        self.width = width
        self.height = height
        self.cursor = cursor
        
        self.history = []
        self.hist_pos = -1
        
        if side_text != None:
            self.side_text = side_text.strip('\n').split('\n')
        else:
            self.side_text = None

        

        self.__content = []
        
        for i in range(height):
            
            self.__content.append(ColorArray(width, color, cursor = self.cursor, index = i))

        if init_record:
            self.__record()
            
    def __getitem__(self, index):
        return self.__content[index]



    def __setitem__(self, index, value):
        
        if type(value) != ColorArray:
            raise ValueError('ColorMatrix can only contain ColorArray objects')
        self[index] = value

    def paint(self, row = None, column = None, new_color = None):
        row = row if row != None else self.cursor.row
        column = column if column != None else self.cursor.column
        new_color = new_color if new_color != None else self.cursor.color
        self.__content[row][column] = new_color
        self.__record()

    def __str__(self):
        
        res =   '##' * (self.width + 2)  + (self.side_text[0] if self.side_text != None else '') + '\n'
        
        for i in range(self.height):
            res += '##' + str(self[i]) + '##' + (self.side_text[i + 1] if self.side_text != None and i + 1 < len(self.side_text) else '') + '\n'
        return res + '##' * (self.width + 2) + (self.side_text[i + 2] if self.side_text != None and i + 2 < len(self.side_text) else '')
    



    def __add__(self, other):

        if type(other) == Canvas:
            res = copy.deepcopy(other)
            res.insert_layer(0, color_matrix=self)
            return res


        if type(other) != ColorMatrix:
            raise TypeError("can only add ColorMatrix or Canvas to ColorMatrix")
        
        result = ColorMatrix(max(self.width, other.width), max(self.height, other.height), Color(0,0,0,0), self.cursor if self.cursor else other.cursor, init_record=False)


        for i in range(result.height):
            
            for j in range(result.width):

                first, second = Color(0,0,0,0), Color(0,0,0,0)

                if i < self.height and j < self.width:
                    first = self[i][j]
                    
                if i < other.height and j < other.width:
                    second = other[i][j]
                
                result[i][j] = first + second
        result.__record()

        result.side_text = None       
        
        if other.side_text != None:
            result.side_text = other.side_text
        if self.side_text != None:
            result.side_text = self.side_text
            
        return result   


        

    def __fill(self, row: int, column: int, new_color: Color):
        
        filling = [(row, column)]
        checked = [[0] * self.width for _ in range(self.height)]
        
        while filling:

            to_fill = []
            for elem in filling:
                x, y = elem
                
                if x > 0 and not checked[x-1][y]:
                    checked[x-1][y] = 1
                    if self[x-1][y] == self[x][y]: to_fill.append((x-1, y))

                if y > 0 and not checked[x][y-1]:
                    checked[x][y-1] = 1
                    if self[x][y-1] == self[x][y]: to_fill.append((x, y-1))


                if x < (self.height - 1) and not checked[x+1][y]:
                    checked[x+1][y] = 1
                    if self[x+1][y] == self[x][y]: to_fill.append((x+1, y))

                if y < (self.width - 1) and not checked[x][y + 1]:
                    checked[x][y+1] = 1
                    if self[x][y+1] == self[x][y]: to_fill.append((x, y+1))
                    
                self[x][y] = new_color

            filling = to_fill[::]

    def fill(self, row = None, column = None, new_color = None):
        row = row if row else self.cursor.row
        column = column if column else self.cursor.column
        new_color = new_color if new_color else self.cursor.color
        self.__fill(row, column, new_color)
        self.__record()

    def __replace(self, from_color: Color, to_color: Color):
        for i in range(self.height):
            for j in range(self.width):
                if self[i][j] == from_color:
                    self[i][j] = to_color
    
    def replace(self, row: int = None, column: int = None, new_color: Color = None):
        row = row if row != None else self.cursor.row
        column = column if column != None else self.cursor.column
        new_color = new_color if new_color != None else self.cursor.color
        self.__replace(self[row][column], new_color)
        self.__record()

    def get_trskin(self):
        res = ''
        for i in range(self.height):
            for j in range(self.width):
                res += self[i][j].get_hex() + ';'
                
        deflate_compress = compressobj(9, DEFLATED, -MAX_WBITS)
        compressed = deflate_compress.compress(bytes(res, encoding ='utf-8')) + deflate_compress.flush()
        encrypted = b64encode(compressed)
        return "trSkin1" + encrypted.decode()


    @classmethod
    def create_from_trskin(cls, skin: str, cursor=None, side_text=None, init_record=False):
        res = ColorMatrix(LOOPER_WIDTH, LOOPER_HEIGHT, Color(0,0,0,0), cursor, side_text, init_record)
        compressed = b64decode(skin[7:])
        hexes = str(decompress(compressed, -MAX_WBITS).decode()).split(';')
        hexes.pop()
        i, j = 0, 0
        for h in hexes:
            if j == 20:
                i += 1
                j = 0
            res[i][j] = Color.create_from_hex(h)
            j += 1
        res.__record()
        return res


    def get_img(self, img_path):

        img = Image.new("RGBA", (self.width, self.height), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        for i in range(self.height):
            for j in range(self.width):
                draw.point((j, i), ImageColor.getcolor('#' + self[i][j].get_hex(), "RGBA"))

        img.save(img_path)



    @classmethod
    def create_from_img(cls, img_path: str, cursor = None, side_text = None, init_record = False):
        img = Image.open(img_path).convert('RGBA')
        res = ColorMatrix(*img.size, Color(0,0,0,0), cursor, side_text, init_record)
        img = img.load()
        for i in range(res.height):
            for j in range(res.width):
                new = img[j, i]
                res[i][j] = Color(*new)
        res.__record()
        return res




    @classmethod
    def create_from_list(cls, source: list, cursor=None, side_text = None, init_record = False):

        result = ColorMatrix(len(max(source, key = len)), len(source), Color(0,0,0,0), cursor, side_text, init_record)

        for i in range(result.height):

            for j in range(result.width):

                if j < len(source[i]):

                    if type(source) != Color:
                        result[i][j] = source[i][j]
        return result
                        

    @classmethod
    def create_looper(cls, primary_color = Color(255, 255, 255), secondary_color = Color(0, 0, 0), background = Color(0,0,0,0), cursor=None, side_text = None, init_record = False):
        e = background
        p, s = primary_color, secondary_color
        x, y = p + Color(0,0,0,68), s + Color(0,0,0,68)
        return ColorMatrix.create_from_list([
            
            [e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e, e],
            [e, e, e, x, x, p, p, p, p, p, p, p, p, p, p, p, p, e, e, e],
            [e, e, x, x, p, p, p, p, p, p, p, p, p, p, p, p, p, p, e, e],
            [e, e, x, x, p, p, p, p, p, p, p, p, p, p, p, p, p, p, e, e],
            [e, e, x, x, p, p, p, p, p, s, s, p, p, p, s, s, p, p, e, e],
            [e, e, x, x, p, p, p, p, p, s, s, p, p, p, s, s, p, p, e, e],
            [e, e, x, x, p, p, p, p, p, s, s, p, p, p, s, s, p, p, e, e],
            [e, e, x, x, p, p, p, p, p, s, s, p, p, p, s, s, p, p, e, e],
            [e, e, x, x, p, p, p, p, p, p, p, p, p, p, p, p, p, p, e, e],
            [e, e, x, x, p, p, p, p, p, p, p, p, p, p, p, p, p, p, e, e],
            [e, e, y, y, s, s, s, s, s, s, s, s, s, s, s, s, s, s, e, e],
            [e, e, y, y, s, s, s, s, s, s, s, s, s, s, s, s, s, s, e, e],
            [e, e, y, y, s, s, s, s, s, s, s, s, s, s, s, s, s, s, e, e],
            [e, e, y, y, s, s, s, s, s, s, s, s, s, s, s, s, s, s, e, e],
            [e, e, e, y, y, s, s, s, s, s, s, s, s, s, s, s, s, e, e, e],
            [e, e, e, e, e, e, s, s, s, e, e, e, e, s, s, s, e, e, e, e],
            [e, e, e, e, e, e, s, s, s, e, e, e, e, s, s, s, e, e, e, e]
            
            ], cursor, side_text, init_record)

    def get_list(self):
        return copy.deepcopy(self.__content)

    def __record(self): #he rember :D
        if self.hist_pos != -1:
            self.history = self.history[:self.hist_pos+1]
        self.hist_pos = -1
        self.history.append(self.get_list())

    def __restore(self, index): #why.
        cm = self.history[index]
        for i in range(self.height):
            for j in range(self.width):
                self[i][j] = cm[i][j]

    def undo(self):
        if len(self.history) <= -self.hist_pos:
            return 0
        self.hist_pos -= 1
        self.__restore(self.hist_pos)
        return 1

    def redo(self):
        if self.hist_pos == -1:
            return 0
        self.hist_pos += 1
        self.__restore(self.hist_pos)
        return 1

    def prepend_history_from(self, other):
        self.history = other.history + self.history
        #self.hist_pos += len(other.history)        

def is_valid_trskin(skin: str):
    try:
        ColorMatrix.create_from_trskin(skin)
        return True
    except:
        return False

class ColorPicker:
    def __init__(self, radius: int = 10, hue: int = 0, saturation: int = 0, value: int = 0, alpha: float = 1.0,
                 prompts: dict = {
                     "-hue": "<- [q]",
                     "+hue": "[w] ->",
                     "-saturation": "<- [a]",
                     "+saturation": "[s] ->",
                     "-value": "<- [z]",
                     "+value": "[x] ->",
                     "-alpha": "<- [f]",
                     "+alpha": "[g] ->"
                 },
                 deltas: dict = {
                     "hue": 5,
                     "saturation": 5,
                     "value": 5,
                     "alpha": 0.05
                 }):
        self.radius = radius
        self.hue = hue
        self.saturation = saturation
        self.alpha = alpha
        self.value = value
        self.prompts = prompts
        self.deltas = deltas
        self._update_color()

    def _update_color(self):
        self.color = Color.create_from_hsva(self.hue, self.saturation, self.value, self.alpha)

    def __str__(self):
        
        tc1, tc2 = Color(255, 255, 255), Color(191, 191, 191)

        def draw_square_line(index: int, padding=10):
            WIDTH = 16
            if index == 0 or index == 17:
                return " " * padding + "##" * (WIDTH + 2)
            res = " " * padding + "##"
            if index % 2 == 0:
                res += (str(tc1 + self.color) + "#" + str(tc2 + self.color) + "#") * WIDTH
            else:
                res += (str(tc2 + self.color) + "#" + str(tc1 + self.color) + "#") * WIDTH
            res += CLEAR_COLOR
            res += "##"
            return res

        

        res = ""

        hue = self.hue
        saturation = self.saturation
        value = self.value
        alpha = self.alpha

        width = 2 * (2 * self.radius + 3)

        #hue
        res += "#" * width + draw_square_line(0) + "\n##"
        color_list = []
        hue1 = hue
        for _ in range(self.radius):
            hue1 -= self.deltas["hue"]
            if hue1 < 0:
                hue1 = 0
            color_list.append(Color.create_from_hsva(hue1, saturation, value, alpha))

        color_list.reverse()

        color_list.append(Color.create_from_hsva(hue, saturation, value, alpha))

        hue1 = hue
        for _ in range(self.radius):
            hue1 += self.deltas["hue"]
            if hue1 > 360:
                hue1 = 360
            color_list.append(Color.create_from_hsva(hue1, saturation, value, alpha))

        for color in color_list:
            res += str(tc1 + color) + "#" + str(tc2 + color) + "#"
        res += CLEAR_COLOR
        res += "##"
        res += f"{hue: 6}"
        res += draw_square_line(1, padding=4) + "\n"
        res += "#" * width + draw_square_line(2) + "\n"
        mprompt = self.prompts["-hue"]
        pprompt = self.prompts["+hue"]
        res += mprompt
        title = "hue"
        res += " " * ((width // 2) - len(mprompt) - ((len(title) + 1)//2))
        res += title
        res += " " * ((width // 2) - len(pprompt) - (len(title)//2))
        res += pprompt
        res += draw_square_line(3) + "\n" 
        res += " " * width + draw_square_line(4) + "\n"

        #saturation
        res += "#" * width + draw_square_line(5) + "\n##"
        color_list = []
        saturation1 = saturation
        for _ in range(self.radius):
            saturation1 -= self.deltas["saturation"]
            if saturation1 < 0:
                saturation1 = 0
            color_list.append(Color.create_from_hsva(hue, saturation1, value, alpha))

        color_list.reverse()

        color_list.append(Color.create_from_hsva(hue, saturation, value, alpha))

        saturation1 = saturation
        for _ in range(self.radius):
            saturation1 += self.deltas["saturation"]
            if saturation1 > 100:
                saturation1 = 100
            color_list.append(Color.create_from_hsva(hue, saturation1, value, alpha))

        for color in color_list:
            res +=  str(tc1 + color) + "#" + str(tc2 + color) + "#"

        res += CLEAR_COLOR
        res += "##"
        res += f"{saturation: 6}"
        res += draw_square_line(6, padding=4) + "\n"
        res += "#" * width + draw_square_line(7) + "\n"
        mprompt = self.prompts["-saturation"]
        pprompt = self.prompts["+saturation"]
        res += mprompt
        title = "saturation"
        res += " " * ((width // 2) - len(mprompt) - ((len(title) + 1)//2))
        res += title
        res += " " * ((width // 2) - len(pprompt) - (len(title)//2))
        res += pprompt
        res += draw_square_line(8) + "\n" 
        res += " " * width + draw_square_line(9) + "\n"

        #value
        res += "#" * width + draw_square_line(10) + "\n##"
        color_list = []
        value1 = value
        for _ in range(self.radius):
            value1 -= self.deltas["value"]
            if value1 < 0:
                value1 = 0
            color_list.append(Color.create_from_hsva(hue, saturation, value1, alpha))

        color_list.reverse()

        color_list.append(Color.create_from_hsva(hue, saturation, value, alpha))

        value1 = value
        for _ in range(self.radius):
            value1 += self.deltas["value"]
            if value1 > 100:
                value1 = 100
            color_list.append(Color.create_from_hsva(hue, saturation, value1, alpha))

        for color in color_list:
            res +=  str(tc1 + color) + "#" + str(tc2 + color) + "#"

        res += CLEAR_COLOR
        res += "##"
        res += f"{value: 6}"
        res += draw_square_line(11, padding=4) + "\n"
        res += "#" * width + draw_square_line(12) + "\n"
        mprompt = self.prompts["-value"]
        pprompt = self.prompts["+value"]
        res += mprompt
        title = "value"
        res += " " * ((width // 2) - len(mprompt) - ((len(title) + 1)//2))
        res += title
        res += " " * ((width // 2) - len(pprompt) - (len(title)//2))
        res += pprompt
        res += draw_square_line(13) + "\n"
        res += " " * width + draw_square_line(14) + "\n"


        #alpha
        res += "#" * width + draw_square_line(15) + "\n##"
        color_list = []
        alpha1 = alpha
        for _ in range(self.radius):
            alpha1 -= self.deltas["alpha"]
            if alpha1 < 0.0:
                alpha1 = 0.0
            color_list.append(Color.create_from_hsva(hue, saturation, value, alpha1))

        color_list.reverse()

        color_list.append(Color.create_from_hsva(hue, saturation, value, alpha))

        alpha1 = alpha
        for _ in range(self.radius):
            alpha1 += self.deltas["alpha"]
            if alpha1 > 1.0:
                alpha1 = 1.0
            color_list.append(Color.create_from_hsva(hue, saturation, value, alpha1))

        for color in color_list:
            res += str(tc1 + color) + "#" + str(tc2 + color) + "#"
            
        res += CLEAR_COLOR
        res += "##"
        res += f"{round(alpha * 100): 6}"
        res += draw_square_line(16, padding=4) + "\n"
        res += "#" * width + draw_square_line(17) + "\n"
        mprompt = self.prompts["-alpha"]
        pprompt = self.prompts["+alpha"]
        res += mprompt
        title = "alpha"
        res += " " * ((width // 2) - len(mprompt) - ((len(title) + 1)//2))
        res += title
        res += " " * ((width // 2) - len(pprompt) - (len(title)//2))
        res += pprompt
        res += "\n"


        return res
    
    def increase_hue(self):
        self.hue += self.deltas["hue"]
        if self.hue > 360:
            self.hue = 360
        self._update_color()
        
    def decrease_hue(self):
        self.hue -= self.deltas["hue"]
        if self.hue < 0:
            self.hue = 0
        self._update_color()
    
    def increase_saturation(self):
        self.saturation += self.deltas["saturation"]
        if self.saturation > 100:
            self.saturation = 100
        self._update_color()
        
    def decrease_saturation(self):
        self.saturation -= self.deltas["saturation"]
        if self.saturation < 0:
            self.saturation = 0
        self._update_color()
    
    def increase_value(self):
        self.value += self.deltas["value"]
        if self.value > 100:
            self.value = 100
        self._update_color()
        
    def decrease_value(self):
        self.value -= self.deltas["value"]
        if self.value < 0:
            self.value = 0
        self._update_color()
    
    def increase_alpha(self):
        self.alpha += self.deltas["alpha"]
        if self.alpha > 1.0:
            self.alpha = 1.0
        self._update_color()
        
    def decrease_alpha(self):
        self.alpha -= self.deltas["alpha"]
        if self.alpha < 0.0:
            self.alpha = 0.0
        self._update_color()

    def set_color(self, color: Color):
        self.color = color
        self.hue, self.saturation, self.value, self.alpha = color.get_hsva()
    
    @classmethod
    def create_from_color(cls, radius: int = 10, color: Color = Color(255, 255, 255),
                 prompts: dict = {
                     "-hue": "<- [q]",
                     "+hue": "[w] ->",
                     "-saturation": "<- [a]",
                     "+saturation": "[s] ->",
                     "-value": "<- [z]",
                     "+value": "[x] ->",
                     "-alpha": "<- [f]",
                     "+alpha": "[g] ->"
                 },
                 deltas: dict = {
                     "hue": 5,
                     "saturation": 5,
                     "value": 5,
                     "alpha": 0.05
                 }):
        res = ColorPicker(radius=radius, prompts=prompts, deltas=deltas)
        res.set_color(color)
        return res


class Cursor3D(Cursor):
    def __init__(self, row: int, column: int, layer: int, maxrow: int, maxcolumn: int, maxlayer: int, color: Color):
        super().__init__(row, column, maxrow, maxcolumn, color)
        self.layer = layer
        self.maxlayer = maxlayer

    def layer_down(self): 
        self.layer -= (1 if self.layer > 0 else 0)

    def layer_up(self): 
        self.layer += (1 if self.layer < self.maxlayer - 1 else 0)

    def is_on3(self, row: int, column: int, layer: int) -> bool:
        return self.is_on(row, column) and (layer == self.layer)

class Canvas:

    def __init__(self, width: int, height: int, color: Color = Color.transparent(), cursor: Cursor3D = None, side_text: str = None):
        self.width = width
        self.height = height
        self.side_text = side_text
        if cursor == None:
            cursor = Cursor3D(0, 0, 0, height, width, 1, Color.black())
        self.cursor = cursor
        self.layers = [ColorMatrix(width, height, color)]
        self.show_layer = [True]

    def sum(self, ignore_cursor: bool = True, ignore_hidden: bool = True) -> ColorMatrix:
        res = ColorMatrix(self.width, self.height, side_text=self.side_text)
        for i in range(self.cursor.maxlayer):
            if ignore_hidden and not self.show_layer[i]:
                continue
            cm = copy.deepcopy(self.layers[i])
            if (not ignore_cursor) and (i == self.cursor.layer):
                cm.paint(self.cursor.row, self.cursor.column, self.cursor.color)
            res = res + cm
        return res

    def __str__(self):
        return self.sum(ignore_cursor=False).__str__()
    
    def __getitem__(self, index: int):
        return self.layers[index]
    
    def __setitem__(self, index: int, value: ColorMatrix):
        self.layers[index] = value

    def paint(self, row: int = None, column: int = None, layer: int = None, new_color: Color = None):
        row = row if row != None else self.cursor.row
        column = column if column != None else self.cursor.column
        layer = layer if layer != None else self.cursor.layer
        new_color = new_color if new_color != None else self.cursor.color
        self[layer].paint(row, column, new_color)

    def fill(self, row: int = None, column: int = None, layer: int = None, new_color: Color = None):
        row = row if row != None else self.cursor.row
        column = column if column != None else self.cursor.column
        layer = layer if layer != None else self.cursor.layer
        new_color = new_color if new_color != None else self.cursor.color
        self[layer].fill(row, column, new_color)

    def undo(self, index: int = None):
        if index == None:
            index = self.cursor.layer
        return self[index].undo()

    def redo(self, index: int = None):
        if index == None:
            index = self.cursor.layer
        return self[index].redo()

    def add_layer(self, color: Color = Color.transparent(), color_matrix: ColorMatrix = None):
        if color_matrix == None:
            color_matrix = ColorMatrix(self.width, self.height, color)
        self.layers.append(color_matrix)
        self.show_layer.append(True)
        self.cursor.maxlayer += 1
    
    def insert_layer(self, index: int = None, color: Color = Color.transparent(), color_matrix: ColorMatrix = None):
        if index == None:
            index = self.cursor.layer
        if color_matrix == None:
            color_matrix = ColorMatrix(self.width, self.height, color)
        self.layers.insert(index, color_matrix)
        self.show_layer.insert(index, True)
        self.cursor.maxlayer += 1
    
    def remove_layer(self, index: int = None):
        if index == None:
            index = self.cursor.layer
        if index >= self.cursor.maxlayer:
            raise IndexError(f"cant close {index} layer when there are only {self.cursor.maxlayer} of them")
        self.layers.pop(index)
        self.show_layer.pop(index)
        self.cursor.maxlayer -= 1
        if self.cursor.layer >= self.cursor.maxlayer: 
            self.cursor.layer_down()
        
    def combine_with_next(self, index: int = None):
        if index == None:
            index = self.cursor.layer
        if index >= self.cursor.maxlayer - 1:
            return
        self[index] = self[index] + self[index + 1]
        self.remove_layer(index + 1)

    def swap_with_next(self, index: int = None):
        if index == None:
            index = self.cursor.layer
        if index >= self.cursor.maxlayer - 1:
            return
        self[index], self[index + 1] = self[index + 1], self[index]

    def combine_with_prev(self, index: int = None):
        if index == None:
            index = self.cursor.layer
        if index <= 0:
            return
        self[index] = self[index] + self[index - 1]
        self.remove_layer(index - 1)

    def swap_with_prev(self, index: int = None):
        if index == None:
            index = self.cursor.layer
        if index <= 0:
            return
        self[index], self[index - 1] = self[index - 1], self[index]


    def switch(self, index: int = None, show: bool = None):
        if index == None:
            index = self.cursor.layer
        if show == None:
            show = not self.show_layer[index]
        self.show_layer[index] = show
    
    def __add__(self, other: ColorMatrix):
        res = copy.deepcopy(self)
        res.add_layer(color_matrix=other)
        return res

    def get(self, row: int = None, column: int = None, layer: int = None):
        row = row if row != None else self.cursor.row
        column = column if column != None else self.cursor.column
        layer = layer if layer != None else self.cursor.layer
        return self[layer][row][column]
    
    def setl(self, cm: ColorMatrix, layer: int = None, prep_hist: bool = True):
        if layer == None:
            layer = self.cursor.layer
        if prep_hist:
            cm.prepend_history_from(self[layer])
        self[layer] = cm
