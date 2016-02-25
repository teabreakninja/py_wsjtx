# -*- coding: utf-8 -*-
import myutils


class Decode:
    packet_type = 2

    id_key = 0
    new_id = False
    now_time = ''
    snr = 0
    delta_time = 0.0
    delta_freq = 0
    mode = ""
    message = ""

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)
        # print("  id_key: {} (len:{})".format(self.id_key, string_length))

        tmp = 4 + string_length
        self.new_id = myutils.get_boolean(data[tmp:])
        # print("  [*] new: {}".format(self.new_id))

        tmp += 1
        self.now_time = myutils.get_datetime(data[tmp:])

        tmp += 4
        self.snr = myutils.get_int32(data[tmp:])

        tmp += 4
        self.delta_time = myutils.get_double(data[tmp:])

        tmp += 8
        self.delta_freq = myutils.get_uint32(data[tmp:])

        tmp += 4
        mode_len, self.mode = myutils.get_utf8_string(data[tmp:])

        tmp += (4 + mode_len)
        msg_len, self.message = myutils.get_utf8_string(data[tmp:])

    def do_print(self):
        print("Time:{} db:{} DT:{:.1f} Freq:{} Mode:{} Msg: {}".format(
                self.now_time,
                str(self.snr).rjust(2),
                self.delta_time,
                str(self.delta_freq).rjust(4),
                self.mode,
                self.message
             ))
