"""
Classes to handle Top, Bottom, and Lateral toolbars.
"""

from mip.communication.mserial import MIPSerial
import mip.communication
import mip.widgets.dialogs as dialogs
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
import time

class BottomBar(BoxLayout):
    """
    
    """
    message_label = ObjectProperty(None)
    connection_label = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(BottomBar, self).__init__(**kwargs)
        self.board = MIPSerial()
        self.board.bind(connected=self.connection_event)

    def update_text(self, instance, value):
        self.message_label.text = value
    
    def update_str(self, value):
        self.message_label.text = value

    def connection_event(self, instance, value):
        if (value == mip.communication.mserial.BOARD_FOUND):
            self.connection_label.update_color(1, 1, 0, 0.7)
            self.connection_label.color = (0, 0, 0, 1)
        elif (value == mip.communication.mserial.BOARD_CONNECTED):
            self.connection_label.update_color(0, 0.5, 0, 0.7)
            self.connection_label.color = (1, 1, 1, 1)
        elif (value == mip.communication.mserial.BOARD_DISCONNECTED):
            self.connection_label.update_color(1, 0.0, 0, 0.7)
            self.connection_label.color = (1, 1, 1, 1)
        
class ColoredLabel(Label):
    def update_color(self, r, g, b, a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(r,g,b,a)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect,
                    size=self.update_rect)
    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size



class Toolbar(BoxLayout):
    """
    """

    """
    """
    message_string = StringProperty("")
    """
    """
    average = NumericProperty()
    """
    """
    mode = StringProperty("")

    def __init__(self, **kwargs):
        super(Toolbar, self).__init__(**kwargs)

    def sample_rate_dialog(self):
        """
        """
        self.message_string = "Sample Rate Configuration"
        self.popup = dialogs.PopupRetrieval()
        self.popup.open()
    
    def temp_rh_dialog(self):
        self.message_string = "Temperature Sensor Configuration"
        popup = dialogs.TRHConfigurationDialog()
        popup.open()

    def sd_card_dialog(self):
        self.message_string = "Configuring SD Card recording"
        popup = dialogs.SDCardDialog()
        popup.open()
    
    def is_streaming(self, instance, value):
        self.disabled = value

class TopBar(BoxLayout):
    enable_buttons = BooleanProperty(False)
    streaming_button = ObjectProperty(None)
    battery_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.ser = MIPSerial()

    def streaming(self):
        """!
        @brief Callback called on streaming button pressed.

        This function checks whether the board is currently
        streaming data or not, and based on that triggers
        the start/stop of data streaming and also 
        updates the text of the button. 
        """
        if (self.ser.is_streaming):
            self.ser.stop_streaming()
            self.streaming_button.text = 'Start'
        else:
            self.ser.start_streaming()
            self.streaming_button.text = 'Stop'


    def enable_widgets(self, enabled):
        """!
        @brief Enable/disable widgets for interaction with board.
        """
        self.streaming_button.disabled = (not enabled)
        self.battery_label.disabled = (not enabled)
        if (not enabled):
            self.battery_label.update_color(0.6,0.6,0.6)
            self.battery_label.color = (1,1,1,1)
            self.battery_label.text = f'Battery: '
    
    def update_battery_level(self, instance, value):
        self.battery_label.text = f'Battery: {value:.1f}'
        if (value >= 3.7):
            self.battery_label.update_color(0,1,0)
            self.battery_label.color = (0,0,0,1)
        elif (value >= 3.3 and value < 3.7):
            self.battery_label.update_color(1,1,0)
            self.battery_label.color = (0,0,0,1)
        else:
            self.battery_label.update_color(1,0,0)
            self.battery_label.color = (1,1,1,1)