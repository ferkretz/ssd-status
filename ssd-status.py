#!/usr/bin/env python3

# Simple human readable SSD health status python script for Linux
#
# Copyright (C) 2017 Ferenc Kretz <ferkretz@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import getopt, sys, subprocess

version = "0.0.1"
smartctl = "smartctl"
limit = 75
write_warning = 70
time_warning = 5
device = "/dev/sda"

# Prints simple usage.
def usage():
    print("""
usage: ssd-status.py [options] [device]

Options:
    -h, --help, --usage
        Show this text and exit.
    -l, --limit
        Factory write limit in TB. Default: 75.
    -w, --write-warning
        Warning, when write more than that in TB. Default: 70.
    -t, --time-warning
        Warning, when reach this online time in year. Default: 5.

Device:
        Device path. Default: /dev/sda
""")

# Creates status information.
def status():
    try:
        status = subprocess.check_output(["sudo", smartctl, "-s", "on", "-i", "-A", "-f", "brief", "-f", "hex,id", "-l", "devstat", device], universal_newlines=True).split("\n")
    except FileNotFoundError as err:
        print(str(err), file=sys.stderr)
        print("""
*** Please install smartmontools! ***
http://smartmontools.sourceforge.net/
""")
        sys.exit(2)
    except subprocess.CalledProcessError as err:
        print(str(err), file=sys.stderr)
        print("""
*** %s error, please check the device '%s' and see the documentation ***
""" % (smartctl, device))
        sys.exit(2)

    # Get sector size (usually 512), power on time and written data.
    for line in status:
        if line.startswith("Sector Size:"):
            sector_size = int(line.split()[2])
        if line.startswith("0x09"):
            power_on = int(line.split()[7]) / 24.0
        if line.startswith("0xf1"):
            written = int(line.split()[7]) * sector_size / 1000000000000.0

    # Print status information.
    print("""
    Total data written: %8.2f TB
    Total power on:     %8.2f day(s)
    Health status:      %8.2f percent
    Estamined remaining:%8.2f day(s)
""" % (written, power_on, 100 - written * 100 / limit, (limit / written - 1) * power_on))
    if ((written > write_warning) or (power_on > time_warning * 365)):
        print("""*** Warning!!! The SSD has been degraded too much! ***
""")

# Main function.
def main():
    # Get options.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:w:t:", ["help", "usage", "limit=", "write-warning=", "time-warning"])
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(2)

    global limit, write_warning, time_warning, device

    # Process options.
    for opt, arg in opts:
        if opt in ("-h", "--help", "--usage"):
            usage()
            sys.exit(0)
        if opt in ("-v", "--version"):
            print("Version: ", version)
            sys.exit(0)
        if opt in ("-l", "--limit"):
            limit = int(arg)
        elif opt in ("-w", "--write-warning"):
            write_warning = int(arg)
        elif opt in ("-t", "--time-warning"):
            time_warning = int(arg)
    if (len(args) != 0):
        device = args[0]

    status()

if __name__ == "__main__":
    main()
