#!/usr/bin/env python
import socket
import struct
import sys
import datetime
import json

from header import header
from wsjtx import *
import myutils
from myutils import PacketType
from pyhamtools import locator
from read_log import WsjtxLog
from WsjtxCurses import WsjtxCurses

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from cgi import escape  # popup notify needs html escaped

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


def popup_toast(cty):
    Notify.init("DX")
    dx = Notify.Notification.new("DX", "New Country:{}".format(escape(cty)), "dialog-information")
    dx.set_timeout(2000)
    dx.show()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 2237)

    # sock.sendto('test message', server_address)

    sock.bind(server_address)

    use_curses = True
    if use_curses:
        jt_curses = WsjtxCurses()

    # Exit py_wsjtx on WSJT-X exit
    exit_on_wsjtxexit = False

    # Enable DXCC notify alerts
    notify_alert = True

    # Publish mqtt messages, requires paho installed
    use_mqtt = True
    mqtt_server = "192.168.0.12"

    # Write all decodes to a log file
    log_decodes = False
    log_outfile = "/tmp/py_wsjtx.log"

    # Read existing log file
    log = WsjtxLog()
    log_info = "[*] Logfile found, {} entries read, {} stations.".format(log.entry_count, len(log.log_entries))
    if use_curses:
        jt_curses.add_main_window(log_info)
    else:
        print(log_info)

    current_band = ""
    state = {}

    if log_decodes:
        out_log = open(log_outfile, 'a', 0)
        out_log.write("Started Log at {}\n".format(datetime.datetime.now()))

    if use_mqtt:
        import paho.mqtt.client as paho
        mqtt_client=paho.Client()
        mqtt_client.connect(mqtt_server, keepalive=60)
        mqtt_client.loop_start()
        mqtt_client.publish("py_wsjtx/status", "Started at {}".format(datetime.datetime.now()))

    # # Replay is PITA when testing
    # data, server = sock.recvfrom(1024)
    # p = header.create_header()
    # p += Replay.create_packet()
    # sock.sendto(p, server)

    try:
        while True:
            data, server = sock.recvfrom(1024)
            h = header(data[0:16])
            # print "data:", data
            packet_type = struct.unpack(">L", data[8:12])[0]

            # print("[*] packet_type:{}".format(packet_type))
            if packet_type == PacketType.Heartbeat:
                payload = Heartbeat(data[12:])
                if use_curses:
                    jt_curses.update_heartbeat(datetime.datetime.now().strftime("%H:%M:%S"))
                else:
                    print("[*] Heartbeat [{}]".format(datetime.datetime.now()))

            elif packet_type == PacketType.Status:
                payload = StateChange(data[12:])

                # Set a per radio state
                state[payload.id_key] = {'freq': payload.dial_freq, 'mode': payload.tx_mode, 'tx': payload.tx_enabled, 'band': log.get_band(str(payload.dial_freq/1000/1000))}

                if use_mqtt:
                    mqtt_msg = json.dumps({'status_frequency': payload.dial_freq, 'status_mode': payload.tx_mode, 'status_tx': payload.tx_enabled})
                    mqtt_client.publish("py_wsjtx/{}/status".format(payload.id_key), mqtt_msg)

                if use_curses:
                    jt_curses.set_banner(payload.dial_freq,
                                         payload.tx_mode,
                                         payload.tx_enabled)
                else:
                    print payload.do_print()
                current_band = log.get_band(str(payload.dial_freq/1000/1000))
                # print("[!] Current band: {}".format(current_band))

            elif packet_type == PacketType.Decode:
                # myutils.debug_packet(data)
                payload = Decode(data[12:])

		        # Get current radio state or return ???
                decode_mode = state.get(payload.id_key, {}).get('mode','???')
                decode_band = state.get(payload.id_key, {}).get('band','???')
                decode_dialfreq = state.get(payload.id_key, {}).get('freq','???')

                if use_mqtt:
                    mqtt_msg = json.dumps({'time': payload.now_time, 'db': str(payload.snr).rjust(2), 'dt': payload.delta_time, 'dialfreq': decode_dialfreq, 'freq': str(payload.delta_freq).rjust(4), 'mode': decode_mode, 'band': decode_band, 'msg': payload.message})
                    mqtt_client.publish("py_wsjtx/{}/decodes".format(payload.id_key), mqtt_msg)


                # info = "[{}] db:{:0>2} DT:{:.1f} Freq:{} DFreq:{} Mode:{} Msg: {}".format(
                #         payload.now_time,
                #         str(payload.snr).rjust(2),
                #         payload.delta_time,
                #         decode_dialfreq,
                #         str(payload.delta_freq).rjust(4),
                #         decode_mode,
                #         payload.message)

                info = "[{}] {:>3}db, {:>4}Hz, {:>3}, {:>3}, Msg: {}".format(
                        payload.now_time,
                        str(payload.snr).rjust(2),
                        str(payload.delta_freq).rjust(4),
                        decode_band,
                        decode_mode,
                        payload.message)

                if log_decodes:
                    out_log.write("{}\n".format(info))

                if use_curses:
                    jt_curses.add_main_window(info)
                else:
                    payload.do_print()

                if payload.message[:2] == "CQ":
                    cq = payload.message.split(" ")
                    if len(cq) > 1:
                        # CQ call should be 'CQ CALL LOC', but can be:
                        # 'CQ DX CALL LOC' or
                        # 'CQ CALL DX LOC'
                        cq_call = cq[1]
                        if len(cq) == 2:
                            cq_loc = ""
                        else:
                            cq_loc = cq[2]

                        if cq_call == "DX":
                            cq_call = cq[2]
                            if len(cq) > 3:
                                cq_loc = cq[3]
                            else:
                                cq_loc = ""

                        if cq_loc == "DX":
                            if len(cq) > 3:
                                cq_loc = cq[3]
                            else:
                                cq_loc = ""

                        if (myutils.validate_callsign(cq_call)):
                            band = log.check_entry2(cq_call, current_band)
                            if band["call"]:
                                if band["call_band"]:
                                    colour = bcolors.WKD_BEFORE
                                    status = log.WORKED_COUNTRY_AND_STATION
                                elif band["country_band"]:
                                    colour = bcolors.WKD_COUNTRY_NOT_STATION
                                    status = log.WORKED_COUNTRY_NOT_STATION
                                else:
                                    colour = bcolors.WKD_COUNTRY_DIFF_BAND
                                    status = log.WORKED_COUNTRY_DIFF_BAND
                            else:
                                if band["country"]:
                                    if band["country_band"]:
                                        colour = bcolors.WKD_COUNTRY_NOT_STATION
                                        status = log.WORKED_COUNTRY_NOT_STATION
                                    else:
                                        colour = bcolors.WKD_COUNTRY_DIFF_BAND
                                        status = log.WORKED_COUNTRY_DIFF_BAND
                                else:
                                    colour = bcolors.NOT_WORKED
                                    status = log.NOT_WORKED
                                    if notify_alert:
                                        popup_toast(log.dxcc.find_country(cq_call))
                                    if use_mqtt:
                                        mqtt_msg = json.dumps({'time': payload.now_time, 'db': str(payload.snr), 'dxcc_call': cq_call, 'dxcc_locator': cq_loc, 'dxcc_country': log.dxcc.find_country(cq_call), 'dxcc_band': decode_band, 'dialfreq': decode_dialfreq})
                                        mqtt_client.publish("py_wsjtx/{}/dxcc".format(payload.id_key), mqtt_msg)

                            # Now display
                            if use_curses:
                                jt_curses.add_cq(cq_call,
                                                status+1,
                                                cq_loc,
                                                log.dxcc.find_country(cq_call),
                                                band)
                            else:
                                print("[***] CQ CALLED BY {}{}{} ({}) [{}]".format(colour, cq_call, bcolors.ENDC, cq_loc, status))
                                if (myutils.validate_locator(cq_loc)):
                                    print("  [*] Distance: {:.0f}km, Bearing:{:.0f}".format(
                                            locator.calculate_distance("io64", cq_loc),
                                            locator.calculate_heading("io64", cq_loc)
                                        ))
                        else:
                            msg = "[*] CQ by non-valid callsign?"
                            if use_curses:
                                jt_curses.add_main_window(msg)
                            else:
                                print(msg)

            elif packet_type == PacketType.Clear:
                payload = Clear(data[12:])
                if use_curses:
                    jt_curses.add_main_window("[*] Clear Called")
                else:
                    payload.do_print()

            elif packet_type == PacketType.Reply:
                # Not used, this is an out message
                pass

            elif packet_type == PacketType.QSO_Logged:
                # myutils.debug_packet(data)
                payload = Qso_Logged(data[12:])
                if use_curses:
                    jt_curses.add_main_window("[*] Logged QSO with {}".format(payload.dx_call))
                else:
                    payload.do_print()
                # re-read the log file
                log.read_log()

            elif packet_type == PacketType.Close:
                payload = Close(data[12:])
                if use_curses:
                    jt_curses.add_main_window("[!] Exit called")
                else:
                    payload.do_print
                if exit_on_wsjtxexit:
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

                decode_band = state.get(payload.id_key, {}).get('band','???')

                if use_mqtt:
                    mqtt_msg = json.dumps({'WSPR_call': payload.callsign, 'band': decode_band, 'grid': payload.grid, 'dist': int(payload.dist), 'pwr': payload.power, 'db': payload.snr})
                    mqtt_client.publish("py_wsjtx/{}/wspr".format(payload.id_key), mqtt_msg)

                info = "WSPR [{}]: {:10} ({:6}) db:{:4}, Freq:{:>10,}Hz, pwr:{:4}, Dist:{:>5.0f}km, Az: {:>3.0f}".format(
                    payload.now_time,
                    payload.callsign,
                    payload.grid,
                    payload.snr,
                    payload.delta_freq,
                    payload.power,
                    payload.dist,
                    payload.bearing)

                if log_decodes:
                    out_log.write("{}\n".format(info))

                if use_curses:
                    jt_curses.add_main_window(info)
                else:
                    payload.do_print()

            else:
                if use_curses:
                    jt_curses.add_main_window("[*] Packet type: {}".format(packet_type))
                else:
                    print("[*] Packet type: {}".format(packet_type))

    except KeyboardInterrupt:
        if use_curses:
            jt_curses.exit_now()
        if log_decodes:
            out_log.write("Closed Log at {}\n".format(datetime.datetime.now()))
            out_log.close()
        print("ctrl-c caught, exiting")

if __name__ == "__main__":
    main()
