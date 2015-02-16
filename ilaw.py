import time
import thread
import serial
import os
import subprocess
from datetime import datetime
#Pin 18, GPIO 24
relayPin = 24
#Pin 22, GPIO 25
ledPin = 25

pwmDelay = 0.005;
lastRelaySetup = 0;

state = "on"
mode= "control"

lastBrightness = 0
lastPowerReading = ""

#LIGHTS START ----------------------------------------------------
def piBlasterPwm(brightness):
	os.system('echo "%d=%f" > /dev/pi-blaster'%(ledPin,brightness))

def setBrightness(brightness):
	global lastBrightness
	
	if brightness < lastBrightness:
		dimLed(brightness)
	else:
		brightenLed(brightness)

def dimLed(newBrightness):
	global lastBrightness
	index = 1	
	for i in range(newBrightness, lastBrightness):
		
		piBlasterPwm((lastBrightness - index) * 0.01)		
		time.sleep(pwmDelay)
		index+=1
	lastBrightness = newBrightness
	
def brightenLed(newBrightness):
	relaySwitch(1)
	global lastBrightness
	for i in range(lastBrightness, newBrightness):
		piBlasterPwm(i*0.01)				
		time.sleep(pwmDelay)
	lastBrightness = newBrightness


#Relay swtich - 0 is off, 1 is on
def relaySwitch(action):
	global lastRelaySetup	
	
	if(action == 0 and lastRelaySetup != 0):
		os.system('echo "%d=%d" > /dev/pi-blaster'%(relayPin,0)) 
		lastRelaySetup = 0
		
	else:
	#if Relay is off, turn On
		if(lastRelaySetup == 0):
			os.system('echo "%d=%d" > /dev/pi-blaster'%(relayPin,1))
			lastRelaySetup = 1
			
#LIGHTS END -------------------------------------------------------------


#POWER READING START ----------------------------------------------------
	
def savePowerReading(powerReading):
	file = open('/var/www/readings.txt', 'a')
	currentDate = str(datetime.now())
	file.write(powerReading+","+currentDate+"\n")
	file.close()
		
#POWER READING END ----------------------------------------------------


#THREADS START  -------------------------------------------------------
def sendToServerTask():
	timeInterval = 10;
	while True:
		subprocess.call(["php", "/var/www/send.php"]);
		time.sleep(timeInterval)

def powerAnalyzerTask():
	port = serial.Serial("/dev/ttyAMA0")
	global lastPowerReading
	while True:
		#time.sleep(1)
		rcv = port.read(53)
		#Compare power reading before saving to text file
		if(rcv != lastPowerReading):
			lastPowerReading = rcv
			savePowerReading(lastPowerReading)	
			#print lastPowerReading;		
			#time.sleep(4)
		time.sleep(10)
	port.close()
	
def ilawTask():
	global lastBrightness
	global state
	global lastRelaySetup
	while True:
		file = open('/var/www/lightvalues.txt')
		settings = file.read()
		file.close()
		try:
			status,brightness,mode = settings.split(",")
			newBrightness = int(brightness)
			if(status == "on"):
				relaySwitch(1)
				if(lastBrightness != newBrightness):	
					#For debugging purposes only	
					#print "\nLast brightness =" + str(lastBrightness)
					setBrightness(newBrightness)
					print "Status = " + status
					print "New Brightness = " + brightness
					print "Mode = " + mode
					print "\n\n"		
					lastBrightness = newBrightness
		#Server should send 0 level with "off" mode		
			else:
				if(lastRelaySetup != 0):
					print "Relay turned off"	
					setBrightness(0)
					relaySwitch(0)								
			time.sleep(1)
		except ValueError:
			time.sleep(2)
			print "Invalid light settings. Please check lightvalues.txt."
#THREADS END  -------------------------------------------------------

def main():
	
	thread.start_new_thread(ilawTask , () )
	thread.start_new_thread(powerAnalyzerTask , () )
	#thread.start_new_thread(sendToServerTask , () )

try:
	main()
except KeyboardInterrupt:
	print "Thread Stopped"
	os.system('echo "25=0" > /dev/pi-blaster')
	os.system('echo "24=0" > /dev/pi-blaster')
	#port.close()

while 1:
	pass

print "Thread stopped.";
os.system('echo "25=0" > /dev/pi-blaster')
os.system('echo "24=0" > /dev/pi-blaster')

