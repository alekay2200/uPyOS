from display.abstract_display import Colors, Fonts
from icon.abstract_icon import Icon
from view.abstract_view import View

class Text(Icon):

    def __init__(self, view: View, p1, text: str, font: Fonts, text_color: Colors, background_color: Colors):
        (char_width, char_height) = font[1]
        super().__init__(view, p1, (p1[0] + (char_width * len(text)), p1[1] + char_height))
        self.__text = text
        self.__font = font
        self.__text_color = text_color
        self.__background_color = background_color

    def set_text(self, text: str):
        self.__text = text
        (char_width, char_height) = self.__font[1]
        self._p2 = (self._p1[0] + (char_width * len(text)), self._p1[1] + char_height)
        self.update()

    def update(self):
        self._view.get_display().print_text(self.__text, self._p1[0], self._p1[1], self.__font, self.__text_color, self.__background_color)