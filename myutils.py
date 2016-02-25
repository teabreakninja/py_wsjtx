# -*- coding: utf-8 -*-
import struct


class PacketType():
    Heartbeat = 0
    Status = 1
    Decode = 2
    Clear = 3
    Reply = 4
    QSO_Logged = 5
    Close = 6
    Replay = 7
    Halt_TX = 8
    Free_Text = 9
    WSPRDecode = 10


class DataSize():
    _uint32 = 4
    _int32 = 4
    _int64 = 8
    _uint8 = 1
    _float = 4
    _double = 8
    _boolean = 1
    _datetime = 4


def debug_packet(data):
    print ":".join("{:02x}".format(ord(c)) for c in data)


def debug_hex(data):
    print "[=] ",
    print ":".join("{:02x}".format(ord(c)) for c in data)


def get_utf8_string(data):
    # string_length = struct.unpack(">L", data[0:4])[0]
    string_length = get_uint32(data)
    # print("[*] String length:{}".format(string_length))
    if string_length == 0:
        id_key = ""
    elif data[0:4] == "\xFF\xFF\xFF\xFF":
        string_length, id_key = 0, ""
    else:
        id_key = data[4:4 + string_length]
        # print("[*] Key = {}".format(id_key))

    return string_length, id_key


def get_uint32(data):
    return struct.unpack(">I", data[0: 4])[0]


def get_int32(data):
    return struct.unpack(">i", data[0: 4])[0]


def get_int64(data):
    return struct.unpack(">q", data[0: 8])[0]


def get_uint8(data):
    return struct.unpack(">B", data[0: 1])[0]


def get_float(data):
    return struct.unpack(">f", data[0: 4])[0]


def get_double(data):
    return struct.unpack(">d", data[0: 8])[0]


def get_boolean(data):
    my_bool = struct.unpack("?", data[0: 1])[0]
    # print("[*] my_bool = {}".format(my_bool))
    return my_bool


def get_datetime(data):
    # debug_hex(data)
    # julian_day = get_int64(data)
    julian_day = get_int32(data)

    import time
    t = time.gmtime(julian_day/1000)
    dt = time.strftime("%H:%M", t)

    # print("j-day:{}".format(julian_day))
    return dt


def validate_callsign(call):
    import re
    valid = re.match('^[a-zA-Z]{1,2}\d{1,2}[a-zA-z]{1,3}$', call, re.DOTALL)
    if valid:
        return True
    else:
        return False


def validate_locator(loc):
    import re
    valid = re.match('^[a-zA-Z]{2}\d{2}$', loc, re.DOTALL)
    if valid:
        return True
    else:
        return False
