import RPi.GPIO as GPIO
import os
import time
from time import sleep
from datetime import datetime
from threading import Thread
import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import butter, sosfilt, lfilter, buttord

buffer_1 = []
buffer_2 = []
output = np.array([])
rate = 48000
flag = 1
gain_range_0_500 = 1;
gain_range_500_1000 = 1;
gain_range_1000_1500 = 1;
gain_range_1500_2000 = 1;
gain_range_2000_2500 = 1;
gain_range_2500_3000 = 1;
gain_range_3000_3500 = 1;
gain_range_3500_4000 = 1;

def gain_filter(y):
	global gain_range_0_500, gain_range_500_1000, gain_range_1000_1500, gain_range_1500_2000, gain_range_2000_2500, gain_range_2500_3000, gain_range_3000_3500, gain_range_3500_4000 
	y = gain_correction(y, 1, 500, gain_range_0_500)
	y = gain_correction(y, 500, 1000, gain_range_500_1000)
	y = gain_correction(y, 1000, 1500, gain_range_1000_1500)
	y = gain_correction(y, 1500, 2000, gain_range_1500_2000)
	y = gain_correction(y, 2000, 2500, gain_range_2000_2500)
	y = gain_correction(y, 2500, 3000, gain_range_2500_3000)
	y = gain_correction(y, 3000, 3500, gain_range_3000_3500)
	y = gain_correction(y, 3500, 3999, gain_range_3500_4000)
	return y

def gain_correction(y, a, b, gain):
	N = 1024;
	Fs = 48000;
	out = y;
	out[-(N*b)/Fs + N/2 : -(N*a)/Fs + N/2] = gain * y[-(N*b)/Fs + N/2 : -(N*a)/Fs + N/2]
	out[(N*a)/Fs + N/2 : (N*b)/Fs + N/2] = gain * y[(N*a)/Fs + N/2 : (N*b)/Fs + N/2]
	return y

def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def process_audio():
    global buffer_1, buffer_2, output, rate
    while(True):
        if(flag == 2 and buffer_1 != []):
            print("processing buffer 1 started")
            # output = butter_bandpass_filter(buffer_1, 100, 4000, rate, order=3)
            output = gain_filter(buffer_1)
            buffer_1 = []
            print("processing buffer 1 ended")
        elif(flag == 1 and buffer_2 != []):
            print("processing buffer 2 started")
            # output = butter_bandpass_filter(buffer_2, 100, 4000, rate, order=3)
            output = gain_filter(buffer_2)
            buffer_2 = []
            print("processing buffer 2 ended")

        output = output.astype(np.int16)

    return


def record_audio():
    global buffer_1, buffer_2, output, rate, flag
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    p = pyaudio.PyAudio()

    p.get_default_input_device_info()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=rate,
                    input=True,
                    frames_per_buffer=CHUNK)

    output_stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=46000,
                           output=True)

    raw_data = stream.read(CHUNK)
    print("filling buffer 1 ")
    buffer_1 = np.fromstring(raw_data, dtype=np.int16)
    flag = 2
    t2.start()
    output_stream.write(output.tostring())

    while(True):
        raw_data = stream.read(CHUNK)
        if(flag == 1):
            print("filling buffer 1")
            buffer_1 = np.fromstring(raw_data, dtype=np.int16)
            flag = 2
        elif (flag == 2):
            print("filling buffer 2")
            buffer_2 = np.fromstring(raw_data, dtype=np.int16)
            flag = 1
        else:
            print("buffers blocked !!")
            continue
        output_stream.write(output.tostring())

    stream.stop_stream()
    output_stream.stop_stream()
    stream.close()
    output_stream.close()
    p.terminate()

f = open('gain.txt','r')
Gain = f.readline().split(',')
gain_range_0_500 = Gain[0];
gain_range_500_1000 = Gain[1];
gain_range_1000_1500 = Gain[2];
gain_range_1500_2000 = Gain[3];
gain_range_2000_2500 = Gain[4];
gain_range_2500_3000 = Gain[5];
gain_range_3000_3500 = Gain[6];
gain_range_3500_4000 = Gain[7];
t1 = Thread(target=record_audio, args=())
t2 = Thread(target=process_audio, args=())
t1.start()

