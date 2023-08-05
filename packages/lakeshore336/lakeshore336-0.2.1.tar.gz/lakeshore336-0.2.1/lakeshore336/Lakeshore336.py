""" Driver for the Lakeshore 336 Temperature Controller.

The :class:`Lakeshore336` main class manages the interface
to the device and implements some of the available
operations through Ethernet communication. A custom
exception :class:`StateError` is used for internal
error management.
"""

# Imports
from typing import List, Tuple
import configparser
from enum import IntEnum

# Third party
from lab_utils.custom_logging import getLogger
from lakeshore import Model336, InstrumentException
from parse import *


class DataStatus(IntEnum):
    ok = 0
    invalid_reading = 1
    temp_under_range = 16
    temp_over_range = 32
    sensor_units_zero = 64
    sensor_units_over_range = 128


class Channel:
    """ Simple container to hold channel information.

    """

    # Configuration
    channel_id: chr     #: The channel ID (A to D).
    logging: bool       #: Data from the gauge should be recorded.
    label: str          #: Label of the gauge, to be used when logging to a database.
    curve_id: int       #: Sensor curve ID
    temp_limit: float   #: Maximum sensor temperature, when it is exceeded all control outputs are shut down

    # Data
    data_status: DataStatus     #: Valid data readout
    data_temp: float            #: Latest temperature readout value.
    data_res: float             #: Latest resistance readout value.

    def __init__(
            self,
            channel_id: chr,
            log_flag: bool,
            label: str,
            curve_id: int,
            temp_limit: float,
    ):
        """ Initializes the :class:`Channel` object.

        Parameters
        ----------
        channel_id : str
            Channel ID, 'A' to 'D'.

        log_flag : bool, optional
            Data from the channel is to be logged, default is 'False'.

        label : str, optional
            Channel label, default is 'None'.

        curve_id : int, optional
            Sensor curve ID, default is 'None'.

        temp_limit : float, optional
            Temperature limit above which control outputs are disabled, default is 0.0 (none).

        Raises
        ------
        :class:`ValueError`
            Channel property out of bounds, e.g. negative temperature limit.
        """
        # Sanity checks
        if ord('A') > ord(channel_id) or ord('D') < ord(channel_id):
            raise ValueError('Invalid channel ID {}'.format(channel_id))

        if temp_limit < 0.0 or temp_limit > 350.0:
            raise ValueError('Invalid temperature limit {}'.format(temp_limit))

        # Assignments
        self.channel_id = channel_id
        self.logging = log_flag
        self.label = label
        self.curve_id = curve_id
        self.temp_limit = temp_limit


class HeaterOutputMode(IntEnum):
    off = 0
    closed_loop = 1
    zone = 2
    open_loop = 3
    monitor_out = 4
    warmup = 5


class HeaterRange(IntEnum):
    off = 0
    low = 1
    medium = 2
    high = 3


class Heater:
    """ Simple container to hold heater information.
    """
    # General configuration
    heater_id: int          #: The heater ID (1 or 2).
    active: bool            #: Heater is active
    resistance: int         #: Heater resistance: 25 or 50 Ohm.
    resistance_code: int    #: Heater resistance code (1 for 25 Ohm, 2 for 50 Ohm)
    max_current: float      #: Maximum heater current.
    max_power: float        #: Maximum heater power.
    control_input: chr      #: Input channel to be used for control (in PID mode only)

    # Data
    data: float = None          #: Latest heater power value, as a percentage of the heater :param:'~Heater.range'.
    power: float = None         #: Actual heater power, in Watt.

    # Device state
    mode: HeaterOutputMode   #: Heater mode (see :class:`HeaterOutputMode`)
    manual_output: float     #: Manual control of the heater output
    range: HeaterRange       #: Heater range (see :class:`HeaterRange`)
    set_point: float         #: Target set point
    P: int                   #: Proportional (gain) control parameter.
    I: int                   #: Integral (reset) control parameter.
    D: int                   #: Derivative (rate) control parameter.

    def __init__(
            self,
            heater_id: int,
            active: bool,
            resistance: int,
            max_current: float,
            control_input: chr,
    ):
        """ Initializes the :class:`Heater` object.

        Parameters
        ----------
        heater_id : int
            Heater ID, 1 or 2.

        active : bool, optional
            The heater is active, default is 'False'

        resistance : int, optional
            Heater resistance: 25 or 50 Ohm, default is 50 Ohm.

        max_current : float, optional
            Maximum heater current, default is 1.0 A.

        Raises
        ------
        :class:`ValueError`
            Heater property out of bounds, e.g. negative resistance.
        """

        # Sanity checks
        if heater_id not in [1, 2]:
            raise ValueError('Invalid heater ID {}'.format(heater_id))

        if resistance not in [25, 50]:
            raise ValueError('Invalid heater resistance {}'.format(resistance))

        if max_current < 0.0 or max_current > 1.0:
            raise ValueError('Invalid heater maximum current {}'.format(max_current))

        if ord('A') > ord(control_input) or ord('D') < ord(control_input):
            raise ValueError('Invalid control input ID {}'.format(control_input))

        # Assignments
        self.heater_id = heater_id
        self.active = active
        self.resistance = resistance
        self.resistance_code = int(resistance/25)
        self.max_current = max_current
        self.control_input = control_input
        self.max_power = 0.

        self.mode = HeaterOutputMode.off
        self.range = HeaterRange.off
        self.manual_output = 0.0

        self.set_point = 0.0
        self.P = 0
        self.I = 0
        self.D = 0


class CurveFormat(IntEnum):
    mV_per_K = 1
    V_per_K = 2
    Ohm_per_K = 3
    log_Ohm_per_K = 4


class CurveCoefficient(IntEnum):
    negative = 1
    positive = 2


class UserCurve:
    # Properties
    name: str = None                        #: Curve name
    id: int = None                          #: Curve ID (valid entries: 21 - 59)
    serial_number: str = None               #: Serial number (max. 10 characters)
    format: CurveFormat = None              #: Curve data format
    limit_value: float = None               #: Curve temperature limit in K
    coefficient: CurveCoefficient = None    #: Curve temperature coefficient
    data: List[Tuple[float, float]] = None  #: Data container

    def __init__(self, curve_id: int = 0):
        self.id = curve_id
        self.data = []

    def parse_header(self, header: List[str]):
        [self.name, self.serial_number, f, self.limit_value, c] = header
        self.format = CurveFormat(int(f))
        self.coefficient = CurveCoefficient(int(c))

    def add_point(self, p: Tuple[float, float]):
        self.data.append(p)

    def write_to_file(self, filename: str):
        getLogger().debug('Saving curve data to file {}'.format(filename))

        with open(filename, 'w') as f:
            f.write('Curve ID: {}\n'.format(self.id))
            f.write('Curve Name: {}\n'.format(self.name))
            f.write('Serial Number: {}\n'.format(self.serial_number))
            f.write('Format: {}\n'.format(self.format.name))
            f.write('Limit Value: {} K\n'.format(self.limit_value))
            f.write('Coefficient: {}\n'.format(self.coefficient.name))

            f.write('Data points:\n')
            for [p1, p2] in self.data:
                f.write('{:10} {}\n'.format(p1, p2))

    def read_from_file(self, filename: str):
        getLogger().debug('Reading curve data from file {}'.format(filename))

        with open(filename, 'r') as f:
            # Line 1: ID
            line = f.readline()
            match = parse("Curve ID: {}", line)
            if match is None:
                raise RuntimeError('Error parsing line \'{}\' from file \'{}\''.format(line, filename))
            self.id = int(match.fixed[0])
            print(self.id)

            # Line 2: Name
            line = f.readline()
            match = parse("Curve Name: {}", line)
            if match is None:
                raise RuntimeError('Error parsing line \'{}\' from file \'{}\''.format(line, filename))
            self.name = match.fixed[0]
            print(self.name)

            # Line 3: Serial Number
            line = f.readline()
            match = parse("Serial Number: {}", line)
            if match is None:
                raise RuntimeError('Error parsing line \'{}\' from file \'{}\''.format(line, filename))
            self.serial_number = match.fixed[0]
            print(self.serial_number)

            # Line 4: Format
            line = f.readline()
            match = parse("Format: {}", line)
            if match is None:
                raise RuntimeError('Error parsing line \'{}\' from file \'{}\''.format(line, filename))
            self.format = CurveFormat[match.fixed[0]]
            print(self.format.name)

            # Line 5: Limit Value
            line = f.readline()
            match = parse("Limit Value: +{} K", line)
            if match is None:
                raise RuntimeError('Error parsing line \'{}\' from file \'{}\''.format(line, filename))
            self.limit_value = float(match.fixed[0])
            print(self.limit_value)

            # Line 6: Coefficient
            line = f.readline()
            match = parse("Coefficient: {}", line)
            if match is None:
                raise RuntimeError('Error parsing line \'{}\' from file \'{}\''.format(line, filename))
            self.coefficient = CurveCoefficient[match.fixed[0]]
            print(self.coefficient.name)

            # Lines 8 -> EOF: Data points
            # TODO


class LakeShore336(Model336): # noqa (ignore CamelCase convention)
    """ Driver implementation for the Lakeshore 336 Temperature Controller.

    The driver is based upon the official implementation :class:`~lakeshore.model_336.Model336`
    """

    # Connection configuration
    ip_address: str = '10.42.43.200'    #: The device IP address
    timeout: float = 1.0                #: Time-out for Ethernet connection error.

    # Device setup
    config_file: str = 'conf/lakeshore336.ini'  #: Device configuration file
    channel_info: List[Channel] = []            #: Channel information, loaded from the configuration file.
    number_of_channels: int = 4                 #: Available input channels.
    heater_info: List[Heater] = []              #: Heater information, loaded from the configuration file.
    number_of_heaters: int = 2                  #: Available control outputs.

    def __init__(self,
                 config_file: str = None,
                 ip_address: str = None,
                 timeout: float = None,
                 ):
        """ Initializes the :class:`Lakeshore336` object. It calls
        the :meth:`config` method to set up the device if a
        :paramref:`~LakeShore336.__init__.config_file` is given. Upon
        initialization, the parent driver :class:`~lakeshore.Model336`
        will immediately attempt to connect over TCP to the device and
        raise an :class:`~lakeshore.InstrumentException` otherwise.

        Parameters
        ----------
        config_file : str, optional
            Configuration file, default is 'None'.

        ip_address : str, optional
            IP address of the device, default is 'None'

        timeout : float, optional
            Ethernet communication time out, default is 'None'

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error

        :class:'lakeshore.InstrumentException`
            Generic device error

        :class:`StateError`
            Device was in the wrong state.
        """

        # Load config file, if given
        if config_file is not None:
            self.config(config_file)

        # Assign attributes, if given
        # They override they configuration file
        if ip_address is not None:
            self.ip_address = ip_address
        if timeout is not None:
            self.timeout = timeout

        # Call the parent class initializer, which attempts connection to the device over TCP
        getLogger().info('Connecting to Lakeshore 336 Temperature Controller at IP {}'.format(self.ip_address))
        Model336.__init__(
            self,
            ip_address=self.ip_address,
            timeout=self.timeout
        )

        # Override logger
        self.logger = getLogger()

        # Print out some confirmation message
        getLogger().info('Connection successful. Model: {}. Serial number: {}. Firmware: {}'.format(
            self.model_number,
            self.serial_number,
            self.firmware_version
        ))

        # Apply configuration
        self.apply_config()

        # Lock device
        self.lock()

    def query(self, query_string: str) -> str:
        """Override parent method due to excessive logging.

        Parameters
        ----------
        query_string : str
            A serial query ending in a question mark.

        Raises
        ------
        :class:'lakeshore.InstrumentException`
            Generic device error

        Returns
        -------
        str
            The instrument query response as a string.
        """

        # Check that a valid connection is active
        if self.device_tcp is None:
            raise InstrumentException("No connections configured")

        # Query the instrument over TCP.
        with self.dut_lock:
            getLogger().debug('Sending query over TCP to %s: %s', self.serial_number, query_string)
            response = self._tcp_query(query_string)

        getLogger().debug('Received response from %s: %s', self.serial_number, response)
        return response

    def command(self, command_string: str):
        """Override parent method due to excessive logging.

        Parameters
        ----------
        command_string : str
            A serial command.

        Raises
        ------
        :class:'lakeshore.InstrumentException`
            Generic device error
        """

        # Check that a valid connection is active
        if self.device_tcp is None:
            raise InstrumentException("No connections configured")

        # Query the instrument over serial. If serial is not configured, use TCP.
        with self.dut_lock:
            getLogger().debug('Sending command over TCP to %s: %s', self.serial_number, command_string)
            self._tcp_command(command_string)

    def reconnect(self):
        """ Closes the TCP connection, reloads device configuration
        and connects to the device again.

        Raises
        ------
        :class:'lakeshore.InstrumentException`
            Generic device error

        :class:`configparser.Error`
           Configuration file error
        """
        self.disconnect_tcp()
        self.config()
        super().__init__(
            ip_address=self.ip_address,
            timeout=self.timeout
        )
        self.apply_config()

    def config(self, new_config_file: str = None):
        """ Loads the Lakeshore 336 configuration from a file. If
        :paramref:`~Lakeshore336.config.new_config_file` is not
        given, the latest :attr:`config_file` is re-loaded;
        if it is given and the file is successfully parsed,
        :attr:`config_file` is updated to the new value.

        Parameters
        ----------
        new_config_file : str, optional
            New configuration file to be loaded.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error
        """

        # Save previous configuration
        old_channel_config = self.channel_info
        old_heater_info = self.heater_info

        # Clear previous configuration
        self.channel_info = []
        self.heater_info = []

        # Update configuration file, if given
        if new_config_file is None:
            new_config_file = self.config_file

        # Try to execute, otherwise revert to previous state
        try:
            # Initialize config parser and read file
            getLogger().info("Loading configuration file %s", new_config_file)
            config_parser = configparser.ConfigParser()
            config_parser.read(new_config_file)

            # Load Ethernet communication configuration
            self.ip_address = config_parser.get(section='Connection', option='ip_address')
            self.timeout = config_parser.getfloat(section='Connection', option='timeout')

            # Load input channels information
            for ch in range(self.number_of_channels):
                sec_name = 'Sensor_{}'.format(chr(ord('A')+ch))
                if not config_parser.has_section(sec_name):
                    getLogger().info('%s not found', sec_name)
                    continue

                log_flag = config_parser.getboolean(sec_name, 'logging')
                cur = config_parser.getint(sec_name, 'curve')
                lab = config_parser.get(sec_name, 'label')
                temp_limit = config_parser.getfloat(sec_name, 'temp_limit')
                getLogger().info(
                    'Found sensor %d: %s, curve %d, %s, %f K', ch+1, str(log_flag), cur, lab, temp_limit)

                try:
                    self.channel_info.append(Channel(
                        channel_id=chr(ord('A')+ch),
                        log_flag=log_flag,
                        label=lab,
                        temp_limit=temp_limit,
                        curve_id=cur,
                    ))
                except ValueError as e:
                    raise configparser.Error('{}'.format(e))

            # Load control output channels information
            for h in range(self.number_of_heaters):
                # Read info
                sec_name = 'Heater_{}'.format(h+1)
                if not config_parser.has_section(sec_name):
                    getLogger().info('%s not found', sec_name)
                    continue

                act = config_parser.getboolean(sec_name, 'active')
                res = config_parser.getint(sec_name, 'resistance')
                max_cur = config_parser.getfloat(sec_name, 'max_current')
                control_input = config_parser.get(sec_name, 'control_input')
                getLogger().info('Found heater %d: %d Ohm, %f A, input %s', h+1, res, max_cur, control_input)

                # Initialize heater object
                try:
                    self.heater_info.append(Heater(
                        heater_id=h+1,
                        active=act,
                        resistance=res,
                        max_current=max_cur,
                        control_input=control_input
                    ))
                except ValueError as e:
                    raise configparser.Error('{}'.format(e))

                # Check control input is configured AND logging
                if not act:
                    continue
                found = False
                for ch in self.channel_info:
                    if ch.channel_id == control_input and ch.logging:
                        found = True
                        break
                if not found:
                    raise configparser.Error('Heater {} is controlled by Input {}, which is not active'.format(
                        h+1,
                        control_input
                    ))

            # If everything worked, update local config_file for future calls
            self.config_file = new_config_file

        except Exception as e:
            # Restore previous configuration
            self.channel_info = old_channel_config
            self.heater_info = old_heater_info
            raise e

    def apply_config(self):
        """ Applies the configuration to the device.

        - Input sensors.
        - Control outputs.

        Raises
        ------
        :class:'lakeshore.InstrumentException`
            Generic device error
        """

        # Configure device input channels
        getLogger().info('Configuring device input channels')
        for ch in self.channel_info:
            # Channel enabled?
            if ch.label is None:
                continue

            # Set channel label
            self.command('INNAME {},{}'.format(ch.channel_id, ch.label))
            lab = self.query('INNAME? {}'.format(ch.channel_id))
            if lab.casefold() != ch.label.casefold():
                getLogger().warning(
                    'Mismatch of Sensor {} Label: {} (device) and {} (user)'.format(ch.channel_id, lab, ch.label)
                )

            # Set channel curve
            self.command('INCRV {},{}'.format(ch.channel_id, ch.curve_id))
            cur = self.query('INCRV? {}'.format(ch.channel_id))
            if int(cur) != ch.curve_id:
                getLogger().warning(
                    'Mismatch of Sensor {} curve: {} (device) and {} (user)'.format(lab, int(cur), ch.curve_id)
                )

            # Set limit temperature
            self.command('TLIMIT {},{}'.format(ch.channel_id, ch.temp_limit))

        # Configure device output channels
        getLogger().info('Configuring device output channels')
        for h in self.heater_info:
            # Page 133
            self.command('HTRSET {},{},{},{},{}'.format(
                h.heater_id,        # The heater ID
                h.resistance_code,  # Resistance code (1 for 25 Ohm, 2 for 50 Ohm)
                0,                  # Max current mode, 0 for user-defined
                h.max_current,      # User-defined max current
                2                   # Heater output display, 1 for current and 2 for power
            ))

    def lock(self):
        """ Locks out all front panel entries except pressing the All Off
        key to immediately turn off all heater outputs.
        """

        # Send lock command
        getLogger().info('Locking device')
        self.command('LOCK 1,123')

    def unlock(self):
        """ Unlocks front panel entries.
        """

        # Send lock command
        getLogger().info('Unlocking device')
        self.command('LOCK 0,123')

    def is_lock(self) -> bool:
        """ Checks whether the front panel is locked.

        Raises
        ------
        :class:'lakeshore.InstrumentException`
            Generic device error
        """

        # Send lock query
        getLogger().debug('Querying device LOCK status')
        resp = self.query('LOCK?').split(sep=',')[0]

        if resp == '1':
            getLogger().debug('Device is locked')
            return True
        elif resp == '0':
            getLogger().debug('Device is unlocked')
            return False
        else:
            raise InstrumentException('Invalid lock query response: {}'.format(resp))

    def retrieve_data(self):
        """ Queries the device for the latest temperature and heater data.

        Raises
        ------
        :class:'lakeshore.InstrumentException`
            Generic device error
        """

        # Query for data status
        for ch in self.channel_info:
            if ch.logging:
                resp = self.query('RDGST? {}'.format(ch.channel_id))
                try:
                    ch.data_status = DataStatus(int(resp))
                    getLogger().debug('Data status for channel {}: {}'.format(ch.label, ch.data_status.name))
                except ValueError:
                    getLogger().warning('Invalid input status query for sensor {}: {}'.format(ch.label, resp))
                    ch.data_res = None

        # Query for all resistances
        for ch in self.channel_info:
            if ch.logging:
                if ch.data_status.value < 64:
                    resp = self.query('SRDG? {}'.format(ch.channel_id))
                    try:
                        ch.data_res = float(resp)
                    except ValueError:
                        getLogger().warning('Invalid resistance string for sensor {}: {}'.format(ch.label, resp))
                        ch.data_res = None
                        continue
                else:
                    ch.data_res = 'NaN'
                getLogger().debug('Resistance of channel {}: {} Ohm'.format(ch.label, ch.data_res))

        # Query for all temperatures
        for ch in self.channel_info:
            if ch.logging:
                if ch.data_status == DataStatus.ok:
                    resp = self.query('KRDG? {}'.format(ch.channel_id))
                    try:
                        ch.data_temp = float(resp)
                    except ValueError:
                        getLogger().warning('Invalid temperature string for sensor {}: {}'.format(ch.label, resp))
                        ch.data_temp = None
                        continue
                else:
                    ch.data_temp = 'NaN'
                getLogger().debug('Temperature of channel {}: {} K'.format(ch.label, ch.data_temp))

        # Query for heater outputs
        for h in self.heater_info:
            if h.active:
                resp = self.query('HTR? {}'.format(h.heater_id))
                try:
                    h.data = float(resp)
                    h.power = h.data*h.max_power/100.
                    getLogger().debug('Heater {}: {} W'.format(h.heater_id, h.power))
                except ValueError:
                    getLogger().warning('Invalid power output string for heater {}: {}'.format(h.heater_id, resp))
                    h.data = None
                    h.power = None

    def apply_setpoint(self, heater_id: int, setpoint: float, heater_range: HeaterRange):
        """ Changes setpoint and range of a heater.

        Raises
        ------
        :class:'ValueError'
            Invalid parameters

        :class:'lakeshore.InstrumentException`
            Generic device error
        """

        # Validate data
        # Look for heater
        heater = None
        for h in self.heater_info:
            if h.heater_id == heater_id:
                heater = h
                getLogger().debug('Configuring setpoint for heater {}'.format(heater.heater_id))
                break
        if heater is None:
            raise ValueError('Invalid heater ID {}'.format(heater_id))

        # Heater is active
        if not heater.active:
            raise ValueError('Heater {} is not active'.format(heater_id))

        # Heater has a sensor linked
        if heater.control_input is None:
            raise ValueError('No valid input sensor configured for heater {}'.format(heater_id))
        getLogger().debug('Heater control sensor: {}'.format(heater.control_input))

        # The sensor linked is valid
        sensor = None
        for s in self.channel_info:
            if s.channel_id == heater.control_input:
                sensor = s
                getLogger().debug('Feedback sensor: {}, {}'.format(s.channel_id, s.label))
                break
        if sensor is None:
            raise ValueError('Input sensor {} configured for heater {} is not valid'.format(
                heater.control_input,
                heater_id
            ))

        # Setpoint
        if setpoint < 0:
            raise ValueError('Invalid setpoint {}')
        elif setpoint > sensor.temp_limit:
            raise ValueError('Setpoint {} beyond temperature limit {}'.format(setpoint, sensor.temp_limit))

        # Heater range should be fine by definition

        # Apply setpoint
        self.command('SETP {},{}'.format(heater_id, setpoint))

        # Check if successful
        resp = self.query('SETP? {}'.format(heater_id))
        if abs(float(resp) - setpoint) > 0.1:
            raise InstrumentException('Error updating setpoint for heater {}'.format(heater_id))

        # Update heater_info
        for h in self.heater_info:
            if h.heater_id == heater_id:
                h.set_point = setpoint
                break

        # Apply range
        self.command('RANGE {},{}'.format(heater_id, heater_range.value))

        # Check if successful
        resp = self.query('RANGE? {}'.format(heater_id))
        if int(resp) != heater_range.value:
            raise InstrumentException('Heater range could not be updated for heater {}'.format(heater_id))

        # Update heater_info
        max_power = 0
        if heater_range is not HeaterRange.off:
            max_power = heater.resistance * pow(heater.max_current, 2) * pow(10, heater_range.value-3)
        getLogger().debug('Heater {} maximum power set to {} W ({})'.format(heater_id, max_power, heater_range.name))

        for h in self.heater_info:
            if h.heater_id == heater_id:
                h.range = heater_range
                h.max_power = max_power
                break

        getLogger().info('Setpoint of heater {} set to {}K with maximum power {}W'.format(
            heater_id,
            setpoint,
            max_power
        ))

    def get_heater_setpoint(self, heater_id: int) -> float:
        """ Returns the setpoint of heater :param:`~.get_heater_setpoint.heater_id`.

        Raises
        ------
        :class:'ValueError'
            Invalid parameters, or heater not properly set

        :class:'lakeshore.InstrumentException`
            Generic device error

        Returns
        -------
        float:
            The setpoint of the heater
        """

        # Validate data
        # Look for heater
        heater = None
        for h in self.heater_info:
            if h.heater_id == heater_id:
                heater = h
                getLogger().debug('Retrieving setpoint of heater {}'.format(heater.heater_id))
                break
        if heater is None:
            raise ValueError('Invalid heater ID {}'.format(heater_id))

        # Heater is active
        if not heater.active:
            raise ValueError('Heater {} is not active'.format(heater_id))

        # Heater has a sensor linked
        if heater.control_input is None:
            raise ValueError('No valid input sensor configured for heater {}'.format(heater_id))

        # The sensor linked is valid
        sensor = None
        for s in self.channel_info:
            if s.channel_id == heater.control_input:
                sensor = s
                break
        if sensor is None:
            raise ValueError('Input sensor {} configured for heater {} is not valid'.format(
                heater.control_input,
                heater_id
            ))

        return heater.set_point

    def get_heater_range(self, heater_id: int) -> HeaterRange:
        """ Returns the range of heater :param:`~.get_heater_setpoint.heater_id`.

        Raises
        ------
        :class:'ValueError'
            Invalid parameters, or heater not properly set

        :class:'lakeshore.InstrumentException`
            Generic device error

        Returns
        -------
        HeaterRange:
            The range of the heater
        """

        # Validate data
        # Look for heater
        heater = None
        for h in self.heater_info:
            if h.heater_id == heater_id:
                heater = h
                getLogger().debug('Retrieving setpoint of heater {}'.format(heater.heater_id))
                break
        if heater is None:
            raise ValueError('Invalid heater ID {}'.format(heater_id))

        # Heater is active
        if not heater.active:
            raise ValueError('Heater {} is not active'.format(heater_id))

        # Heater has a sensor linked
        if heater.control_input is None:
            raise ValueError('No valid input sensor configured for heater {}'.format(heater_id))

        # The sensor linked is valid
        sensor = None
        for s in self.channel_info:
            if s.channel_id == heater.control_input:
                sensor = s
                break
        if sensor is None:
            raise ValueError('Input sensor {} configured for heater {} is not valid'.format(
                heater.control_input,
                heater_id
            ))

        return heater.range

    def curve_retrieve(self, curve_id: int, only_header: bool = False) -> UserCurve:
        """ Retrieves user curve information.

        Parameters
        ----------
        curve_id : int
            The user curve ID.

        only_header : bool, optional
            Read only curve header info, default is False
        """

        # Initialize user curve
        curve = UserCurve(curve_id)

        # Get the curve header
        getLogger().info('Retrieving header for curve {}'.format(curve_id))
        resp = self.query('CRVHDR? {}'.format(curve_id))
        curve.parse_header(resp.split(',', 5))
        getLogger().info('Name: {}'.format(curve.name))
        getLogger().info('Serial Number: {}'.format(curve.serial_number))
        getLogger().info('Format: {}'.format(curve.format.name))
        getLogger().info('Limit Value: {}'.format(curve.limit_value))
        getLogger().info('Coefficient: {}'.format(curve.coefficient.name))

        # Return?
        if only_header:
            return curve

        # Get the curve data points
        getLogger().info('Data points:')
        for p in range(200):
            resp = self.query('CRVPT? {},{}'.format(curve_id, p + 1))
            [p1, p2] = resp.split(',', 2)
            curve.add_point((float(p1), float(p2)))
            getLogger().info('{}  {}'.format(p1, p2))

        return curve

    def curve_load(self, curve: UserCurve):
        """ Loads a user curve to the device.

        Parameters
        ----------
        curve : UserCurve
            The user curve.
        """

        # Load the curve header
        getLogger().info('Loading curve {} header'.format(curve.id))
        self.command('CRVHDR {},{},{},{},{},{}'.format(
            curve.id,
            curve.name,
            curve.serial_number,
            curve.format.value,
            curve.limit_value,
            curve.coefficient.value
        ))
