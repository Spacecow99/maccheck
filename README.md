
# maccheck - MAC address OUI vendor search tool

A simple script that prints the registrant information for a MAC address. It supports just about every popular method of representing an MAC address.


## Usage

```
usage: maccheck.py [-h] [-l PATH] MAC [MAC ...]

positional arguments:
  MAC                   MAC/OUI address to look up.

optional arguments:
  -h, --help            show this help message and exit
  -l PATH, --oui-list PATH
                        Path to OUI list. (Default:
                        /Users/user/Programming/maccheck/OUI.json)
```