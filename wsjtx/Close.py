# -*- coding: utf-8 -*-
import myutils


class Close:
    packet_type = 6

    id_key = 0

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)
        # print("  id_key: {} (len:{})".format(self.id_key, string_length))

    def do_print(self):
        print("Close sent by host. Bye!")
