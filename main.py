#!/usr/bin/env python
import socket
import struct
import sys
import datetime

from header import header
from wsjtx import *
import myutils
from myutils import PacketType
from pyhamtools import locator
from read_log import WsjtxLog

class bcolors:
    """
    Print the terminal colours with bash:
    while [ $color -lt 245 ]; do
        echo -e "$color: \\033[38;5;${color}mhello\\033[48;5;${color}mworld\\033[0m" ((color++));
    done
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Four possible outcomes:
    # 1 - worked station on this band = green
    WKD_BEFORE = '\033[92m'

    # 2 - worked country no station this band = pink
    WKD_COUNTRY_NOT_STATION = '\033[38;5;213m' # PINK

    # 3 - worked country diff band = blue
    WKD_COUNTRY_DIFF_BAND = '\033[38;5;39m' # blue

    # 4 - not worked country before = white on read
    NOT_WORKED = '\033[41m' # WHITE_ON_RED


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('127.0.0.1', 2237)

    # sock.sendto('test message', server_address)

    sock.bind(server_address)

    # Read existing log file
    log = WsjtxLog()
    print("[*] Logfile found, {} entries read, {} stations.".format(log.entry_count, len(log.log_entries)))

    current_band = ""

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
                current_band = log.get_band(str(payload.dial_freq/1000/1000))
                # print("[!] Current band: {}".format(current_band))

            elif packet_type == PacketType.Decode:
                # myutils.debug_packet(data)
                payload = Decode(data[12:])
                payload.do_print()
                if payload.message[:2] == "CQ":
                    cq = payload.message.split(" ")
                    if len(cq) > 1:
                        # CQ call should be 'CQ CALL LOC', but can be:
                        # 'CQ DX CALL LOC' or
                        # 'CQ CALL DX LOC'
                        cq_call = cq[1]
                        cq_loc = cq[2]

                        if cq_call == "DX":
                            cq_call = cq[2]
                            cq_loc = cq[3]

                        if cq_loc == "DX":
                            if len(cq) > 3:
                                cq_loc = cq[3]
                            else:
                                cq_loc = ""

                        if (myutils.validate_callsign(cq_call)):
                            band = log.check_entry(cq_call, current_band)

                            if band == log.WORKED_COUNTRY_AND_STATION:
                                # Worked before on same band
                                colour = bcolors.WKD_BEFORE
                                status = "Call:Y;Band:Y;Country:Y"

                            elif band == log.WORKED_COUNTRY_DIFF_BAND:
                                # worked before on different band
                                colour = bcolors.WKD_COUNTRY_DIFF_BAND
                                status = "Call:N;Band:N;Country:Y"

                            elif band == log.WORKED_COUNTRY_NOT_STATION:
                                # Worked country, not station
                                colour = bcolors.WKD_COUNTRY_NOT_STATION
                                status = "Call:N;Band:Y;Country:Y"

                            else:
                                # not worked
                                colour = bcolors.NOT_WORKED
                                status = "Call:N;Band:N;Country:N"

                            print("[***] CQ CALLED BY {}{}{} ({}) [{}]".format(colour, cq_call, bcolors.ENDC, cq_loc, status))
                            if (myutils.validate_locator(cq[2])):
                                print("  [*] Distance: {:.0f}km, Bearing:{:.0f}".format(
                                        locator.calculate_distance("io64", cq_loc),
                                        locator.calculate_heading("io64", cq_loc)
                                    ))

            elif packet_type == PacketType.Clear:
                payload = Clear(data[12:])
                payload.do_print()

            elif packet_type == PacketType.Reply:
                # Not used, this is an out message
                pass

            elif packet_type == PacketType.QSO_Logged:
                # myutils.debug_packet(data)
                payload = Qso_Logged(data[12:])
                payload.do_print()
                # re-read the log file
                log.read_log()

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
