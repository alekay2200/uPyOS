from display.abstract_display import Display, Colors, Fonts
from machine import SoftSPI, Pin
import st7789
from system import System_Manager
import vga1_8x8 as font1
import vga1_8x16 as font2
import vga1_bold_16x16 as font3
import vga1_bold_16x32 as font4
    
WIDTH = 135
HEIGHT = 240

class Color_Display(Display):

    def __init__(self, system_manager: System_Manager = None):

        # Define colors
        colors = Colors()
        colors.BLACK = st7789.BLACK
        colors.BLUE = st7789.BLUE
        colors.RED = st7789.RED
        colors.GREEN = st7789.GREEN
        colors.CYAN = st7789.CYAN
        colors.MAGENTA = st7789.MAGENTA
        colors.YELLOW = st7789.YELLOW
        colors.WHITE = st7789.WHITE

        # Define fonts, --> (Font, (width, height))
        fonts = Fonts()
        fonts.FONT1 = (font1, (8,8))
        fonts.FONT2 = (font2, (8,16))
        fonts.FONT3 = (font3, (16,16))
        fonts.FONT4 = (font4, (16,32))

        super().__init__(colors, fonts)

        spi = SoftSPI(
        baudrate=40000000,
        polarity=1,
        phase=0,
        sck=Pin(18),
        mosi=Pin(19),
        miso=Pin(13))

        self.__tft = st7789.ST7789(
            spi,
            WIDTH, # width
            HEIGHT, # height
            reset=Pin(23, Pin.OUT),
            cs=Pin(5, Pin.OUT),
            dc=Pin(16, Pin.OUT),
            backlight=Pin(4, Pin.OUT),
            rotation=1)

        self.__tft.init()
        self.__tft.fill(st7789.BLACK)


    def get_width(self) -> int: 
        return self.__tft.width()

    def get_height(self) -> int:
        return self.__tft.height()

    def clean(self): 
        self.__tft.fill(st7789.BLACK)

    def draw_pixel(self, x: int, y: int, color: Colors):
        self.__tft.pixel(x, y, color)

    def print_text(self, text: str, x: int, y: int, font: Fonts, font_color: Colors, bg_color: Colors):
        self.__tft.text(font[0], text, x, y, font_color, bg_color)

    def draw_fill_rect(self, x: int, y: int, width: int, height: int, color: Colors):
        self.__tft.fill_rect(x, y, width, height, color)

    def draw_jpg(self, x: int, y: int, filename: str):
        self.__tft.jpg(filename, x, y, st7789.SLOW)

    def power_off(self):
        self.__tft.off()

    def power_on(self):
        self.__tft.on()