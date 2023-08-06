import logging
import os
import re
from itertools import compress
from time import sleep, time
from datetime import datetime

from serial import SerialException

from .comm_package import validate_data, define_package, data_to_parsed_string, replace_repeating_chars
from .serialib import SerialComm
from .const import *
from .exceptions import NoAnswer, InvalidAnswer, InvalidCommand, CRCError, DeviceNotInitialized, ParameterError

logger = logging.getLogger(__name__)


class Ziva(SerialComm):
    def __init__(self):
        super().__init__()
        # Serial port
        self.port = None
        self.baudrate = 38400
        self.timeout = 0.1
        self.package_counter = 63

        self.recv_address = None
        self.rf = None

        # Real values (actual values from device)
        self.rv_units = []
        self.rv_names = []
        self.real_values = []

        # info values, user values and memory status
        # Latest data combines all of the above with last
        self.info_values = {}
        self.user_values = {}
        self.memory_status = None
        self.data = {
            'real_values': self.real_values,
            'info_params': self.info_values,
            'user_params': self.user_values,
            'memory_status': self.memory_status,
        }

        self.parameters = {}  # dict of all parameters that are read
        self.settings = []

        # Application commands for communication
        self.real_values_params = [RV_MASK, RV_UNITS, RV_NAMES]
        self.info_params = [IDENT_A, IDENT_B, IDENT_C]
        self.user_params = []

    def __update_param(self, name, value):
        self.parameters[name] = value
        # also update in settings
        item = [i for i in self.settings if i['name'] == name]
        if item:
            item[0]['value'] = value

    def __increment_counter(self):
        """Counter. Increment counter after every sent packet"""
        if self.package_counter == 255:
            self.package_counter = 63
        else:
            self.package_counter += 1

    def __define_package(self, app_cmd: str = None, var_name: str = None, var_val: str = None):
        """Define package
        :param app_cmd: Application command (VR (Value read), VW (Value write),...)
        :param var_name: Variable name  (RV, IDENT_A, IDENT_B,..)
        :param var_val: Variable value (string that can represent anything)
        """

        package = define_package(
            recv_addr=self.recv_address,
            app_cmd=app_cmd,
            var_name=var_name,
            var_val=var_val,
            counter=self.package_counter,
            rf=self.rf
        )
        return package

    def initialize(self, recv_address: int, rf: bool = True, wake_up_time: int = WAKE_UP_TIME_TOTAL,
                   user_params: list = None):
        """
        Set device. Call this on start of the communication.

        :param recv_address: receiver address (eg 1 for ISM or 1019 for RF)
        :param rf: RF or ISM
        :user_params : Additional user params that are called when connecting to device
        """

        self.recv_address = recv_address
        self.rf = rf
        self.user_params = []
        self.user_values = {}
        self.wake_up_time = wake_up_time if wake_up_time else WAKE_UP_TIME_TOTAL
        if self.rf:
            self.user_params.append(RECORD_TIME)
        if user_params:
            self.user_params += user_params

    def deinitialize(self):
        """Deinitialize device."""

        self.__init__()

    def read_variable(self, name: str) -> dict:
        """Read variable

        :param name: Name of parameter to read e.g. RECORD_TIME"""

        if name is None:
            raise ValueError('Name of the variable is not defined')
        data = self.send_receive(app_cmd=VALUE_READ, var_name=name)
        self.parameters[name] = data['data']
        return data

    def write_variable(self, name=None, value=None) -> dict:
        """Write variable

        :param name: Name of parameter to write e.g. RECORD_TIME
        :param value: Value to write e.g. 60
        :return ??
        """

        if name is None or value is None:
            raise ValueError('Name or value of the variable is not defined')
        name, value = str(name), str(value)
        data = self.send_receive(app_cmd=VALUE_WRITE, var_name=name, var_val=value)
        self.__update_param(name=name, value=value)
        return data

    def send_receive(self, app_cmd: str, var_name: str = None, var_val: str = None, retry_limit: int = None,
                     timeout: float = 1, stream_channel: bool = False, parse: bool = True) -> dict:
        """Sent package and receive answer."""

        if not self.recv_address:
            raise DeviceNotInitialized('Device is not initialized')

        # if self.ser != None:
            # Here is the problem
            # self.ser.timeout = timeout

        for error_count in range(20):
            try:
                self.__increment_counter()
                package = self.__define_package(
                    app_cmd=app_cmd,
                    var_name=var_name,
                    var_val=var_val,
                )
                self.write(data=package)
                data = self.read(last_char=END_MARKER_BYTES)
                data = replace_repeating_chars(data, reverse=True)
                data = validate_data(data, stream_channel=stream_channel)
                if stream_channel:
                    # data['data'] = data_decompress(data=data['data'])
                    data['data'] = ''.join(chr(i) for i in data['data'])
                else:
                    data['data'] = data_to_parsed_string(data=data['data'])
            except SerialException:
                raise

            except (NoAnswer, InvalidAnswer, CRCError, InvalidCommand, Exception) as e:
                if retry_limit:
                    if retry_limit == error_count:
                        raise
                else:
                    if type(e).__name__ == NoAnswer.__name__:
                        retry = RETRY_NO_ANSWER
                    elif type(e).__name__ == InvalidAnswer.__name__:
                        retry = RETRY_INVALID_ANSWER
                    elif type(e).__name__ == CRCError.__name__:
                        retry = RETRY_CRC_ERROR
                        logger.error('CRC ERROR')
                    elif type(e).__name__ == InvalidCommand.__name__:
                        retry = RETRY_INVALID_COMMAND
                    else:
                        retry = 2
                    if error_count == retry:
                        raise
            else:
                return data

    def get_data(self) -> dict:
        """ Get latest data from device and update parameters if they were changed

        :return: dictionary with latest data
        """

        self.data['real_values'] = self.get_real_values()
        self.data['info_params'] = self.get_params(params=self.info_params)
        self.data['user_params'] = self.get_params(params=self.user_params)
        self.data['memory_status'] = self.memory_status

        return self.data

    def get_params(self, params:list = None):
        for param in params:
            if param not in self.parameters:
                value = None
                try:
                    value = self.read_variable(name=param)['data']
                except (DeviceNotInitialized, NoAnswer):
                    raise
                except Exception as e:
                    logger.warning(e)
                self.__update_param(name=param, value=value)
        return {k:v for (k,v) in self.parameters.items() if k in params}

    def get_real_values(self) -> list:
        """ Read real values from device
        Possible output from real values variable:
        - ISM: '7005968.000','0.00','-83.94'
        - RF: '29/08/2020 18:39:47','25.740','3.42'
        """

        rv_mask = [bool(int(i)) for i in self.get_params([RV_MASK])[RV_MASK]]
        rv_units = self.get_params([RV_UNITS])[RV_UNITS].split(';')
        rv_names = self.get_params([RV_NAMES])[RV_NAMES].split(';')
        rv_units = list(compress(rv_units, rv_mask))
        rv_names = list(compress(rv_names, rv_mask))

        # Read real values
        real_values = self.read_variable(name=REAL_VALUES)['data']
        self.real_values = []

        # First real value can be timestamp
        try:
            datetime.strptime(real_values[0], "%d/%m/%Y %H:%M:%S")
            self.real_values.append({'channel': 'Timestamp', 'value': real_values[0], 'unit': None})
            real_values.pop(0)
        except ValueError:
            pass

        for i, val in enumerate(real_values):
            try:
                meas = {
                    'channel': rv_names[i] if len(rv_names) > i else None,
                    'value': float(val),
                    'unit': rv_units[i] if len(rv_units) > i else None
                }
                self.real_values.append(meas)
            except (DeviceNotInitialized, NoAnswer):
                raise
            except Exception as e:
                logger.exception(e)
        return self.real_values

    def get_time(self):
        """Get time from device"""

        return self.read_variable(name=TIME)

    def set_time(self, timestamp: datetime = datetime.now()):
        """Set time of device
        :param timestamp: timestamp to set; if None datetime.now() is used
        :type timestamp: datetime
        """

        if timestamp is None:
            timestamp = datetime.now()
        if type(timestamp) == str:
            try:
                timestamp = datetime.strptime(timestamp.replace(microsecond=0), '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                # print (e)
                raise ValueError('Wrong time format')
        timestamp = str(timestamp.replace(microsecond=0))
        return self.write_variable(name=TIME, value=timestamp)

    def get_memory_status(self) -> dict:
        """Read memory status"""

        if self.rf:

            try:
                data = self.send_receive(app_cmd=MEMORY_STATUS)['data']
                size, free, used = int(data[0]), int(data[1]), int(data[2])
                self.memory_status = {'size': size, 'free': free, 'used': used,
                                      'used_percentage': round(used / size * 100, 1)}
            except Exception:
                self.memory_status = {'error': True}
        else:
            self.memory_status = None
        return self.memory_status

    def read_params(self, force=True):
        """Read parameters from device """

        if self.settings and not force:
            return self.settings
        data = []
        error_count = 0
        max_error_count = 5
        for i in range(500):
            var_name = f'PAR[{i}]'
            try:
                params = self.send_receive(app_cmd=VALUE_READ, var_name=var_name)['data']
                if params == 'End':
                    break
                elif len(params) > 0:
                    params_dict = {}
                    for par in params:
                        if '=' in par:
                            params_dict[par.split('=')[0].lower()] = par.split('=')[1]
                        else:
                            params_dict[par.lower()] = True
                    value = self.read_variable(name=params_dict['name'])['data']
                    params_dict['value'] = value

                    # Extract choices
                    # {'mode': 'T_LIST', 'i0': '0 Enable', 'i1': '1 Disable'}
                    if 'mode' in params_dict:
                        mode = params_dict['mode']
                        if mode == 'T_LIST':
                            choices = []
                            for i in range(0, 50):
                                if f'i{i}' in params_dict:
                                    value = params_dict[f'i{i}'].split(' ')[0]
                                    title = params_dict[f'i{i}'].split(' ')[1]
                                    choices.append({'value':value, 'title':title})
                                else:
                                    break
                            params_dict['choices'] = choices
                    data.append(params_dict)
            except Exception as e:
                logger.warning(f'Cant read param {var_name}, e:{e}')
                error_count += 1
                if error_count == max_error_count:
                    break
                else:
                    continue
        logger.info(f'Settings parameters read, count:{len(data)}')
        self.settings = data
        return data

    def read_memory_data(self, filepath: str = 'data.jda'):
        """Read memory from device and save data to filepath"""

        self.send_receive(app_cmd=OPEN_MEMORY_DIR)
        data_out = ''
        while True:
            data = self.send_receive(app_cmd=MEMORY_START_READING, stream_channel=True, timeout=2)
            # print (data)
            data_out += data['data']
            if data['status'] == 'OT':
                break
        if data_out:
            # print (data_out)
            with open(filepath, 'w', encoding='latin1') as f:
                f.write(data_out)

    def export_params(self, filepath: str = 'settings.txt'):
        """Save params to filepath"""

        data = self.read_params(force=False)
        data_write = []
        for i, param in enumerate(data):
            # print (param)
            comment = param['com']
            value = param['value']
            name = param['name']
            data_write.append(f'// Par {i}: {comment}\n')
            data_write.append(f'{name}={value}\n')
        with open(filepath, 'w', encoding='iso-8859-2') as f:
            f.writelines(data_write)
        logger.info(f'Parameters exported: {len(data)}')

    def import_params(self):
        """Import parameters from self.settings to device."""

        if not self.settings:
            raise ParameterError('Zero parameters to import')

        data   = self.settings
        failed = []
        for item in data:
            name = item['name']
            value = item['value']
            try:
                self.write_variable(name=name, value=value)
            except Exception as e:
                logger.error(f'Failed to write param {name}, e:{e}')
                failed.append((name, value))


        logger.info(f"Parameters imported:{len(data) - len(failed)}{', error:{}'.format(len(failed)) if failed else ''}")
        if failed:
            raise ParameterError(f'Parameters failed to import {[i[0] for i in failed]}')

    def load_params(self, filepath: str) -> list:
        """Load parameters from file into settings variable. Params are loaded not
        actually imported to device. Call import_params for importing this params into device

        :param filepath: Filepath of file with parameters.
        """

        if filepath is None or not os.path.exists(filepath):
            raise FileNotFoundError('File does not exists')

        with open(filepath) as f:
            lines = f.readlines()

        data = {}
        for line in lines:
            if not re.search('//', line) and re.search('=', line):
                name = line.split('=')[0].strip()
                value = line.split('=')[1].strip()
                data[name] = value

        failed = []
        if self.settings:
            for name, value in data.items():
                # Replace values with the ones from file
                item = [i for i in self.settings if i['name'] == name]
                if item:
                    item[0]['value'] = value
                else:
                    failed.append(name)
                    logger.error(f'Failed to load param {name}')
        else:
            self.settings = [{'name':i[0], 'value':i[1]} for i in data.items()]
        if failed:
            raise ParameterError(f'Parameters failed to import {[i for i in failed]}')
        return self.settings

    def reset_rf_device(self):
        # !!! Not done
        pass

    def reset_cpu(self):
        """Reset CPU of device"""

        return self.send_receive(app_cmd=RESET_CPU)

    def goto_sleep(self):
        """Send RF device to sleep"""

        return self.send_receive(app_cmd=DEVICE_SLEEP)

    def start_wake_up_routine(self):
        """Start wake up procedure for RF devices"""

        if self.rf:
            start = time()
            app_cmd = f"{WAKE_UP_DEVICE}{self.recv_address},{self.wake_up_time}"
            try:
                self.send_receive(app_cmd=app_cmd, retry_limit=3, timeout=0.1)
                sleep(self.wake_up_time)
            except NoAnswer:
                raise NoAnswer('USB router is not working properly')
            wake_time = round(time() - start, 1)
            logger.info(f'Device woke up in {wake_time} seconds')

    def connect(self) -> dict:
        """Connect to device (Online mode). If remote device is RF start wake_up procedure."""
        if not self.recv_address:
            raise DeviceNotInitialized('Device is not initialized')

        self.start_wake_up_routine()
        self.get_memory_status()
        data = self.get_data()
        return data

    def disconnect(self, deinit: bool = True):
        """Disconnect from device"""
        if self.rf:
            self.reset_cpu()
        if deinit:
            self.deinitialize()


if __name__ == '__main__':
    z = Ziva()
