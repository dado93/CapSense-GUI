from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
import re
from kivy.garden.Graph import LinePlot

class GraphTabs(TabbedPanel):
    data_sample_rate = NumericProperty(0)
    temperature_sample_rate = NumericProperty(0)
    num_samples_per_second = NumericProperty(1)

    temperature_tab = ObjectProperty(None)
    resistance_tab = ObjectProperty(None)
    current_tab = ObjectProperty(None)
    humidity_tab = ObjectProperty(None)
    capacitance_tab = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GraphTabs, self).__init__(**kwargs)
        self.n_points_per_update = 10
        
    def on_data_sample_rate(self, instance, value):
        self.capacitance_tab.update_sample_rate(value)
        self.resistance_tab.update_sample_rate(value)
        self.temperature_tab.update_sample_rate(value)
        self.humidity_tab.update_sample_rate(value)
        self.current_tab.update_sample_rate(value)
    
    def on_temperature_sample_rate(self, instance, value):
        self.capacitance_tab.update_temperature_sample_rate(value)
        self.resistance_tab.update_temperature_sample_rate(value)
        self.temperature_tab.update_temperature_sample_rate(value)
        self.humidity_tab.update_temperature_sample_rate(value)
        self.current_tab.update_temperature_sample_rate(value)

    def update_plots(self, packet):
        self.capacitance_tab.update_plot(packet)
        self.temperature_tab.update_plot(packet)
        self.humidity_tab.update_plot(packet)
    
    def on_num_samples_per_second(self, instance, value):
        

class GraphPanelItem(TabbedPanelItem):
    graph = ObjectProperty(None)
    plot_settings = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GraphPanelItem, self).__init__(**kwargs)
        self.n_seconds = 60
        self.n_points_per_update = 1
        self.temp_points = []

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
        self.n_points = self.n_seconds * 1  # Number of points to plot
        self.time_between_points = (self.n_seconds)/float(self.n_points)
        self.x_points = [x for x in range(-self.n_points, 0)]
        self.y_points = [10 for y in range(-self.n_points, 0)]
        
    def on_plot_settings(self, instance, value):
        self.plot_settings.bind(n_seconds=self.graph.setter('xmin'))
        self.plot_settings.bind(ymin=self.graph.setter('ymin'))
        self.plot_settings.bind(ymax=self.graph.setter('ymax'))
    
    def update_sample_rate(self, value):
        self.plot_settings.update_sample_rate(value)
    
    def update_temperature_sample_rate(self, value):
        self.plot_settings.update_temperature_sample_rate(value)
    
    def update_plot(self, packet):
        pass

class TemperaturePlot(GraphPanelItem):
    
    def __init__(self, **kwargs):
        super(TemperaturePlot, self).__init__(**kwargs)
        self.last_temperature = 10

    def on_graph(self, instance, value):
        super(TemperaturePlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Temperature (C)'
        self.plot = LinePlot(color=(0.5, 0.4, 0.4, 1.0))
        self.plot.line_width = 2
        """
        self.y_points.append(list([0 for y in range(-self.n_points, 0)]))
        for j in range(self.n_points):
            self.x_points[j] = -self.n_seconds + \
                    j * self.time_between_points
        """
        self.plot.points = zip(self.x_points, self.y_points)
        self.graph.add_plot(self.plot)
    
    def update_plot(self, packet):
        if (not packet.has_temperature_data()):
            value = self.last_temperature
        else:
            value = packet.get_temperature()
            self.last_temperature = value
        self.temp_points.append(value)
        if (len(self.temp_points) == self.n_points_per_update):
            for val in self.temp_points:
                self.y_points.append(self.y_points.pop(0))
                self.y_points[-1] = val
            self.temp_points = []
            self.plot.points = zip(self.x_points, self.y_points)

class HumidityPlot(GraphPanelItem):
    def on_graph(self, instance, value):
        super(HumidityPlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Humidity (%)'
        self.graph.ymax = 100
        self.graph.y_ticks_minor = 5
        self.graph.y_ticks_major = 10

class CurrentPlot(GraphPanelItem):
    def on_graph(self, instance, value):
        super(CurrentPlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Current (mA)'
        self.graph.ymax = 100
        self.graph.y_ticks_minor = 5
        self.graph.y_ticks_major = 10

class CapacitancePlot(GraphPanelItem):
    pass

class ResistancePlot(GraphPanelItem):
    def on_graph(self, instance, value):
        super(ResistancePlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Resistance (kOhm)'

class PlotSettings(BoxLayout):
    seconds_spinner = ObjectProperty(None)
    autorange_cb = ObjectProperty(None)
    ymin_input = ObjectProperty(None)
    ymax_input = ObjectProperty(None)
    data_sr_label = ObjectProperty(None)
    temperature_sr_label = ObjectProperty(None)

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
    
    def update_sample_rate(self, value):
        self.data_sr_label.text = f"Data SR: {value:.1f} Hz"

    def update_temperature_sample_rate(self, value):
        self.temperature_sr_label.text = f"T&RH SR: {value:.1f} Hz"

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