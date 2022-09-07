from _thread import start_new_thread, exit as t_exit
from micropython import const

class Thread:

    ONE_SHOT = const(0)
    INFINITY = const(1)

    def __init__(self, system_manager, function, stop_function, t: ONE_SHOT | INFINITY, *args):
        self.__function = function
        self.__system_manager = system_manager
        self.__args = args
        self.__type = t
        self.__active = True
        self.__stop_function = stop_function

    def __thread_function(self, *args):
        # execute thread function
        while self.__active:
            self.__function(*args)
            if self.__type == Thread.ONE_SHOT:
                self.stop()
        # terminate thread
        if self.__stop_function is not None:
            self.__stop_function()
        t_exit()

    def start(self):
        start_new_thread(self.__thread_function, self.__args)

    def stop(self):
        self.__active = False

    def is_active(self) -> bool:
        return self.__active