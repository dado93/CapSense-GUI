"""
Main file to run the MIP GUI.
"""
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from mip.widgets.container import ContainerLayout
import random

Config.set('kivy', 'exit_on_escape', '0')
Config.set('kivy', 'desktop', '1')
Config.set('kivy', 'allow_screensaver', '0')

Builder.load_file('mip/widgets/toolbars.kv')
Builder.load_file('mip/widgets/dialogs.kv')
Builder.load_file('mip/widgets/graph_tabs.kv')
Builder.load_file('mip/widgets/container.kv')


class MIPBoard(App):
    def build(self):
        return ContainerLayout()

if __name__ == '__main__':
    MIPBoard().run()