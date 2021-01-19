Module mip.communication.mserial
================================

Variables
---------

    
`BOARD_CONNECTED`
:   !
    @brief Start streaming command.

    
`BOARD_DISCONNECTED`
:   !
    @brief Board found but not connected.

    
`BOARD_FOUND`
:   !
    @brief Board connected.

    
`CONN_REQUEST_CMD`
:   !
    @brief Voltage packet header byte.

    
`DATA_PACKET_HEADER`
:   !
    @brief Data packet tail byte.

    
`DATA_PACKET_TAIL`
:   !
    @brief Sample rate packet header byte.

    
`SAMPLE_RATE_PACKET_HEADER`
:   !
    @brief Sample rate packet tail byte.

    
`START_STREAMING_CMD`
:   !
    @brief Stop streaming command.

    
`STOP_STREAMING_CMD`
:   !
    @brief Time set command.

    
`TEMP_RH_SETTINGS_SET_CMD`
:   !
    @brief Temperature and relative humidity latch command.

    
`TIME_LATCH_CMD`
:   !
    @brief Temperature and relative humidity set command.

    
`TIME_SET_CMD`
:   !
    @brief Time latch command.

    
`VOLTAGE_PACKET_HEADER`
:   !
    @brief Voltage packet tail byte.

    
`VOLTAGE_PACKET_TAIL`
:   !
    @brief Data packet header byte.

Classes
-------

`DataPacket(packet_counter=0, temperature=0, humidity=0, cap_ch_1=0, cap_ch_2=0, cap_ch_3=0, cap_ch_4=0, current=0, aux=0, has_temp_data=False)`
:   !
    @brief Data packet holding data received from board.

    ### Methods

    `get_capacitance(self, channel_number=None)`
    :

    `get_humidity(self)`
    :

    `get_temperature(self)`
    :

    `has_temperature_data(self)`
    :

`MIPSerial()`
:   EventDispatcher(**kwargs)
    Generic event dispatcher interface.
    
        See the module docstring for usage.

    ### Ancestors (in MRO)

    * kivy._event.EventDispatcher
    * kivy._event.ObjectWithUid

    ### Instance variables

    `battery_voltage`
    :   NumericProperty(defaultvalue=0, **kw)
        Property that represents a numeric value.
        
            :Parameters:
                `defaultvalue`: int or float, defaults to 0
                    Specifies the default value of the property.
        
            >>> wid = Widget()
            >>> wid.x = 42
            >>> print(wid.x)
            42
            >>> wid.x = "plop"
             Traceback (most recent call last):
               File "<stdin>", line 1, in <module>
               File "properties.pyx", line 93, in kivy.properties.Property.__set__
               File "properties.pyx", line 111, in kivy.properties.Property.set
               File "properties.pyx", line 159, in kivy.properties.NumericProperty.check
             ValueError: NumericProperty accept only int/float
        
            .. versionchanged:: 1.4.1
                NumericProperty can now accept custom text and tuple value to indicate a
                type, like "in", "pt", "px", "cm", "mm", in the format: '10pt' or (10,
                'pt').

    `configured_sample_rate`
    :   StringProperty(defaultvalue=u'', **kw)
        Property that represents a string value.
        
            :Parameters:
                `defaultvalue`: string, defaults to ''
                    Specifies the default value of the property.

    `configured_temp_rh_sample_rate`
    :   StringProperty(defaultvalue=u'', **kw)
        Property that represents a string value.
        
            :Parameters:
                `defaultvalue`: string, defaults to ''
                    Specifies the default value of the property.

    `configured_temp_rh_sample_rep`
    :   StringProperty(defaultvalue=u'', **kw)
        Property that represents a string value.
        
            :Parameters:
                `defaultvalue`: string, defaults to ''
                    Specifies the default value of the property.

    `connected`
    :   NumericProperty(defaultvalue=0, **kw)
        Property that represents a numeric value.
        
            :Parameters:
                `defaultvalue`: int or float, defaults to 0
                    Specifies the default value of the property.
        
            >>> wid = Widget()
            >>> wid.x = 42
            >>> print(wid.x)
            42
            >>> wid.x = "plop"
             Traceback (most recent call last):
               File "<stdin>", line 1, in <module>
               File "properties.pyx", line 93, in kivy.properties.Property.__set__
               File "properties.pyx", line 111, in kivy.properties.Property.set
               File "properties.pyx", line 159, in kivy.properties.NumericProperty.check
             ValueError: NumericProperty accept only int/float
        
            .. versionchanged:: 1.4.1
                NumericProperty can now accept custom text and tuple value to indicate a
                type, like "in", "pt", "px", "cm", "mm", in the format: '10pt' or (10,
                'pt').

    `data_sample_rate`
    :   NumericProperty(defaultvalue=0, **kw)
        Property that represents a numeric value.
        
            :Parameters:
                `defaultvalue`: int or float, defaults to 0
                    Specifies the default value of the property.
        
            >>> wid = Widget()
            >>> wid.x = 42
            >>> print(wid.x)
            42
            >>> wid.x = "plop"
             Traceback (most recent call last):
               File "<stdin>", line 1, in <module>
               File "properties.pyx", line 93, in kivy.properties.Property.__set__
               File "properties.pyx", line 111, in kivy.properties.Property.set
               File "properties.pyx", line 159, in kivy.properties.NumericProperty.check
             ValueError: NumericProperty accept only int/float
        
            .. versionchanged:: 1.4.1
                NumericProperty can now accept custom text and tuple value to indicate a
                type, like "in", "pt", "px", "cm", "mm", in the format: '10pt' or (10,
                'pt').

    `is_streaming`
    :   BooleanProperty(defaultvalue=True, **kw)
        Property that represents only a boolean value.
        
            :Parameters:
                `defaultvalue`: boolean
                    Specifies the default value of the property.

    `message_string`
    :   StringProperty(defaultvalue=u'', **kw)
        Property that represents a string value.
        
            :Parameters:
                `defaultvalue`: string, defaults to ''
                    Specifies the default value of the property.

    `sample_rate_num_samples`
    :   NumericProperty(defaultvalue=0, **kw)
        Property that represents a numeric value.
        
            :Parameters:
                `defaultvalue`: int or float, defaults to 0
                    Specifies the default value of the property.
        
            >>> wid = Widget()
            >>> wid.x = 42
            >>> print(wid.x)
            42
            >>> wid.x = "plop"
             Traceback (most recent call last):
               File "<stdin>", line 1, in <module>
               File "properties.pyx", line 93, in kivy.properties.Property.__set__
               File "properties.pyx", line 111, in kivy.properties.Property.set
               File "properties.pyx", line 159, in kivy.properties.NumericProperty.check
             ValueError: NumericProperty accept only int/float
        
            .. versionchanged:: 1.4.1
                NumericProperty can now accept custom text and tuple value to indicate a
                type, like "in", "pt", "px", "cm", "mm", in the format: '10pt' or (10,
                'pt').

    `temperature_sample_rate`
    :   NumericProperty(defaultvalue=0, **kw)
        Property that represents a numeric value.
        
            :Parameters:
                `defaultvalue`: int or float, defaults to 0
                    Specifies the default value of the property.
        
            >>> wid = Widget()
            >>> wid.x = 42
            >>> print(wid.x)
            42
            >>> wid.x = "plop"
             Traceback (most recent call last):
               File "<stdin>", line 1, in <module>
               File "properties.pyx", line 93, in kivy.properties.Property.__set__
               File "properties.pyx", line 111, in kivy.properties.Property.set
               File "properties.pyx", line 159, in kivy.properties.NumericProperty.check
             ValueError: NumericProperty accept only int/float
        
            .. versionchanged:: 1.4.1
                NumericProperty can now accept custom text and tuple value to indicate a
                type, like "in", "pt", "px", "cm", "mm", in the format: '10pt' or (10,
                'pt').

    ### Methods

    `add_callback(self, callback)`
    :

    `check_mip_port(self, port_name)`
    :   !
        @brief Check if the port is the correct one.
        
        This function checks whether the port passed in as
        parameter correspons to a proper device.
        @param port_name name of the port to be checked.
        @return True if the port was found to be corrected.
        @return False if the port was not found to be corrected.

    `compute_num_samples_sample_rate(self, sample_rate)`
    :

    `connect(self)`
    :

    `convert_battery_voltage(self, value)`
    :   !
        @brief Convert raw bytes to battery voltage.
        
        This function converts the bytes passed in as
        parameter to a proper voltage value. The
        battery voltage is equal to the 16 bit data
        computed from the two bytes (MSB first) and
        divided by 100.
        @param value battery voltage raw values
        @return computed battery voltage

    `convert_capacitance(self, capacitance, capdac)`
    :   !
        @brief Convert raw bytes and capdac value into capacitance.
        
        This function converts the bytes passed in as
        parameter to a proper capacitance value based
        on capdac settings. The capacitance value is 
        computed given the equation stated in the FDC1004Q datasheet.
        @param capacitance capacitance bytes
        @param capdac capacitance channel capdac value
        @return computed capacitance value

    `convert_humidity(self, raw_humidity)`
    :   !
        @brief Convert raw bytes into humidity.
        
        This function converts the bytes passed in as
        parameter to a proper humidity value. The 
        humidity value is computed given the
        equation stated in the SHT85 datasheet.
        @param raw_humidity humidity bytes
        @return computed humidity value

    `convert_temperature(self, raw_temperature)`
    :   !
        @brief Convert raw bytes into temperature.
        
        This function converts the bytes passed in as
        parameter to a proper temperature value. The 
        temperature value is computed given the
        equation stated in the SHT85 datasheet.
        @param raw_temperature temperature bytes
        @return computed temperature value

    `find_port(self)`
    :   !
        @brief Find the serial port to which the device is connected.
        
        This function scans all the available serial ports until
        the one to which the device is connected is found. Once
        found, it attempts to connect to it.

    `get_sample_rate_cmd(self, sample_rate)`
    :   !
        @brief Get command to set sample rate.
        
        This function returns the correct command to send to the
        board to set the proper sample rate.

    `get_temp_hum_config_cmd(self, th_sample_rate, th_repeatability)`
    :

    `get_temp_hum_config_value(self, th_sample_rate, th_repeatability)`
    :

    `parse_sample_rate(self, sample_rate_packet)`
    :

    `read_data(self)`
    :

    `retrieve_sample_rate_from_board(self)`
    :   !
        @brief Send command to the board to retrieve current sample rate configuration.
        
        This function sends a command to the board to retrieve the current
        sample rate configuration for both data and temperature and relative
        humidity sensor.
        The response from the board is parsed in the main read data function.

    `send_updated_time_to_board(self)`
    :   !
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

    `set_sample_rate(self, sample_rate)`
    :   !
        @brief Send command to set sample rate on the board.
        
        This function sends the appropriate command to the board
        to set the sample rate to a new value. It then sends a 
        command to the board to retrieve the sample rate value that
        was set, that is checked inside the read data function
        and the class property is then updated accordingly.
        @param sample_rate string identifying the new sample rate to be set.

    `set_temperature_settings(self, sample_rate, repeatability)`
    :   !
        @brief Set new configuration for temperature and relative humidity sensor.
        
        This function sends the proper commands to the board to configure the
        temperature and relative humidity sensor.
        @param sample_rate the new desidered sample rate value
        @param repeatability the new desidered repeatability settings

    `start_streaming(self)`
    :   !
        @brief Start data streaming from the board.
        
        This function starts data streaming from the board.
        It also sets up a running thread to retrieve the
        data from the board, parse it and send it to the
        data receivers.

    `stop_streaming(self)`
    :   !
        @brief Stop data streaming from the board.
        This function stops data streaming from the
        board. This function sends the appropriate command
        to the board and stops the running thread.

    `update_computed_sample_rate(self)`
    :

`Singleton(*args, **kwargs)`
:   type(object_or_name, bases, dict)
    type(object) -> the object's type
    type(name, bases, dict) -> a new type

    ### Ancestors (in MRO)

    * builtins.type