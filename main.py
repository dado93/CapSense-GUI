from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from communication import MIPSerial

Builder.load_file('toolbar.kv')
Builder.load_file('bottom_bar.kv')
Builder.load_file('dialogs.kv')
Builder.load_file('top_bar.kv')
Builder.load_file('graph_tabs.kv')

class ContainerLayout(BoxLayout):
    
    toolbar = ObjectProperty(None)
    bottom_bar = ObjectProperty(None)
    progress_bar = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        self.serial = MIPSerial()
        super(ContainerLayout, self).__init__(**kwargs)
        # Start moving progress bar
        self.pb_update_sign = 1
        self.pb_update_event = Clock.schedule_interval(self.progress_bar_update, 0.05)
    
    def on_toolbar(self, instance, value):
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
    
    def progress_bar_update(self, dt):
        if (self.serial.connected == 2):
            self.progress_bar.value = 100
            self.pb_update_event.cancel()

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