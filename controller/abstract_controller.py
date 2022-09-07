# Abstractclass
from system import System_Manager


class Controller:

    # __signals: Set[int]
    # __system_manager: System_Manager

    def __init__(self, signals):
        self._signals = signals
        self._system_manager = None

    def get_signals(self):
        return self._signals

    def set_sys_manager(self, system_manager: System_Manager):
        self._system_manager = system_manager

    # abstractmethod
    def arrive_signal(self, signal: int, data = None):
        pass