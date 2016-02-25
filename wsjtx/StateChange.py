#!/usr/bin/env python
import myutils


class StateChange:
    packet_type = 1
    id_key = ""
    dial_freq = 0   # uint64
    mode = ""
    dx_call = ""
    report = ""
    tx_mode = ""
    tx_enabled = False
    transmitting = False
    decoding = False

    def __init__(self, data):
        string_length, self.id_key = myutils.get_utf8_string(data)

        # Dial Freq
        tmp = 4 + string_length
        self.dial_freq = myutils.get_int64(data[tmp:])

        # Current Mode
        tmp += 8
        mode_len, self.mode = myutils.get_utf8_string(data[tmp:])

        # DX Call
        tmp += (4 + mode_len)
        dx_len, self.dx_call = myutils.get_utf8_string(data[tmp:])

        # Report
        tmp += (4 + dx_len)
        rpt_len, self.report = myutils.get_utf8_string(data[tmp:])

        # TX Mode
        tmp += (4 + rpt_len)
        tx_len, self.tx_mode = myutils.get_utf8_string(data[tmp:])

        # TX Enabled?
        tmp += (4 + tx_len)
        self.tx_enabled = myutils.get_boolean(data[tmp:])

        # Transmitting
        tmp += 1
        self.transmitting = myutils.get_boolean(data[tmp:])

        # Decoding
        tmp += 1
        self.decoding = myutils.get_boolean(data[tmp:])

        # self.debug_print()


    def do_print(self):
        # print("  [*] Dial_freq = {}".format(self.dial_freq))
        # print("  [*] Mode = {}".format(self.mode))
        # print("  [*] DX call = {}".format(self.dx_call))
        # print("  [*] Report = {}".format(self.report))
        # print("  [*] TX Mode = {}".format(self.tx_mode))
        # print("  [*] TX Enabled = {}".format("Yes" if self.tx_enabled else "No"))
        # print("  [*] Transmitting = {}".format("Yes" if self.transmitting else "No"))
        # print("  [*] Decoding = {}".format("Yes" if self.decoding else "No"))

        print("[*] State: Dial: {:,}hz, Mode: {}, TX-Mode:{}, tx_enabled:{}, Transmitting:{}, Decoding:{}".format(
                self.dial_freq,
                self.mode,
                self.tx_mode,
                self.tx_enabled,
                self.transmitting,
                self.decoding
            ))
