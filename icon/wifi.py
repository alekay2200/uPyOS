from icon.abstract_icon import Icon
from view.abstract_view import View

class Wifi(Icon):

    def __init__(self, view: View, p1, p2):
        super().__init__(view, p1, p2)

    def __connected(self) -> bool:
        return self._view.get_display().get_sys_manager().wifi_isconnected()

    def update(self):
        color = self._view.get_display().get_colors().GREEN
        c = self.__connected()
        if not self.__connected():
            color = self._view.get_display().get_colors().RED

        # if state not change, dont draw
        if self._cache is not None and self._cache == c: return

        # draw icon
        self._view.get_display().draw_fill_rect(self._p1[0], self._p1[1], self._p2[0] - self._p1[0], self._p2[1] - self._p1[1], color)
        
        # upate connection state
        self._cache = c

    def clean(self):
        self._view.get_display().draw_fill_rect(self._p1[0], self._p1[1], self._p2[0] - self._p1[0], self._p2[1] - self._p1[1], self._view.get_display().get_colors().BLACK)