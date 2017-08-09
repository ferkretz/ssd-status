#!/usr/bin/env python3

# Simple human readable SSD health status PyQt script for Linux
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

import sys, os, subprocess
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QSpacerItem, QSizePolicy

APP_NAME = "SSD Health Status"
SMARTCTL = "smartctl"
SMARTCTL_SCAN=SMARTCTL + " --scan"
SMARTCTL_INFO=SMARTCTL + " -s on -i -A -f brief -f hex,id -l devstat "

class CriticalBox(QMessageBox):
    def __init__(self, domain, message):
        super().__init__()
        self.initComponents()
        self.initTexts(domain, message)

    def initComponents(self):
        self.setIcon(QMessageBox.Critical)
        self.setStandardButtons(QMessageBox.Close)
        horizontalSpacer = QSpacerItem(720, 0, QSizePolicy.Minimum, QSizePolicy.Expanding);
        layout = self.layout();
        layout.addItem(horizontalSpacer, layout.rowCount(), 0, 1, layout.columnCount());        

    def initTexts(self, domain, message):
        self.setWindowTitle(domain + " - " + APP_NAME)
        self.setText(message)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.deviceList = []
        self.initComponents()
        self.initTexts()

    def initComponents(self):
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.frameSettings = QtWidgets.QFrame(self.centralwidget)
        self.frameSettings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameSettings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout1 = QtWidgets.QGridLayout(self.frameSettings)
        self.groupBoxDevice = QtWidgets.QGroupBox(self.frameSettings)
        self.groupBoxDevice.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxDevice)
        self.comboBoxDevices = QtWidgets.QComboBox(self.groupBoxDevice)
        self.comboBoxDevices.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.comboBoxDevices)
        self.pushButtonCalculate = QtWidgets.QPushButton(self.groupBoxDevice)
        self.pushButtonCalculate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButtonCalculate)
        self.gridLayout1.addWidget(self.groupBoxDevice, 0, 2, 2, 1)
        self.groupBoxPreferences = QtWidgets.QGroupBox(self.frameSettings)
        self.gridLayout2 = QtWidgets.QGridLayout(self.groupBoxPreferences)
        self.spinBoxWriteLimit = QtWidgets.QSpinBox(self.groupBoxPreferences)
        self.spinBoxWriteLimit.setMaximum(300)
        self.spinBoxWriteLimit.setSingleStep(5)
        self.spinBoxWriteLimit.setProperty("value", 70)
        self.gridLayout2.addWidget(self.spinBoxWriteLimit, 2, 1, 1, 1)
        self.spinBoxFactoryLimit = QtWidgets.QSpinBox(self.groupBoxPreferences)
        self.spinBoxFactoryLimit.setMaximum(300)
        self.spinBoxFactoryLimit.setSingleStep(5)
        self.spinBoxFactoryLimit.setProperty("value", 75)
        self.gridLayout2.addWidget(self.spinBoxFactoryLimit, 0, 1, 1, 1)
        self.labelWriteLimit = QtWidgets.QLabel(self.groupBoxPreferences)
        self.gridLayout2.addWidget(self.labelWriteLimit, 2, 0, 1, 1)
        self.labelFactoryLimit = QtWidgets.QLabel(self.groupBoxPreferences)
        self.gridLayout2.addWidget(self.labelFactoryLimit, 0, 0, 1, 1)
        self.spinBoxOnlineLimit = QtWidgets.QSpinBox(self.groupBoxPreferences)
        self.spinBoxOnlineLimit.setMaximum(15)
        self.spinBoxOnlineLimit.setProperty("value", 5)
        self.gridLayout2.addWidget(self.spinBoxOnlineLimit, 4, 1, 1, 1)
        self.labelOnlineLimit = QtWidgets.QLabel(self.groupBoxPreferences)
        self.gridLayout2.addWidget(self.labelOnlineLimit, 4, 0, 1, 1)
        self.labelTerraByte1 = QtWidgets.QLabel(self.groupBoxPreferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTerraByte1.sizePolicy().hasHeightForWidth())
        self.labelTerraByte1.setSizePolicy(sizePolicy)
        self.gridLayout2.addWidget(self.labelTerraByte1, 0, 2, 1, 1)
        self.labelTerraByte2 = QtWidgets.QLabel(self.groupBoxPreferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTerraByte2.sizePolicy().hasHeightForWidth())
        self.labelTerraByte2.setSizePolicy(sizePolicy)
        self.gridLayout2.addWidget(self.labelTerraByte2, 2, 2, 1, 1)
        self.labelYear = QtWidgets.QLabel(self.groupBoxPreferences)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelYear.sizePolicy().hasHeightForWidth())
        self.labelYear.setSizePolicy(sizePolicy)
        self.gridLayout2.addWidget(self.labelYear, 4, 2, 1, 1)
        self.gridLayout1.addWidget(self.groupBoxPreferences, 0, 0, 2, 1)
        self.verticalLayout.addWidget(self.frameSettings)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.verticalLayout.addWidget(self.textBrowser)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        # center position
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        # connections
        self.pushButtonCalculate.clicked.connect(self.pushButtonCalculateClicked)

    def initTexts(self):
        self.setWindowTitle(APP_NAME)
        self.groupBoxDevice.setTitle("Device")
        self.pushButtonCalculate.setText("Calculate")
        self.groupBoxPreferences.setTitle("Preferences")
        self.labelWriteLimit.setText("Write warning limit:")
        self.labelFactoryLimit.setText("Factory capacity limit:")
        self.labelOnlineLimit.setText("Online warning limit:")
        self.labelTerraByte1.setText("TByte")
        self.labelTerraByte2.setText("TByte")
        self.labelYear.setText("Year")
        self.scanDevices()

    def pushButtonCalculateClicked(self):
        date = datetime.now().strftime("<p>%Y-%m-%d %H:%M:%S</p>")

        device = self.deviceList[self.comboBoxDevices.currentIndex()]
        try:
            properties = subprocess.check_output((SMARTCTL_INFO + device).split(), universal_newlines=True).split("\n")
        except subprocess.CalledProcessError as err:
            properties = err.output.split("\n")

        sectorSize = None
        powerOnHours = None
        lbasWritten = None
        for property in properties:
            if property.startswith("Sector Size:"):
                sectorSize = int(property.split()[2])
            if property.startswith("0x09"):
                powerOnHours = int(property.split()[7])
            if property.startswith("0xf1"):
                lbasWritten = int(property.split()[7])

        healthInfo = "<u>Health status:</u><ul>"
        tbLimit = int(self.spinBoxFactoryLimit.value())
        tbWriteLimit = int(self.spinBoxWriteLimit.value())
        onlineLimit = int(self.spinBoxOnlineLimit.value())
        if (sectorSize != None or lbasWritten != None):
            tbWritten = lbasWritten * sectorSize / 1000000000000.0
            if (tbWritten > tbWriteLimit):
                healthInfo = healthInfo + "<li style=\"color:red\">Total data written: %8.2f TB *** WARNING ***</li>" % (tbWritten)
            else:
                healthInfo = healthInfo + "<li>Total data written: %8.2f TB</li>" % (tbWritten)
        if (powerOnHours != None):
            powerOnDays = powerOnHours / 24.0
            if ((powerOnDays / 365) > onlineLimit):
                healthInfo = healthInfo + "<li style=\"color:red\">Total power on: %8.2f day(s) *** WARNING ***</li>" % (powerOnDays)
            else:
                healthInfo = healthInfo + "<li>Total power on: %8.2f day(s)</li>" % (powerOnDays)
        if (sectorSize != None or lbasWritten != None):
            percent = 100 - tbWritten * 100 / tbLimit
            healthInfo = healthInfo + "<li>Health status: %8.2f percent</li>" % (percent)
        if (sectorSize != None or lbasWritten != None or powerOnHours != None):
            remainingDays = (tbLimit / tbWritten - 1) * powerOnDays
            healthInfo = healthInfo + "<li>Estamined remaining: %8.2f day(s)</li>" % (remainingDays)
        healthInfo = healthInfo + "</ul>"

        self.textBrowser.setHtml("<!DOCTYPE html><body>" + date + healthInfo +"</body></html>")

    def scanDevices(self):
        try:
            devices = subprocess.check_output(SMARTCTL_SCAN.split(), universal_newlines=True).split("\n")
            for device in devices:
                if device.startswith("/dev/"):
                    device = device.split()[0]
                    try:
                        properties = subprocess.check_output((SMARTCTL_INFO + device).split(), universal_newlines=True).split("\n")
                    except subprocess.CalledProcessError as err:
                        properties = err.output.split("\n")
                    for property in properties:
                        if property.startswith("Device Model:"):
                            property = property.split(":")[1].strip()
                            comboItem = "(" + device + ")"
                            if "[No Information Found]" in property:
                                self.comboBoxDevices.addItem(device)
                            else:
                                self.comboBoxDevices.addItem(property + " (" + device + ")")
                            self.deviceList.append(device)
                            break
        except FileNotFoundError as err:
            CriticalBox("FileNotFoundError Error", str(err) + """
*** Please install smartmontools! ***
http://smartmontools.sourceforge.net/
            """).exec()
            sys.exit(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if os.geteuid() != 0:
        CriticalBox("Access Error", "You should have root access to run SMART Monitoring Tools").exec()
        sys.exit(1)
    else:
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec())
