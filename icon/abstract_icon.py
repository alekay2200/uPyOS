from view.abstract_view import View

# Abstractclass
class Icon:

    # _view: View
    # _p1: Tuple[int, int]
    # _p2: Tuple[int, int]
    # _cache: Any -> To store the last value and draw it based on this

    def __init__(self, view: View, p1, p2):
        self._view = view
        self._p1 = p1
        self._p2 = p2
        self._cache = None

    # abstractmethod
    def update(self): pass

    def clean(self, color):
        width = self._p2[0] - self._p1[0]
        height = self._p2[1] - self._p1[1]
        self._view.get_display().draw_fill_rect(self._p1[0], self._p1[1], width, height, color)