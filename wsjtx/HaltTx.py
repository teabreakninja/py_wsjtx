# -*- coding: utf-8 -*-
import myutils


class HaltTx:
    # This is a out message - i.e. This script send the msg to the WSJT-X
    # running instance. This will stop the current transmission
    packet_type = 8

    def __init__(self, data):
        pass

    def do_print(self):
        pass

    def send(self):
        pass
