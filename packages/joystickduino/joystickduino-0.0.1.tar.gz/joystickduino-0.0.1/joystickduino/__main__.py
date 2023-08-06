
import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m joysticky"

import pyautogui, sys
import time
import serial
import os

os.system('clear')
print('____________________________\n')
print('Using Joystick to control mouse | 1.0.1 ')
print('Created by Shaurya Pratap Singh')
i = input('Default port?(y/N) ')
port = None
if i == 'y':
    port = '/dev/cu.usbmodem14201'
else:
    p = input('Port: ')
    port = p
print('connecting..............')
time.sleep(3)
print('connected.')
print('ctrl+c to exit;')
print('For gui type j on terminal')
print('_____________________________')
pyautogui.FAILSAFE=False
ArduinoSerial=serial.Serial(port,9600) 

while 1:
    data=str(ArduinoSerial.readline().decode('ascii'))   
    (x,y,z)=data.split(":")           
    (X,Y)=pyautogui.position()        
    x=int(x)                          
    y=int(y)
    pyautogui.moveTo(X+x,Y-y)    

    if '1' in z:                        
        pyautogui.click(button="right")  