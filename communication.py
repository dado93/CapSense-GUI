from datetime import datetime
import serial
import serial.tools.list_ports as list_ports
import struct
import threading
import kivy.properties
from kivy.event import EventDispatcher
import time

#############################################
#                 Constants                 #
#############################################

# Connection status

"""!
@brief Board disconnected.
"""
BOARD_DISCONNECTED = 0 
"""!
@brief Board found but not connected.
"""
BOARD_FOUND = 1
"""!
@brief Board connected.
"""
BOARD_CONNECTED = 2

# Commands
"""!
@brief Start streaming command.
"""
START_STREAMING_CMD = 'b'

"""!
@brief Stop streaming command.
"""
STOP_STREAMING_CMD = 's'

"""!
@brief Time set command.
"""
TIME_SET_CMD = 't'

"""!
@brief Time latch command.
"""
TIME_LATCH_CMD = 'T'

"""!
@brief Temperature and relative humidity set command.
"""
TEMP_RH_SETTINGS_SET_CMD = 'x'

"""!
@brief Temperature and relative humidity latch command.
"""
TEMP_RH_SETTINGS_LATCH_CMD = 'X'

"""!
@brief Voltage packet header byte.
"""
VOLTAGE_PACKET_HEADER = 0xA0

"""!
@brief Voltage packet tail byte.
"""
VOLTAGE_PACKET_TAIL = 0xC0

"""!
@brief Data packet header byte.
"""
DATA_PACKET_HEADER = 0xA1

"""!
@brief Data packet tail byte.
"""
DATA_PACKET_TAIL = 0xC0

SAMPLE_RATE_1_HZ_CMD   = '1'
SAMPLE_RATE_10_HZ_CMD  = '2'
SAMPLE_RATE_25_HZ_CMD  = '3'
SAMPLE_RATE_50_HZ_CMD  = '4'
SAMPLE_RATE_100_HZ_CMD = '5'

GET_SAMPLE_RATE_CMD = 'w'

CONN_REQUEST_CMD = 'v'


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MIPSerial(EventDispatcher, metaclass=Singleton):
    connected = kivy.properties.NumericProperty(defaultvalue=BOARD_DISCONNECTED)
    message_string = kivy.properties.StringProperty('')
    battery_voltage = kivy.properties.NumericProperty(defaultvalue=0.0)
    data_sample_rate = kivy.properties.NumericProperty(defaultvalue=0.0)
    temperature_sample_rate = kivy.properties.NumericProperty(defaultvalue=0.0)

    def __init__(self):
        self.port_name = ""
        self.baudrate = 115200
        self.read_state = 0
        self.packet_type = ''
        self.received_packet_time = 0
        self.temperature_received_packet_time = 0
        self.samples_read = 0
        self.temp_rh_samples_read = 0
        self.is_streaming = False
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
        """!
        @brief Check if the port is the correct one.

        This function checks whether the port passed in as
        parameter correspons to a proper device.
        @param port_name name of the port to be checked.
        @return True if the port was found to be corrected.
        @return False if the port was not found to be corrected.
        """
        self.message_string = 'Checking: {}'.format(port_name)
        if (not 'MIP' in port_name):
            return False
        try:
            port = serial.Serial(port=port_name, baudrate=self.baudrate)
            if (port.is_open):
                port.write(CONN_REQUEST_CMD.encode('utf-8'))
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
                    time.sleep(1)
                    self.set_sample_rate('100 Hz')
                    # Start thread for data reading
                    read_thread = threading.Thread(target=self.read_data)
                    read_thread.daemon = True
                    read_thread.start()
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
                self.is_streaming = True
                self.samples_read = 0
                self.temp_rh_samples_read = 0
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
                self.is_streaming = False
            except:
                self.message_string = 'Could not write command to board'
        else:
            self.message_string = 'Board is not connected'

    def read_data(self):
        while True:
            if (self.port.in_waiting > 0):
                if (self.read_state == 0):
                    b = self.port.read(1)
                    # Header byte
                    b = struct.unpack('B', b)[0]
                    if (b == DATA_PACKET_HEADER or b == VOLTAGE_PACKET_HEADER):
                        self.read_state = 1
                        if (b == VOLTAGE_PACKET_HEADER):
                            self.packet_type = 'voltage'
                        else:
                            self.packet_type = 'data'
                elif (self.read_state == 1):
                    if (self.is_streaming and self.packet_type == 'data'):
                        # Get CRC packet value
                        crc = self.port.read(1)
                    elif (self.packet_type == 'voltage'):
                        temp_voltage = self.port.read(2)
                    self.read_state = 2
                elif (self.read_state == 2):
                    if (self.is_streaming and self.packet_type == 'data'):
                        # Packet counter
                        packet_counter = self.port.read(1)
                        packet_counter = struct.unpack('B',packet_counter)[0]
                        self.read_state = 3
                    elif (self.packet_type == 'voltage'):
                        voltage_end_byte = self.port.read(1)
                        voltage_end_byte = struct.unpack('B',voltage_end_byte)[0]
                        if (voltage_end_byte == VOLTAGE_PACKET_TAIL):
                            self.battery_voltage = self.convert_battery_voltage(temp_voltage)
                            self.read_state = 0
                elif (self.read_state == 3):
                    # Temperature and humidity
                    temperature_raw = self.port.read(2)
                    temperature_raw = struct.unpack('2B', temperature_raw)
                    temperature = self.convert_temperature(temperature_raw)
                    humidity_raw = self.port.read(2)
                    humidity_raw = struct.unpack('2B', humidity_raw)
                    humidity = self.convert_humidity(humidity_raw)
                    if (temperature != -45 and humidity != 0):
                        self.temp_rh_samples_read += 1
                        if (self.temp_rh_samples_read == 1):
                            self.temperature_received_packet_time = datetime.now()
                    self.read_state = 4
                elif (self.read_state == 4):
                    # Extract capdac values
                    capdac = self.port.read(4)
                    capdac = struct.unpack('4B',capdac)
                    
                    # Capacitance
                    cap = self.port.read(12)
                    cap_ch_1 = struct.unpack('3B',cap[:3])
                    cap_ch_2 = struct.unpack('3B',cap[3:6])
                    cap_ch_3 = struct.unpack('3B',cap[6:9])
                    cap_ch_4 = struct.unpack('3B',cap[9:])

                    # Convert capacitance
                    cap_ch_1 = self.convert_capacitance(cap_ch_1, capdac[0])
                    cap_ch_2 = self.convert_capacitance(cap_ch_2, capdac[1])
                    cap_ch_3 = self.convert_capacitance(cap_ch_3, capdac[2])
                    cap_ch_4 = self.convert_capacitance(cap_ch_4, capdac[3])
                    self.read_state = 5

                elif (self.read_state == 5):
                    # Current from DS2438 and aux bytes
                    current = self.port.read(2)
                    aux = self.port.read(2)
                    self.read_state = 6
                elif (self.read_state == 6):
                    end_byte = self.port.read(1)
                    end_byte = struct.unpack('B',end_byte)[0]
                    if (end_byte == DATA_PACKET_TAIL):
                        # Check CRC
                        self.read_state = 0
                        self.samples_read += 1
                        # Compute overall data sample rate
                        if (self.samples_read == 1):
                            self.received_packet_time = datetime.now()
                        if (self.samples_read > 0 and self.samples_read % 10 == 0):
                            curr_time = datetime.now()
                            diff = (curr_time - self.received_packet_time)
                            self.data_sample_rate = (self.samples_read) / diff.total_seconds()
                        # Compute temperature and humidity sample rate
                        if (self.temp_rh_samples_read >  0 and self.temp_rh_samples_read % 100 == 0):
                            curr_time = datetime.now()
                            diff = (curr_time - self.received_packet_time)
                            self.temperature_sample_rate = (self.temp_rh_samples_read) / diff.total_seconds()
                            self.temp_rh_samples_read = 0
                        # Create packet and send it to the receiver callbacks
                        packet = DataPacket(temperature=temperature,
                                                humidity=humidity,
                                                cap_ch_1=cap_ch_1,
                                                cap_ch_2=cap_ch_2,
                                                cap_ch_3=cap_ch_3,
                                                cap_ch_4=cap_ch_4,
                                                packet_counter=packet_counter)
                        #print(packet)
                    else:
                        print('Skipped one packet')
                        self.read_state = 0 
            time.sleep(0.001)

    def get_sample_rate_cmd(self, sample_rate):
        """!
        @brief Get command to set sample rate.

        This function returns the correct command to send to the
        board to set the proper sample rate.
        """
        sample_rate_dict = {
            '1 Hz': SAMPLE_RATE_1_HZ_CMD,
            '10 Hz': SAMPLE_RATE_10_HZ_CMD,
            '25 Hz': SAMPLE_RATE_25_HZ_CMD,
            '50 Hz': SAMPLE_RATE_50_HZ_CMD,
            '100 Hz': SAMPLE_RATE_100_HZ_CMD,
        }
        return sample_rate_dict[sample_rate]

    def set_sample_rate(self, sample_rate):
        """!
        @brief Send command to set sample rate on the board.
        
        This function sends the appropriate command to the board
        to set the sample rate to a new value. It then sends a 
        command to the board to retrieve the sample rate value that
        was set, that is checked inside the read data function
        and the class property is then updated accordingly.
        @param sample_rate string identifying the new sample rate to be set.
        """
        self.message_string = f'Setting sample rate to {sample_rate}'
        sample_rate_cmd = self.get_sample_rate_cmd(sample_rate)
        self.port.write(sample_rate_cmd.encode('utf-8'))

    #def get_temp_hum_sample_rate_cmd(self, th_sample_rate, th_rep):

    
    def convert_battery_voltage(self, value):
        """!
        @brief Convert raw bytes to battery voltage.

        This function converts the bytes passed in as
        parameter to a proper voltage value. The
        battery voltage is equal to the 16 bit data
        computed from the two bytes (MSB first) and
        divided by 100.
        @param value battery voltage raw values
        @return computed battery voltage
        """
        value = struct.unpack('2B', value)
        val = value[0] << 8 | value[1] 
        battery_voltage = val / 100.
        return battery_voltage
    
    def convert_temperature(self, raw_temperature):
        """!
        @brief Convert raw bytes into temperature.

        This function converts the bytes passed in as
        parameter to a proper temperature value. The 
        temperature value is computed given the
        equation stated in the SHT85 datasheet.
        @param raw_temperature temperature bytes
        @return computed temperature value
        """
        temp = raw_temperature[0] << 8 | raw_temperature[1] 
        temperature = -45 + 175 * temp / 65535
        return temperature

    def convert_humidity(self, raw_humidity):
        """!
        @brief Convert raw bytes into humidity.

        This function converts the bytes passed in as
        parameter to a proper humidity value. The 
        humidity value is computed given the
        equation stated in the SHT85 datasheet.
        @param raw_humidity humidity bytes
        @return computed humidity value
        """
        temp = raw_humidity[0] << 8 | raw_humidity[1] 
        humidity = 100 * temp / 65535
        return humidity

    def convert_capacitance(self, capacitance, capdac):
        """!
        @brief Convert raw bytes and capdac value into capacitance.

        This function converts the bytes passed in as
        parameter to a proper capacitance value based
        on capdac settings. The capacitance value is 
        computed given the equation stated in the FDC1004Q datasheet.
        @param capacitance capacitance bytes
        @param capdac capacitance channel capdac value
        @return computed capacitance value
        """
        capacitance = capacitance[0] << 16 | capacitance[1] << 8 | capacitance[2]
        capacitance = capacitance / (2<<18)
        capacitance = capacitance + capdac * 3.125
        return capacitance

class DataPacket():
    """!
    @brief Data packet holding data received from board.
    """
    def __init__(self, packet_counter = 0,
                        temperature = 0, 
                        humidity = 0, 
                        cap_ch_1 = 0, 
                        cap_ch_2 = 0,
                        cap_ch_3 = 0,
                        cap_ch_4 = 0,
                        current = 0,
                        aux = 0,
                        has_temp_data=False):
        self.packet_counter = packet_counter
        self.temperature = temperature
        self.humidity = humidity
        self.capacitance_values = [cap_ch_1, cap_ch_2, cap_ch_3, cap_ch_4]
        self.current = current
        self.aux = aux
    
    def __str__(self):
        st = f"[{self.packet_counter}] - {self.temperature:.2f} - "
        st += f"{self.humidity:.2f} - {self.capacitance_values}"
        return st
                