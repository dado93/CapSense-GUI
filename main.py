from kivy.app import App
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
    
    def __init__(self, **kwargs):
        self.serial = MIPSerial()
        super(ContainerLayout, self).__init__(**kwargs)
    
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

class MIPBoard(App):
    def build(self):
        return ContainerLayout()

MIPBoard().run()