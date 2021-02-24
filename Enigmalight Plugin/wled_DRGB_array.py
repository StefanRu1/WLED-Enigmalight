# Advanced WLED control v 1.0 by stefanru for EnigmaLight - (pclin edition) 
# See: https://board.newnigma2.to/wbb4/index.php/Thread/32156-EnigmaLight-pclin-edition/
#
# For WLED see https://github.com/Aircoookie/WLED
#
# Strip is controlled in DRGB UDP mode (max 490 LEDs per Device) 
# For WLED UDP contol see: https://github.com/Aircoookie/WLED/wiki/UDP-Realtime-Control
#
# This is the array version. Values are stored and calculted in an array.
#
# Setup:
# Device must have as many lights as the stripe
#
# Device has to be specified like this:
#
#[device]
#name            WLED_Device_Name
#output          python /[path]/wled_DRGB_array.py [IP of WLED device] [WLED UDP port, standard:21324]
#channels        288
#type            popen
#interval        40000
#debug           off
#
# Adaptions:
# You can adapt the colors for the WLED plugin by adapting the values in
# multired, multigreen, multiblue
# Color is provided by Enigmalight as number between 0 .. 1.
# So multiply with 255 would be the normal setup. But this was to dark for my taste.
# If the calculated value gets > 255 it is cut off to 255
#
# Intervall consideration:
# Enigmalight has intervall as 1 divided by FPS you want to achieve.
# Config Intervall is calculated by 1000000 divided by FPS you want to achieve.
# Less FPS, less CPU load, more FPS more CPU load, very linear behaviour.
# So 40000 matches to 25FPS and Enigmalight intervall should be set to 0.04#
#

import sys
import time
import json
import math
import socket

def popen(ip, port):	
	url = '/json/state'
	multired = float(765) # Multiplication, you can make the light/color brighter (old 1200)
	multigreen = float(765) # Multiplication, you can make the light/color brighter (old 1250)
	multiblue = float(765) # Multiplication, you can make the light/color brighter (old 850)
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

	sock.close()
	sock = None
	# End of popen
				
#Get full command-line arguments
full_cmd_arguments = sys.argv

#Get 1 command-line argument !WLED IP!
#Get 2 command-line argument !WLED UDP port!
ip = sys.argv[1]
port = sys.argv[2]

#Calc filename 
filename = '/home/elight-addons/.enigmalight/wled' + ip + '.log'

#Open logfile
spidev = file(filename, "wb")
#spidev = file(file, "wb")
spidev.write("Starting WLED DRGB array ...\n")
spidev.flush()

#Log arguments
spidev.write("Commandline call: " + str(full_cmd_arguments) + "\n")
spidev.write("Executing for IP: " + ip + "\n")
spidev.write("Executing for PORT: " + port + "\n")
spidev.flush()

#Wait 2 sec
time.sleep(2)

#Call popen
popen(ip, port)
