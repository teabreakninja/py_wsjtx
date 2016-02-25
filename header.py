# -*- coding: utf-8 -*-
import struct


class header:
    magic_number = 0l
    schema_number = 0l
    valid_magic = "0xadbccbda"
    valid_schemas = (1, 2, 3)

    def __init__(self, data):
        magic = struct.unpack(">L", data[0:4])[0]
        schema = struct.unpack(">L", data[4:8])[0]

        if magic != int(self.valid_magic, 0):
            print("Magic Number doesn't match: {}".format(magic))

        if schema not in self.valid_schemas:
            print("Not a valid schema: {}".format(schema))

        # print("[*] Header OK: {}, {}".format(magic, schema))
