from view.abstract_view import View
from icon.abstract_icon import Icon

class Battery(Icon):

    def __init__(self, view: View, p1, p2):
        super().__init__(view, p1, p2)
        self.__first_init = True


    def __get_battery_percent(self) -> float:
        """
        Return Battery percent

        Return
        ------

        float [0,1]
        """
        return 0.59
    

    def update(self):
        percent = self.__get_battery_percent()

        if self._cache is not None and percent == self._cache: return # If level not change, dont draw

        color = self._view.get_display().get_colors().GREEN
        if percent <= 0.3: color = self._view.get_display().get_colors().YELLOW
        if percent <= 0.1: color = self._view.get_display().get_colors().RED
        
        
        # Draw first part of the battery icon
        height = int((self._p2[1] - self._p1[1]) * 0.25)
        width = int((self._p2[0] - self._p1[0]) * 0.10)
        p1 = (self._p1[0], self._p1[1] + height)
        p2 = (self._p1[0] + width, self._p2[1] - height)

        if self.__first_init:
            self._view.get_display().draw_fill_rect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1], self._view.get_display().get_colors().WHITE)

        # Get points begin at the end of first part of the icon
        p1 = (p2[0], self._p1[1])
        p2 = self._p2

        if self.__first_init:
            # Fill battery
            self._view.get_display().draw_fill_rect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1], self._view.get_display().get_colors().WHITE)

        # Draw a black rectangle inside
        height = int((self._p2[1] - self._p1[1]) * 0.1)
        width = int((self._p2[0] - self._p1[0]) * 0.1)
        p1 = (p1[0] + width, p1[1] + height)
        p2 = (p2[0] - width, p2[1] - height)

        self._view.get_display().draw_fill_rect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1], self._view.get_display().get_colors().BLACK)

        # Fill battery depend on percent
        width = p2[0] - p1[0]
        delta_width = width - int(width * percent)
        p1 = (p1[0] + delta_width, p1[1])

        self._view.get_display().draw_fill_rect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1], color)

        # draw percent next to battery icon
        x = self._p2[0] + 5
        y = self._p1[1] # ((self._p2[1] - self._p1[1]) // 2) + self._p1[1]
        self._view.get_display().print_text(str(round(percent * 100)) + "%", x, y, self._view.get_display().get_fonts().FONT2, self._view.get_display().get_colors().WHITE, self._view.get_display().get_colors().BLACK)

        self._cache = percent
        if self.__first_init: self.__first_init = False