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
name3 = ''
flag1 = ''
flag2 = ''


def process_audio():
    global name2, name3, flag1
    print("-------------------processing " + name2 + "-----------------------")
    os.system("python noise_bandfilter.py " + name2)
    print("-------------------processing ended-----------------------")
    flag1 = name2
    if name3 != name2:
        name3 = name2
    t2.start()

    while():
        if flag1 != name2:
            print("-------------------processing " + name2 + "-----------------------")
            os.system("python noise_bandfilter.py " + name2)
            print("-------------------processing ended-----------------------")
            flag1 = name2
            if name3 != name2:
                name3 = name2


def remove_audio():
    while():
        l = os.listdir("/home/pi/summer/recordings/")
        count = len(l)
        if count > 3:
            l.sort()
            os.remove("/home/pi/summer/recordings/" + l.pop(0))
        else:
            time.sleep(10)


def play_audio():
    global flag2, name3, name2
    while():
        if flag2 != name2:
            print("-------------------playing " + name2 + "-----------------------")
            playsound.playsound(name2)
            print("-------------------playing ended -----------------------")
            flag2 = name2


def record_audio():
    global name1, name2
    print("-------------------recording started-----------------------")
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    RECORD_SECONDS = 30

    a=datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    WAVE_OUTPUT_FILENAME = "/home/pi/summer/recordings/"+"rec"+str(a)+".wav"

    p = pyaudio.PyAudio()
    q = pyaudio.PyAudio()
    p.get_default_input_device_info()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    output_stream = q.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           output=True,
                           frames_per_buffer=CHUNK)

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        output_stream.write(data)

    stream.stop_stream()
    output_stream.stop_stream()
    stream.close()
    output_stream.close()
    p.terminate()
    q.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    name1 = WAVE_OUTPUT_FILENAME
    print("-------------------recorded " + name1 + "-----------------------")
    if name2 != name1:
        name2 = name1
    t2.start()
    while():
        print("-------------------recording started -----------------------")

        a=datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        WAVE_OUTPUT_FILENAME = "/home/pi/summer/recordings/"+"rec"+str(a)+".wav"

        p = pyaudio.PyAudio()
        p.get_default_input_device_info()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for i in range(0,int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            output_stream.write(data)

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
        print("-------------------recorded " + name1 + "-----------------------")
        if name2 != name1:
            name2 = name1

t1 = Thread(target=record_audio, args=())
t2 = Thread(target=play_audio, args=())
t3 = Thread(target=remove_audio, args=())
t4 = Thread(target=process_audio, args=())
t1.start()
t3.start() 
        
