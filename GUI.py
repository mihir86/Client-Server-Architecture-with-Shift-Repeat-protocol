
# Gaurang Gupta - 2018A7PS0225H

# Rushabh Musthyala - 2018A7PS0433H

# Mihir Bansal - 2018A7PS0215H

# Aditya Jhaveri Alok - 2018A7PS0209H

# Dev Gupta - 2017B3A71082H

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.Qt import Qt
import json
import subprocess


class MyWindow(QtWidgets.QMainWindow, QPushButton):

    def exec(self):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setWindowTitle('Error While Running Program')
        error_dialog.setIcon(QtWidgets.QMessageBox.Critical)

        serverIP = self.server_ip.text().strip()
        serverPort = int(self.server_port.text().strip())
        clientIP = self.client_ip.text().strip()
        clientPort = int(self.client_port.text().strip())
        globalTimer = int(self.global_timer.text().strip())
        reTransCount = int(self.retrans_count.text().strip())
        packetSize = int(self.packet_size.text().strip())
        windowSize = int(self.window_size.text().strip())
        bufferLen = int(self.buffer_len.text().strip())
        reTransTime = float(self.reTransTime.text().strip())
        reqFile = self.req_file.text().strip()

        dic = {}

        if bufferLen < 2 * windowSize:
            error_dialog.setText(
                "Buffer Length should be atleast twice the window size")
            error_dialog.exec_()
            return

        if packetSize <= 1024:
            error_dialog.setText(
                "Packet Size should be atleast 1024")
            error_dialog.exec_()
            return

        dic["bufLen"] = bufferLen
        dic["windowSize"] = windowSize
        dic["globalTimer"] = globalTimer
        dic["packetSize"] = packetSize
        dic["reTransCount"] = reTransCount
        dic["serverIpAddr"] = serverIP
        dic["serverPortNo"] = serverPort
        dic["clientIpAddr"] = clientIP
        dic["clientPortNo"] = clientPort
        dic["reqFileName"] = reqFile
        dic["reTransTime"] = reTransTime

        with open("params.json", "w") as outfile:
            json.dump(dic, outfile, indent=4)

    def server(self):
        self.result_label.setText("Server Running !!")
        self.result_label.repaint()
        print("Server Running")
        self.exec()
        check = subprocess.run(["python3", "server.py"])
        # print("Server ", check.returncode)
        if check.returncode == 0:
            self.result_label.setText("Server Ended Properly")
        if check.returncode == 1:
            self.result_label.setText("Server Timed Out")
        if check.returncode == 2:
            self.result_label.setText(
                "Server Ended Due To Retransmission Count")

    def client(self):
        self.result_label.setText("Client Running !!")
        self.result_label.repaint()
        print("Client Running")
        self.exec()
        check = subprocess.run(["python3", "client.py"])
        # print("CHECK ", check.returncode)
        if check.returncode == 0:
            self.result_label.setText("Client Ended Properly")
        if check.returncode == 1:
            self.result_label.setText("Client Timed Out")

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('gui.ui', self).show()
        self.client_button.clicked.connect(self.client)
        self.server_button.clicked.connect(self.server)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
