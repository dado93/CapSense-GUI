"""
Main file to run the MIP GUI.
"""
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from mip.widgets.container import ContainerLayout
import random
import mip.widgets.dialogs
from kivy.core.window import Window

Config.set('kivy', 'exit_on_escape', '0')
Config.set('kivy', 'desktop', '1')
Config.set('kivy', 'allow_screensaver', '0')

Builder.load_file('mip/widgets/toolbars.kv')
Builder.load_file('mip/widgets/dialogs.kv')
Builder.load_file('mip/widgets/graph_tabs.kv')
Builder.load_file('mip/widgets/container.kv')

class MIPBoard(App):

    def __init__(self, **kwargs):
        super(MIPBoard, self).__init__(**kwargs)
        self.exit_check_opened = False

    def build(self):
        Window.bind(on_request_close=self.exit_check)
        return ContainerLayout()
    
    def exit_check(self, *args):
        if (not self.exit_check_opened):
            popup = mip.widgets.dialogs.ClosePopup()
            popup.open()
            popup.bind(ok_button_pressed=self.stop)
            popup.bind(on_dismiss=self.close_popup_dismissed)
            self.exit_check_opened = True
        return True
    
    def close_popup_dismissed(self, instance):
        self.exit_check_opened = False

if __name__ == '__main__':
    MIPBoard().run()