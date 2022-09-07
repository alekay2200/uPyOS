from display import abstract_display as abc_display

# Abstractclass
class View:

    # _display: Display
    # _icons: List[Icon]
    # _data: Dict[str, Any]
    # _id: view id to identify the view
    # _signals: Set[int] Set of signals which this view can receive

    def __init__(self, id: int, display: abc_display.Display, signals):
        self._id = id
        self._display = display
        self._icons = list()
        self._signals = signals

    # abstractmethod
    def arrive_signal(self, signal: int): pass

    def refresh(self):
        for icon in self._icons:
            icon.update()

    def get_display(self) -> abc_display.Display:
        return self._display

    def get_id(self) -> int:
        return self._id

    def get_signals(self):
        return self._signals