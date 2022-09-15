# Author = Alejandro Palomino
# Created = March 28, 2022

from network import WLAN, STA_IF
from time import time, localtime
from input.abstract_input import Input
from machine import Timer
from micropython import const
import ntptimelib
from uthreading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from _thread import stack_size, allocate_lock
from notifier.abstract_notifier import Notifier
from umqtt.simple import MQTTClient
from time import sleep
from gc import collect

# Timers modes
TIMER_ONE_SHOT = Timer.ONE_SHOT
TIMER_PERIODIC = Timer.PERIODIC

# System Signals
SIG_SLEEP = const(0)
SIG_WAKEUP = const(1)

class __Timer:

    def __init__(self, timer_id: int, system_manager, callback, period: float, mode: TIMER_ONE_SHOT | TIMER_PERIODIC):
        self._timer_id = timer_id
        self.__system_manager = system_manager
        self.__timer = None
        self.__callback = callback
        self.__period = period
        self._mode = mode

    def __callback_timer(self, timer):
        # # Execute in other thread
        # thread = Thread(self.__system_manager, self.__callback, None, Thread.ONE_SHOT, self.__system_manager)
        # thread.start()

        # Execute on main thread
        self.__callback(self.__system_manager)

    def init(self):
        collect()
        t = Timer(self._timer_id)
        self.__timer = t
        t.init(period=self.__period, mode=self._mode, callback=self.__callback_timer)

    def deinit(self):
        collect()
        self.__timer.deinit()


class System_Manager:

    def __init__(self, ssid: str = None, password: str = None, stack_size_KiB: float = 0, timezone: int = 0):
        stack_size(int(stack_size_KiB * 1024))
        self.__wifi = None # Wifi connection object
        self.__display = None # Display object
        self.__inputs = dict() # Dict[int, Input] dictionary, key pin, value input
        self.__timers = [None,None,None,None] # List[int] list of ids of the timers, on esp32 there are timers from 0 to 3 both includes
        self.__controller = None # Controller to manage transition from views
        self.__data = dict() # Dict[str, Any]
        self.__socket = None # socket to use on the socket_task
        self.__socket_thread = None # variable to store thread of the socket in order to stop on the future
        self.__lock = allocate_lock() # Lock to syncronize threads
        self.__mqtt_client = None # instance to save mqtt client connection
        self.__mqtt_thread = None # thread that controll the mqtt process
        self.__mqtt_subscriber_callback = None # Function to call when subscriber task of mqtt is initialized
        self.__mqtt_notify_when_message_receive = False 
        self.__notifiers = list() # List of notifiers in the system
        self.__timezone = timezone # [int] Timezone
        self.__signals = {SIG_SLEEP, SIG_WAKEUP} # System signals
        self.__sleeping = False # Flag to know if the system is sleeping or not

        # Enable wifi
        if ssid is not None and password is not None: self.init_wifi(ssid, password)

    def __enable_necessary_inputs(self):
        view_signals = set()
        controller_signals = set()
        if self.__display is not None:
            view = self.__display.get_view()
            if view is not None:
                view_signals = view.get_signals()

        if self.__controller is not None:
            controller_signals = self.__controller.get_signals()

        all_signals = view_signals.union(controller_signals)
        for pin, input_system in self.__inputs.items():
            signals = input_system.get_signals()
            if len(self.__signals.intersection(signals)) > 0: continue # System signals, pass next input
            if len(signals.intersection(all_signals)) <= 0:
                input_system.disable()
            else:
                input_system.enable()

    def __refresh_display(self, clean = False):
        if self.__display is not None:
            if clean: self.__display.clean()
            self.__display.refresh()

    def __syncronize_clock(self):
        """
        Syncronize clock using ntp server
        """
        if self.wifi_isconnected():
            print("Local time before synchronization: %s" %str(localtime()))
            ntptimelib.settime()
            print("Local time after synchronization %s" %str(localtime()))

    def get_localtime(self):
        """
        Return a 8 tuple
        (year, month, day, hour, minutes, seconds, week day [0,6], year day [1,366])
        """
        return localtime()

    def get_unix_timestamp(self) -> int:
        return 946_684_800 + time() + (self.__timezone * 3600)

    def __copy_data(self) -> dict:
        copy = dict()
        for key, value in self.__data.items():
            if type(value) is list or type(value) is dict:
                copy[key] = value.copy()
            else:
                copy[key] = value
        return copy

    def get_data(self):
        self.__lock.acquire()
        data = self.__copy_data()
        self.__lock.release()
        return data

    def set_value_of_data(self, key: str, value):
        self.__lock.acquire()
        self.__data[key] = value
        self.__lock.release()

    def init_wifi(self, ssid: str, password: str):
        self.__wifi = WLAN(STA_IF) # Create wlan interface
        self.__wifi.active(True) # activate interface

        if not self.__wifi.isconnected():
            self.__wifi.active(True)
            self.__wifi.connect(ssid, password)
            end = time() + 30 # the system have 30 seconds to connect to the access point
            while not self.__wifi.isconnected() and time() < end: pass # wait until connection stabilized
        self.__syncronize_clock()

    def wifi_isconnected(self) -> bool:
        if self.__wifi == None: return False
        return self.__wifi.isconnected()

    def add_input(self, input: Input):
        for pin in input.get_pin_numbers():
            self.__inputs[pin] = input
        input.set_sys_manager(self)
        
        # The input have system signals, enable all
        if len(self.__signals.intersection(input.get_signals())) > 0:
            input.enable()
        else:
            self.__enable_necessary_inputs()

        
    def add_display(self, display):
        self.__display = display
        self.__display.set_sys_manager(self)
        self.__enable_necessary_inputs()

    def get_display(self):
        return self.__display

    def get_view_id(self) -> int:
        return self.__display.get_view().get_id()

    def send_signal(self, signal: int, data = None, refresh_display = True, enable_necessary_inputs = True):
        collect()
        if signal in self.__signals:
            if signal == SIG_SLEEP: self.sleep()
            elif signal == SIG_WAKEUP: self.wakeup() 

        elif self.__controller is not None and signal in self.__controller.get_signals():
            self.__controller.arrive_signal(signal, data = data)
            if refresh_display: self.__refresh_display()
            if enable_necessary_inputs: self.__enable_necessary_inputs()

        elif self.__display is not None and signal in self.__display.get_view().get_signals():
            self.__display.get_view().arrive_signal(signal)
            if refresh_display: self.__refresh_display()
            if enable_necessary_inputs: self.__enable_necessary_inputs()
        

        
    # Los timers no son concurrentes, la IRQ que genera se ejecuta en el hilo principal
    def create_timer(self, timer_id:int, callback, period: float, mode: TIMER_ONE_SHOT | TIMER_PERIODIC):
        """
        Create new timer if timer which timer_id is free
        Parameters
        ----------
        - timer_id (int) : id of the timer to use, possible timers_id --> [0,1,2,3]
        - callback : function to execute when timer activated, this function dont have any parameters
        - period (float) : period of the timer in milliseconds
        - mode (TIMER_ONE_SHOT | TIMER_PERIODIC)
        
        Return
        ------
        void
        """
        collect()
        if timer_id < 0 or timer_id > (len(self.__timers) - 1): return # Timer not exists
        if self.__timers[timer_id] is not None: return # Timer are in use, so we cant create it
        
        # Create timer
        t = __Timer(timer_id, self, callback, period, mode)
        t.init()
        self.__timers[timer_id] = t

    def delete_timer(self, timer_id: int):
        collect()
        timer = self.__timers[timer_id]
        if timer is None: return # Timer not exists, so do nothing
        timer.deinit()
        del timer
        self.__timers[timer_id] = None

    def add_controller(self, controller):
        self.__controller = controller
        self.__controller.set_sys_manager(self)
        self.__enable_necessary_inputs()

    def change_view(self, view):
        if self.__display is not None:
            self.__display.set_view(view)
            self.__refresh_display(clean = True)
            self.__enable_necessary_inputs()

    def create_socket_task(self, host: str, port: int, function, loop_infinity: bool):
        """
        Create a socket task using threads if server is available, otherwise the socket task will not be executed
        Parameters:
        -----------
        - host (str) : host address
        - port (int) : host port
        - function (Function<System_Manager, socket>) : Function to execute with the socket connection.
        
        Return:
        -------
        void
        """
        self.__socket = socket(AF_INET, SOCK_STREAM)
        address = (host, port)

        try:
            self.__socket.connect(address)
            thread_type = Thread.ONE_SHOT if not loop_infinity else Thread.INFINITY
            self.__socket_thread = Thread(self, function, self.delete_socket_task, thread_type, self, self.__socket)
            self.__socket_thread.start()
            
        except:
            # if error ocurr, delete task
            self.delete_socket_task()
                      

    def delete_socket_task(self):
        if self.__socket_thread is not None:
            self.__socket_thread.stop()
            self.__socket_thread = None

        if self.__socket is not None:
            try:
                self.__socket.close()
            finally:
                self.__socket = None


    def __mqtt_callback(self, topic: bytes, message: bytes):
        if self.__mqtt_notify_when_message_receive: self.notify()
        self.__mqtt_subscriber_callback(self, topic.decode("utf-8"), message.decode("utf-8"))

    def __mqtt_check_messages(self):
        """
        Check for new messages every second
        """
        self.__mqtt_client.check_msg()
        sleep(5)

    def mqtt_create_subscriber_task(self, clientID: str, ip: str, port: int, topics_and_qos, function, user: str = None, password: str = None, clean_session: bool = False, enable_notifiers: bool = False) -> bool:
        """
        Connects to the mqtt server as a subscriber. If the connection is successful it returns true, otherwise it returns false.

        Parameters:
        -----------

        - ip (str) : host address
        - port (int) : host port
        - topics_and_qos (Dict[str, int]): dicctionary where the keys are the topics to subscribe and the values the QoS
        - function (Function<System_Manager, topic: str, message: str>) : Function to execute when a message was receive from the broker
        """
        
        # Create mqtt client, connect and subscribe to topics
        try:
            
            self.__mqtt_notify_when_message_receive = enable_notifiers
            self.__mqtt_subscriber_callback = function

            self.__mqtt_client = MQTTClient(clientID, ip, port)
            self.__mqtt_client.connect(clean_session = clean_session)
            self.__mqtt_client.set_callback(self.__mqtt_callback)

            for topic, qos in topics_and_qos.items():
                print(f"Subsribe topic {topic} QoS {qos}")
                self.__mqtt_client.subscribe(topic, qos)

        except Exception as e:
            print(str(e))
            return False
        
        
        # Create a task to execute when a message was received
        self.__mqtt_thread = Thread(self, self.__mqtt_check_messages, self.mqtt_delete_subscriber_task, Thread.INFINITY)
        self.__mqtt_thread.start()

        return True

    def mqtt_delete_subscriber_task(self):
        if self.__mqtt_thread is not None:
            self.__mqtt_thread.stop()

        if self.__mqtt_client is not None:
            self.__mqtt_client.disconnect()
        
        self.__mqtt_client = None
        self.__mqtt_subscriber_callback = None
        self.__mqtt_thread = None

    def add_notifier(self, notifier: Notifier):
        self.__notifiers.append(notifier)

    def notify(self):
        for notifier in self.__notifiers:
            notifier.notify()

    def close_notify(self):
        for notifier in self.__notifiers:
            notifier.close_notify()

    def sleep(self):
        if self.__sleeping: return
        self.__display.power_off()
        # disable all inputs minus SIG_WAKEUP and SIG_SLEEP
        for _, _input in self.__inputs.items():
            if not SIG_WAKEUP in _input.get_signals() and not SIG_SLEEP in _input.get_signals():
                _input.disable()

        # disable periodic timers
        for timer in self.__timers:
            if timer is not None and timer._mode == TIMER_PERIODIC:
                timer.deinit()

        self.__sleeping = True

            
    def wakeup(self):
        if not self.__sleeping: return
        self.__display.power_on()
        # Enable periodic timers
        for timer in self.__timers:
            if timer is not None and timer._mode == TIMER_PERIODIC:
                timer.init()
        self.__enable_necessary_inputs()
        self.__sleeping = False
