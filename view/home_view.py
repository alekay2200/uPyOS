from icon.battery import Battery
from icon.wifi import Wifi
from view.abstract_view import View
from display.abstract_display import Display
from icon.text import Text
from constants.signals import SIG_CLOCK

class Home_View(View):

    def __init__(self, display: Display):
        signals = {SIG_CLOCK}
        super().__init__(1, display, signals)

        clock_time = self.__get_time()
        
        self._icons.append(Text(self, (57, 68), clock_time, self._display.get_fonts().FONT4, self._display.get_colors().WHITE, self._display.get_colors().BLACK))
        self._icons.append(Battery(self, (10, 10), (60, 25)))
        self._icons.append(Wifi(self, (self._display.get_width() - 20, 5), (self.get_display().get_width() - 10, 25)))

    def __get_time(self) -> str:
        datetime = self._display.get_sys_manager().get_localtime()
        hour = str(datetime[3])
        minutes = str(datetime[4])
        seconds = str(datetime[5])
        if len(hour) < 2: hour = "0" + hour
        if len(minutes) < 2: minutes = "0" + minutes
        if len(seconds) < 2: seconds = "0" + seconds
        return f"{hour}:{minutes}:{seconds}"

    def arrive_signal(self, signal):
        if signal == SIG_CLOCK:
            self._icons[0].set_text(self.__get_time())