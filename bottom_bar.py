from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from communication import MIPSerial
import communication
from kivy.graphics import Color, Rectangle

class BottomBar(BoxLayout):
    message_label = ObjectProperty(None)
    connection_label = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(BottomBar, self).__init__(**kwargs)
        self.board = MIPSerial()
        self.board.bind(connected=self.connection_event)

    def update_text(self, instance, value):
        self.message_label.text = value

    def connection_event(self, instance, value):
        if (value == communication.BOARD_FOUND):
            self.connection_label.update_color(1, 1, 0, 0.7)
            self.connection_label.color = (0, 0, 0, 1)
        elif (value == communication.BOARD_CONNECTED):
            self.connection_label.update_color(0, 0.5, 0, 0.7)
            self.connection_label.color = (1, 1, 1, 1)
        elif (value == communication.BOARD_DISCONNECTED):
            self.connection_label.update_color(1, 0.0, 0, 0.7)
            self.connection_label.color = (1, 1, 1, 1)
        
class ColoredLabel(Label):
    def update_color(self, r, g, b, a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(r,g,b,a)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect,
                    size=self.update_rect)
    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size