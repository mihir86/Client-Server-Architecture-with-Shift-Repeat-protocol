
# Gaurang Gupta - 2018A7PS0225H

# Rushabh Musthyala - 2018A7PS0433H

# Mihir Bansal - 2018A7PS0215H

# Aditya Jhaveri Alok - 2018A7PS0209H

# Dev Gupta - 2017B3A71082H

from connection import Connection
from packet import Packet
import base64
import threading
import time
import random
import json
import os


class Client:
    def __init__(self, bufLen, windowSize, globalTimer, packetSize, reTransCount, ipAddr, portNo, destIpAddr, destPortNo, reqFileName, reTransTime):
        # Creating a connection object which will be used to send/receive packets
        self.clientConnection = Connection(
            bufLen, windowSize, globalTimer, packetSize, reTransCount, ipAddr, portNo, destIpAddr, destPortNo, reTransTime)

        # First Packet in handshake
        firstPack = threading.Thread(target=self.sendFirstPacket)
        firstPack.start()

        # Initialising variables
        self.isReceivedSecondPacket = 0
        self.isReceivedDataPackets = 0
        self.lastPackReceivedTime = time.time()
        self.reqFileName = reqFileName

        # Starting the global thread
        globalTimerThread = threading.Thread(target=self.globalTimerFunction)
        globalTimerThread.start()

        # Second Packet in handshake
        while True:
            pack = self.clientConnection.recv_packet()
            if pack is not None and pack.syn == True:
                self.isReceivedSecondPacket = 1
                break

        # Third Packet in handshake
        thirdPack = threading.Thread(target=self.sendThirdPacket)
        thirdPack.start()

        # Creating a file pointer for the file received
        self.fileWrite = open('RECEIVED_' + self.reqFileName, 'wb')
        self.finalfile = b""

        # Initialising the buffer and window pointer
        self.buffer = [b""] * self.clientConnection.bufLen
        self.windowPointer = 0

        # Calling the receive file function
        self.receiveFileFunction()

    # First Packet in handshake
    def sendFirstPacket(self):
        while True:
            firstHand = Packet(True, False, False, -1, -1,
                               bytes("First Packet", 'utf-8'))
            self.clientConnection.send_packet(firstHand)
            time.sleep(self.clientConnection.reTransTime)

            if self.isReceivedSecondPacket == 1:
                return

    # Third Packet in handshake
    def sendThirdPacket(self):
        while True:
            thirdHand = Packet(False, False, False, 0, -1,
                               bytes(self.reqFileName, 'utf-8'))
            self.clientConnection.send_packet(thirdHand)

            time.sleep(self.clientConnection.reTransTime)
            if self.isReceivedDataPackets == 1:
                return

    # Function which checks for expiration of global timer
    def globalTimerFunction(self):
        while True:
            if (time.time() - self.lastPackReceivedTime) >= self.clientConnection.globalTimer:
                self.fileWrite.write(base64.decodebytes(self.finalfile))
                self.fileWrite.close()
                print("Global Timer expired !!")
                os._exit(1)

    # Function used to receive packets and sending corresponding acks
    def receiveFileFunction(self):
        while True:
            pack = self.clientConnection.recv_packet()
            self.lastPackReceivedTime = time.time()
            if pack is not None:
                if pack.syn == True:
                    continue

                self.isReceivedDataPackets = 1
                if pack.fin == True:
                    # Final packet used to end connection and sending ack for the same
                    ackPacket = Packet(False, True, True, pack.packetNumber, pack.ackNumber, bytes(
                        "Ending Connection !!", 'utf-8'))
                    self.clientConnection.send_packet(ackPacket)
                    print('Client Ending Properly !!')

                    try:
                        self.fileWrite.write(
                            base64.decodebytes(self.finalfile))
                        self.fileWrite.close()
                    except:
                        print("The file was not transferred properly")

                    os._exit(0)

                # Receiving a packet, have to check if it's in the window or not
                if pack.ackNumber < self.windowPointer:
                    if (((self.windowPointer + self.clientConnection.windowSize) >= self.clientConnection.bufLen) and ((self.windowPointer + self.clientConnection.windowSize) % self.clientConnection.bufLen) >= pack.ackNumber):
                        self.buffer[pack.ackNumber] = pack.body
                else:
                    if pack.ackNumber <= (self.windowPointer + self.clientConnection.windowSize):
                        self.buffer[pack.ackNumber] = pack.body

                # Shifting the window if possible
                while len(self.buffer[self.windowPointer]) > 0:
                    self.finalfile += self.buffer[self.windowPointer]
                    self.buffer[self.windowPointer] = b""
                    self.windowPointer += 1
                    self.windowPointer %= self.clientConnection.bufLen

                # Sending an ACK for the given packet
                ackPacket = Packet(False, True, False, pack.packetNumber, pack.ackNumber, bytes(
                    "ACK Packet", 'utf-8'))
                self.clientConnection.send_packet(ackPacket)


# Opening the parameter JSON file
with open("params.json") as f:
    params = json.load(f)

# Make a client object with the given connection parameters
client = Client(params["bufLen"], params["windowSize"], params["globalTimer"], params["packetSize"], params["reTransCount"], params["clientIpAddr"],
                params["clientPortNo"], params["serverIpAddr"], params["serverPortNo"], params["reqFileName"], params["reTransTime"])
