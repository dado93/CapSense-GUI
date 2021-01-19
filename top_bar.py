from mip.communication.mserial import MIPSerial
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class TopBar(BoxLayout):
    enable_buttons = BooleanProperty(False)
    streaming_button = ObjectProperty(None)
    battery_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.ser = MIPSerial()

    def streaming(self):
        """!
        @brief Callback called on streaming button pressed.

        This function checks whether the board is currently
        streaming data or not, and based on that triggers
        the start/stop of data streaming and also 
        updates the text of the button. 
        """
        if (self.ser.is_streaming):
            self.ser.stop_streaming()
            self.streaming_button.text = 'Start'
        else:
            self.ser.start_streaming()
            self.streaming_button.text = 'Stop'


    def enable_widgets(self, enabled):
        """!
        @brief Enable/disable widgets for interaction with board.
        """
        self.streaming_button.disabled = (not enabled)
        self.battery_label.disabled = (not enabled)
        if (not enabled):
            self.battery_label.update_color(0.6,0.6,0.6)
            self.battery_label.color = (1,1,1,1)
            self.battery_label.text = f'Battery: '
    
    def update_battery_level(self, instance, value):
        self.battery_label.text = f'Battery: {value:.1f}'
        if (value >= 3.7):
            self.battery_label.update_color(0,1,0)
            self.battery_label.color = (0,0,0,1)
        elif (value >= 3.3 and value < 3.7):
            self.battery_label.update_color(1,1,0)
            self.battery_label.color = (0,0,0,1)
        else:
            self.battery_label.update_color(1,0,0)
            self.battery_label.color = (1,1,1,1)

class TopBarColoredLabel(Label):
    def update_color(self, r, g, b):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(r,g,b,1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect,
                    size=self.update_rect)
    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size