from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

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

    def sample_avg_dialog(self):
        """
        """
        self.message_string = "Samples Average Configuration"
        popup = SampleAverageDialog()
        popup.bind(average=self.setter('average'))
        popup.open()

class SampleAverageDialog(Popup):
    average = NumericProperty()
    avg_samples_sinner = ObjectProperty(None)

    def spinner_updated(self):
        self.average = int(self.avg_samples_sinner.text)
        print(f'Average Samples {self.average}')