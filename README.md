# WLED-Enigmalight
WLED Enigmalight Plugin and Config Tool for Matrix LED

I have good news regarding the WLED Python script. I have reworked it.

It is now working with UDP (Live) transfer in WLED DRGB mode.
This supports 490 LEDs per Device.
De facto this is now the EnigmaLight support for WLED over WIFI.
In the WLED UI you do not see a difference if it is bound by cable or this python skript, it is in Live mode.

There are now 3 versions available:
The numpy version. You need python numpy. It uses 25% less CPU than the other two versions.
The array version. Values are stored and calculted in an array.
The list version. Values are stored and calculted in a list.

The device is configured like this:
[device]
name wled2
output python /usr/wled_DRGB_[numpy or array or list].py 192.168.69.46 21324
channels 462
type popen
interval 40000
debug off

IP and port of the light is handed over to the python skript.
Standard port of WLED is 21324.

Intervall consideration:
Enigmalight has intervall as 1 divided by FPS you want to achieve.
Config Intervall is calculated by 1000000 divided by FPS you want to achieve.
Less FPS, less CPU load, more FPS more CPU load, very linear behaviour.
So 40000 matches to 25FPS and Enigmalight intervall should be set to 0.04

The lights per Device are configured as known.
[light]
position top
name 001
color red wled2 1
color green wled2 2
color blue wled2 3
hscan 0 9.091
vscan 0 7.143

I drive now 3 devices with total over 500 lights, it works like a charm.

A logfile is created which shows the start and the handed over parameters in the same directory where you start the script.
Logfile is created per device and has the ip of the device in the name.


See: https://board.newnigma2.to/wbb4/index.php/Thread/32156-EnigmaLight-pclin-edition/
for the complete plugin for Dreambox.
