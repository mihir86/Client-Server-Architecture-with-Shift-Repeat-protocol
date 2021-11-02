
# Gaurang Gupta - 2018A7PS0225H

# Rushabh Musthyala - 2018A7PS0433H

# Mihir Bansal - 2018A7PS0215H

# Aditya Jhaveri Alok - 2018A7PS0209H

# Dev Gupta - 2017B3A71082H

import socket
from packet import Packet
from packet import convertToPacket


# Class Connection is used to store the properties of the connection used in RUDP
class Connection:
    def __init__(self, bufLen, windowSize, globalTimer, packetSize, reTransCount, ipAddr, portNo, destIpAddr, destPortNo, reTransTime):
        # Buffer Length of the connection used in RUDP
        self.bufLen = bufLen

        # Window size of the connection used in RUDP
        self.windowSize = windowSize

        # Global timer of the connection which will be used to timeout in case the connection is broken
        self.globalTimer = globalTimer

        # Packet size of the packets used to transfer
        self.packetSize = packetSize

        # The maximum number of times a packet will be retransitted before breaking the connection
        self.reTransCount = reTransCount

        # IP Address of the source
        self.ipAddr = ipAddr

        # Port Number of the source
        self.portNo = portNo

        # IP Address of the destination
        self.destIpAddr = destIpAddr

        # Port Number of the destination
        self.destPortNo = destPortNo

        # The time after which a retransmission will happen
        self.reTransTime = reTransTime

        # We open a UDP Socket and bind it to the IP and Port of the source
        try:
            self.Socket = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.Socket.bind(
                (self.ipAddr, self.portNo))
        except socket.error:
            print(socket.error)
            print("Socket Couldn't Be Opened")

    # A function which sends a packet to it's destination by converting it to a string and encoding it to bytes
    def send_packet(self, packetToBeSent):
        stringToSend = packetToBeSent.convertToString()
        stringToSend = bytes(stringToSend, encoding="utf-8")
        self.Socket.sendto(stringToSend,
                           (self.destIpAddr, self.destPortNo))

    # Function used to receive packets in form of bytes from destination and then converting it to a packet and sending it to the application
    def recv_packet(self):
        pack, addr = self.Socket.recvfrom(self.packetSize)
        pack = pack.decode(encoding="utf-8")
        packetToRecv = convertToPacket(pack)
        if packetToRecv.checkCheckSum() == True:
            return packetToRecv
        else:
            return None
