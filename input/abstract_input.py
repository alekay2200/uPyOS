class Input:

    # __pin_numbers: Set<int>
    # __signals: Set[int]

    def __init__(self, pin_numbers, signals, init_value):
        """
        Parameters
        ----------

        handler: function to execute when irq activated
        trigger: when to launch the irq
        """
        self._pin_numbers = pin_numbers
        self._system_manager = None
        self._signals = signals
        self._enable = False
        self._last_value = init_value

    # abstractmethod
    def get_value(self): pass

    # abstractmethod
    def enable(self): pass

    # abstractmethod
    def disable(self): pass

    def get_pin_numbers(self):
        return self._pin_numbers

    def set_sys_manager(self, system_manager):
        self._system_manager = system_manager

    def get_signals(self):
        return self._signals

    # abstractmethod
    def _irq(self, pin): pass