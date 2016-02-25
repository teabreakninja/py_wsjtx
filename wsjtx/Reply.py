# -*- coding: utf-8 -*-
import myutils


class Reply:
    # This is a out message - i.e. This script send the msg to the WSJT-X
    # running instance. It will initiate a QSO but must follow a CQ or QRZ
    packet_type = 4

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)
        # print("  id_key: {} (len:{})".format(self.id_key, string_length))

    def do_print(self):
        pass
