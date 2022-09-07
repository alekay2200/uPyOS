from machine import Pin
from input.abstract_input import Input

IRQ_FALLING = Pin.IRQ_FALLING
IRQ_RISING = Pin.IRQ_RISING

class Button(Input):

    # __pin = Pin
    # __trigger = IRQ_FALLING | IRQ_RISING
    # _pin_numbers: Set<int>
    # _trigger: IRQ_TRIGGER --> IRQ_FALLING | IRQ_RISING
    # _signla: int

    def __init__(self, pin_numbers, trigger, signal):
        """
        Parameters
        ----------

        handler: function to execute when irq activated
        trigger: when to launch the irq
        """
        super().__init__({pin_numbers}, {signal}, None)
        self.__pin = Pin(pin_numbers, Pin.IN, Pin.PULL_UP)
        self.__trigger = trigger

    def get_value(self):
        return None

    def enable(self):
        if not self._enable:
            self.__pin.irq(self._irq, self.__trigger)
            self._enable = True
        
    def disable(self):
        if self._enable:
            self.__pin.irq(handler = None) 
            self._enable = False

    def _irq(self, pin):
        if self._system_manager is not None:
            signal = next(iter(self._signals))
            self.disable()
            self._system_manager.send_signal(signal, data = None)
            self.enable()