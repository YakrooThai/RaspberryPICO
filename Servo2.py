import time
import board
import pwmio
import busio
from adafruit_motor import servo

uart = busio.UART(board.GP8,board.GP9,baudrate=9600)

def send_uart_data(data):
    uart.write(bytes(data,'utf-8'))
    
def receive_uart_data():
    if uart.in_waiting:
        return uart.read(uart.in_waiting)
    else:
        return None
    
pwm = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15,frequency=50)

Yakroo_servo = servo.Servo(pwm)
Yakroo_servo.angle = 90
time.sleep(1)

while True:
    received_data = receive_uart_data()
    if received_data:
        try:
            angle = int(received_data.decode('utf-8').strip())
            if 0<= angle <= 180:
                Yakroo_servo.angle = angle
        except ValueError:
            pass
    time.sleep(0.1)    
    