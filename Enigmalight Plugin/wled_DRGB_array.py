# Advanced WLED control v 0.5 by stefanru for EnigmaLight - (pclin edition) 
# See: https://board.newnigma2.to/wbb4/index.php/Thread/32156-EnigmaLight-pclin-edition/
#
# For WLED see https://github.com/Aircoookie/WLED
#
# Strip is controlled in DRGB UDP mode (max 490 LEDs per Device) 
# For WLED UDP contol see: https://github.com/Aircoookie/WLED/wiki/UDP-Realtime-Control
#
# Setup:
# Device must have as many lights as the stripe
#
# Device has to be specified like this:
#
#[device]
#name            WLED_Device_Name
#output          python /[path]/wled_DRGB.py [IP of WLED device] [WLED UDP port, standard:21324]
#channels        288
#type            popen
#interval        200000
#debug           off
#
# Adaptions:
# You can adapt the colors for the WLED plugin by adapting the values in 
# multired, multigreen, multiblue
# If the calculated value gets > 255 it is cut off to 255

import sys
import time
import json
import math
import socket

def popen(ip, port):	
	url = '/json/state'
	multired = float(1200) # Multiplication, you can make the light brighter
	multigreen = float(1250) # Multiplication, you can make the light brighter
	multiblue = float(850) # Multiplication, you can make the light brighter
	spidev.write("Start processing input from wled ... \n")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

	while True:
		color = []
		colorbyte = bytearray([2,5]) # DRGB Header, 2 for DRGB Protocol, 5 for 5 Sec until return to normal mode
		#print(colorbyte)

		i = 0
		eingabe = sys.stdin.readline()
		#spidev.write("Eingabe: " + str(eingabe) + "\n")

		if len(eingabe)>0:

			data = eingabe.split(' ')	

			for temp in data:		  
			  color.append(temp)
			  i = i + 1

			  if i == 3:
			   
			   red = float(color[0])
			   green = float(color[1])
			   blue = float(color[2])

			   red = red * multired
			   green = green * multigreen
			   blue = blue * multiblue

			   if red > 255:
			    red = 255

			   if green > 255:
			    green = 255
			
			   if blue > 255:
			    blue = 255			  

			   intred = int(red)
			   intgreen = int(green)
			   intblue = int(blue)
			   colorbyte = colorbyte + bytearray([intred,intgreen,intblue])
			   i = 0
			   color = []  
			try:
			  #spidev.write("Message: " + colorbyte + "\n")
			  sock.sendto(colorbyte, (ip, int(port)))			  
			  #spidev.write("Message: " + data + "\n")
			  #spidev.flush()
			except:
			  spidev.write("Exception while sending to socket\n")			  

		else:
			break
			
#Get full command-line arguments
full_cmd_arguments = sys.argv

#Get 1 command-line argument !WLED IP!
#Get 2 command-line argument !WLED UDP port!
ip = sys.argv[1]
port = sys.argv[2]

#Calc filename 
filename = '/usr/wled' + ip + '.log'

#Open logfile
spidev = file(filename, "wb")
#spidev = file(file, "wb")
spidev.write("Starting ...\n")
spidev.flush()

#Log arguments
spidev.write("Commandline call: " + str(full_cmd_arguments) + "\n")
spidev.write("Executing for IP: " + ip + "\n")
spidev.write("Executing for PORT: " + port + "\n")
spidev.flush()

#Wait 5 sec
time.sleep(5)

#Call popen
popen(ip, port)