import RPi.GPIO as GPIO
import os
import time
from time import sleep
from datetime import datetime
from threading import Thread
import pyaudio
import wave
import zipfile
import sys
import playsound

name1 = ''
name2 = ''
firstRun = False


def remove_audio():
	global name1, name2
	while(True):
		l = os.listdir("/home/pi/summer/recordings/")
		count  = len(l)
		if(count>2):
			l.sort()
			os.remove("/home/pi/summer/recordings/" + l.pop(0))
		else:
			time.sleep(10)

def play_audio():
	global name1, name2
	while(True):	
		playsound.playsound(name2)

def record_audio():
	global name1, name2, firstRun
	while(True):
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 48000
		RECORD_SECONDS = 15
		#name of the file...
		#now=datetime.now()
		a=datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
		WAVE_OUTPUT_FILENAME = "/home/pi/summer/recordings/"+"rec"+str(a)+".wav"
		    	    
		p = pyaudio.PyAudio()
		p.get_default_input_device_info()
		stream = p.open(format=FORMAT,
		            channels=CHANNELS,
		            rate=RATE,
		            input=True,
		            frames_per_buffer=CHUNK)
		print "* Recording audio..."

		frames = []

		for i in range(0,int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)
		print "* done\n" 

		stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		name1 = WAVE_OUTPUT_FILENAME
		if (name2 != name1):
			name2 = name1
		if(firstRun == False):
			t2.start()
			firstRun = True

t1 = Thread(target=record_audio, args=())
t2 = Thread(target=play_audio, args=())
t3 = Thread(target=remove_audio, args=())
t1.start()                 
t3.start()
        
