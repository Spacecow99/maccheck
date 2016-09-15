#!/bin/bash
#
#  Author: Spacecow
#  Date: 15/09/2016
#  Description:
#    Grab oui.txt from http://standards-oui.ieee.org/oui/oui.txt
#    and generate a maccheck compatible list to ieee-oui.txt


function main() {

    while getopts 'h' OPT; do
        case ${OPT} in
            h)
                printf "${0} [-h] \n"
                exit 0
                ;;
        esac
    done

    if [ -f ieee-oui.txt ]; then
        rm -f ieee-oui.txt
    fi

    curl http://standards-oui.ieee.org/oui/oui.txt -o /tmp/oui.txt
    cat /tmp/oui.txt | grep '(base 16)' > /tmp/ieee-oui.txt
    while read LINE; do
        echo -e "${LINE:0:6}\t${LINE:22}" >> ieee-oui.txt
    done < /tmp/ieee-oui.txt
}


main ${@}
