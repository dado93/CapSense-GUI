from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

import communication
from communication import MIPSerial

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
Config.set('kivy', 'desktop', '1')
Config.set('kivy', 'allow_screensaver', '0')

Builder.load_file('toolbar.kv')
Builder.load_file('bottom_bar.kv')
Builder.load_file('dialogs.kv')
Builder.load_file('top_bar.kv')
Builder.load_file('graph_tabs.kv')

class ContainerLayout(BoxLayout):
    
    top_bar = ObjectProperty(None)
    toolbar = ObjectProperty(None)
    bottom_bar = ObjectProperty(None)
    progress_bar = ObjectProperty(None)
    graph_tabs = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        self.serial = MIPSerial()
        self.serial.bind(connected=self.connection_event)
        super(ContainerLayout, self).__init__(**kwargs)
        Window.bind(on_request_close=self.exit_check)
        # Start moving progress bar based on connection status
        self.pb_update_sign = 1
        self.pb_update_event = Clock.schedule_interval(self.progress_bar_update, 0.05)
    
    def exit_check(self, *args):
        print('Exit check')
        return False

    def on_toolbar(self, instance, value):
        self.serial.bind(is_streaming=self.toolbar.is_streaming)
        try:
            self.toolbar.bind(message_string=self.bottom_bar.update_text)
        except:
            pass
    
    def on_bottom_bar(self, instance, value):
        try:
            self.toolbar.bind(message_string=self.bottom_bar.update_text)
            self.serial.bind(message_string=self.bottom_bar.update_text)
        except:
            raise

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
    
    def on_graph_tabs(self, instance, value):
        self.serial.bind(data_sample_rate=self.graph_tabs.setter('data_sample_rate'))
        self.serial.bind(temperature_sample_rate=self.graph_tabs.setter('temperature_sample_rate'))
        self.serial.bind(sample_rate_num_sampels=self.graph_tabs.setter('num_samples_per_second'))
        self.serial.add_callback(self.graph_tabs.update_plots)

    def connection_event(self, instance, value):
        """!
        @brief Callback called on serial connection event.

        This callback is called when there is a connection event
        from the serial port. It is called when the board is
        found on one serial port, when the board is connected
        and when the board is disconnected.
        @param value the current connection status
        @param instance the instance calling this callback
        """
        if (value == communication.BOARD_CONNECTED):
            self.progress_bar.value = 100
            self.pb_update_event.cancel()
            self.top_bar.enable_widgets(True)
            self.toolbar.disabled = False
            self.pb_update_sign = 0
        elif (value == communication.BOARD_DISCONNECTED):
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

class MIPBoard(App):
    def build(self):
        return ContainerLayout()

MIPBoard().run()