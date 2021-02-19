

from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher

from datetime import datetime
import json
from loguru import logger
from pathlib import Path

PACKET_BUFFER_MAX_DIM = 10

class CSVExporter(EventDispatcher):
    save_data = BooleanProperty(False)

    def __init__(self):
        logger.debug('Data Exporter Initialized')
        self.load_export_settings()
        self.packet_list = []
    
    def on_save_data(self, instance, value):
        logger.debug(value)
    
    def load_export_settings(self):
        if (Path('settings.json').exists()):
            with open('settings.json', 'r') as f:
                settings_json = json.load(f)
                self.save_data = settings_json['save_data']
                self.data_format = settings_json['data_format']
                self.data_path = Path(settings_json['data_path'])
                if (self.data_format == 'csv'):
                    self.delim = ','
                else:
                    self.delim = ' '
        else:
            self.save_data = False
            self.data_path = Path.cwd() / 'Data'
            self.data_format = 'txt'
            self.delim = ' '
            if (not self.data_path.exists()):
                self.data_path.mkdir(parents=True, exist_ok=True)

    def set_output_path(self, instance, path):
        if (Path(path).exists()):
            self.data_path = Path(path)
            logger.debug(f'Saving data in {self.data_path}')
        else:
            self.data_path = Path.cwd() / 'Data'
            logger.debug(f'Path does not exist. Saving data in {self.data_path}')
    
    def set_output_format(self, instance, data_format):
        if (data_format != 'txt' and data_format != 'csv'):
            logger.critical(f'{data_format} is not a valid format. Using txt instead.')
            self.data_format = 'txt'
            self.delim = ' '
        else:
            self.format = data_format
            logger.debug(f'Saving data in {self.format} format')
            if (self.data_format == 'csv'):
                self.delim = ','
            else:
                self.delim = ' '

    def is_streaming(self, instance, streaming):
        print(streaming)
        if (streaming):
            self.packet_list = []
            self.init_file()
        else:
            self.close_file()

    def init_file(self):
        curr_time = datetime.now()
        self.file_name = datetime.strftime(curr_time, "%Y%m%d_%H%M%S") + '.' + self.data_format
        self.file_name = self.data_path /self.file_name
        if (self.save_data):
            self.write_header()

    def write_header(self):
        header = ''
        header += "Packet_ID"
        header += self.delim
        header += "Temperature"
        header += self.delim
        header += "Humidity"
        header += self.delim
        header += "Ch 1"
        header += self.delim
        header += "Ch 2"
        header += self.delim
        header += "Ch 3"
        header += self.delim
        header += "Ch 4"
        header += '\n'
        with open(self.file_name, 'a') as f:
            f.write(header)

    def add_packet(self, packet):
        if (self.save_data):
            self.packet_list.append(packet)
            if (len(self.packet_list) == PACKET_BUFFER_MAX_DIM):
                for packet_temp in self.packet_list:
                    self.write_packet(packet_temp)
                self.packet_list = []

    def write_packet(self, packet):
        row = ''
        row += str(packet.get_packet_counter())
        row += self.delim
        if not (packet.has_temperature_data()):
            row += ''
            row += self.delim
            row += ''
        else:
            row += str(packet.get_temperature())
            row += self.delim
            row += str(packet.get_humidity())
        row += self.delim
        cap_values = packet.get_capacitance_array()
        for idx, capacitance in enumerate(cap_values):
            row += str(capacitance)
            if (idx < (len(cap_values) - 1)):
                row += self.delim
        row += '\n'
        with open(self.file_name, 'a') as f:
            f.write(row)

    def close_file(self):
        if (len(self.packet_list) > 0 and self.save_data):
            for packet_temp in self.packet_list:
                self.write_packet(packet_temp)