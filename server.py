
# Gaurang Gupta - 2018A7PS0225H

# Rushabh Musthyala - 2018A7PS0433H

# Mihir Bansal - 2018A7PS0215H

# Aditya Jhaveri Alok - 2018A7PS0209H

# Dev Gupta - 2017B3A71082H

from connection import Connection
from packet import Packet
import math
import base64
import threading
import time
import json
import os


class Server:
    def __init__(self, bufLen, windowSize, globalTimer, packetSize, reTransCount, ipAddr, portNo, destIpAddr, destPortNo, reTransTime):
        # Creating a connection object which will be used to send/receive packets
        self.serverConnection = Connection(
            bufLen, windowSize, globalTimer, packetSize, reTransCount, ipAddr, portNo, destIpAddr, destPortNo, reTransTime)

        # First Packet in handshake
        while True:
            pack = self.serverConnection.recv_packet()
            if pack is not None and pack.syn == True:
                break

        # Starting the global thread
        self.lastPackReceivedTime = time.time()
        globalTimerThread = threading.Thread(target=self.globalTimerFunction)
        globalTimerThread.start()

        # Second Packet in handshake
        secondHand = Packet(True, True, False, -1, -1,
                            bytes("ACK Packet", 'utf-8'))
        self.serverConnection.send_packet(secondHand)

        # Third Packet in handshake
        while True:
            pack = self.serverConnection.recv_packet()
            if pack is not None and pack.syn == False:  # If we receive the third packet
                filename = pack.body
                break
            if pack is not None and pack.syn == True:  # If we receive the first packet again
                secondHand = Packet(True, True, False, -
                                    1, -1, bytes("ACK Packet", 'utf-8'))
                self.serverConnection.send_packet(secondHand)

        # Assigning the buffer fot the ACKs
        self.buffer = [0] * self.serverConnection.bufLen

        # Sending the corresponding file
        self.sendFile(filename)

    # Function which checks for expiration of global timer
    def globalTimerFunction(self):
        while True:
            if (time.time() - self.lastPackReceivedTime) >= self.serverConnection.globalTimer:
                print("Global Timer expired !!")
                os._exit(1)

    # Function which sends a given packet with packNum
    def sendGivenPacket(self, packNum):
        while True:
            if self.numberOfRetransmissions[packNum] > self.serverConnection.reTransCount:
                # Retransimissions for the packet exceeded, hence should exit
                print(
                    "Retransmission Exceeded, hence breaking at packet " + str(packNum))
                os._exit(2)

            # Calculating the body for the given packet
            body = self.data[packNum *
                             self.bodySize: min(((packNum + 1) * self.bodySize), self.lenOfData)]

            # Making the packet and sending it using the connection object and increasing the count of transmissions of the packet
            packet = Packet(False, False, False, packNum, (packNum %
                            self.serverConnection.bufLen), body)
            self.serverConnection.send_packet(packet)
            self.numberOfRetransmissions[packNum] += 1

            # Sleeping for the retransmission time
            time.sleep(self.serverConnection.reTransTime)

            # If the Ack for this packet is still not received, send it again
            if self.receivedAckFor[packNum] == 1:
                # Shifting the window if possible
                while self.buffer[self.windowPointer] == 1:
                    self.buffer[self.windowPointer] = 0
                    self.windowPointer += 1
                    self.windowPointer %= self.serverConnection.bufLen
                    self.numberOfOutstandingPackets -= 1
                return

    # Function which listens for ACKs for the packets
    def listenForAck(self):
        while True:
            pack = self.serverConnection.recv_packet()
            self.lastPackReceivedTime = time.time()
            if pack is not None and pack.syn == False and pack.ack == True:
                print("ACK Received for", pack.ackNumber)
                if pack.ackNumber < self.windowPointer:
                    if (((self.windowPointer + self.serverConnection.windowSize) >= self.serverConnection.bufLen) and ((self.windowPointer + self.serverConnection.windowSize) % self.serverConnection.bufLen) >= pack.ackNumber):
                        self.buffer[pack.ackNumber] = 1
                        if self.receivedAckFor[pack.packetNumber] == 0:
                            self.numberOfAcksReceived += 1
                        self.receivedAckFor[pack.packetNumber] = 1
                else:
                    if pack.ackNumber <= (self.windowPointer + self.serverConnection.windowSize):
                        self.buffer[pack.ackNumber] = 1
                        if self.receivedAckFor[pack.packetNumber] == 0:
                            self.numberOfAcksReceived += 1
                        self.receivedAckFor[pack.packetNumber] = 1
            if self.numberOfAcksReceived == self.numOfPackets:
                return

    # Function for ending the connection
    def endConnection(self):
        while True:
            if self.numberOfAcksReceived == self.numOfPackets:
                # Making the ending packet and sending it and waiting for the ack for the same
                packet = Packet(False, False, True, self.packetNum,
                                (self.packetNum % self.serverConnection.bufLen), bytes('BYE BYE', 'utf-8'))
                self.serverConnection.send_packet(packet)
                while True:
                    pack = self.serverConnection.recv_packet()
                    if pack is not None and pack.ack == True and pack.fin == True:
                        print("Server ended properly !!")
                    os._exit(0)

    # Function which sends the given file
    def sendFile(self, filename):

        # Opening the file and converting it to base64
        fileRead = open(filename, 'rb')
        self.data = fileRead.read()
        self.data = base64.encodebytes(self.data)
        fileRead.close()

        # Calculating the length of data and calculating the number of packets to be transferred
        self.lenOfData = len(self.data)
        self.bodySize = self.serverConnection.packetSize - 1024
        self.numOfPackets = math.ceil(self.lenOfData / self.bodySize)

        # Initialising variables
        self.numberOfAcksReceived = 0
        self.packetNum = 0
        self.numberOfRetransmissions = [0] * self.numOfPackets
        self.numberOfOutstandingPackets = 0
        self.windowPointer = 0
        self.receivedAckFor = [0] * self.numOfPackets
        self.lastPackReceivedTime = time.time()

        # Spawing a thread for listening for acks
        t = threading.Thread(target=self.listenForAck)
        t.start()

        # Spawing a thread for ending connection
        tEnd = threading.Thread(target=self.endConnection)
        tEnd.start()

        # Max number of outstanding packets should be windowsized
        while self.packetNum < self.numOfPackets:
            if self.numberOfOutstandingPackets < self.serverConnection.windowSize:
                # Spawn a new thread for the particular packet
                tx = threading.Thread(
                    target=self.sendGivenPacket, args=(self.packetNum, ))
                tx.start()
                self.numberOfOutstandingPackets += 1
                self.packetNum += 1


# Opening the parameter JSON file
with open("params.json") as f:
    params = json.load(f)

# Make a server object with the given connection parameters
server = Server(params["bufLen"], params["windowSize"], params["globalTimer"], params["packetSize"], params["reTransCount"], params["serverIpAddr"],
                params["serverPortNo"], params["clientIpAddr"], params["clientPortNo"], params["reTransTime"])
