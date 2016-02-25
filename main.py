#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import struct
import sys
import datetime

from header import header
from wsjtx import *
import myutils
from myutils import PacketType
from pyhamtools import locator


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('127.0.0.1', 2237)

    # sock.sendto('test message', server_address)

    sock.bind(server_address)

    try:
        while True:
            data, server = sock.recvfrom(1024)
            h = header(data[0:16])
            # print "data:", data
            packet_type = struct.unpack(">L", data[8:12])[0]

            # print("[*] packet_type:{}".format(packet_type))
            if packet_type == PacketType.Heartbeat:
                payload = Heartbeat(data[12:])
                print("[*] Heartbeat [{}]".format(datetime.datetime.now()))

            elif packet_type == PacketType.Status:
                payload = StateChange(data[12:])
                payload.do_print()

            elif packet_type == PacketType.Decode:
                # myutils.debug_packet(data)
                payload = Decode(data[12:])
                payload.do_print()
                if payload.message[:2] == "CQ":
                    cq = payload.message.split(" ")
                    if (myutils.validate_callsign(cq[1])):
                        if (len(cq) ==2):
                            cq[2] = 'None'
                        print("[***] CQ CALLED BY {} ({})".format(cq[1], cq[2]))
                        if (myutils.validate_locator(cq[2])):
                            print("  [*] Distance: {:.0f}km, Bearing:{:.0f}".format(
                                    locator.calculate_distance("io64", cq[2]),
                                    locator.calculate_heading("io64", cq[2])
                                ))

            elif packet_type == PacketType.Clear:
                payload = Clear(data[12:])
                payload.do_print()

            elif packet_type == PacketType.Reply:
                # Not used, this is an out message
                pass

            elif packet_type == PacketType.QSO_Logged:
                payload = Qso_Logged(data[12:])
                payload.do_print()

            elif packet_type == PacketType.Close:
                payload = Close(data[12:])
                payload.do_print
                sys.exit(0)

            elif packet_type == PacketType.Replay:
                # Not used, this is an out message
                pass

            elif packet_type == PacketType.Halt_TX:
                # Not used, this is an out message
                pass

            elif packet_type == PacketType.Free_Text:
                # Not used, this is an out message
                pass

            elif packet_type == PacketType.WSPRDecode:
                payload = WSPRDecode(data[12:])
                payload.do_print()

            else:
                print("[*] Packet type: {}".format(packet_type))
    except KeyboardInterrupt:
        print("ctrl-c caught, exiting")

if __name__ == "__main__":
    main()
