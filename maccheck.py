#!/usr/bin/env python3
#
#  Author: Spacecow
#  Date: 28/04/2019
#  Description:
#    A simple script that prints the OUI registrant information for a MAC address.
#


import os
import sys
import json
import argparse


class OUIList(object):
    """
    OUI registrant list object.

    :arg oui_list: Path to the OUI information JSON file.
    """

    def __init__(self, oui_list):
        self.__oui_list = oui_list

    def find_oui(self, oui):
        """
        Iterate over the OUI list and extract registrant information for OUI.
        
        :arg oui: Parsed OUI to search for.

        :return: OUI registrant information.
        """
        for result in self.__oui_list.get("OUI"):
            if result.get("pfx", "") == oui:
                return result.get("desc", "")
        raise ValueError("Could not find OUI '{0}'".format(oui))

    @staticmethod
    def parse_oui(mac_addr):
        """
        Parses a given MAC address format and returns the OUI value.
        Accepted delimiters '-', '.' or ':'. Accepted MAC formats:
        - FF-FF-FF
        - FF-FF-FF-FF-FF-FF
        - FFFF-FFFF-FFFF
        - FFFFFF
        - FFFFFFFFFFFF

        :arg mac_addr: MAC address to parse.
        
        :return: Parsed lower case OUI string.
        """
        oui = str()
        hexchars = frozenset('abcdefABCDEF0123456789')
        if len(mac_addr) in [8, 14, 17]:  # Handles 00-11-22/0011.2233.4455/00:11:22:33:44:55
            if '.' in mac_addr or '-' in mac_addr or ':' in mac_addr:
                mac_addr = mac_addr.split('.').split('-').split(':')
                if len(mac_addr) not in [3, 6]:
                    raise SyntaxError("Invalid address format.")
            else:
                raise SyntaxError("Invalid delimiter character.")
            
            if len(mac_addr[0]) == 4:  # Splits ['0011', '2233', '4455'] in to ['00', '11', '22'] format
                mac_addr = [mac_addr[0][:2], mac_addr[0][2:], mac_addr[1][:2]]
            
            for byte in mac_addr[:3]:
                if byte[0] not in hexchars or byte[1] not in hexchars:
                    raise ValueError("'{0}' not a valid hex character.".format(''.join(''.join(byte))))
                oui += ''.join(byte)
            return oui.lower()
        elif len(mac_addr) in [6, 12]:  # Handles 001122/001122334455
            for c in mac_addr[:6]:
                if c not in hexchars:
                    raise ValueError(("'{0}' not a valid hex character.").format(c))
            return mac_addr[:6].lower()
        else:
            raise SyntaxError("Cannot parse address of that length.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('MAC', action='store', type=str, nargs='+',
                        help='MAC/OUI address to look up.')
    parser.add_argument('-l', '--oui-list', metavar='PATH', action='store',
                        type=str, default=os.path.join(os.getcwd(), "OUI.json"), required=False,
                        help='Path to OUI list. (Default: {0})'.format(os.path.join(os.getcwd(), "OUI.json")))
    parser.add_argument("--version", action="version", version="maccheck version 2.0")
    args = parser.parse_args()

    # Check to make sure file exists
    if not os.path.isfile(args.oui_list):
        sys.stderr.write(("{0}: File Error: File '{1}' not found.\n").format(sys.argv[0], args.oui_list))
        sys.exit(1)

    # Load JSON file and instantiate OUIList object
    with open(args.oui_list, 'r') as f:
        oui_list = json.load(f)

    OUIParser = OUIList(oui_list)

    # Parse provided MAC OUIs
    parsed_oui = list()
    for address in args.MAC:
        try:
            parsed_oui.append(OUIParser.parse_oui(address))
        except(SyntaxError) as e:
            sys.stderr.write(("{0}: Invalid MAC address syntax: {1}\n").format(sys.argv[0], str(e)))
        except(ValueError) as e:
            sys.stderr.write(("{0}: Invalid MAC address value: {1}\n").format(sys.argv[0], str(e)))

    # Validate found OUIs
    for oui in parsed_oui:
        try:
            print("{0}: {1}".format(oui, OUIParser.find_oui(oui)))
        except(ValueError) as e:
            sys.stderr.write("{0}: MAC address not found: {1}\n".format(sys.argv[0], str(e)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
    except Exception as e:
        sys.stderr.write(("{0}: Unhandled Exception: {1}\n").format(sys.argv[0], str(e)))
        sys.exit(9)
