# -*- coding: utf-8 -*-
import struct
import math


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
    _datetime = 13
    _time = 4


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
        the_string = ""
    elif data[0:4] == "\xFF\xFF\xFF\xFF":
        string_length, the_string = 0, ""
    else:
        the_string = data[4:4 + string_length]
        # print("[*] Key = {}".format(the_string))

    return string_length, the_string

def set_utf8_string(val):
    string_length = len(val)
    data = set_uint32(string_length)
    data += val
    return data

def get_uint32(data):
    return struct.unpack(">I", data[0: 4])[0]

def set_uint32(val):
    return struct.pack(">I", val)

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
	return get_date(data[:8])  + " " + get_time(data[8:12]) + " " + get_timespec(data[12:1])


def get_date(data):
    # debug_hex(data)
    julian_day = get_int64(data)
    print julian_day

    year, month, day = jd_to_date(julian_day)
    return "{}/{}/{}".format(year, month, int(day))


def get_time(data):
    # debug_hex(data)
    julian_day = get_int32(data)

    import time
    t = time.gmtime(julian_day/1000)
    dt = time.strftime("%H:%M", t)

    return dt


def get_timespec(data):
    # debug_hex(data)
    if data == "\x00":
        return "Local"
    elif data == "\x01":
        return "UTC"
    elif data == "\x02":
        return "Offset from UTC"
    elif data == "\x03":
        return "TimeZone"
    else:
        return ""

"""
Taken from:
	Matt Davis
	http://github.com/jiffyclub
"""
def jd_to_date(jd):
    jd = jd + 0.5

    F, I = math.modf(jd)
    I = int(I)

    A = math.trunc((I - 1867216.25)/36524.25)

    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I

    C = B + 1524
    D = math.trunc((C - 122.1) / 365.25)
    E = math.trunc(365.25 * D)
    G = math.trunc((C - E) / 30.6001)
    day = C - E + F - math.trunc(30.6001 * G)

    if G < 13.5:
        month = G - 1
    else:
        month = G - 13

    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715

    return year, month, day


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
