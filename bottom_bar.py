from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class BottomBar(BoxLayout):
    message_label = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(BottomBar, self).__init__(**kwargs)

    def update_text(self, instance, value):
        self.message_label.text = value
