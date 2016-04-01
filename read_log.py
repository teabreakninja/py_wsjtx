# -*- coding: utf-8 -*-
from os import path
from dxcc import Dxcc

class WsjtxLog:
    NOT_WORKED = 0
    WORKED_COUNTRY_AND_STATION = 1
    WORKED_COUNTRY_NOT_STATION = 2
    WORKED_COUNTRY_DIFF_BAND = 3

    # TODO: Figure out country
    def __init__(self):
        # Log file
        user_dir = path.expanduser("~")
        self.log_file = user_dir + '/.local/share/WSJT-X/wsjtx.log'
        self.log_entries = {}
        # Load the country untilities
        self.country_list = {}
        self.dxcc = Dxcc()

        # Read the log
        self.read_log()


    def get_band(self, freq):
        bands = {"144": "2m",
                 "145": "2m",
                 "70": "4m",
                 "50": "6m",
                 "28": "10m",
                 "24": "12m",
                 "21": "15m",
                 "18": "17m",
                 "14": "20m",
                 "10": "30m",
                 "7" : "40m",
                 "3" : "80m"
                }
        f = freq.split(".")
        return bands[f[0]]

    def read_log(self):
        self.log_entries = {}
        self.entry_count = 0

        with open(self.log_file) as f:
            f = f.readlines()

            for row in f:
                entry = row.split(",")
                # print entry[2], self.get_band(entry[4])
                call = entry[2]
                band = self.get_band(entry[4])

                if not call in self.log_entries:
                    self.log_entries[call] = []

                self.log_entries[call].append( band )
                self.entry_count += 1

                # Add to country list
                country = self.dxcc.find_country(call)
                if not country is None:
                    if not country in self.country_list:
                        self.country_list[country] = []

                    self.country_list[country].append( band )


    def check_entry(self, call, band):
        if call in self.log_entries:
            if band in self.log_entries[call]:
                # Worked call on this band - GREEN
                return self.WORKED_COUNTRY_AND_STATION
            else:
                # print("[*] worked diff band")
                pass
        # Haven't worked the callsign on this band
        # before, have we worked the country?
        callsign_country = self.dxcc.find_country(call)
        # print("[*] Country:{}".format(callsign_country))

        if callsign_country in self.country_list:
            if band in self.country_list[callsign_country]:
                # Not call, but worked country this band - PINK
                return self.WORKED_COUNTRY_NOT_STATION
            else:
                # Worked country on different band - BLUE
                return self.WORKED_COUNTRY_DIFF_BAND

        # New country - WHITE ON RED
        return self.NOT_WORKED

    # def check_entry2(self, call, band):
    #     result = {"call": False, "band": False, "country": False}
    #     if call in self.log_entries:
    #         # by working the call, you've worked the country too
    #         result["call"] = True
    #         result["country"] = True
    #
    #         # on this band?
    #         if band in self.log_entries[call]:
    #             result["band"] = True
    #         return result
    #
    #     # Haven't worked the call, have we worked the country?
    #     callsign_country = self.dxcc.find_country(call)
    #     if callsign_country in self.country_list:
    #         result["country"] = True
    #         if band in self.country_list[callsign_country]:
    #             result["band"] = True
    #     return result


if __name__ == "__main__":
    log = WsjtxLog()

    # Print the list
    # for entry in log:
    #     print("Call:{} on band:{}".format(entry, log[entry]))

    # Test
    call = "SQ9OUM"
    band = log.check_entry(call)
    if band:
        print("'{}': found exisiting QSO on {} band".format(call, band))
    else:
        print("'{}' Not found".format(call))

    call = "DL5JMN"
    band = log.check_entry(call)
    if band:
        print("'{}': found exisiting QSO on {} band".format(call, band))
    else:
        print("'{}' Not found".format(call))
