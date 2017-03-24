# -----------------------------------------------------------------------------
# FUNCTION:       Client
#
# DATE:           January 06, 2017
#
# DESIGNERS:      Paul Cabanez, Justin Chau
#
# PROGRAMMERS:    Paul Cabanez, Justin Chau
#
# NOTES: program sends strings to the server and will receive the string back in a reply
#
#
#
#
#
# ----------------------------------------------------------------------------*/

from socket import *
from Tkinter import *
import threading
import time
import random
import sys
import datetime

global T
global text_file
#default values
serverIP = ""
port = 8005
message = ""
msgMultiple = 1
newTotal = 0
clients = 1

#list of inputs you need
fields = 'Server IP', 'Port', 'Clients', 'Message', 'Num of Msgs'

#---------------------------------------------------
# getTime()
# Time function that gives the current time
# return timeStamp
#---------------------------------------------------
def getTime():
    ts = time.time()
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return timeStamp

#------------------------------------------------------------
# run 
# method that runs the receive and send
# 
# clientNumber - ID number of a client
# serverIP - IP of the multithread,edge,level triggered server
# port - port of the server
# msgMultiple - number of times the message is sent
# message - the message to send
#
#------------------------------------------------------------        
def run(clientNumber,serverIP,port,msgMultiple,message):
    buffer = 1024

    global totalTime
    global newTotal
    global bytes

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serverIP, port))
    threadRTT = 0

    while 1:
        for _ in range(msgMultiple + 1):
            cData = message + "  From: Client " + str(clientNumber)
            bytes = len(cData)
            # Start timer and send data
            start = time.time()
            if _ == msgMultiple :
                print("\nSent: quit From : Client " + str(clientNumber))
                s.send('quit')
            else:
                s.send(cData.encode('utf-8'))
                print "\nSent: " + cData
                newTotal += len(cData)
            # Stop timer when data is received
            sData = s.recv(buffer) + "  From: Client " + str(clientNumber)
            end = time.time()
                # Keep track of RTT and update total time
            response_time = end - start
            threadRTT += end - start
            totalTime += response_time
            print "\nReceived: " + sData 
            t = random.randint(0, 9)
            time.sleep(t)

        # Log information of Client
        text_file.write(
            "\nClient " + str(clientNumber) + " RTT time taken for " + str(msgMultiple) + " messages was: " + str(
                threadRTT) + " seconds.")
        threadRTT = 0
        break
        
#------------------------------------------------------------
# threadclients 
# creates the threads for the number of clients
# 
# clients - number of clients 
# serverIP - IP of the multithread,edge,level triggered server
# port - port of the server
# msgMultiple - number of times the message is sent
# message - the message to send
#
#------------------------------------------------------------        
def threadclients(clients,serverIP,port,msgMultiple,message):
	# Used to maintain list of all running threads
    threads = []
    
	# Create a seperate thread for each client
    for x in range(clients):
        thread = threading.Thread(target=run, args=(x,serverIP,port,msgMultiple,message))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        
        
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
	
def fetch(entries):
	serverIP = entries[0][1].get()
	port = int(entries[1][1].get())
	clients = int(entries[2][1].get())
	message = entries[3][1].get()
	msgMultiple = int(entries[4][1].get())
	
	
    
	threadclients(clients,serverIP,port,msgMultiple,message)
	
	bytes2 = len('quit') * clients
	totalRequests = (clients * msgMultiple) + clients
	averageRTT = totalTime / totalRequests
	
	print("\nTotal Clients : " + str(clients))
	print("\nTotal RTT : "  + str(totalTime))
	print("Total Data sent : " + str(newTotal + bytes2) + " Bytes.")
	print("Total Number of Requests : " + str(totalRequests))
	print("\nRequest per client : " + str(msgMultiple + 1))
	print("\nAverage Bytes in the messages : " + str((newTotal + bytes2)/totalRequests))
	print("Average RTT was : " + str(averageRTT) + " seconds.")
	
	# Write data to log file
	text_file.write("\nTotal Clients : " + str(clients))
	text_file.write("\nTotal RTT : "  + str(totalTime))
	text_file.write("\nTotal Data sent : " + str(newTotal + bytes2) + " Bytes.")
	text_file.write("\nTotal Number of Requests : " + str(totalRequests))
	text_file.write("\nRequest per client : " + str(msgMultiple + 1))
	text_file.write("\nAverage Bytes in the messages : " + str((newTotal + bytes2)/totalRequests))
	text_file.write("\nAverage RTT : " + str(averageRTT) + " seconds.")
	
	text_file.close()
	
	T.config(state=NORMAL)
	
	T.insert(END, "\nTotal Clients : " + str(clients))
	T.insert(END, "\nTotal RTT : "  + str(totalTime))
	T.insert(END, "\nTotal Data sent  : " + str(newTotal + bytes2) + " Bytes.")
	T.insert(END, "\nTotal Number of Requests : " + str(totalRequests))
	T.insert(END, "\nRequest per client : " + str(msgMultiple + 1))
	T.insert(END, "\nAverage Bytes in the messages : " + str((newTotal + bytes2)/totalRequests))
	T.insert(END, "\nAverage RTT was : " + str(averageRTT) + " seconds.\n")
	T.config(state=DISABLED)
	


if __name__ == '__main__':
    #serverIP = '192.168.0.16' #raw_input('Enter the server IP: ')
    #port = 2017 #int(input('Enter the port: '))
    #clients = 5 #int(input('Enter number of clients: '))
    #message = 'Hello '#raw_input('Enter a message to send: ')
    #msgMultiple = 2 #int(input('Enter the number of times you would like to send the message: '))
    
    totalTime = 0
    text_file = open(str(getTime()) + "_ClientLog.txt", "w")
    
    
    #create GUI
    root = Tk()
    
    ents = makeform(root,fields)
    #root.bind("<Return>', (lambda events, e=ents: fetch(e)))
    
    #buttonFrame
    buttonFrame = Frame(root)
    buttonFrame.pack(side=TOP,padx=5,pady=5)
    
    b1 = Button(root, text="Send", command=(lambda e=ents: fetch(e)))
    b1.pack(in_=buttonFrame, side=LEFT, padx=5,pady=5)
    
   
    resultFrame = Frame(root)
    resultFrame.pack(side=TOP, padx=5 , pady=5 , expand= YES, fill=BOTH)
    
    lab = Label(root,width=15,text='Results', anchor='w')
    lab.pack(in_=resultFrame,side=LEFT)
    
    
    T = Text(root)
    T.pack(in_=resultFrame,side=LEFT,expand = YES, fill=BOTH,padx=5,pady=5)
    T.config(state= DISABLED,borderwidth=4,highlightbackground ="gray")
    
    root.title("Client")
    root.mainloop()
    
    
   
