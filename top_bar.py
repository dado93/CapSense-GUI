from communication import MIPSerial
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

class TopBar(BoxLayout):
    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.ser = MIPSerial()

    def start_streaming(self):
        self.ser.start_streaming()

    def stop_streaming(self):
        self.ser.stop_streaming()