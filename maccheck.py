#!/usr/bin/env python3

import os
import sys
import argparse


def parse_oui(mac_addr):
    """
    Parses a given MAC address format and returns the OUI value.

    Accepted MAC formats:
        FF-FF-FF
        FF-FF-FF-FF-FF-FF
        FFFF-FFFF-FFFF
        FFFFFF
        FFFFFFFFFFFF

    Also accepts "." or ":" as delimiters in lieu of "-".
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

        if len(mac_addr) not in [3, 6]:
            raise SyntaxError("")

        if len(mac_addr[0]) == 4:
            mac_addr = [mac_addr[0][:2], mac_addr[0][2:], mac_addr[1][:2]]

        oui = str()
        for e in mac_addr[:3]:
            if e[0] not in hexchars or e[1] not in hexchars:
                raise ValueError("{0} -> {1} not a valid hex character".format(''.join(mac_addr), ''.join(e)))
            oui += ''.join(e)
        return oui.upper()

    elif len(mac_addr) in [6, 12]:
        # Handles 001122/001122334455
        for c in mac_addr[:6]:
            if c not in hexchars:
                raise ValueError("{0} -> {1} not a valid hex character".format(mac_addr[:6], c))
        return mac_addr[:6].upper()

    else:
        raise SyntaxError("Cannot parse address of that length")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('oui', metavar='OUI', action='store', type=str, nargs='+', help='')
    args = parser.parse_args()

    parsed_oui = list()
    for e in args.oui:
        try:
            s = parse_oui(e)
            parsed_oui.append(s)
        except SyntaxError as err_log:
            sys.stderr.write("{0}: Invalid MAC address syntax: {1}\n".format(sys.argv[0], err_log))
            sys.exit(3)
        except ValueError as err_log:
            sys.stderr.write("{0}: Invalid MAC address value: {1}\n".format(sys.argv[0], err_log))
            sys.exit(4)

    valid_oui = list()
    with open('{0}/.bin/ieee-oui.txt'.format(os.getenv('HOME')), 'r') as f:
        for line in f.readlines():
            oui = line[:6]
            vendor = line[7:]
            if oui in parsed_oui:
                valid_oui.append(oui)
                print(oui + ' : ' + vendor.strip('\n'))

    if len(valid_oui) == 0:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

