from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout

from mip.communication.mserial import MIPSerial
import mip.communication

import time

import mip.widgets.dialogs as dialogs

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

