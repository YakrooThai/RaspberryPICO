import board
import busio
from time import sleep
from adafruit_st7735r import ST7735R
import displayio

import adafruit_imageload
import displayio
import time

mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin = board.GP18
dc_pin = board.GP16


displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)
display = ST7735R(display_bus, width=160, height=128, bgr=True, rotation=270)

Nixie_Yakroo = displayio.OnDiskBitmap("/cat.bmp")

group = displayio.Group()

tile_grid = displayio.TileGrid(Nixie_Yakroo, pixel_shader=Nixie_Yakroo.pixel_shader,x=1, y=1)

group = displayio.Group()
group.append(tile_grid)
display.show(group)

while True:

    sleep(.1)


