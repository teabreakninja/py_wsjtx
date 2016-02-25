# -*- coding: utf-8 -*-
import myutils


class Replay:
    # This is a out message - i.e. This script send the msg to the WSJT-X
    # running instance to get the status. It is usually replied with
    # a Decode message (type 2)
    packet_type = 7

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)
        # print("  id_key: {} (len:{})".format(self.id_key, string_length))

    def do_print(self):
        pass
