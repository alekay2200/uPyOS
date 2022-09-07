from notifier.buzzer_notifier import Buzzer_Notifier
from notifier.led_notifier import Led_Notifier
from constants.signals import SIG_PUSH, SIG_BACK, SIG_NEXT, SIG_CLOCK
from input.rotary_encoder import Encoder
from system import System_Manager, TIMER_PERIODIC, SIG_SLEEP, SIG_WAKEUP
from display.color_display import Color_Display
from view.home_view import Home_View
from time import sleep
from input.button import Button, IRQ_FALLING
from time import sleep


SSID = None
PASSWORD = None
MQTT_SERVER = ""
MQTT_PORT = 1884


def mqtt_message(sys: System_Manager, topic: str, msg: str):
    print("Message from topic: ", topic)
    print("Message: ", msg)

def update_clock(sys: System_Manager):
    sys.send_signal(SIG_CLOCK, enable_necessary_inputs=False)


# Create notifiers
green_led = Led_Notifier(32)
buzzer = Buzzer_Notifier(25, 500, 512, 0.5)

# Define topics
topics = {
    "test/uPyOS" : 2,
}

# Create components
display = Color_Display()

# Create inputs
button = Button(17, IRQ_FALLING, SIG_PUSH)
encoder = Encoder(2, 15, 5, SIG_BACK, SIG_NEXT, pull_up=True)
btn_on = Button(0, IRQ_FALLING, SIG_WAKEUP)
btn_off = Button(35, IRQ_FALLING, SIG_SLEEP)


# Create system manager
sys = System_Manager(ssid=SSID, password=PASSWORD, stack_size_KiB=8, timezone=-2)

# add componentes to system manager
sys.add_display(display)
sys.add_input(encoder)
sys.add_input(button)
sys.add_input(btn_on)
sys.add_input(btn_off)

# Add notifiers
sys.add_notifier(buzzer)
sys.add_notifier(green_led)
sys.close_notify()

# Create initial view
home = Home_View(display)

# Set view to system
sys.change_view(home)

# Create a timer
sys.create_timer(0, update_clock, 1000, TIMER_PERIODIC)

# # Create mqtt task
# res = sys.mqtt_create_subscriber_task("esp32", MQTT_SERVER, MQTT_PORT, topics, mqtt_message, clean_session=True, enable_notifiers=False)
# if res:
#     print("MQTT conection successful")
# else:
#     print("Error coneccting to MQTT server")

# Enable for debug proposals
while True:
    print("...")
    sleep(4)