import time
import subprocess
import json
import RPi.GPIO as GPIO


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
time.sleep(1)
GPIO.output(23, GPIO.LOW)


file = json.load(open("/home/pi/tannery/json/volume.json", "r"))
vol = file.get('volume')


file2 = json.load(open("/home/pi/tannery/json/volume2.json", "r"))
vol2 = file2.get('volume')

file3 = json.load(open("/home/pi/tannery/json/value.json", "r"))
val= file3.get('value')

while vol >= 0:
    subprocess.run("amixer -c 2 set Speaker " + str(vol) + "%", shell=True)
    vol-= 3
    time.sleep(0.2)
    print(vol)
subprocess.run('sudo killall screen', shell=True)    
subprocess.run('sudo screen -S voice -X quit', shell=True)
file = json.load(open("/home/pi/tannery/json/volume.json", "r"))
vol = file.get('volume')
subprocess.run("amixer -c 2 set Speaker " + str(vol) + "%",shell=True)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
subprocess.run('sudo screen -dmS voice omxplayer -o alsa:hw:S3_1,0 /home/pi/tannery/sound/narrator.mp3',shell=True)

time.sleep(87)
GPIO.output(23, GPIO.HIGH)
GPIO.output(17, GPIO.LOW)
time.sleep(17)
GPIO.output(17, GPIO.HIGH)
time.sleep(1)
GPIO.output(4, GPIO.LOW)
time.sleep(21)
GPIO.output(4, GPIO.HIGH)
time.sleep(1)
GPIO.output(22, GPIO.LOW)
GPIO.output(5, GPIO.LOW)
time.sleep(21)
GPIO.output(22, GPIO.HIGH)
GPIO.output(5, GPIO.HIGH)
time.sleep(1)
GPIO.output(6, GPIO.LOW)
time.sleep(11)
GPIO.output(6, GPIO.HIGH)
time.sleep(1)
GPIO.output(13, GPIO.LOW)
time.sleep(13)
GPIO.output(13, GPIO.HIGH)
time.sleep(1)
GPIO.output(19, GPIO.LOW)
time.sleep(64)
GPIO.output(19, GPIO.HIGH)
time.sleep(1)
GPIO.output(26, GPIO.LOW)
time.sleep(35)

GPIO.output(17, GPIO.LOW)
GPIO.output(4, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(19, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)

subprocess.run('sudo killall screen', shell=True)
subprocess.run('sudo screen -S come -X quit', shell=True)
subprocess.run('sudo screen -S voice -X quit', shell=True)
print("przed liczeniem 2 min")
time.sleep(120)
print("po liczeniem 2 min")
subprocess.run('sudo screen -dmS voice omxplayer --loop -o alsa:hw:S3,0 /home/pi/tannery/sound/dialog.mp3',shell=True)

GPIO.output(17, GPIO.HIGH)
GPIO.output(4, GPIO.HIGH)
GPIO.output(22, GPIO.HIGH)
GPIO.output(5, GPIO.HIGH)
GPIO.output(6, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(19, GPIO.HIGH)
GPIO.output(24, GPIO.HIGH)
GPIO.output(26, GPIO.HIGH)



val = "done"
file3.update(value = val)
json.dump(file3,open("/home/pi/tannery/json/value.json", "w"))
