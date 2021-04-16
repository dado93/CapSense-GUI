from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from loguru import logger

from mip.communication.mserial import MIPSerial
import mip.communication
from mip.widgets.dialogs import ClosePopup

class ContainerLayout(BoxLayout):
    """
    Main layout used as container for the GUI.
    This is the layout that contains all GUI widgets: 
    all the main interactions among the GUI widgets is
    defined here, along with the update of the main
    progress bar showing current connection status.
    """

    top_bar = ObjectProperty(None)
    """
    Top bar widget, used to show battery status and to
    start/stop data streaming from the board.
    """
    toolbar = ObjectProperty(None)
    """
    Lateral toolbar widget, used to configure the 
    functionality of the device connected to the serial port.
    """
    bottom_bar = ObjectProperty(None)
    """
    Bottom bar widget, used to show log messages from all
    the GUI classes (widgets or non widgets).
    """
    progress_bar = ObjectProperty(None)
    """
    Progress bar widget, used to show updates on the
    current connection status to the serial port.
    """
    graph_manager = ObjectProperty(None)
    """
    Manager for graph tabs, where data received from
    the device will be shown in a real time fashion.
    """
    
    def __init__(self, **kwargs):
        self.serial = MIPSerial()
        self.serial.bind(connected=self.connection_event)
        super(ContainerLayout, self).__init__(**kwargs)
        
        # Start moving progress bar based on connection status
        self.pb_update_sign = 1
        self.pb_update_event = Clock.schedule_interval(self.progress_bar_update, 0.05)
    
    def on_toolbar(self, instance, value):
        self.serial.bind(is_streaming=self.toolbar.is_streaming)
        self.toolbar.bind(data_path=self.serial.exporter.set_output_path)
        self.toolbar.bind(data_format=self.serial.exporter.set_output_format)
        self.toolbar.bind(save_data=self.serial.exporter.setter('save_data'))
        self.toolbar.bind(custom_header=self.serial.exporter.setter('custom_header'))

    def on_bottom_bar(self, instance, value):
        #logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
        logger.add(self.bottom_bar.update_str, format="[color=7f7fff]{time:DD-MM-YYYY HH:mm:ss}[/color] | [color=ff33cc]{level}[/color] | {message}")

    def on_top_bar(self, instance, value):
        """!
        @brief Callback called when the top bar widget is ready.

        This function is called when the top bar widget is ready
        to be displayed on the screen. Here we bind the battery
        voltage property of the serial object to a callback 
        of the top bar widget, so that the battery voltage is
        updated properly.
        """
        self.serial.bind(battery_voltage=self.top_bar.update_battery_level)
    
    def on_graph_manager(self, instance, value):
        self.serial.bind(data_sample_rate=self.graph_manager.setter('data_sample_rate'))
        self.serial.bind(temperature_sample_rate=self.graph_manager.setter('temperature_sample_rate'))
        self.serial.bind(sample_rate_num_samples=self.graph_manager.setter('num_samples_per_second'))
        self.serial.add_callback(self.graph_manager.update_plots)

    def connection_event(self, instance, value):
        """
        Callback called on serial connection event.

        This callback is called when there is a connection event
        from the serial port. It is called when the board is
        found on one serial port, when the board is connected
        and when the board is disconnected.
        @param value the current connection status
        @param instance the instance calling this callback
        """
        if (value == mip.communication.mserial.BOARD_CONNECTED):
            self.progress_bar.value = 100
            self.pb_update_event.cancel()
            self.top_bar.enable_widgets(True)
            self.toolbar.disabled = False
            self.pb_update_sign = 0
        elif (value == mip.communication.mserial.BOARD_DISCONNECTED):
            self.top_bar.enable_widgets(False)
            self.toolbar.disabled = True
            if (self.pb_update_sign == 0):
                self.progress_bar.value = 0
                self.pb_update_sign = 1
                self.pb_update_event = Clock.schedule_interval(self.progress_bar_update, 0.05)

    def progress_bar_update(self, dt):
        if (self.pb_update_sign > 0):
            self.progress_bar.value += 1
            if (self.progress_bar.value == 100):
                self.pb_update_sign = -1
        else:
            self.progress_bar.value -= 1
            if (self.progress_bar.value == 0):
                self.pb_update_sign = 1