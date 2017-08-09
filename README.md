# ssd-status
Simple human readable SSD health status PyQt script for Linux.

This script generate readable health status using smarttools (http://smartmontools.sourceforge.net/).
Furter depends Qt framework, and Python bindings for the Qt framework (https://www.riverbankcomputing.com/software/pyqt/intro)

You can define
- the factory limit (in TB), default: 75
- warning limit (in TB), default: 70
- online time limit (in year), default: 5

Screenshot
![ScreenShot](./ssd-status-qt-screenshot.png?raw=true)
