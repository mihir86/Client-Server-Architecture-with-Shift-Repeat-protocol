
# Gaurang Gupta - 2018A7PS0225H

# Rushabh Musthyala - 2018A7PS0433H

# Mihir Bansal - 2018A7PS0215H

# Aditya Jhaveri Alok - 2018A7PS0209H

# Dev Gupta - 2017B3A71082H

import mmh3


# Class Packet is the class whose objects are tranferred between the client and the server
class Packet:
    def __init__(self, syn, ack, fin, packetNumber, ackNumber, body):
        # One bit SYN flag
        self.syn = syn

        # One bit ACK flag
        self.ack = ack

        # One bit FIN flag
        self.fin = fin

        # Body of the packet which contains the data which has to be transferred between the server and client in case of normal UDP as well
        self.body = body

        # The packet number of packet
        self.packetNumber = packetNumber

        # Ack number of the packet which can be calculated using packet number and connection properties
        self.ackNumber = ackNumber

        # Size of the body
        self.bodySize = len(body)

        # Check Sum of the packet which is used to tell if the packet is corrupted or not
        self.checkSum = self.calcCheckSum()

    # A function which gives a string representation of the packet used to call. This will be sent/received after encoding using utf-8
    def convertToString(self):
        return "True~" + str(self.syn) + "~" + str(self.fin) + "~" + str(self.ack) + "~" + str(self.packetNumber) + "~" + str(self.ackNumber) + "~" + str(self.checkSum) + "~" + str(self.bodySize) + "~" + str(self.body.decode('utf-8'))

    # A function used to check if the packet is corrupted or not
    def checkCheckSum(self):
        tempCheckSum = ((mmh3.hash("True~" + str(self.syn) + "~" + str(self.fin) + "~" + str(self.ack) + "~" + str(self.packetNumber) +
                        "~" + str(self.ackNumber) + "~" + str(self.bodySize) + "~" + str(self.body.decode('utf-8')))) % (1 << 16))
        return tempCheckSum == self.checkSum

    # Function used to calculate the check sum of the packet. It is the mmh3 hash of the packet converted to string and using a modulo of 2^16
    def calcCheckSum(self):
        return (((mmh3.hash("True~" + str(self.syn) + "~" + str(self.fin) + "~" + str(self.ack) + "~" + str(self.packetNumber) + "~" + str(self.ackNumber) + "~" + str(self.bodySize) + "~" + str(self.body.decode('utf-8'))))) % (1 << 16))


# A function used to make a packet from the string which was received from the socket for further use
def convertToPacket(pack):
    split_packet = pack.split("~")
    temp = str(split_packet[8])
    temp = bytes(temp, 'utf-8')
    temp_pkt = Packet((split_packet[1] == "True"), (split_packet[3] == "True"), (split_packet[2] == "True"), int(
        split_packet[4]), int(split_packet[5]), temp)
    temp_pkt.checkSum = int(split_packet[6])
    return temp_pkt
