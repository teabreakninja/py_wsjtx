# -*- coding: utf-8 -*-
import myutils


class Clear:
    packet_type = 3

    id_key = 0

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)

    def do_print(self):
        print("[*] Clear called")
