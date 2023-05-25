from weakref import ref
from base64 import b64encode, b64decode
from zlib import decompress, compressobj, MAX_WBITS, DEFLATED
import copy

from PIL import Image, ImageColor, ImageDraw

CLEAR_COLOR = '\033[0m'
LOOPER_WIDTH = 20
LOOPER_HEIGHT = 18

class Color():
    
    '''literally color!!'''
    
    def __init__(self, red: int, green: int, blue: int, alpha = 1):
        
        '''create Color using red, green, and alpha values'''
        
        try:
            assert type(red) == int and 0 <= red <= 255
            self.red = red
            
        except:
            raise ValueError('invalid red value')

        try:
            assert type(green) == int and 0 <= green <= 255
            self.green = green
            
        except:
            raise ValueError('invalid green value')


        try:
            assert type(blue) == int and 0 <= blue <= 255
            self.blue = blue
            
        except:
            raise ValueError('invalid blue value')
        
        try:
            if alpha > 1: alpha /= 255
            assert (type(alpha) == float or type(alpha) == int) and 0 <= alpha <= 1
            self.alpha = alpha
            
        except:
            raise ValueError('invalid alpha value')
        


        
    @classmethod
    def create_from_rgba(cls, r: int, g: int, b: int, a: int):
        
        '''create Color using red, green, blue and alpha values'''
        
        return Color(r, g, b, a)



    @classmethod
    def create_from_hex(cls, hex_: str):

        '''create Color using six- or eight-digit HEX'''
        
        hex_ = hex_.replace('#', '')
        
        try:
            
            r = int(hex_[:2], 16)
            g = int(hex_[2:4], 16)
            b = int(hex_[4:6], 16)
            a = 1
            if len(hex_) > 6: a = int(hex_[6:8], 16)  / 255

            
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


    def get_hex(self):

        '''get eight-digit HEX from Color'''
    
        alphabet = '0123456789abcdef'
        
        return (alphabet[self.red // 16] + alphabet[self.red % 16] +
               alphabet[self.green // 16] + alphabet[self.green % 16] +
               alphabet[self.blue // 16] + alphabet[self.blue % 16] +
               alphabet[round(self.alpha * 255) // 16] + alphabet[round(self.alpha * 255) % 16])

    def get_ansi(self, back = 0, fore = 1):
        
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
        return iter((self.red, self.green, self.blue, self.alpha))

  



class Cursor():

    def __init__(self, row: int, column: int, maxrow: int, maxcolumn: int, color: Color):
        
        self.row = row
        self.column = column
        self.maxrow = maxrow
        self.maxcolumn = maxcolumn
        self.color = color

    def up(self): self.row -= 1 if self.row > 0 else 0
    
    def left(self): self.column -= 1 if self.column > 0 else 0
    
    def down(self): self.row += 1 if self.row < self.maxrow - 1 else 0

    def right(self): self.column += 1 if self.column < self.maxcolumn - 1 else 0




class ColorArray():
    
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
        
        for i in range(self.size):
            
            c = self[i]
            
            if self.cursor and self.cursor.column == i and self.cursor.row == self.index:
                c = self.cursor.color
    
            res += str(c) + '##'

            
        return res + CLEAR_COLOR



    def __len__(self):
        return len(self.__content)







class ColorMatrix(): 

    '''array of ColorArrays'''
    
    def __init__(self, width: int, height: int, color: Color, cursor = None, side_text: str = ''):

        self.width = width
        self.height = height
        self.cursor = cursor
        
        self.history = []
        self.hist_pos = -1
        
        self.side_text = side_text.strip('\n').split('\n')

        

        self.__content = []
        
        for i in range(height):
            
            self.__content.append(ColorArray(width, color, cursor = self.cursor, index = i))

        self.__record()

    def set_cursor(self, cursor):
        self.cursor = cursor
        for i in range(self.height):
            self.__content[i].cursor = cursor()
            
    def __getitem__(self, index):
        return self.__content[index]



    def __setitem__(self, index, value):
        
        if type(value) != ColorArray:
            raise ValueError('ColorMatrix can only contain ColorArray objects')
        self[index] = value

    def paint(self, row = None, column = None, new_color = None):
        row = row if row else self.cursor.row
        column = column if column else self.cursor.column
        new_color = new_color if new_color else self.cursor.color
        self.__content[row][column] = new_color
        self.__record()

    def __str__(self):
        
        res =   '##' * (self.width + 2)  + '\n'
        
        for i in range(self.height):
            res += '##' + str(self[i]) + '##' + (self.side_text[i] if i < len(self.side_text) else '') + '\n'
        return res + '##' * (self.width + 2)
    



    def __add__(self, other):

        if type(other) != ColorMatrix:
            raise TypeError("can only add ColorMatrix to ColorMatrix")
        
        result = ColorMatrix(max(self.width, other.width), max(self.height, other.height), Color(0,0,0,0), self.cursor if self.cursor else other.cursor)


        for i in range(result.height):
            
            for j in range(result.width):

                first, second = Color(0,0,0,0), Color(0,0,0,0)

                if i < self.height and j < self.width:
                    first = self[i][j]
                    
                if i < other.height and j < other.width:
                    second = other[i][j]
                
                result[i][j] = first + second
                
        result.side_text = None       
        if self.side_text:
            result.side_text = self.side_text
        if other.side_text:
            result.side_text = other.side_text
            
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

    def get_trskin(self):
        res = ''
        for i in range(LOOPER_HEIGHT):
            for j in range(LOOPER_WIDTH):
                res += self[i][j].get_hex() + ';'
                
        deflate_compress = compressobj(9, DEFLATED, -MAX_WBITS)
        compressed = deflate_compress.compress(bytes(res, encoding ='utf-8')) + deflate_compress.flush()
        encrypted = b64encode(compressed)
        return "trSkin1" + encrypted.decode()


    @classmethod
    def create_from_trskin(cls, skin: str, cursor=None, side_text=''):
        res = ColorMatrix(LOOPER_WIDTH, LOOPER_HEIGHT, Color(0,0,0,0), cursor, side_text)
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
            
        return res


    def get_img(self, img_path):

        img = Image.new("RGBA", (self.width, self.height), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        for i in range(self.height):
            for j in range(self.width):
                draw.point((j, i), ImageColor.getcolor('#' + self[i][j].get_hex(), "RGBA"))

        img.save(img_path)



    @classmethod
    def create_from_img(cls, img_path: str, cursor = None, side_text=''):
        img = Image.open(img_path).convert('RGBA')
        res = ColorMatrix(*img.size, Color(0,0,0,0), cursor,side_text)
        img = img.load()
        for i in range(res.height):
            for j in range(res.width):
                new = img[j, i]
                res[i][j] = Color(*new)
        return res




    @classmethod
    def create_from_list(cls, source: list, cursor=None, side_text=''):

        result = ColorMatrix(len(max(source, key = len)), len(source), Color(0,0,0,0), cursor, side_text)

        for i in range(result.height):

            for j in range(result.width):

                if j < len(source[i]):

                    if type(source) != Color:
                        result[i][j] = source[i][j]
        return result
                        

    @classmethod
    def create_looper(cls, primary_color = Color(255, 255, 255), secondary_color = Color(0, 0, 0), background = Color(0,0,0,0), cursor=None, side_text=''):
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
            
            ], cursor, side_text)
    

    def __record(self): #he rember :D
        if self.hist_pos != -1:
            self.history = self.history[:self.hist_pos+1]
        self.hist_pos = -1
        self.history.append(copy.deepcopy(self))

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
