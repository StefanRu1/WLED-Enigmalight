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
import numpy
#import binascii

def popen(ip, port):	
	url = '/json/state'	
	multired = 1200 # Multiplication, you can make the light/color brighter	
	multigreen = 1250 # Multiplication, you can make the light/color brighter	
	multiblue = 850 # Multiplication, you can make the light/color brighter
	multiplycol = numpy.array([multired,multigreen,multiblue]) # Colormultiplicator
	spidev.write("Start processing input from wled ... \n")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP	

	while True:		
		colorbyte = bytearray([2,5]) # DRGB Header, 2 for DRGB Protocol, 5 for 5 Sec until return to normal mode		
		data = numpy.fromstring(sys.stdin.readline(), dtype=float, sep=' ')	 # Read Input frim Enigmalight into numpy array
		data = data.reshape(-1, 3) # Reshape the array to triplets RGB
		data = numpy.multiply(data, multiplycol) # Multiply the colors regarding to multiplicators
		data[data > 255] = 255	# Cut off if Value got bigger than 255
		data = data.astype('i1') # Convert to i1 is necessary to have a proper Hex value to send to WLED
		colorbyte = colorbyte + bytearray(data)		
		try:
			  #spidev.write("Message: " + str(colorbyte) + "\n")			  
			  sock.sendto(colorbyte, (ip, int(port)))		  
			  #spidev.flush()
		except:
			  print("Exception while sending to socket\n") 

			
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

#Wait 2 sec
time.sleep(2)

#Call popen
popen(ip, port)
