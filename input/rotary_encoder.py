from input.abstract_input import Input
from input.encoder_lib.rotary_irq_esp import RotaryIRQ

class Encoder(Input):

    # __pin_numbers: Set<int>
    # __handler: Function(Pin)
    # __trigger: IRQ_TRIGGER --> IRQ_FALLING | IRQ_RISING
    # __signals: Set[int]
    # __encoder: Encoder object from library

    def __init__(self, pin_a, pin_b, max_val, signal_rot_left: int, signal_rot_right: int, pull_up = False):
        """
        Parameters
        ----------

        handler: function to execute when irq activated
        trigger: when to launch the irq
        pull_up: True use internal resistor of esp32, false do not use it (you have to add external pull up resistor)
        """
        self.__encoder = RotaryIRQ( pin_num_clk=pin_a,
                                    pin_num_dt=pin_b,
                                    min_val=0,
                                    max_val=max_val,
                                    reverse=False,
                                    pull_up=pull_up,
                                    range_mode=RotaryIRQ.RANGE_UNBOUNDED)

        super().__init__({pin_a, pin_b}, {signal_rot_left, signal_rot_right}, self.__encoder.value())
        self.__signal_rot_left = signal_rot_left
        self.__signal_rot_right = signal_rot_right
        

    def get_value(self):
        return self.__encoder.value()

    def enable(self):
        if not self._enable:
            self.__encoder.add_listener(self._irq)
            self._enable = True

    def disable(self):
        if self._enable:
            self.__encoder.remove_listener(self._irq)
            self._enable = False

    def _irq(self, pin):
        if self._system_manager is not None:
            current = self.get_value()
            
            if current > self._last_value:
                signal = self.__signal_rot_right
            else:
                signal = self.__signal_rot_left
                
            self._system_manager.send_signal(signal, data = [current, self._last_value])
            self._last_value = current