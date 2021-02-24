# This is main Pythom program for multimedia system. Listens in a loop informations from an Arduino.
# Play staged dialogue between the tannery employees, outside of the historic building.
# When get information from Arduino starts Python program from "ex.py" file.
import time
import subprocess
import json
import serial
import RPi.GPIO as GPIO

#Import library

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(5, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(6, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(19, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
time.sleep(2)
GPIO.output(23, GPIO.LOW)

# Initialization HIGH on relays (HIGH is OFF light, LOW is ON light)


file = json.load(open("/home/pi/tannery/json/volume.json", "r"))
vol = file.get('volume')
print(vol)
# Load value volume front speakers from json file.
file2 = json.load(open("/home/pi/tannery/json/volume2.json", "r"))
vol2 = file2.get('volume')
print(vol2)
# Load value volume back speakers from json file.
ser = serial.Serial('/dev/ttyUSB0', 9600)
subprocess.run("amixer -c 2 set Speaker " + str(vol) + "%", shell=True)
subprocess.run("amixer -c 2 set Speaker unmute",shell=True)
subprocess.run("amixer -c 3 set Speaker " + str(vol2) + "%", shell=True)
subprocess.run("amixer -c 3 set Speaker unmute",shell=True)
subprocess.run('sudo killall screen', shell=True)
subprocess.run('sudo screen -S voice -X quit', shell=True)
subprocess.run('sudo screen -S come -X quit', shell=True)
subprocess.run('sudo screen -dmS voice omxplayer --loop -o alsa:hw:S3,0 /home/pi/tannery/sound/dialog.mp3',shell=True)

# 

file3 = json.load(open("/home/pi/tannery/json/value.json", "r"))
val = "done"
file3.update(value = val)
json.dump(file3,open("/home/pi/tannery/json/value.json", "w"))

switch = False
switch2= False
ser.reset_input_buffer()

while True:
    ser.reset_input_buffer()
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    if line == "1":
        file3 = json.load(open("/home/pi/tannery/json/value.json", "r"))
        val = file3.get('value')
        if val == "done":
            val = ""
            file3.update(value = val)
            json.dump(file3,open("/home/pi/tannery/json/value.json", "w"))
            subprocess.run('python3 /home/pi/tannery/ex.py &',shell=True)
            subprocess.run('sudo screen -dmS come omxplayer -o alsa:hw:S3_1,0 /home/pi/tannery/sound/come.mp3',shell=True)
    if line == "-vol":
        file = json.load(open("/home/pi/tannery/json/volume.json", "r"))
        vol = file.get('volume')
        file2 = json.load(open("/home/pi/tannery/json/volume2.json", "r"))
        vol2 = file2.get('volume')
        vol -= 4
        vol2 -= 4
        if vol <= 0:
            vol = 0
        if vol2 <= 0:
            vol2 = 0
        
        file.update(volume = vol)
        file2.update(volume = vol2)
        json.dump(file,open("/home/pi/tannery/json/volume.json", "w"))
        print(vol)
        json.dump(file2,open("/home/pi/tannery/json/volume2.json", "w"))
        print(vol2)
        
        subprocess.run("amixer -c 2 set Speaker " + str(vol) + "%", shell=True)
        subprocess.run("amixer -c 3 set Speaker " + str(vol2) + "%", shell=True)
    if line == "+vol":
        file = json.load(open("/home/pi/tannery/json/volume.json", "r"))
        vol = file.get('volume')
        file2 = json.load(open("/home/pi/tannery/json/volume2.json", "r"))
        vol2 = file2.get('volume')
        vol += 4
        vol2 += 4
        if vol >= 100:
            vol = 100
        if vol2 >= 100:
            vol2 = 100
           
        file.update(volume = vol)
        file2.update(volume = vol2)
        json.dump(file,open("/home/pi/tannery/json/volume.json", "w"))
        print(vol)
        json.dump(file2,open("/home/pi/tannery/json/volume2.json", "w"))
        print(vol2)
        
        subprocess.run("amixer -c 2 set Speaker " + str(vol) + "%", shell=True)
        subprocess.run("amixer -c 3 set Speaker " + str(vol2) + "%", shell=True)
    if line == "a" or switch == True:
        seconds_before = time.monotonic()
        flag = True
        while flag == True:
            seconds_now = time.monotonic()
            print("a")
            time.sleep(0.3)
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if line == "-vol":
                    file = json.load(open("/home/pi/tannery/json/volume.json", "r"))
                    vol = file.get('volume')
                    vol -= 4
                    if vol <= 0:
                        vol = 0
                    subprocess.run("amixer -c 2 set Speaker " + str(vol) + "%", shell=True)
                    file.update(volume = vol)
                    json.dump(file,open("/home/pi/tannery/json/volume.json", "w"))
                    print(vol)
                    seconds_before = time.monotonic()
                    
                
                if line == "+vol":
                    file = json.load(open("/home/pi/tannery/json/volume.json", "r"))
                    vol = file.get('volume')
                    vol += 4
                    if vol >= 100:
                        vol = 100
                    subprocess.run("amixer -c 2 set Speaker " + str(vol) + "%", shell=True)
                    file.update(volume = vol)
                    json.dump(file,open("/home/pi/tannery/json/volume.json", "w"))
                    print(vol)
                    seconds_before = time.monotonic()
                if line == "b":
                    switch = False
                    switch2 = True
                    flag = False
                if line == "c":
                    switch = False
                    switch2 = False
                    flag = False
            seconds_result = int(seconds_now - seconds_before)
            print("a",seconds_result)
            if seconds_result == 10:
                switch = False
                switch2 = False
                flag = False
            ser.reset_input_buffer()
            
    if line == "b" or switch2 == True:
        seconds_before = time.monotonic()
        flag = True
        while flag == True:
            seconds_now = time.monotonic()
            print("b")
            time.sleep(0.3)
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if line == "-vol":
                    file2 = json.load(open("/home/pi/tannery/json/volume.json", "r"))
                    vol2 = file2.get('volume')
                    vol2 -= 4
                    if vol2 <= 0:
                        vol2 = 0
                    subprocess.run("amixer -c 3 set Speaker " + str(vol2) + "%", shell=True)
                    file2.update(volume = vol2)
                    json.dump(file2,open("/home/pi/tannery/json/volume.json", "w"))
                    print(vol2)
                    seconds_before = time.monotonic()
                    
                
                if line == "+vol":
                    file2 = json.load(open("/home/pi/tannery/json/volume.json", "r"))
                    vol2 = file2.get('volume')
                    vol2 += 4
                    if vol2 >= 100:
                        vol2 = 100
                    subprocess.run("amixer -c 3 set Speaker " + str(vol2) + "%", shell=True)
                    file2.update(volume = vol2)
                    json.dump(file2,open("/home/pi/tannery/json/volume.json", "w"))
                    print(vol2)
                    seconds_before = time.monotonic()
                if line == "a":
                    switch = True
                    switch2 = False
                    flag = False
                if line == "c":
                    switch = False
                    switch2 = False
                    flag = False
            seconds_result = int(seconds_now - seconds_before)
            print("b",seconds_result)
            if seconds_result == 10:
                switch = False
                switch2 = False
                flag = False
            ser.reset_input_buffer()
            
    
    ser.reset_input_buffer()