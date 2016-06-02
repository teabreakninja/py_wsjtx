# -*- coding: utf-8 -*-
import sys
import os.path

class Dxcc():
    def __init__(self):
        self.country_list = {}

        # Check for necessary files
        if not os.path.isfile('dxcc.csv'):
            if not os.path.isfile('cty.xml'):
                print("[!] No local country file or clublog file found")
                print("    Please download the cty.xml file from clublog.org")
                sys.exit(1)
            else:
                self.read_dxcc_xml()

        print("[*] dxcc.csv found, loading...")
        self.read_country_file()


    def read_dxcc_xml(self):
        # Read the clublog xml file, extracting country and prefix
        import xml.etree.ElementTree

        print("[*] local country file not found, reading XML")
        xmldoc = xml.etree.ElementTree.parse('cty.xml').getroot()

        f = open('dxcc.csv', 'w')

        # 0 - entities, 1 - exceptions, 2 - prefixes, 3 - invalid_operations, 4 - zone_exceptions
        for child in xmldoc[2]: # entities
            # have entity, print name and prefix
            # 0 = call, 1 = entity (country)

            if child.find("{http://www.clublog.org/cty/v1.0}end") is not None:
                # prefix has ended allocation, continue next in loop
                continue

            f.write("{},{}\n".format(child.find('{http://www.clublog.org/cty/v1.0}entity').text,
                                     child.find('{http://www.clublog.org/cty/v1.0}call').text)
                                    )

        f.close()
        print("[*] File created")


    def read_country_file(self):
        # read the country csv file into an dictionary
        f = open("dxcc.csv", 'r')

        for line in f.readlines():
            l = line.split(",")
            #print(l[0], l[1].replace('\n','')
            self.country_list[l[1].replace('\n','')] = l[0]
        f.close()


    def find_country(self, callsign):
        c_len = len(callsign)
        size = 0

        # Work from the end of the callsign to
        # the start, trying to match a prefix
        while size < c_len:
            if size == 0:
                to_test = callsign
            else:
                to_test = callsign[:-size]

            for prefix in self.country_list:
                if to_test == prefix:
                    return self.country_list[prefix]

            size += 1

        return None


if __name__ == "__main__":
    dxcc = Dxcc()

    country = dxcc.find_country('EA9BO')
    print country
