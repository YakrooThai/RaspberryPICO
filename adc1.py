import board
import busio

import analogio
import displayio
from time import sleep

adc = analogio.AnalogIn(board.A0)

while True:
    value= adc.value
    print(value)
    sleep(1)
