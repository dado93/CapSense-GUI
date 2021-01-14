from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from communication import MIPSerial
import communication

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
        popup = SampleRateDialog()
        #popup.bind(average=self.setter('average'))
        popup.open()
    
    def temp_rh_dialog(self):
        self.message_string = "Temperature Sensor Configuration"
        popup = TRHConfigurationDialog()
        #popup.bind(average=self.setter('average'))
        popup.open()
    
    def is_streaming(self, instance, value):
        self.disabled = value

class SampleRateDialog(Popup):
    data_sample_rate_spinner = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SampleRateDialog, self).__init__(**kwargs)
        self.serial = MIPSerial()

    def update(self):
        self.serial.set_sample_rate(self.data_sample_rate_spinner.text)
        self.dismiss()

class TRHConfigurationDialog(Popup):
    """
    """
    temperature_sample_rate_spinner = ObjectProperty(None)
    temperature_rep_spinner = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TRHConfigurationDialog, self).__init__(**kwargs)
        self.serial = MIPSerial()

    def update(self):
        self.serial.set_temperature_settings(self.temperature_sample_rate_spinner.text,
                                                self.temperature_rep_spinner.text)
        self.dismiss()