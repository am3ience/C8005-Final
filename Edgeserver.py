# -----------------------------------------------------------------------------
# FUNCTION:       EDGE EPO server
#
# DATE:           January 06, 2017
#
# DESIGNERS:      Paul Cabanez, Justin Chau
#
# PROGRAMMERS:    Paul Cabanez, Justin Chau
#
# NOTES: receives an echo from the client and rplies back, utilizes edge level trigging
#
#
#
#
#
# ----------------------------------------------------------------------------*/

from Tkinter import *
import socket
import select
import thread
import time
import datetime
import sys
import signal

#list of inputs you need
fields = 'Server IP' , 'Port'
global root

#---------------------------------------------------
# getTime()
# Time function that gives the current time
# returns timeStamp
#---------------------------------------------------
def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp

#---------------------------------------------------
# edgeFunction(hostIP, port)
# General function to run the epoll (edge triggered) server
# hostIP = IP of the server
# port = port number you want to use for the server
#---------------------------------------------------
def edgeFunction(entries):

	#variables
    bufferSize = 1024
    running = True
    SentTotal = 0
    ReceivedTotal = 0
    sSize = 0
    rSize = 0
    counter = 0
    requestCounter = 0
    concurrentConnections = 0
    connections = {}

    #create the server socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #non-blocking mode
    serverSocket.setblocking(0)
    #create epoll
    epoll = select.epoll()

    address = (entries[0][1].get(), int(entries[1][1].get()))

    #add socket to connections
    connections.update({serverSocket.fileno(): serverSocket})
    #allows a bind to occur for reusedaddr
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    #socket binds
    serverSocket.bind(address)

    print ("Server is listening for connections\n")
    serverSocket.listen(10000)


    #read when socket accepts connection
    epoll.register(serverSocket.fileno(), select.EPOLLIN | select.EPOLLET)

    try:

    	while running:

			#checking epoll for any events
			events = epoll.poll(-1)

			for fileno, event in events:
				if fileno == serverSocket.fileno():
					while running:
						try:
							clientConnection, clientAddress = serverSocket.accept()
							counter += 1

							if counter > concurrentConnections:
								concurrentConnections = counter
							connections.update({clientConnection.fileno(): clientConnection})
							#set new socket to non blocking
							clientConnection.setblocking(0)
							#register the epoll
							epoll.register(clientConnection.fileno(), select.EPOLLIN | select.EPOLLET)

							text_file.write("\n\n" +str(clientAddress) + " connected")
							text_file.write("\nNumber of connected clients: " + str(counter))

							print (str(clientAddress) + " connected.")
							print ("\nNumber of connected clients: " + str(counter))
						except socket.error:
							break

				elif event & select.EPOLLIN:
					rSock = connections.get(fileno)
					#receieve the data and send it back
					try:
						data = rSock.recv(bufferSize)
						clientAddress, clientSocket = rSock.getpeername()
						rSize = len(data)
						ReceivedTotal += rSize
						sSize = len(data)
						SentTotal += sSize
						rSock.send(data)

						requestCounter += 1
						
						if data == 'quit':
							rSock.close()
							counter -= 1
							
							print "\nClient " + clientAddress + ":" + str(clientSocket) + " has disconnected"
							print "\nNumber of connected clients: " + str(counter)
							
							text_file.write("\n\nClient " + clientAddress + ":" + str(clientSocket) + " has disconnected")
							text_file.write("\nNumber of connected clients: " + str(counter))


					except socket.error:
						pass

    except KeyboardInterrupt:
    	Close(epoll,serverSocket,concurrentConnections, ReceivedTotal, SentTotal, requestCounter)

#----------------------------------------------------------------------------
# Close Function
# Function to turn off the server
#
# epoll = epoll object
# serverSocket = the server socket opened
# counter = number of connections
# ReceivedData = Amount of data received from the clients
# SentData = Amount of data sent back to the clients
# Request Counter = number of request the server got from the client
#-----------------------------------------------------------------------------

def Close(epoll,serverSocket,counter, ReceivedData, SentData, requestCounter):
    print ("Shutting down Server...")
    epoll.unregister(serverSocket.fileno())
    epoll.close()
    serverSocket.close()

    text_file.write("\n\nMax # of concurrent connections: " + str(counter))
    text_file.write("\nTotal # of request: " + str(requestCounter))
    text_file.write("\nTotal data received: " + str(ReceivedData))
    text_file.write("\nTotal data sent: " + str(SentData))
    text_file.close()
    sys.exit()

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

    #serverIP = '192.168.0.16'#raw_input('Enter your server IP \n')
    #port = 2017#int(raw_input('What port would you like to use?\n'))


    # Create and initialize the text file with the date in the filename in the logfiles directory
    filename = str(getTime()) + "_edgeserverlog.txt"
    text_file = open(filename, "w")

    root = Tk()
    ents = makeform(root,fields)

    buttonFrame = Frame(root)
    buttonFrame.pack(side=TOP,padx=5,pady=5)

    b1 = Button(root, text='Start Server', command=(lambda e=ents: edgeFunction(e)))
    b1.pack(in_=buttonFrame , side=LEFT, padx=5,pady=5)

    root.title("Edge Triggered Server")
    root.mainloop()
