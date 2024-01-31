import board
import busio
from time import sleep
from adafruit_st7735r import ST7735R
import displayio

import adafruit_imageload
import displayio
import time

import os,sys
import gc

mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin = board.GP18
dc_pin = board.GP16

displayio.release_displays()
spi = busio.SPI(clock=clk_pin,MOSI=mosi_pin)
display_bus = displayio.FourWire(spi,command=dc_pin,chip_select=cs_pin,reset=reset_pin)
display = ST7735R(display_bus,width=160,height=128,bgr=True,rotation=90)

group = displayio.Group()

def pic():
    pic_folder = "/"
    pic_files = [f for f in os.listdir(pic_folder) if f.endswith(".bmp")]
    print(pic_files)
    
    numpic_files = len(pic_files)
    print("Number of .bmp files:",numpic_files)
    
    group = displayio.Group()
    display.show(group)
    
    image_counter = 0
    
    while True:
        current_image = displayio.OnDiskBitmap("/"+pic_files[image_counter])
        tile_grid = displayio.TileGrid(current_image,pixel_shader=current_image.pixel_shader)
        group.append(tile_grid)
        
        display.show(group)
        
        image_counter = (image_counter + 1)% len(pic_files)
        
        for _ in range(50):
               time.sleep(.1)
               
pic()               
                     
        
        
        
        
        
    


while True:
    sleep(1)
