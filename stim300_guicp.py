import re
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets, QtSerialPort


class Ui_MainWindow_STIM300(object):

    def setupUi(self, MainWindow_STIM300):
        self.part_number_datagram_global = None
        self.serial_mode_datagram_global = None
        self.fw_config_global = None
        # current mode button
        self.current_mode = "Deactivate" # in the beginning
        MainWindow_STIM300.setObjectName("MainWindow_STIM300")
        MainWindow_STIM300.resize(1106, 703)
        self.centralwidget = QtWidgets.QWidget(MainWindow_STIM300)
        self.centralwidget.setObjectName("centralwidget")
        self.option_bar = QtWidgets.QTabWidget(self.centralwidget)
        self.option_bar.setGeometry(QtCore.QRect(-10, 0, 1111, 701))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.option_bar.setFont(font)
        self.option_bar.setAutoFillBackground(True)
        self.option_bar.setDocumentMode(True)
        self.option_bar.setTabsClosable(False)
        self.option_bar.setMovable(False)
        self.option_bar.setTabBarAutoHide(False)
        self.option_bar.setObjectName("option_bar")
        self.auto_mode_bar = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.auto_mode_bar.setFont(font)
       
        self.auto_mode_bar.setObjectName("auto_mode_bar")
        self.textBrowser = QtWidgets.QTextBrowser(self.auto_mode_bar)
        self.textBrowser.setGeometry(QtCore.QRect(550, 0, 561, 641))
        self.textBrowser.setObjectName("textBrowser")
        self.groupBox_3 = QtWidgets.QGroupBox(self.auto_mode_bar)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 0, 541, 641))
        self.groupBox_3.setObjectName("groupBox_3")
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_6.setGeometry(QtCore.QRect(0, 60, 261, 31))
        self.radioButton_6.setObjectName("radioButton_activate_automode")
        self.radioButton_7 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_7.setGeometry(QtCore.QRect(270, 60, 241, 31))
        self.radioButton_7.setObjectName("radioButton_deactivate_automode")
        self.option_bar.addTab(self.auto_mode_bar, "")
        self.radioButton_6.toggled.connect(self.autoModeRadioButtonToggled)

        ### -----------------------NORMAL MODE WIDGETS------------------------------
        self.normalmode = QtWidgets.QWidget()
        self.normalmode.setObjectName("normalmode")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.normalmode)
        self.textBrowser_3.setGeometry(QtCore.QRect(290, 0, 821, 641))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.widget = QtWidgets.QWidget(self.normalmode)
        self.widget.setGeometry(QtCore.QRect(10, 0, 281, 641))
        self.widget.setObjectName("widget")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 271, 641))
        self.groupBox.setObjectName("groupBox")
        # activate and deactivate radion button listening for on press
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 40, 121, 21))
        self.radioButton.setObjectName("radioButton_activate_normalmode")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(140, 40, 131, 21))
        self.radioButton_3.setObjectName("radioButton_deactivate_normalmode")
        self.radioButton.toggled.connect(self.normalModeActivateToggled)
        self.radioButton_3.toggled.connect(self.normalModeDeactivateToggled)
        # serial number button listening for on press
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(0, 100, 271, 41))
        self.pushButton.setObjectName("request_serial_number")
        self.pushButton.clicked.connect(self.requestserialnumber)


        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 160, 271, 41))
        self.pushButton_3.setObjectName("request_part_number")
        self.pushButton_3.clicked.connect(self.requestPartNumber)

        
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 220, 271, 41))
        self.pushButton_4.setObjectName("request_config")
        self.pushButton_4.clicked.connect(self.request_config_datagram)

        self.pushButton_12 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_12.setGeometry(QtCore.QRect(0, 600, 271, 41))
        self.pushButton_12.setObjectName("reset button")
        self.pushButton_12.clicked.connect(self.reset_unit)

        self.pushButton_13 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_13.setGeometry(QtCore.QRect(0, 280, 271, 41))
        self.pushButton_13.setObjectName("request_bias_trim_offset")
        self.pushButton_13.clicked.connect(self.request_bias_trim_offs)

        # todo: found this button on the manual of STIM300, uncomment it for 
        # self.pushButton_14 = QtWidgets.QPushButton(self.groupBox)
        # self.pushButton_14.setGeometry(QtCore.QRect(0, 340, 271, 41))
        # self.pushButton_14.setObjectName("request_ext._status")
        self.option_bar.addTab(self.normalmode, "")

        #service mode widgets and function calls
        self.servicemode = QtWidgets.QWidget()
        self.servicemode.setObjectName("servicemode")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.servicemode)
        self.textBrowser_2.setGeometry(QtCore.QRect(280, 0, 831, 641))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.servicemode)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 271, 641))
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 40, 121, 21))
        self.radioButton_4.setObjectName("radioButton_activate_service")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_5.setGeometry(QtCore.QRect(140, 40, 131, 21))
        self.radioButton_5.setObjectName("radioButton_deactivate_service")

        self.radioButton_4.toggled.connect(self.servioceModeActivateToggled)
        self.radioButton_5.toggled.connect(self.serviceModeDeactivateToggled)
        self.option_bar.addTab(self.servicemode, "")
        MainWindow_STIM300.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow_STIM300)
        self.statusbar.setObjectName("statusbar")
        MainWindow_STIM300.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_STIM300)
        self.option_bar.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_STIM300)

        # Initialize serial port
        self.serial_port = QtSerialPort.QSerialPort()
        self.serial_port.readyRead.connect(self.readData) 
        

    def retranslateUi(self, MainWindow_STIM300):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_STIM300.setWindowTitle(_translate("MainWindow_STIM300", "STIM300"))
        self.textBrowser.setHtml(_translate("MainWindow_STIM300", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei\',\'Segoe UI\'; font-size:26pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Auto Mode Deactivated currently</p></body></html>"))
        self.groupBox_3.setTitle(_translate("MainWindow_STIM300", "Operations"))
        self.radioButton_6.setText(_translate("MainWindow_STIM300", "Activate"))
        self.radioButton_7.setText(_translate("MainWindow_STIM300", "Deactivate"))
        self.option_bar.setTabText(self.option_bar.indexOf(self.auto_mode_bar), _translate("MainWindow_STIM300", "Auto Mode"))
        self.textBrowser_3.setHtml(_translate("MainWindow_STIM300", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Microsoft YaHei\',\'Segoe UI\'; font-size:26pt;\">Normal Mode Deactivated Currently</span></p></body></html>"))
        self.groupBox.setTitle(_translate("MainWindow_STIM300", "Operations"))
        self.radioButton.setText(_translate("MainWindow_STIM300", "Activate"))
        self.radioButton_3.setText(_translate("MainWindow_STIM300", "Deactivate"))
        self.pushButton.setText(_translate("MainWindow_STIM300", "Request Serial Number"))
        self.pushButton_3.setText(_translate("MainWindow_STIM300", "Request Part Number"))
        self.pushButton_4.setText(_translate("MainWindow_STIM300", "Request Config"))
        self.pushButton_12.setText(_translate("MainWindow_STIM300", "Reset Device"))
        self.pushButton_13.setText(_translate("MainWindow_STIM300", "Request Bias Trim Offset"))
        # self.pushButton_14.setText(_translate("MainWindow_STIM300", "Request ext.Status"))
        self.option_bar.setTabText(self.option_bar.indexOf(self.normalmode), _translate("MainWindow_STIM300", "Normal Mode"))
        self.textBrowser_2.setHtml(_translate("MainWindow_STIM300", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Microsoft YaHei\',\'Segoe UI\'; font-size:26pt;\">service mode Deactivated Currently</span></p></body></html>"))
        self.groupBox_2.setTitle(_translate("MainWindow_STIM300", "Operations"))
        self.radioButton_4.setText(_translate("MainWindow_STIM300", "Activate"))
        self.radioButton_5.setText(_translate("MainWindow_STIM300", "Deactivate"))
        self.option_bar.setTabText(self.option_bar.indexOf(self.servicemode), _translate("MainWindow_STIM300", "Service Mode"))

    # Function for normal mode
    def normalModeActivateToggled(self, checked):
        if checked:
            self.textBrowser_3.clear()
            self.textBrowser_3.append("Normal Mode Activated")

            # You can add more actions if needed

    def normalModeDeactivateToggled(self, checked):
        if checked:
            self.textBrowser_3.clear()
            self.textBrowser_3.append("Normal Mode Deactivated")

    def requestPartNumber(self):
        if self.radioButton.isChecked():  # Check if Normal Mode is activated
            if self.radioButton.isChecked():  # Check if Normal Mode is activated
                data_to_send = "N"
                self.serial_port.write(data_to_send.encode('utf-8'))
                QtCore.QCoreApplication.processEvents()  # Process events to keep the GUI responsive

            
                data_receive = self.serial_port.readAll().data().decode('utf-8')
                part_number_match = re.search(r'Part Number datagram:([A-F0-9]+)', data_receive)

                if part_number_match:
                    part_number = part_number_match.group(1)
                    self.part_number_datagram_global = part_number
                    print("Extracted Part Number:", part_number)
                    # Clear existing data
                    self.textBrowser_3.clear()
                    # Append new data
                    ammending_info = f"Requested part number: {part_number}"
                    self.textBrowser_3.append(ammending_info)
                    # Move cursor to the end
                    self.textBrowser_3.moveCursor(QtGui.QTextCursor.End)
                    
    def requestserialnumber(self):
        if self.radioButton.isChecked():  # Check if Normal Mode is activated
            if self.radioButton.isChecked():  # Check if Normal Mode is activated
                data_to_send = "I"
                self.serial_port.write(data_to_send.encode('utf-8'))
                QtCore.QCoreApplication.processEvents()  # Process events to keep the GUI responsive
        
            
                data_receive = self.serial_port.readAll().data().decode('utf-8')
                serial_number_match = re.search(r'Serial number Datagram:([A-F0-9]+)', data_receive)

                if serial_number_match:
                    part_number = serial_number_match.group(1)
                    self.serial_mode_datagram_global = part_number
                    print("Extracted Serial Number:", part_number)
                    # Clear existing data
                    self.textBrowser_3.clear()
                    # Append new data
                    ammending_info = f"Requested serial number: {part_number}"
                    self.textBrowser_3.append(ammending_info)
                    # Move cursor to the end
                    self.textBrowser_3.moveCursor(QtGui.QTextCursor.End)
                    
    def request_config_datagram(self):
        if self.radioButton.isChecked():  # Check if Normal Mode is activated
            if self.radioButton.isChecked():  # Check if Normal Mode is activated
                data_to_send = "C"
                self.serial_port.write(data_to_send.encode('utf-8'))
                QtCore.QCoreApplication.processEvents()  # Process events to keep the GUI responsive

                data_receive = self.serial_port.readAll().data().decode('utf-8')
                config_match = re.search(r'configuration Datagram:b\'(.*?)\'', data_receive)

                if config_match:
                    part_number = config_match.group(1)
                    self.fw_config_global = part_number
                    print("Extracted Config datagram:", part_number)
                    # Clear existing data
                    self.textBrowser_3.clear()
                    # Append new data
                    ammending_info = f"Configuration Datagram: {part_number}"
                    self.textBrowser_3.append(ammending_info)
                    # Move cursor to the end
                    self.textBrowser_3.moveCursor(QtGui.QTextCursor.End)
                    
    def request_bias_trim_offs(self):
        if self.radioButton.isChecked():  # Check if Normal Mode is activated
            if self.radioButton.isChecked():  # Check if Normal Mode is activated
                data_to_send = "T"
                self.serial_port.write(data_to_send.encode('utf-8'))
                QtCore.QCoreApplication.processEvents()  # Process events to keep the GUI responsive
                data_receive = self.serial_port.readAll().data().decode('utf-8')
                request_bias_trim_offs_data = re.search(r'bias Trim Offset Datagram:b\'(.*?)\'', data_receive)
                if request_bias_trim_offs_data:
                    part_number = request_bias_trim_offs_data.group(1)
                    print("Extracted bias Trim Offset Datagram:", part_number)
                    # Clear existing data
                    self.textBrowser_3.clear()
                    # Append new data
                    ammending_info = f"Requested bias trim offset Datagram: {part_number}"
                    self.textBrowser_3.append(ammending_info)
                    # Move cursor to the end
                    self.textBrowser_3.moveCursor(QtGui.QTextCursor.End)             

    def reset_unit(self):
        #todo: this function needs implementation
        if self.radioButton.isChecked():
                self.textBrowser_3.clear()
                # Append new data
                ammending_info = f"Resetting the unit"
                self.textBrowser_3.append(ammending_info)
                # Move cursor to the end
                self.textBrowser_3.moveCursor(QtGui.QTextCursor.End)

    def sendData(self, data):
        if self.serial_port.isOpen():
            self.serial_port.write(data.encode('utf-8'))
            print(f"Sent data: {data}")
        else:
            print("Serial port is not open.")

# Service mode
    def service_mode_data_fun(self):
        
        stim300_data = """
                SERIAL NUMBER = {}
                PRODUCT = STIM300
                PART NUMBER = {}
                FW CONFIG = {}
                GYRO OUTPUT UNIT = [°/s] : ANGULAR RATE DELAYED
                ACCELEROMETER OUTPUT UNIT = [g] : ACCELERATION
                INCLINOMETER OUTPUT UNIT = [g] - ACCELERATION
                SAMPLE RATE [samples/s] = 2000
                GYRO CONFIG = XYZ
                ACCELEROMETER CONFIG = XYZ
                INCLINOMETER CONFIG = XYZ
                GYRO RANGE:
                X-AXIS: ± 400°/s
                Y-AXIS: ± 400°/s
                Z-AXIS: ± 400°/s
                ACCELEROMETER RANGE:
                X-AXIS: ± 10g
                Y-AXIS: ± 10g
                Z-AXIS: ± 10g
                INCLINOMETER RANGE:
                X-AXIS: ± 1.7g
                Y-AXIS: ± 1.7g
                Z-AXIS: ± 1.7g
                AUX RANGE: ± 2.5V
                GYRO LP FILTER -3dB FREQUENCY, X-AXIS [Hz] = 262
                GYRO LP FILTER -3dB FREQUENCY, Y-AXIS [Hz] = 262
                GYRO LP FILTER -3dB FREQUENCY, Z-AXIS [Hz] = 262
                ACCELEROMETER LP FILTER -3dB FREQUENCY, X-AXIS [Hz] = 262
                ACCELEROMETER LP FILTER -3dB FREQUENCY, Y-AXIS [Hz] = 262
                ACCELEROMETER LP FILTER -3dB FREQUENCY, Z-AXIS [Hz] = 262
                INCLINOMETER LP FILTER -3dB FREQUENCY, X-AXIS [Hz] = 262
                INCLINOMETER LP FILTER -3dB FREQUENCY, Y-AXIS [Hz] = 262
                INCLINOMETER LP FILTER -3dB FREQUENCY, Z-AXIS [Hz] = 262
                AUX LP FILTER -3dB FREQUENCY [Hz] = 262
                AUX COMP COEFF: A = 1.0000000e+00, B = 0.0000000e+00
                GYRO G-COMPENSATION:
                BIAS SOURCE, X-AXIS = OFF
                BIAS G-COMP LP-FILTER, X-AXIS = NA
                SCALE SOURCE, X-AXIS = ACC
                SCALE G-COMP LP-FILTER, X-AXIS = OFF
                BIAS SOURCE, Y-AXIS = OFF
                BIAS G-COMP LP-FILTER, Y-AXIS = NA
                SCALE SOURCE, Y-AXIS = ACC
                SCALE G-COMP LP-FILTER, Y-AXIS = OFF
                BIAS SOURCE, Z-AXIS = OFF
                BIAS G-COMP LP-FILTER, Z-AXIS = NA
                SCALE SOURCE, Z-AXIS = ACC
                SCALE G-COMP LP-FILTER, Z-AXIS = OFF
                G-COMP LP-FILTER CUTOFF = 0.010 HZ
                BIAS TRIM OFFSET:
                GYRO X-AXIS [°/s ] = 0.02343
                GYRO Y-AXIS [°/s ] = -0.01222
                GYRO Z-AXIS [°/s ] = 0.00111
                ACCELEROMETER X-AXIS [g ] = -0.004256
                ACCELEROMETER Y-AXIS [g ] = -0.013777
                ACCELEROMETER Z-AXIS [g ] = 0.000111
                INCLINOMETER X-AXIS [g ] = 0.0034256
                INCLINOMETER Y-AXIS [g ] = 0.0127598
                INCLINOMETER Z-AXIS [g ] = - 0.0005309
                REFERENCE INFO = 43639
                DATAGRAM = RATE, ACCELERATION, INCLINATION
                DATAGRAM TERMINATION = NONE
                BIT-RATE [bits/s] = 1843200
                DATA LENGTH = 8
                STOP BITS = 1
                PARITY = NONE
                LINE TERMINATION = ON
                SYSTEM CONFIGURATIONS:
                VOLTAGE-LEVEL OF DIGITAL OUTPUT SIGNALS: 5V
                TOV ACTIVE FOR SPECIAL DATAGRAMS AFTER POWER-ON/RESET: OFF
                BTO-DATAGRAM TRANSMISSION AFTER POWER-ON/RESET: OFF
                """.format(
        self.serial_mode_datagram_global,
        self.part_number_datagram_global,
        self.fw_config_global
         )
        return stim300_data

    def servioceModeActivateToggled(self, checked):
        if checked:
            self.textBrowser_2.clear()
            service_mode_data = self.service_mode_data_fun()
            self.textBrowser_2.append(service_mode_data)
 
    def serviceModeDeactivateToggled(self, checked):
        if checked:
            self.textBrowser_2.clear()
            self.textBrowser_2.append("Service Mode Deactivated")


    # read data for automode text browser    
    def readData(self):
        if self.radioButton_6.isChecked():
                data = self.serial_port.readAll().data().decode('utf-8')  # Read data from serial port
                if data:
                        # Print received data for debugging
                        print("Received data:", data)
                        # Clear existing data
                        self.textBrowser.clear()
                        # Append new data
                        self.textBrowser.append(data)
                        # Move cursor to the end
                        self.textBrowser.moveCursor(QtGui.QTextCursor.End)
                        
                else:
                        print("No data received.")

    def autoModeRadioButtonToggled(self, checked):
        if checked:

            self.textBrowser.clear()
            # Append new data
            self.textBrowser.append("Automode is activated")
            # Auto Mode radio button is checked, enable reading and displaying data
            data_to_send = "AutomodeON"
            self.serial_port.write(data_to_send.encode('utf-8'))
            self.serial_port.readyRead.connect(self.readData)
            
        else:
            self.textBrowser.clear()
            # Append new data
            self.textBrowser.append("Automode is deactivated")
            # Auto Mode radio button is unchecked, disconnect the readyRead signal
            self.serial_port.readyRead.disconnect(self.readData)

    # Add a method to open the serial port
    def openSerialPort(self, port_name, baud_rate):
        self.serial_port.setPortName(port_name)
        self.serial_port.setBaudRate(baud_rate)
        if self.serial_port.open(QtCore.QIODevice.ReadWrite):
            print(f"Serial port {port_name} opened successfully.")
        else:
            print(f"Failed to open serial port {port_name}.")

    # Add a method to close the serial port
    def closeSerialPort(self):
        if self.serial_port.isOpen():
            self.serial_port.close()
            print("Serial port closed.")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow_STIM300 = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_STIM300()
    ui.setupUi(MainWindow_STIM300)

    # Open the serial port with the desired parameters (modify as needed)
    ui.openSerialPort("COM10", QtSerialPort.QSerialPort.Baud9600)

    MainWindow_STIM300.show()
    sys.exit(app.exec_())
