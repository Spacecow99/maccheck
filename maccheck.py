#!/usr/bin/env python3
#
#  Author: Spacecow
#  Date: 15/09/2016
#  Description:
#    A simple script that prints the registered OUI for a MAC address.


import os
import sys
import argparse


def parse_oui(mac_addr):
    """
    Parses a given MAC address format and returns the OUI value.
    Accepted delimiters '-', '.' or ':'.

    Accepted MAC formats:
        FF-FF-FF
        FF-FF-FF-FF-FF-FF
        FFFF-FFFF-FFFF
        FFFFFF
        FFFFFFFFFFFF

    Returns
    """
    hexchars = frozenset('abcdefABCDEF0123456789')

    if len(mac_addr) in [8, 14, 17]:
        # Handles 00-11-22/0011.2233.4455/00:11:22:33:44:55
        if '.' in mac_addr:
            mac_addr = mac_addr.split('.')
        elif '-' in mac_addr:
            mac_addr = mac_addr.split('-')
        elif ':' in mac_addr:
            mac_addr = mac_addr.split(':')
        else:
            raise SyntaxError("Invalid delimiter character")

        if len(mac_addr) not in [3, 6]:
            raise SyntaxError("Invalid address format")

        if len(mac_addr[0]) == 4:
            # Splits ['0011', '2233', '4455'] in to ['00', '11', '22'] format
            mac_addr = [mac_addr[0][:2], mac_addr[0][2:], mac_addr[1][:2]]

        oui = str()
        for byte in mac_addr[:3]:
            if byte[0] not in hexchars or byte[1] not in hexchars:
                raise ValueError(("{0} -> {1} not a valid hex character"
                                  "").format(''.join(mac_addr), ''.join(byte)))
            oui += ''.join(byte)
        return oui.upper()

    elif len(mac_addr) in [6, 12]:
        # Handles 001122/001122334455
        for c in mac_addr[:6]:
            if c not in hexchars:
                raise ValueError(("{0} -> {1} not a valid hex "
                                 "character").format(mac_addr[:6], c))
        return mac_addr[:6].upper()

    else:
        raise SyntaxError("Cannot parse address of that length")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mac', metavar='MAC', action='store', type=str,
                        nargs='+', help='MAC/OUI to look up')
    parser.add_argument('-l', '--oui-list', metavar='PATH', action='store',
                        type=str, default="{0}/ieee-oui.txt".format(os.getcwd()),
                        help='Path to ieee-oui list.')
    args = parser.parse_args()

    if not os.path.isfile(args.oui_list):
        sys.stderr.write(("{0}: File Error: "
                          "{1} not found\n").format(sys.argv[0], args.oui_list))
        sys.exit(1)

    parsed_oui = list()
    for address in args.mac:
        try:
            oui = parse_oui(address)
            parsed_oui.append(oui)
        except SyntaxError as err_log:
            sys.stderr.write(("{0}: Invalid MAC address syntax: "
                              "{1}\n").format(sys.argv[0], err_log))
            sys.exit(2)
        except ValueError as err_log:
            sys.stderr.write(("{0}: Invalid MAC address value: "
                              "{1}\n").format(sys.argv[0], err_log))
            sys.exit(3)

    valid_oui_c = 0
    with open(args.oui_list, 'r') as f:
        for line in f.readlines():
            oui = line[:6]
            vendor = line[7:]
            if oui in parsed_oui:
                valid_oui_c += 1
                print("{0} : {1}".format(oui, vendor.strip('\n')))

    if valid_oui_c == 0:
        sys.stderr.write(("{0}: Invalid MAC OUI: "
                          "No registered OUI found\n").format(sys.argv[0]))
        sys.exit(4)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
    except Exception as err_log:
        sys.stderr.write(("{0}: Unhandled Exception: "
                         "{1}\n").format(sys.argv[0], err_log))
        sys.exit(9)
