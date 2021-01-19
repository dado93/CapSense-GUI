import os
os.environ["KIVY_NO_ARGS"] = "1"
from datetime import datetime
import serial
import serial.tools.list_ports as list_ports
import struct
import threading
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.event import EventDispatcher
import time
from loguru import logger

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

SAMPLE_RATE_1_HZ_CMD   = '1'
SAMPLE_RATE_10_HZ_CMD  = '2'
SAMPLE_RATE_25_HZ_CMD  = '3'
SAMPLE_RATE_50_HZ_CMD  = '4'
SAMPLE_RATE_100_HZ_CMD = '5'

RETRIEVE_SAMPLE_RATE_CMD = 'w'

CONN_REQUEST_CMD = 'v'

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

"""!
@brief Sample rate packet header byte.
"""
SAMPLE_RATE_PACKET_HEADER = 0xA3

"""!
@brief Sample rate packet tail byte.
"""
SAMPLE_RATE_PACKET_TAIL = 0xC3


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MIPSerial(EventDispatcher, metaclass=Singleton):
    connected = NumericProperty(defaultvalue=BOARD_DISCONNECTED)
    message_string = StringProperty('')
    battery_voltage = NumericProperty(defaultvalue=0.0)
    data_sample_rate = NumericProperty(defaultvalue=0.0)
    temperature_sample_rate = NumericProperty(defaultvalue=0.0)
    is_streaming = BooleanProperty(False)
    configured_sample_rate = StringProperty('')
    sample_rate_num_samples = NumericProperty(defaultvalue=0)
    configured_temp_rh_sample_rate = StringProperty('')
    configured_temp_rh_sample_rep = StringProperty('')

    def __init__(self):
        self.port_name = ""
        self.baudrate = 115200
        self.read_state = 0
        self.packet_type = ''
        self.voltage_received_packet_time = 0
        self.received_packet_time = 0
        self.temperature_received_packet_time = 0
        self.samples_read = 0
        self.temp_rh_samples_read = 0
        self.callbacks = []
        self.available_sample_rates = ['1 Hz', '10 Hz', '25 Hz', '50 Hz', '100 Hz']
        self.available_temp_rh_sample_rates = ['0.5 Hz','1 Hz', '2 Hz', '4 Hz', '10 Hz']
        find_port_thread = threading.Thread(target=self.find_port, daemon=True)
        find_port_thread.start()

    def add_callback(self, callback):
        if (callback not in self.callbacks):
            self.callbacks.append(callback)

    def find_port(self):
        """!
        @brief Find the serial port to which the device is connected.

        This function scans all the available serial ports until
        the one to which the device is connected is found. Once
        found, it attempts to connect to it.
        """
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
                    self.connected = BOARD_CONNECTED
                    time.sleep(1)
                    self.send_updated_time_to_board()
                    time.sleep(0.5)
                    self.retrieve_sample_rate_from_board()
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
                self.received_packet_time = 0
                self.temperature_received_packet_time = 0
                self.temp_rh_samples_read = 0
                self.data_sample_rate = '0.00'
                self.temperature_sample_rate = '0.00'
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
                self.read_state = 0
            except:
                self.message_string = 'Could not write command to board'
        else:
            self.message_string = 'Board is not connected'

    def read_data(self):
        while (self.connected == BOARD_CONNECTED):
            # Check if more than 10 seconds passed from last voltage packet
            if (self.voltage_received_packet_time != 0):
                curr_time = datetime.now()
                if ((curr_time - self.voltage_received_packet_time).total_seconds() > 13):
                    print(curr_time)
                    print(self.voltage_received_packet_time)
                    self.connected = BOARD_DISCONNECTED
                    self.message_string = 'Device disconnected'
                    find_port_thread = threading.Thread(target=self.find_port, daemon=True)
                    find_port_thread.start()
                    
            
            if (self.port.in_waiting > 0):
                if (self.read_state == 0):
                    b = self.port.read(1)
                    # Header byte
                    b = struct.unpack('B', b)[0]
                    if (b == DATA_PACKET_HEADER or b == VOLTAGE_PACKET_HEADER or b == SAMPLE_RATE_PACKET_HEADER):
                        self.read_state = 1
                        if (b == VOLTAGE_PACKET_HEADER):
                            self.packet_type = 'voltage'
                            self.voltage_received_packet_time = datetime.now()
                        elif (b == SAMPLE_RATE_PACKET_HEADER):
                            self.packet_type = 'sample rate'
                        else:
                            self.packet_type = 'data'
                elif (self.read_state == 1):
                    if (self.packet_type == 'data'):
                        # Get CRC packet value
                        crc = self.port.read(1)
                    elif (self.packet_type == 'voltage'):
                        temp_voltage = self.port.read(2)
                    elif (self.packet_type == 'sample rate'):
                        temp_sample_rate = self.port.read(3)
                    self.read_state = 2
                elif (self.read_state == 2):
                    if (self.packet_type == 'data'):
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
                    elif (self.packet_type == 'sample rate'):
                        sample_rate_end_byte = self.port.read(1)
                        sample_rate_end_byte = struct.unpack('B',sample_rate_end_byte)[0]
                        if (sample_rate_end_byte == SAMPLE_RATE_PACKET_TAIL):
                            self.parse_sample_rate(temp_sample_rate)
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
                        has_temperature_data = True
                    else:
                        has_temperature_data = False
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
                        self.update_computed_sample_rate()
                        # Create packet and send it to the receiver callbacks
                        packet = DataPacket(temperature=temperature,
                                                humidity=humidity,
                                                cap_ch_1=cap_ch_1,
                                                cap_ch_2=cap_ch_2,
                                                cap_ch_3=cap_ch_3,
                                                cap_ch_4=cap_ch_4,
                                                packet_counter=packet_counter,
                                                has_temp_data = has_temperature_data)
                        for callback in self.callbacks:
                            callback(packet)
                    else:
                        print('Skipped one packet')
                        self.read_state = 0 
            time.sleep(0.001)

    def parse_sample_rate(self, sample_rate_packet):
        sample_rate_packet = struct.unpack('3B', sample_rate_packet)
        if (sample_rate_packet[0] < len(self.available_sample_rates)):
            self.configured_sample_rate = self.available_sample_rates[sample_rate_packet[0]]
            self.message_string = f'Current sample rate: {self.configured_sample_rate}'
            self.compute_num_samples_sample_rate(self.configured_sample_rate)
        else:
            self.message_string = 'Error in received sample rate'
        self.configured_temp_rh_sample_rate, self.configured_temp_rh_sample_rep = self.get_temp_hum_config_value(sample_rate_packet[1], 
                                                                                                                sample_rate_packet[2])

    def compute_num_samples_sample_rate(self, sample_rate):
        # Get only the first part of the string --> frequency
        frequency = sample_rate.split(' ')[0]
        print(frequency)
        self.sample_rate_num_samples = int(frequency)

    def update_computed_sample_rate(self):
        # Compute overall data sample rate
        if (self.samples_read == 1):
            self.received_packet_time = datetime.now()
        if (self.samples_read > 0 and self.samples_read % 10 == 0):
            curr_time = datetime.now()
            diff = (curr_time - self.received_packet_time)
            self.data_sample_rate = (self.samples_read) / diff.total_seconds()
        # Compute temperature and humidity sample rate
        if (self.temp_rh_samples_read >  0 and self.temp_rh_samples_read % 50 == 0):
            curr_time = datetime.now()
            diff = (curr_time - self.received_packet_time)
            self.temperature_sample_rate = (self.temp_rh_samples_read) / diff.total_seconds()
            self.temp_rh_samples_read = 0

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
        
        if (sample_rate not in self.available_sample_rates):
            self.message_string = f'{sample_rate} is not a valid sample rate'
        else:
            self.message_string = f'Setting sample rate to {sample_rate}'
            sample_rate_cmd = self.get_sample_rate_cmd(sample_rate)
            self.port.write(sample_rate_cmd.encode('utf-8'))

    def get_temp_hum_config_value(self, th_sample_rate, th_repeatability):
        sr_dict = {
            0x20: '0.5 Hz',
            0X21: '1 Hz',
            0x22: '2 Hz',
            0x23: '4 Hz',
            0x27: '10 Hz'
        }
        rep_dict = {
            0x20: {
                0x2F: 'Low',
                0x24: 'Med',
                0x32: 'High'
            },
            0x21: {
                0x2d: 'Low',
                0x26: 'Med',
                0x30: 'High'
            },
            0x22: {
                0x2B: 'Low',
                0x20: 'Med',
                0x36:  'High'
            },
            0x23: {
                0x29: 'Low',
                0x22: 'Med',
                0x34:  'High'
            },
            0x27: {
                0x2A: 'Low',
                0x21: 'Med',
                0x37:  'High'
            }
        }
        return sr_dict[th_sample_rate], rep_dict[th_sample_rate][th_repeatability]

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
        
        if (sample_rate not in self.available_sample_rates):
            self.message_string = f'{sample_rate} is not a valid sample rate'
        else:
            self.message_string = f'Setting sample rate to {sample_rate}'
            sample_rate_cmd = self.get_sample_rate_cmd(sample_rate)
            self.port.write(sample_rate_cmd.encode('utf-8'))

    def get_temp_hum_config_cmd(self, th_sample_rate, th_repeatability):
        config_dict = {
            '0.5 Hz': {
                'Low': [0x20, 0x2f],
                'Med': [0x20, 0x24],
                'High': [0x20, 0x32],
            },
            '1 Hz': {
                'Low': [0x21, 0x2D],
                'Med': [0x21, 0x26],
                'High': [0x21, 0x30], 
            },
            '2 Hz': {
                'Low': [0x22, 0x2B],
                'Med': [0x22, 0x20],
                'High': [0x22, 0x36],
            },
            '4 Hz': {
                'Low': [0x23, 0x29],
                'Med': [0x23, 0x22],
                'High': [0x23, 0x34],
            },
            '10 Hz': {
                'Low': [0x27, 0x2A],
                'Med': [0x27, 0x21],
                'High': [0x27, 0x37],
            }
        }
        return bytearray(config_dict[th_sample_rate][th_repeatability])

    def set_temperature_settings(self, sample_rate, repeatability):
        """!
        @brief Set new configuration for temperature and relative humidity sensor.

        This function sends the proper commands to the board to configure the
        temperature and relative humidity sensor.
        @param sample_rate the new desidered sample rate value
        @param repeatability the new desidered repeatability settings
        """
        self.message_string = f'Setting temperature sensor to {sample_rate} and {repeatability}'
        try:
            cmds = self.get_temp_hum_config_cmd(sample_rate, repeatability)
        except:
            self.message_string = f'{sample_rate} and {repeatability} are invalid settings'
        self.port.write(TEMP_RH_SETTINGS_SET_CMD.encode('utf-8'))
        self.port.write(cmds)
        self.port.write(TEMP_RH_SETTINGS_LATCH_CMD.encode('utf-8'))
    
    def retrieve_sample_rate_from_board(self):
        """!
        @brief Send command to the board to retrieve current sample rate configuration.

        This function sends a command to the board to retrieve the current
        sample rate configuration for both data and temperature and relative
        humidity sensor.
        The response from the board is parsed in the main read data function.
        """
        self.message_string = 'Retrieving sample rate configuration from board'
        if (self.port.is_open and self.connected == BOARD_CONNECTED):
            self.port.write(RETRIEVE_SAMPLE_RATE_CMD.encode('utf-8'))

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
        self.has_temp_data = has_temp_data
    
    def has_temperature_data(self):
        return self.has_temp_data
    
    def get_temperature(self):
        return self.temperature
    
    def get_humidity(self):
        return self.humidity
    
    def get_capacitance(self, channel_number=None):
        if (channel_number == None):
            return self.capacitance_values

        if (channel_number < 0 or channel_number > 3):
            return 0
        else:
            return self.capacitance_values[channel_number]

    def __str__(self):
        st = f"[{self.packet_counter}] - {self.temperature:.2f} - "
        st += f"{self.humidity:.2f} - {self.capacitance_values}"
        return st
                