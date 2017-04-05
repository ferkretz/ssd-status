# ssd-status
Simple human readable SSD health status python script for Linux.

This script generate readable health status using smarttools (http://smartmontools.sourceforge.net/).

You can define
- the factory limit (in TB), default: 75
- warning limit (in TB), default: 70
- online time limit (in year), default: 5
- device path, default: /dev/sda

Example:
ssd-status.py /dev/sdb

    Total data written:     1.20 TB
    Total power on:        57.50 day(s)
    Health status:         98.40 percent
    Estamined remaining: 3530.34 day(s)

If the SSD parameters esceed your options, you get warning, like this:

    *** Warning!!! The SSD has been degraded too much! ***

You nedd root privilege, that is why this script use sudo. If you don't want to use sudo modify this line:

    status = subprocess.check_output(["sudo", smartctl...
