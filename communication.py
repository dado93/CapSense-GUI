from datetime import datetime
import serial
import serial.tools.list_ports as list_ports
import threading
import kivy.properties
from kivy.event import EventDispatcher
import time

BOARD_DISCONNECTED = 0 
BOARD_FOUND = 1
BOARD_CONNECTED = 2

START_STREAMING_CMD = 'b'
STOP_STREAMING_CMD = 's'
TIME_SET_CMD = 't'
TIME_LATCH_CMD = 'T'

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MIPSerial(EventDispatcher, metaclass=Singleton):
    connected = kivy.properties.NumericProperty(defaultvalue=BOARD_DISCONNECTED)
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
                    else:
                        self.connected = 0

    def check_mip_port(self, port_name):
        self.message_string = 'Checking: {}'.format(port_name)
        if (not 'MIP' in port_name):
            return False
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
                    self.connected = 1
                    time.sleep(3)
                    return True
        except serial.SerialException:
            return False
        except ValueError:
            return False
        return False

    def connect(self):
        for i in range(5):
            try:
                self.port = serial.Serial(port=self.port_name, baudrate=self.baudrate)
                if (self.port.isOpen()):
                    self.message_string = 'Device connected'
                    self.connected = 2
                    time.sleep(1)
                    self.send_updated_time_to_board()
                    return 0
            except serial.SerialException:
                pass
        return 1
    
    def send_updated_time_to_board(self):
        """!
        @brief Update time and date on the board.
        
        This function send updated time and date values to the board
        by using the following packet structure:
            - First byte 't'
            - Two btyes for current year
            - One byte for month
            - One byte for day
            - One byte for hour
            - One byte for minute
            - One byte for second
            - Last byte 'T'
        """
        self.message_string = 'Sending updated time and date to device'
        # Get current time
        curr_time = datetime.now()
        self.port.write(TIME_SET_CMD.encode('utf-8'))
        # Create packet
        time_date_settings = bytearray([curr_time.year >> 8, 
                                        curr_time.year & 0xFF, 
                                        curr_time.month,
                                        curr_time.day, 
                                        curr_time.hour, 
                                        curr_time.minute, 
                                        curr_time.second])
        self.port.write(time_date_settings)
        self.port.write(TIME_LATCH_CMD.encode('utf-8'))
    
    def start_streaming(self):
        """!
        @brief Start data streaming from the board.

        This function starts data streaming from the board.
        It also sets up a running thread to retrieve the
        data from the board, parse it and send it to the
        data receivers. 
        """
        if (self.connected == BOARD_CONNECTED):
            try:
                self.port.write(START_STREAMING_CMD.encode('utf-8'))
                self.message_string = 'Starting data streaming'
                packet = self.read_data()

            except:
                self.message_string = 'Could not write command to board'
        else:
            self.message_string = 'Board is not connected'
            

    def stop_streaming(self):
        """!
        @brief Stop data streaming from the board.
        This function stops data streaming from the
        board. This function sends the appropriate command
        to the board and stops the running thread.
        """
        if (self.connected == BOARD_CONNECTED):
            try:
                self.port.write(STOP_STREAMING_CMD.encode('utf-8'))
                self.message_string = 'Stopping data streaming'
            except:
                self.message_string = 'Could not write command to board'
        else:
            self.message_string = 'Board is not connected'

    def read_data(self):
        pass