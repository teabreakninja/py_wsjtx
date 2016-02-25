# -*- coding: utf-8 -*-
import myutils


class Qso_Logged:
    packet_type = 5

    id_key = 0
    date_time = ''
    dx_call = ''
    dx_grid = ''
    dial_freq = 0
    mode = ''
    report_sent = ''
    report_recv = ''
    tx_power = ''
    name = ''

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)
        # print("  id_key: {} (len:{})".format(self.id_key, string_length))

        tmp = 4 + string_length
        self.date_time = myutils.get_datetime(data[tmp:])

        tmp += 4
        self.dx_call = myutils.get_utf8_string(data[tmp:])

        tmp += 4
        self.dx_grid = myutils.get_utf8_string(data[tmp:])

        tmp += 4
        self.dial_freq = myutils.get_uint32(data[tmp:])

        tmp += 4
        self.mode = myutils.get_utf8_string(data[tmp:])

        tmp += 4
        self.report_send = myutils.get_utf8_string(data[tmp:])

        tmp += 4
        self.report_recv = myutils.get_utf8_string(data[tmp:])

        tmp += 4
        self.tx_power = myutils.get_utf8_string(data[tmp:])

        tmp += 4
        self.name = myutils.get_utf8_string(data[tmp:])

    def do_print(self):
        print("{} logged QSO with {} ({}) on {} using {}. Send {} received {}".format(
            self.date_time,
            self.dx_call,
            self.dx_grid,
            self.dial_freq,
            self.mode,
            self.report_sent,
            self.report_recv
        ))
