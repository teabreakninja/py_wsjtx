# -*- coding: utf-8 -*-
import myutils
from pyhamtools import locator


class WSPRDecode:
    packet_type = 10

    id_key = ''
    new_id = False
    now_time = ''
    snr = 0
    delta_time = 0.0
    delta_freq = 0
    drift = 0
    callsign = ''
    grid = ''
    power = 0

    def __init__(self, data):
        # myutils.debug_hex(data)
        string_length, self.id_key = myutils.get_utf8_string(data)
        tmp = 4 + string_length
        # print("  id_key: {} (len:{})".format(self.id_key, string_length))

        self.new_id = myutils.get_boolean(data[tmp:])
        # print("  [*] new: {}".format(self.new_id))
        tmp += myutils.DataSize._boolean
        # print("  [*] new_id:{}".format(self.new_id))

        self.now_time = myutils.get_time(data[tmp:])
        tmp += myutils.DataSize._time
        # print("  [*] date:{}".format(self.now_time))

        self.snr = myutils.get_int32(data[tmp:])
        tmp += myutils.DataSize._int32
        # print("  [*] snr:{}".format(self.snr))

        self.delta_time = myutils.get_double(data[tmp:])
        tmp += myutils.DataSize._double
        # print("  [*] delta_time:{}".format(self.delta_time))

        # Something in here? Seems zero in the debug
        # myutils.debug_hex(data[tmp:])
        tmp += myutils.DataSize._uint32

        self.delta_freq = myutils.get_uint32(data[tmp:])
        tmp += myutils.DataSize._uint32
        # print("  [*] delta_freq:{}".format(self.delta_freq))

        self.drift = myutils.get_uint32(data[tmp:])
        tmp += myutils.DataSize._uint32
        # print("  [*] drift:{}".format(self.drift))

        string_length, self.callsign = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("  [*] callsign:{}".format(self.callsign))

        string_length, self.grid = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("  [*] grid:{}".format(self.grid))

        self.power = myutils.get_uint32(data[tmp:])
        # print("  [*] power:{}".format(self.power))

        self.dist = 0
        self.bearing = 0
        if (myutils.validate_callsign(self.callsign)):
            if (myutils.validate_locator(self.grid)):
                self.dist = locator.calculate_distance("io64", self.grid)
                self.bearing = locator.calculate_heading("io64", self.grid)

    def do_print(self):
        print("WSPR Decode: {:10} ({:6}) db:{:4}, Freq:{:>10,}Hz, pwr:{:4}, Dist:{:>5.0f}km, Az: {:>3.0f}".format(
            self.callsign,
            self.grid,
            self.snr,
            self.delta_freq,
            self.power,
            self.dist,
            self.bearing
        ))
