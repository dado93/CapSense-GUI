import serial
import serial.tools.list_ports as list_ports
import threading
import kivy.properties
from kivy.event import EventDispatcher
import time

class MAXSerial(EventDispatcher):
    connected = kivy.properties.NumericProperty(defaultvalue=0)
    message_string = kivy.properties.StringProperty('')
    sensor_is_present = kivy.properties.BooleanProperty(False)
    revision_id = kivy.properties.NumericProperty(0xFF)
    part_id = kivy.properties.NumericProperty(0xFF)

    def __init__(self):
        self.port_name = ""
        self.baudrate = 115200
        find_port_thread = threading.Thread(target=self.find_port, daemon=True)
        find_port_thread.start()
    
    def find_port(self):
        max_port_found = False
        while (not max_port_found):
            ports = list_ports.comports()
            for port in ports:
                max_port_found = self.check_max_port(port.device)
                if (max_port_found):
                    self.port_name = port.device
                    if (self.connect() == 0):
                        break

    def check_max_port(self, port_name):
        self.message_string = 'Checking: {}'.format(port_name)
        try:
            port = serial.Serial(port=port_name, baudrate=self.baudrate)
            if (port.is_open):
                port.write('v'.encode('utf-8'))
                time.sleep(2)
                received_string = ''
                while (port.in_waiting > 0):
                    received_string += port.read().decode('utf-8', errors='replace')
                if ('$$$' in received_string):
                    self.message_string = 'Device found on port: {}'.format(portname)
                    port.close()
                    time.sleep(1)
                    self.connected = 1
                    return True
        except serial.SerialException:
            return False
        except ValueError:
            return False
        return False