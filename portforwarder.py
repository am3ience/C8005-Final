#!/usr/bin/env python
import socket
import threading
import thread
import time
import datetime
import sys
from Tkinter import *

fields = 'Host IP :',

srcIP = []
srcPort = []
destIP = []
destPort = []
ConnectionList = []

def readFile():
	global srcIP
	global srcPort
	global destIP
	global destPort
	
	filename = "config.txt"
	file = open(filename, "r")
	for line in file:
		sIP, sPort, dIP, dPort = configDelimeter(line)
        srcIP.append(sIP)
        srcPort.append(sPort)
        destIP.append(dIP)
        destPort.append(dPort)

        Connection = makeConnection(sIP, sPort, dIP, dPort)
        ConnectionList.append(Connection)
        
def configDelimeter(line):
	List = line.split(",")
	source = List[0].split(":")
	
	source_IP = source[0]
	source_Port = source[1]
	source_Port.strip(' \t\n\r')
	
	destination = List[1].split(":")
	destination_IP = destination[0]
	destination_Port = destination[1]
	#Since this is the last delimited value from the line, it will contain a newline character, thus we will need to remove it evey time
	destination_Port = destination_Port.strip(' \t\n\r')
	return source_IP, source_Port, destination_IP, destination_Port

def makeConnection(srcIP, srcPort, destIP, destPort):
    connection = Connection(srcIP, srcPort, destIP, destPort)
    return connection

class Connection(object):
	srcIP = ""
	srcPort = ""
	destIP = ""
	destPort = ""
	
	def __init__(self, srcIP, srcPort, destIP, destPort):
		self.srcIP = srcIP
		self.srcPort = srcPort
		self.destIP = destIP
		self.destPort = destPort
		
def sendData(srcsocket,srcaddr,destsocket,destaddr):
	bufferSize = 1024
	
	while True:
		data = srcsocket.recv(bufferSize)
		print "\nReceived " + data + " from " + str(srcaddr) + " forwarding to " + str(destaddr)
		if data == 'quit':
			destsocket.send(data)
			#srcsocket.close()
			#destsocket.close()
			break
		destsocket.send(data)


def threadHandler(connection,hostIP):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	addr = (hostIP, int(connection.srcPort))
	serversocket.bind(addr)
	serversocket.listen(50)
	print "Listening to Port " + connection.srcPort
	
	while 1:
		clientsocket, clientaddr = serversocket.accept()
		sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sendAddr = (connection.destIP, int(connection.destPort))
		sendsocket.connect(sendAddr)
		
		print str(clientaddr) + " connected"
		print str(sendAddr) + " connected"
		
		clientThread = threading.Thread(target = sendData, args=(sendsocket,sendAddr, clientsocket,clientaddr))
		serverThread = threading.Thread(target = sendData, args=(clientsocket,clientaddr, sendsocket,sendAddr))
		
		clientThread.start()
		serverThread.start()

def run(entries):
	readFile()
	Hostip = entries[0][1].get()
	
	print "Port forwarding...."
	for connection in ConnectionList:
		serverThread = threading.Thread(target = threadHandler, args=(connection,Hostip))
		serverThread.start()

#---------------------------------------------------
# makeform - method to create input box and labels
#
# root - the GUI form
# fields - list of inputs you want i.e (serverip, port)
#-------------------------------------------------
def makeform(root, fields):
	entries = []

	#for each field create an input
	for field in fields:
		row = Frame(root)
		lab = Label(row, width=15, text = field , anchor ='w')
		ent = Entry(row)
		ent.config(highlightbackground = "gray")
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent.pack(side=RIGHT,expand=YES, fill=X)
		entries.append((field,ent))
	return entries
	
if __name__ == '__main__':
    root = Tk()
    ents = makeform(root,fields)

    buttonFrame = Frame(root)
    buttonFrame.pack(side=TOP,padx=5,pady=5)

    b1 = Button(root, text='Start Port Forward', command=(lambda e=ents:run(e)))
    b1.pack(in_=buttonFrame , side=LEFT, padx=5,pady=5)
    

    root.title("Port Forwarder")
    root.mainloop()
