from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
import re

class GraphTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(GraphTabs, self).__init__(**kwargs)

class GraphPanelItem(TabbedPanelItem):
    graph = ObjectProperty(None)
    plot_settings = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GraphPanelItem, self).__init__(**kwargs)
        self.n_seconds = 30

    def on_graph(self, instance, value):
        self.graph.xmin = -self.n_seconds
        self.graph.xmax = 0
        self.graph.xlabel = 'Time (s)'
        self.graph.ylabel = 'Capacitance (pF)'
        self.graph.x_ticks_minor = 1
        self.graph.x_ticks_major = 5
        self.graph.y_ticks_minor = 1
        self.graph.y_ticks_major = 5
        self.graph.x_grid_label = True
        self.graph.ymin = 0
        self.graph.ymax = 10
        self.graph.y_grid_label = True
    
    def on_plot_settings(self, instance, value):
        self.plot_settings.bind(n_seconds=self.graph.setter('xmin'))
        self.plot_settings.bind(ymin=self.graph.setter('ymin'))
        self.plot_settings.bind(ymax=self.graph.setter('ymax'))

class TemperaturePlot(GraphPanelItem):
    def on_graph(self, instance, value):
        super(TemperaturePlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Temperature (C)'

class HumidityPlot(GraphPanelItem):
    def on_graph(self, instance, value):
        super(HumidityPlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Humidity (%)'
        self.graph.ymax = 100
        self.graph.y_ticks_minor = 5
        self.graph.y_ticks_major = 10

class CapacitancePlot(GraphPanelItem):
    pass

class PlotSettings(BoxLayout):
    seconds_spinner = ObjectProperty(None)
    autorange_cb = ObjectProperty(None)
    ymin_input = ObjectProperty(None)
    ymax_input = ObjectProperty(None)
    n_seconds = NumericProperty(0)
    
    ymin = NumericProperty(0)
    ymax = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(PlotSettings, self).__init__(**kwargs)
        self.n_seconds = 30

    def on_seconds_spinner(self, instance, value):
        self.seconds_spinner.bind(text=self.spinner_updated)

    def on_autorange_cb(self, instance, value):
        self.autorange_cb.bind(active=self.autorange_changed)
    
    def on_ymin_input(self, instance, value):
        self.ymin_input.bind(enter_pressed=self.axis_changed)
    
    def on_ymax_input(self, instance, value):
        self.ymax_input.bind(enter_pressed=self.axis_changed)
    
    def spinner_updated(self, instance, value):
        self.n_seconds = -int(self.seconds_spinner.text)

    def autorange_changed(self, instance, value):
        self.ymin_input.disabled = value
        self.ymax_input.disabled = value

    def axis_changed(self, instance, focused):
        if (not focused):
            if (not ((self.ymin_input.text == '') or (self.ymax_input.text == ''))):
                self.ymin = float(self.ymin_input.text)
                self.ymax = float(self.ymax_input.text)
            elif (self.ymin_input.text == ''):
                self.ymin_input.text = f"{self.ymin:.2f}"
            elif (self.ymax_input.text == ''):
                self.ymax_input.text = f"{self.ymax:.2f}"

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    enter_pressed = BooleanProperty(None)
    
    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.bind(focus=self.on_focus)
        self.multiline = False

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)
    
    def on_focus(self, instance, value):
        self.enter_pressed = value