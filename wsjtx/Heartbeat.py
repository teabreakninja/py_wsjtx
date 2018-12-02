#!/usr/bin/env python
import struct
import myutils


class Heartbeat:
    packet_type = 0
    id_key = ""
    max_schema = 0

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)
        tmp = 4 + string_length

        self.max_schema = myutils.get_uint32(data[tmp:])
        # myutils.debug_hex(data[4+self.string_length:])
        # print("[*] max_schema: {}".format(self.max_schema))
