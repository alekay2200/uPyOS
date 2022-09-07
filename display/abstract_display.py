from system import System_Manager

class Colors:
    BLACK = None
    BLUE = None
    RED = None
    GREEN = None
    CYAN = None
    MAGENTA = None
    YELLOW = None
    WHITE = None

class Fonts:
    FONT1 = None
    FONT2 = None
    FONT3 = None
    FONT4 = None

# Abstractclass
class Display:

    # _view: View
    # _colors: Colors
    # _fonts: Fonts
    # __system_manager: System_Manager

    def __init__(self, colors: Colors, fonts: Fonts):
        self.__system_manger = None
        self._view = None
        self._colors = colors
        self._fonts = fonts

    def get_sys_manager(self) -> System_Manager:
        return self.__system_manger

    def set_sys_manager(self, system_manager):
        self.__system_manger = system_manager

    def get_view(self):
        """
        Return current view or None if the display doesn't have any view attached
        
        Return
        ------

        Union[View, None]
        """
        return self._view

    def set_view(self, view):
        """
        Attach given view to the display
        
        Return
        ------

        void
        """
        del self._view
        self._view = view


    def get_colors(self) -> Colors:
        return self._colors

    def get_fonts(self) -> Fonts:
        return self._fonts
    
    # abstractmethod
    def get_width(self) -> int: pass

    # abstractmethod
    def get_height(self) -> int: pass

    def refresh(self):
        """
        Re-draw the current view

        Return
        ------

        void
        """
        if self._view: self._view.refresh()

    # abstractmethod
    def clean(self): 
        """
        Clean all drawn elements on the screen
        
        Return
        ------

        void
        """
        pass

    # abstractmethod
    def draw_pixel(self, x: int, y: int, color: Colors): 
        """
        Draws the pixel from (x,y) coordinate with the given color

        Parameters
        ----------

        - x (int) : x-axis coordinate
        - y (int) : y-axis coordinate
        - color (Any) : pixel color, the type of the parameter depends on the specific screen. On black and white screens this parameter is not used
        
        Return
        ------

        void
        """
        pass

    # abstractmethod
    def print_text(self, text: str, x: int, y: int, font: Fonts, font_color: Colors, bg_color: Colors): 
        """
        Prints the give text starting at (x,y) coordinate

        Parameters
        ----------

        - text (str) : text to print
        - x (int) : x-axis coordinate
        - y (int) : y-axis coordinate
        - font (Font) : size of the font
        - font_color (Union[Color, Any]) : text color
        - bg_color (Union[Color, Any]) : text background color
        
        Return
        ------

        void
        """
        pass

    # abstractmethod
    def draw_fill_rect(self, x: int, y: int, width: int, height: int, color: Colors):
        """
        Prints solid rectangle

        Parameters
        ----------

        - x (int) : x-axis coordinate
        - y (int) : y-axis coordinate
        - width (int) : rectangle width
        - height (int) : rectangle height
        - color (Any) : rectangle color

        
        Return
        ------

        void
        """
        pass

    # abstractmethod  
    def draw_jpg(self, x: int, y: int, filename: str):
        """
        Draw a jpg image

        Parameters
        ----------

        - x (int) : x-axis coordinate
        - y (int) : y-axis coordinate
        - filename (str) : path to file, ej. folder1/folder2/image.jpg

        
        Return
        ------

        void
        """
        pass

    # abstractmethod
    def power_off(self):
        """
        turn off the screen

        Return
        ------

        void
        """
        pass
    
    # abstractmethod
    def power_on(self):
        """
        turn on the screen

        Return
        ------

        void
        """
        pass