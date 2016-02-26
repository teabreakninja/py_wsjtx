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
        tmp += 13
        # print("datetime:{}".format(self.date_time))

        string_length, self.dx_call = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("DX_Call:"+self.dx_call)

        string_length, self.dx_grid = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("dx_grid:"+self.dx_grid)

        self.dial_freq = myutils.get_int64(data[tmp:])
        tmp += 8
        # print("Dial:{}".format(self.dial_freq))

        string_length, self.mode = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("mode:"+self.mode)

        string_length, self.report_sent = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("report_sent:"+self.report_sent)

        string_length, self.report_recv = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("report_recv:"+self.report_recv)

        string_length, self.tx_power = myutils.get_utf8_string(data[tmp:])
        tmp += 4 + string_length
        # print("rx_power:"+self.tx_power)

        string_length, self.name = myutils.get_utf8_string(data[tmp:])
        # print("name:"+self.name)

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
