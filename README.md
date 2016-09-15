
# maccheck - MAC address OUI vendor search tool

A simple script that prints the registered OUI for a MAC address.


##Usage

The first thing I would recommend doing is to run the get-oui script to update
our list of OUIs and to sit back while it downloads.

    $ ./get-oui.sh


Now we can simply query our maccheck.py script to find the manufacturer for
a specific OUI. It supports just about every popular method of representing
an MAC address.

    $ python3 maccheck.py 00:00:00:00:00:00
