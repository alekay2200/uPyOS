from notifier.abstract_notifier import Notifier
from machine import Pin, PWM
from uthreading import Thread
from _thread import allocate_lock
from time import sleep

# PKMCS0909E4000-R1 Buzzer
class Buzzer_Notifier(Notifier):

    def __init__(self, pin_number: int, freq: int, duty: int, secs: int):
        """
        duty: valor de 0 a 1023 que representa el porcentage de ciclo de trabajo
        secs: tiempo que sonará en segundos
        """
        self.__freq = freq
        self.__duty = duty
        self.__pin_number = pin_number
        self.__secs = secs
        self.__pwm = None
        self.__lock = allocate_lock()
        self.__sounding = False

    def __is_sounding(self):
        self.__lock.acquire()
        is_sounding = self.__sounding
        self.__lock.release()
        return is_sounding

    def __set_sounding(self, sounding: bool):
        self.__lock.acquire()
        self.__sounding = sounding
        self.__lock.release()

    def __thread_task(self):
        self.__pwm = PWM(Pin(self.__pin_number, Pin.OUT), freq = self.__freq, duty = self.__duty)
        sleep(self.__secs)


    def notify(self):
        if not self.__is_sounding(): 
            self.__set_sounding(True)
            Thread(None, self.__thread_task, self.close_notify, Thread.ONE_SHOT).start()
        #self.__pwm = Pin(self.__pin_number, Pin.OUT, freq = self.__freq, duty = self.__duty)

    def close_notify(self):
        if self.__pwm is not None: self.__pwm.deinit()
        self.__pwm = None
        self.__set_sounding(False)