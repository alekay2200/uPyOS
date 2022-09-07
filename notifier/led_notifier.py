from notifier.abstract_notifier import Notifier
from machine import Pin
from micropython import const

class Led_Notifier(Notifier):

    HIGH_LEVEL = const(1)
    LOW_LEVEL = const(0)

    def __init__(self, pin_number: int, activation_level: HIGH_LEVEL | LOW_LEVEL = HIGH_LEVEL):
        self.__activation_level = activation_level
        self.__pin = Pin(pin_number, Pin.OUT)

    def notify(self):
        self.__pin.value(self.__activation_level)

    def close_notify(self):
        level = self.LOW_LEVEL if self.__activation_level == self.HIGH_LEVEL else self.HIGH_LEVEL
        self.__pin.value(level)