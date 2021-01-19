import os
os.environ["KIVY_NO_ARGS"] = "1"
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

class PopupRetrieval(Popup):
    retrieval_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PopupRetrieval, self).__init__(**kwargs)
        self.pb_update_sign = 1
        self.pb_update_event = Clock.schedule_interval(self.update_progress_bar, timeout=0.01)
        Clock.schedule_once(self.retrieval_completed, timeout=1)
    
    def on_retrieval_label(self, instance, value):
        pass

    def update_progress_bar(self, dt):
        if (self.pb_update_sign > 0):
            self.pb_update.value += 1
            if (self.pb_update.value == 100):
                self.pb_update_sign = -1
        else:
            self.pb_update.value -= 1
            if (self.pb_update.value == 0):
                self.pb_update_sign = 1

    def retrieval_completed(self, dt):
        self.pb_update_event.cancel()

class SampleRateDialog(PopupRetrieval):
    update_widget = ObjectProperty(None)
    pb_update = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.serial = MIPSerial()
        self.serial.retrieve_sample_rate_from_board()
        super(SampleRateDialog, self).__init__(**kwargs)
        
    def on_retrieval_label(self, instance, value):
        self.retrieval_label.text = 'Retrieving sample rate'

    def retrieval_completed(self, dt):
        super(SampleRateDialog, self).retrieval_completed(dt)
        self.sample_rate_selection = SampleRateSelection()
        self.sample_rate_selection.data_sample_rate_spinner.values = self.serial.available_sample_rates
        self.sample_rate_selection.data_sample_rate_spinner.text = self.serial.configured_sample_rate
        self.content = self.sample_rate_selection
        self.sample_rate_selection.dismiss_button.bind(on_release=self.dismiss)
        self.sample_rate_selection.update_button.bind(on_release=self.update)
    
    def update(self, instance):
        self.serial.set_sample_rate(self.sample_rate_selection.data_sample_rate_spinner.text)
        time.sleep(0.5)
        self.serial.retrieve_sample_rate_from_board()
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


class SampleRateSelection(GridLayout):
    data_sample_rate_spinner = ObjectProperty(None)
    dismiss_button = ObjectProperty(None)
    update_button = ObjectProperty(None)

class SDCardDialog(Popup):
    """
    """

    def __init__(self, **kwargs):
        super(SDCardDialog, self).__init__(**kwargs)
        #self.serial = MIPSerial()

    def update(self):
        #self.serial.set_temperature_settings(self.temperature_sample_rate_spinner.text,
        #                                        self.temperature_rep_spinner.text)
        self.dismiss()

