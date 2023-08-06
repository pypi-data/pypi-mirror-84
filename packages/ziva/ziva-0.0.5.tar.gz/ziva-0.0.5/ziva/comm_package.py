from binascii import unhexlify, hexlify

from .const import EQUALS_SIGN, WAKE_UP_DEVICE, START_MARKER_BYTES, \
    END_MARKER_BYTES, SERVER_ADDR_BYTES
from .crc import calculate_crc16
from .exceptions import (
    NoAnswer,
    InvalidAnswer,
    CRCError,
    InvalidCommand,
)


def replace_repeating_chars(data: bytes = None, reverse=False) -> bytes:
    """Replace possible repeating chars within communication package
    [0x82] -> [0x84][‘2’]
    [0x83] -> [0x84][‘3’]
    [0x84] -> [0x84][‘4’]

    if reverse:
    [0x82] <- [0x84][‘2’]
    [0x83] <- [0x84][‘3’]
    [0x84] <- [0x84][‘4’]

    :param data: Input communication string
    :param reverse: Do a reverse replacing
    :return:
    """
    if not reverse:
        data_block = b''
        for item in data:
            item = bytes([item])
            if item == b'\x82':
                data_block += b'\x842'
            elif item == b'\x83':
                data_block += b'\x843'
            elif item == b'\x84':
                data_block += b'\x844'
            else:
                data_block += item
    else:
        data_block = data
        replace_chars = [
            (b'\x842', b'\x82'),
            (b'\x843', b'\x83'),
            (b'\x844', b'\x84'),
        ]
        for ch, ch_replace in replace_chars:
            while True:
                if not data_block.find(ch) == -1:
                    data_block = data_block.replace(ch, ch_replace)
                else:
                    break

    return data_block

def data_decompress(data:bytes) -> bytes:
    """Decompress data. Repeating set of chars are compressed into shorter set.
    Set of K equal chars is transformed (K=char, X=number of repeats):
    [F0][X]K ; K=4-239
    [F0][3][K-hi][K-low]X ; K=240-65520
     """

    compress_char = b'\xf0'
    bytes_out = b''
    i = 0
    while i < len(data):
        byte_char = bytes([data[i]])
        if byte_char == compress_char:
            n_repeats = data[i + 1]
            char = chr(data[i + 2])
            char = f"{n_repeats * char}".encode()
            bytes_out = b"".join([bytes_out, char])
            i += 3
        else:
            bytes_out = b"".join([bytes_out, byte_char])
            i += 1

    return bytes_out

def define_package(recv_addr: int, app_cmd: str, var_name: str = None, var_val: str = None, counter: int = 0,
                   rf: bool = False) -> bytes:
    """
    Returns string that represent whole communication package. Output string can be directly sent to device.
    Example: read real values from ism (addr 4) "820004FF80000000008101565252563D89C483"

    :param recv_addr: receiver address (e.g. 1000)
    :param app_cmd: application command (e.g. VR - value read)
    :param var_name: variable name (e.g. RV - real values)
    :param var_val: variable value (e.g. `Merilno mest` or `3600`)
    :param rf: RF or not (wifi or wired connection)
    :param counter: package counter (0-255)
    :return: parsed data as string
    """
    if not recv_addr:
        raise ValueError("Receiver address can't be none")

    # Generate receiver address from integer recv_addr
    if rf:
        recv_addr_complete = '{:8X}'.format(recv_addr).replace(' ', '0')
    else:
        recv_addr_1 = '{:2X}'.format(0).replace(' ', '0')
        recv_addr_2 = '{:2X}'.format(recv_addr).replace(' ', '0')
        recv_addr_3 = '{:2X}'.format(255).replace(' ', '0')
        recv_addr_4 = '{:2X}'.format(128).replace(' ', '0')
        recv_addr_complete = recv_addr_1 + recv_addr_2 + recv_addr_3 + recv_addr_4

    # Consts
    recv_addr_complete = unhexlify(recv_addr_complete)
    data_layer = app_cmd
    if var_name:
        data_layer += var_name + '='
    if var_val:
        data_layer += var_val
    data_layer = data_layer.encode('iso-8859-2')
    if rf and WAKE_UP_DEVICE in app_cmd:
        data_layer += b'\x00'

    # Get hex counter value and 16bit CRC code
    counter_hex = unhexlify('81' + '{:2X}'.format(counter).replace(' ', '0'))
    data_for_crc = recv_addr_complete + SERVER_ADDR_BYTES + counter_hex + data_layer
    crc16 = unhexlify(calculate_crc16(data_for_crc))

    # Combine all data layers
    package = recv_addr_complete + SERVER_ADDR_BYTES + \
              counter_hex + data_layer + crc16
    package = replace_repeating_chars(data=package)
    return START_MARKER_BYTES + package + END_MARKER_BYTES


def data_to_parsed_string(data: bytes):
    """Parse data to list. Separate by comma.
    Example of a raw data: b'\x82\x00\x00\x00\x00\x00\x00\x00\x00\x01@O0.638,0.00,21.67,\to\x83
    """
    data_str = data.decode('iso-8859-2')
    if 'Name' and 'Com' in data_str:
        data_str = list(filter(None, data_str.split(',')))
        data_out = []
        for i, item in enumerate(data_str):
            # If first letter after comma is not in the upper case,
            # merge item with previous item
            if item[0].isupper():
                data_out.append(item)
            else:
                data_out[-1] += ',' + item
        data_str = data_out
    else:
        data_str = list(filter(None, data_str.split(',')))

    return data_str[0] if len(data_str) == 1 else data_str


def validate_data(data: bytes, stream_channel: bool = False) -> dict:
    '''Validate data bytes.
    :param data: input bytes
    :param stream_channel: stream channel uses different status_sign (O, E, OT or OM)
    '''

    if not data:
        raise NoAnswer('No answer from device')
    if len(data) < 14:
        raise InvalidAnswer('Data length is not sufficient')

    # data = ''.join(chr(i) for i in data)

    # Remove 82 and 83, server addr, CRC
    start_char = 1
    end_char = 1
    srv_addr = 8
    crc = 2
    data = data[start_char + srv_addr:-(end_char + crc)]
    # print(data)

    # Validate data. Possible combinations are:
    # sign @ signals start of message. First letter or first two letters after @ = status:
    # O[value] - okay
    # E[error message] - error
    # OM[data] -> okay, more data
    # OT[data] -> okay, data read complete
    # OE empty dir
    # W[percent] - not yet completed

    at_sign_pos = data.find(b'@')
    if at_sign_pos == -1 or len(data) == at_sign_pos:
        # Error in message if @ is not present or @ is last char in message
        raise InvalidAnswer('Unkown error:', data)

    status_sign_pos = at_sign_pos + 1
    status_sign = chr(data[status_sign_pos])
    if status_sign == 'O' or status_sign == 'W':
        if stream_channel and len(data[status_sign_pos:]) > 1:
            status_sign_additional_letter = chr(data[status_sign_pos + 1])
            if status_sign_additional_letter == 'T' or status_sign_additional_letter == 'M':
                status_sign += status_sign_additional_letter
        data_out = {'status':status_sign, 'data':data[data.find(status_sign.encode()) + len(status_sign):]}
        return data_out

    if status_sign == 'E':
        error_msg = data[status_sign_pos:]
        if b'implemented' in data:
            raise InvalidCommand('Invalid command')

        elif b'Undefined variable' in data:
            raise InvalidCommand('Undefined variable')

        elif b'CRC error' in data:
            raise CRCError('Invalid CRC code')
        else:
            raise InvalidAnswer('Unkown error:', error_msg)
    elif status_sign == ' ':
        if b'implemented' in data:
            raise InvalidCommand('Invalid command')
    else:
        raise InvalidAnswer('Status sign is not valid: ', data)

    # Get status from data
    # try:
    #     status_data = data.split('@')[1]
    #     if len(status_data) > 1:
    #         status = status_data[0] if status_data[1] not in ['M', 'T'] else status_data[0:2]
    #     else:
    #         status = status_data[0]
    # except IndexError:
    #     raise InvalidAnswer('Unkown error:', data)
    # if status in ['O', 'OT', 'OM', 'W']:
    #     message = data.split('@' + status)[1]
    #     if parse:
    #         message = parse_data(data=message)
    #     return {'status': status, 'data': message}
    # elif status == 'E':
    #     if 'implemented' in data:
    #         raise InvalidCommand('Invalid command')
    #
    #     elif 'Undefined variable' in data:
    #         raise InvalidCommand('Undefined variable')
    #
    #     elif 'CRC error' in data:
    #         raise CRCError('Invalid CRC code')
    #
    #     else:
    #         raise InvalidAnswer('Unkown error:', data.split('@E'))
    # else:
    #     raise InvalidAnswer('Unkown error:', data)

    # elif status == 'E':
    #     raise AnswerIsNotValid("Error: " + data.split('@E')[1])
    # elif status == ' ':
    #     raise AnswerIsNotValid("Error: " + data.split('@ ')[1])
    # else:
    #     raise AnswerIsNotValid('Unkown error:', data)
