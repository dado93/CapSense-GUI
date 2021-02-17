from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from mip.communication.mserial import MIPSerial
import time

class PopupRetrieval(Popup):
    """
    The PopupRetrieval class can be used as a base class for all
    the popups that need to retrieve data from the board and require
    some time to perform the retrieval operation.

    It implements sevaral methods that the sub classes can further 
    implement to perform the desired operations.

    Args:
        - retrieval_timeout: the total timeout to wait for retrieval completion.

    Usage:
    >>> class SampleRatePopup(PopupRetrieval):
    ...     def __init__(self, **kwargs):
    ...         super(SampleRatePopup, self).__init__(**kwargs)
    """

    spinner_layout = ObjectProperty(None)
    """
    The spinner_layout is a grid layout holding all the
    couples of labels and spinners from which the user
    can select the settings to be set.
    """

    message_label = ObjectProperty(None)
    """
    Simple label to show popup messages in the popup.
    """

    ok_button = ObjectProperty(None)
    """
    Button that can be clicked after a successfull setting
    of the configuration.
    """

    def __init__(self, retrieval_timeout = 1, **kwargs):
        super(PopupRetrieval, self).__init__(**kwargs)
        self.pb_update_sign = 1
        self.pb_update_event = Clock.schedule_interval(self.update_progress_bar, timeout=0.01)
        Clock.schedule_once(self.retrieval_completed, timeout=retrieval_timeout)

    def update_progress_bar(self, dt):
        """
        This function is used to show a progress bar update
        during the retrieval of data. It must be called
        from a scheduler with an appropriate interval
        to show a smooth increase/decrease of the progress 
        bar value.

        Args:
            - dt
        """
        if (self.pb_update_sign > 0):
            self.pb_update.value += 1
            if (self.pb_update.value == 100):
                self.pb_update_sign = -1
        else:
            self.pb_update.value -= 1
            if (self.pb_update.value == 0):
                self.pb_update_sign = 1

    def retrieval_completed(self, dt):
        """
        This function is called when the timeout for
        retrieval expires. Subclasses can implement here
        the desired checks and additional code to show
        custom widgets in the popup.
        """
        self.pb_update_event.cancel()
        self.pb_update.value = 100
        self.update_button.disabled = False
        self.spinner_layout.disabled = False
        self.message_label.text = 'Retrieval completed'
    
    def start_checking(self, check_timeout=1):
        """
        Start the clock timeout to check the 
        successfull configuration. 

        Args:
            - check_timeout: the timeout for the checking.
        """
        # Widgets enable/disable
        self.ok_button.disabled = True
        self.update_button.disabled = True
        self.spinner_layout.disabled = True
        # Message label configuration
        self.message_label.text = 'Checking data'
        # Progress bar update
        self.pb_update_sign = 1
        self.pb_update_event = Clock.schedule_interval(self.update_progress_bar, timeout=0.01)
        Clock.schedule_once(self.checking_completed, timeout=check_timeout)

    def checking_completed(self, dt):
        """
        Callback called when the checking is completed.
        The subclasses should implement here the check 
        and call either `checking_success` or `checking_fail`
        to determine the behaviour of the widget.
        """
        self.pb_update.value = 100
        self.pb_update_event.cancel()
        self.spinner_layout.disabled = False
        self.update_button.disabled = False

    def checking_success(self):
        """
        Configuration check was succesfull, enable
        OK button.
        """
        self.message_label.text = 'Checking succesfull'
        self.ok_button.disabled = False
        
    def checking_fail(self):
        """
        Configuration check failed, disable OK button.
        """
        self.ok_button.disabled = True
        self.message_label.text = 'Checking failed'

    def update(self):
        """
        The update function must be properly implemented by
        the subclasses according to the desired actions.
        """
        pass

class SampleRateDialog(PopupRetrieval):

    def __init__(self, **kwargs):
        self.serial = MIPSerial()
        self.serial.retrieve_sample_rate_from_board()
        self.title = 'Sample Rate'
        super(SampleRateDialog, self).__init__(**kwargs)

    def on_spinner_layout(self, instance, value):
        self.spinner_layout.add_widget(Label(text='Sample Rate'))   
        self.data_sample_rate_spinner = Spinner(values=self.serial.available_sample_rates)
        self.spinner_layout.add_widget(self.data_sample_rate_spinner)    
    
    def retrieval_completed(self, dt):
        super(SampleRateDialog, self).retrieval_completed(dt)
        self.data_sample_rate_spinner.text = self.serial.configured_sample_rate

    def checking_completed(self, dt):
        super(SampleRateDialog, self).checking_completed(dt)
        if (self.serial.configured_sample_rate == self.data_sample_rate_spinner.text):
            self.checking_success()
        else:
            self.checking_fail()
    
    def update(self):
        self.serial.set_sample_rate(self.data_sample_rate_spinner.text)
        time.sleep(0.01)
        self.serial.retrieve_sample_rate_from_board()
        self.start_checking()

class TRHConfigurationDialog(PopupRetrieval):
    
    def __init__(self, **kwargs):
        self.serial = MIPSerial()
        self.serial.retrieve_sample_rate_from_board()
        self.title = 'Temperature Sensor'
        super(TRHConfigurationDialog, self).__init__(**kwargs)

    def on_spinner_layout(self, instance, value):
        self.spinner_layout.add_widget(Label(text='T&RH Sample Rate'))   
        self.sample_rate_spinner = Spinner(values=self.serial.available_temp_rh_sample_rates)
        self.spinner_layout.add_widget(self.sample_rate_spinner)
        self.spinner_layout.add_widget(Label(text='T&RH Repeatability'))   
        self.rep_spinner = Spinner(values=['Low', 'Med', 'High'])
        self.spinner_layout.add_widget(self.rep_spinner)    
    
    def retrieval_completed(self, dt):
        super(TRHConfigurationDialog, self).retrieval_completed(dt)
        self.sample_rate_spinner.text = self.serial.configured_temp_rh_sample_rate
        self.rep_spinner.text = self.serial.configured_temp_rh_sample_rep

    def checking_completed(self, dt):
        super(TRHConfigurationDialog, self).checking_completed(dt)
        if (self.serial.configured_temp_rh_sample_rate == self.sample_rate_spinner.text):
            if (self.serial.configured_temp_rh_sample_rep == self.rep_spinner.text):
                self.checking_success()
            else:
                self.checking_fail()
        else:
            self.checking_fail()
    
    def update(self):
        self.serial.set_temperature_settings(self.sample_rate_spinner.text, self.rep_spinner.text)
        time.sleep(0.01)
        self.serial.retrieve_sample_rate_from_board()
        self.start_checking()


class SDCardDialog(Popup):
    """
    """
    rec_min_spinner = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SDCardDialog, self).__init__(**kwargs)
        self.serial = MIPSerial()

    def update(self):
        self.serial.set_sd_card_rec_minutes(self.rec_min_spinner.text)
        self.dismiss()

class ExportDialog(Popup):
    data_export_cb = ObjectProperty(None)
    data_format_spinner = ObjectProperty(None)
    ok_button = ObjectProperty(None)
    folder_button = ObjectProperty(None)
    folder_path = ObjectProperty(None)
    folder_path_scroll = ObjectProperty(None)
    
    folder_path_value = StringProperty('')
    save_data = BooleanProperty(False)
    data_format = StringProperty('txt')
    ok_pressed = BooleanProperty(False)

    def set_settings(self, save_data, data_format='txt', data_path='/Data'):
        if (save_data):
            self.data_export_cb.active = True
        self.data_format_spinner.text = data_format
        self.folder_path.text = data_path

    def on_data_export_cb(self, instance, value):
        self.data_export_cb.bind(active=self.data_export_cb_changed)
    
    def on_data_format_spinner(self, instance, value):
        self.data_format_spinner.bind(text=self.setter('data_format'))

    def data_export_cb_changed(self, instance, value):
        self.data_format_spinner.disabled = not value
        self.folder_button.disabled = not value
        self.save_data = value
        self.folder_path_scroll.disabled = not value
    
    def folder_selection(self):
        popup = FolderPickerDialog()
        popup.open()
        popup.bind(folder_path=self.setter('folder_path_value'))
    
    def on_folder_path_value(self, instance, value):
        self.folder_path.text = value

    def update(self):
        self.ok_pressed = True
        self.dismiss()

class FolderPickerDialog(Popup):
    filechooser = ObjectProperty(None)
    folder_path = StringProperty('')

    def folder_selected(self):   
        self.folder_path = self.filechooser.path
        self.dismiss() 


class ClosePopup(Popup):
    ok_button_pressed = BooleanProperty(False)

    def ok_pressed(self):
        self.ok_button_pressed = True
        self.dismiss()

    def cancel_pressed(self):
        self.dismiss()
