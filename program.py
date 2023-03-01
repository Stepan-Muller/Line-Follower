# LEGO type:standard slot:0 

from spike import PrimeHub, ColorSensor, App, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()

sensorL = ColorSensor('C')
sensorR = ColorSensor('D')
sensorSupL = ColorSensor('A')
sensorSupR = ColorSensor('E')

motorL = Motor('B')
motorR = Motor('F')

baseSpeed = 100

kP = 1
kI = 0
kD = 0
n = 1

limitI = 100

I = 0
lastError = 0

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

while not hub.left_button.is_pressed():
    colorSupL = sensorSupL.get_reflected_light()
    colorL = sensorL.get_reflected_light()
    colorR = sensorR.get_reflected_light()
    colorSupR = sensorSupR.get_reflected_light()
    
    x = colorSupL * 2 + colorL * 1 + colorR * -1 + colorSupR * -2

    error = sign(x) * abs(x ** n)

    P = kP * error

    I = I + kI * error

    D = (error - lastError) * kD

    lastError = error

    PID = P + I + D

    print(PID, error)

    motorL.start_at_power(int(min(100, baseSpeed - PID)))
    motorR.start_at_power(-int(min(100, baseSpeed + PID)))