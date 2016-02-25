#!/usr/bin/env python
import struct
import myutils


class Heartbeat:
    packet_type = 0
    id_key = ""
    max_schema = 0l

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)

        self.max_schema = struct.unpack(">L", data[4 + string_length:])[0]
        # myutils.debug_hex(data[4+self.string_length:])
        # print("[*] max_schema: {}".format(self.max_schema))
