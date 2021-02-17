from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
import re
from mip.graph import LinePlot
from kivy.uix.tabbedpanel import TabbedPanelHeader
from decimal import Decimal
from math import pow, isclose
from kivy.graphics import Color, Rectangle

class GraphManager(TabbedPanel):
    data_sample_rate = NumericProperty(0)
    temperature_sample_rate = NumericProperty(0)
    num_samples_per_second = NumericProperty(1)

    def __init__(self, **kwargs):
        super(GraphManager, self).__init__(**kwargs)
        self.n_points_per_update = 10
        self.tabs_dict = {
            'Capacitance': CapacitancePlot(n_plots=4, color=[(0.5,0.1,0.1,1),
                                                    (0.1,0.5,0.1,1),
                                                    (0.1, 0.1, 0.5, 1),
                                                    (0.5, 0.1, 0.5, 1)],
                                            legend=['Ch 1', 'Ch 2','Ch 3','Ch 4']),
            'Resistance': ResistancePlot(),
            'Temperature': TemperaturePlot(color=(0.5,0.1,0.1,1), legend='Temperature'),
            'Humidity': HumidityPlot(color=(0.5,0.1,0.1,1), legend='Humidity'),
            'Current': CurrentPlot()
        }
        for tab in self.tabs_dict.keys():
            # Create panel
            th = TabbedPanelHeader(text=tab)
            th.content = self.tabs_dict[tab]
            self.add_widget(th)
            # Bind data sample rate
            self.bind(data_sample_rate=self.tabs_dict[tab].setter('data_sample_rate'))
            # Bind temperature and humidity sample rate
            self.bind(temperature_sample_rate=self.tabs_dict[tab].setter('temperature_sample_rate'))
            self.bind(num_samples_per_second=self.tabs_dict[tab].setter('num_samples_per_second'))

    def update_plots(self, packet):
        """

        """
        self.tabs_dict['Temperature'].update_plot(packet.get_temperature(), 
                                            valid_data=packet.has_temperature_data())
        self.tabs_dict['Humidity'].update_plot(packet.get_humidity(),
                                            valid_data=packet.has_temperature_data())
        self.tabs_dict['Capacitance'].update_plot(packet.get_capacitance_array())

class GraphPanelItem(BoxLayout):
    graph = ObjectProperty(None)
    plot_settings = ObjectProperty(None)
    data_sample_rate = NumericProperty(0)
    temperature_sample_rate = NumericProperty(0)
    num_samples_per_second = NumericProperty(1)
    ymin = NumericProperty(0)
    ymax = NumericProperty(10)
    xmin = NumericProperty(-60)
    autoscale = BooleanProperty(False)

    def __init__(self, n_plots=1, color=(0.5, 0.4, 0.4, 0.1), legend=[], **kwargs):
        self.max_seconds = self.xmin * (-1)
        self.n_points_per_update = self.num_samples_per_second
        self.n_plots = n_plots
        if (not isinstance(color, list)):
            self.color =[color]
        else:
            self.color = color
        if (not isinstance(legend, list)):
            self.legend =[legend]
        else:
            self.legend = legend
        self.temp_points = [[] for _ in range(self.n_plots)]
        self.y_points = [[] for _ in range(self.n_plots)]
        self.plots = []
        super(GraphPanelItem, self).__init__(**kwargs)

    def on_graph(self, instance, value):
        self.graph.xmin = self.xmin
        self.graph.xmax = 0
        self.graph.xlabel = 'Time (s)'
        self.graph.ylabel = 'Capacitance (pF)'
        self.graph.x_ticks_minor = 1
        self.graph.x_ticks_major = 5
        self.graph.y_ticks_minor = 1
        self.graph.y_ticks_major = 5
        self.graph.x_grid_label = True
        self.graph.ymin = self.ymin
        self.graph.ymax = self.ymax
        self.graph.y_grid_label = True
        self.n_points = self.max_seconds * self.num_samples_per_second  # Number of points to plot
        self.time_between_points = (self.max_seconds)/float(self.n_points)
        self.x_points = [x for x in range(-self.n_points, 0)]
        for j in range(self.n_points):
            self.x_points[j] = -self.max_seconds + j * self.time_between_points
        for plot_index in range(self.n_plots):
            self.y_points[plot_index] = [0 for y in range(-self.n_points, 0)]
            if plot_index > len(self.color):
                color = self.color[0]
            else:
                color = self.color[plot_index]
            #print(color)
            plot = LinePlot(color=color)
            plot.line_width = 2
            plot.points = zip(self.x_points, self.y_points[plot_index])
            self.plots.append(plot)
            self.graph.add_plot(self.plots[plot_index])

    def on_plot_settings(self, instance, value):
        self.plot_settings.bind(n_seconds=self.setter('xmin'))
        self.plot_settings.bind(ymin=self.setter('ymin'))
        self.plot_settings.bind(ymax=self.setter('ymax'))
        self.plot_settings.bind(autorange_selected=self.setter('autoscale'))
        for plot_index in range(self.n_plots):
            if ( (plot_index <= (len(self.legend) - 1)) and (plot_index <= (len(self.color) - 1)) ):
                self.plot_settings.add_legend_entry(self.legend[plot_index], self.color[plot_index])
    
    def on_ymin(self, instance, value):
        self.graph.ymin = value
        min_val, max_val, major_ticks, minor_ticks = self.get_bounds_and_ticks(self.ymin, self.ymax,10)
        self.graph.y_ticks_major = major_ticks
        self.graph.y_ticks_minor = minor_ticks

    def on_ymax(self, instance, value):
        self.graph.ymax = value
        min_val, max_val, major_ticks, minor_ticks = self.get_bounds_and_ticks(self.ymin, self.ymax,10)
        self.graph.y_ticks_major = major_ticks
        self.graph.y_ticks_minor = minor_ticks

    def on_xmin(self, instance, value):
        self.graph.xmin = value
        min_val, max_val, major_ticks, minor_ticks = self.get_bounds_and_ticks(value, 0, 10)
        self.graph.x_ticks_major = major_ticks
        self.graph.x_ticks_minor = minor_ticks

    def on_data_sample_rate(self, instance, value):
        self.plot_settings.update_sample_rate(value)
    
    def on_temperature_sample_rate(self, instance, value):
        self.plot_settings.update_temperature_sample_rate(value)
    
    def update_plot(self, value, valid_data=True):
        if (not isinstance(value, list)):
            values = [value]
        else:
            values = value
        for plot_index in range(self.n_plots):
            self.temp_points[plot_index].append(values[plot_index])
            if (len(self.temp_points[plot_index]) == self.n_points_per_update):
                for val in self.temp_points[plot_index]:
                    self.y_points[plot_index].append(self.y_points[plot_index].pop(0))
                    self.y_points[plot_index][-1] = val
                self.temp_points[plot_index] = []
                self.plots[plot_index].points = zip(self.x_points, self.y_points[plot_index])

        global_y_min = []
        global_y_max = []
        if (self.autoscale):
            for plot_index in range(self.n_plots):
                # Slice only the visible part
                if (abs(self.graph.xmin) < self.max_seconds):
                    y_points_slice = self.y_points[plot_index][(self.max_seconds-abs(self.graph.xmin)) * self.num_samples_per_second:]       
                else:
                    y_points_slice = self.y_points[plot_index]
                    
                global_y_min.append(min(y_points_slice))
                global_y_max.append(max(y_points_slice))
            
            y_min = min(global_y_min)
            y_max = max(global_y_max)
            min_val, max_val, major_ticks, minor_ticks = self.get_bounds_and_ticks(y_min, y_max, 10)
            self.graph.ymin = min_val
            self.graph.ymax = max_val
            self.graph.y_ticks_major = major_ticks
            self.graph.y_ticks_minor = minor_ticks

    def on_num_samples_per_second(self, instance, value):
        self.n_points = self.max_seconds * self.num_samples_per_second  # Number of points to plot
        self.x_points = [x for x in range(-self.n_points, 0)]
        self.time_between_points = (self.max_seconds)/float(self.n_points)
        for j in range(self.n_points):
            self.x_points[j] = -self.max_seconds + j * self.time_between_points
        if (self.num_samples_per_second < 30):
            self.n_points_per_update = 1
        else:
            self.n_points_per_update = 10
        for plot in range(self.n_plots):
            self.y_points[plot] = [0 for y in range(-self.n_points, 0)]
            self.plots[plot].points = zip(self.x_points, self.y_points[plot])

    def fexp(self, number):
        (sign, digits, exponent) = Decimal(number).as_tuple()
        return len(digits) + exponent - 1

    def fman(self, number):
        return float(Decimal(number).scaleb(-self.fexp(number)).normalize())

    def get_bounds_and_ticks(self, minval, maxval, nticks):
        # amplitude of data
        amp = maxval - minval
        # basic tick
        basictick = self.fman(amp/float(nticks))
        # correct basic tick to 1,2,5 as mantissa
        tickpower = pow(10.0, self.fexp(amp/float(nticks)))
        if basictick < 1.5:
            tick = 1.0*tickpower
            suggested_minor_tick = 4
        elif basictick >= 1.5 and basictick < 2.5:
            tick = 2.0*tickpower
            suggested_minor_tick = 4
        elif basictick >= 2.5 and basictick < 7.5:
            tick = 5.0*tickpower
            suggested_minor_tick = 5
        elif basictick >= 7.5:
            tick = 10.0*tickpower
            suggested_minor_tick = 4
        # calculate good (rounded) min and max
        goodmin = tick * (minval // tick)
        if not isclose(maxval % tick,0.0):
            goodmax = tick * (maxval // tick +1)
        else:
            goodmax = tick * (maxval // tick)
        return goodmin, goodmax, tick, suggested_minor_tick

class TemperaturePlot(GraphPanelItem):
    
    def __init__(self, **kwargs):
        super(TemperaturePlot, self).__init__(**kwargs)
        self.last_temperature = 10

    def on_graph(self, instance, value):
        super(TemperaturePlot, self).on_graph(instance, value)
        print(self.color)
        self.graph.ylabel = 'Temperature (C)'
        self.graph.ymax = 30
        self.graph.ymin = 5
        
    
    def update_plot(self, value, valid_data):
        if (not valid_data):
            value = self.last_temperature
        else:
            self.last_temperature = value
        super(TemperaturePlot, self).update_plot(value)


class HumidityPlot(GraphPanelItem):
    def __init__(self, **kwargs):
        super(HumidityPlot, self).__init__(**kwargs)
        self.last_humidity = 0

    def on_graph(self, instance, value):
        super(HumidityPlot, self).on_graph(instance, value)
        self.graph.ylabel = 'Humidity (%)'
        self.graph.ymax = 100
        self.graph.y_ticks_minor = 5
        self.graph.y_ticks_major = 10

    
    def update_plot(self, value, valid_data):
        if (not valid_data):
            value = self.last_humidity
        else:
            self.last_humidity = value
        super(HumidityPlot, self).update_plot(value)

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
    legend = ObjectProperty(None)

    n_seconds = NumericProperty(0)
    ymin = NumericProperty(0)
    ymax = NumericProperty(0)

    autorange_selected = BooleanProperty(False)
    
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
        self.autorange_selected = value

    def axis_changed(self, instance, focused):
        if (not focused):
            if (not ((self.ymin_input.text == '') or (self.ymax_input.text == ''))):
                y_min = float(self.ymin_input.text)
                y_max = float(self.ymax_input.text)
                if (y_min >= y_max):
                    self.ymin_input.text = f"{self.ymin:.2f}"
                    self.ymax_input.text = f"{self.ymax:.2f}"
                else:
                    self.ymin = y_min
                    self.ymax = y_max
            elif (self.ymin_input.text == ''):
                self.ymin_input.text = f"{self.ymin:.2f}"
            elif (self.ymax_input.text == ''):
                self.ymax_input.text = f"{self.ymax:.2f}"
    
    def update_sample_rate(self, value):
        self.data_sr_label.text = f"Data SR: {value:.1f} Hz"

    def update_temperature_sample_rate(self, value):
        self.temperature_sr_label.text = f"T&RH SR: {value:.1f} Hz"

    def add_legend_entry(self, label, color):
        entry = LegendEntry()
        entry.set_legend_label(label)
        entry.set_legend_color(color)
        self.legend.add_widget(entry)

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    enter_pressed = BooleanProperty(None)
    
    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.bind(focus=self.on_focus)
        self.multiline = False

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if ( (len(self.text) == 0) and substring == '-'):
            s = '-'
        else:
            if '.' in self.text:
                s = re.sub(pat, '', substring)
            else:
                s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)
    
    def on_focus(self, instance, value):
        self.enter_pressed = value


class LegendEntry(BoxLayout):
    legend_label = ObjectProperty(None)
    legend_color = ObjectProperty(None)

    def set_legend_label(self, label):
        self.legend_label.text = label

    def set_legend_color(self, color):
        self.legend_color.update_color(color[0], color[1], color[2], color[3])

class LegendLabel(Label):
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