import time
import board
import busio

import digitalio
import adafruit_pca9685
from adafruit_motor import servo

SDA = board.GP14
SCL = board.GP15

i2c = busio.I2C(SCL,SDA)

pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 50

servo_channels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

servos = []
for channel in servo_channels:
    servo_obj = servo.Servo(pca.channels[channel])
    servos.append(servo_obj)
    
def move_servo(servo,angle):
    servo.angle = angle
    
time.sleep(2)
while True:
    
    move_servo(servos[0],0)
    move_servo(servos[1],0)
    move_servo(servos[2],180)
    move_servo(servos[3],180)
    time.sleep(2)
    move_servo(servos[0],90)
    move_servo(servos[1],90)
    move_servo(servos[2],180-90)
    move_servo(servos[3],180-90)
    time.sleep(2)