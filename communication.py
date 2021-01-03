import serial
import serial.tools.list_ports as list_ports
import threading
import kivy.properties
from kivy.event import EventDispatcher
import time

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MIPSerial(EventDispatcher, metaclass=Singleton):
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
        mip_port_found = False
        while (not mip_port_found):
            ports = list_ports.comports()
            for port in ports:
                mip_port_found = self.check_mip_port(port.device)
                if (mip_port_found):
                    self.port_name = port.device
                    if (self.connect() == 0):
                        break

    def check_mip_port(self, port_name):
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
                    self.message_string = 'Device found on port: {}'.format(port_name)
                    port.close()
                    time.sleep(1)
                    self.connected = 1
                    return True
        except serial.SerialException:
            return False
        except ValueError:
            return False
        return False

    def connect(self):
        self.port = serial.Serial(port=self.port_name, baudrate=self.baudrate)
        if (self.port.isOpen()):
            self.message_string = 'Device connected'
            self.connected = 2
            return 0