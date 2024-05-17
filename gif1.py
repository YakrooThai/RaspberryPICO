import board
import gifio
import displayio
import time

from adafruit_st7789 import ST7789

import board,busio
import digitalio

displayio.release_displays()

#----ST7789
tft_cs = board.GP9 
tft_dc = board.GP12 
tft_res = board.GP13
spi_mosi = board.GP11 
spi_clk = board.GP10 
displayio.release_displays()
spi = busio.SPI(spi_clk, MOSI=spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_res,baudrate=31250000)
display = ST7789(display_bus, rotation=90, width=320, height=240)  #Axis Hor

#display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash

odg = gifio.OnDiskGif('/yakroo108.gif')

start = time.monotonic()
next_delay = odg.next_frame() # Load the first frame
end = time.monotonic()
overhead = end - start

face = displayio.TileGrid(
    odg.bitmap,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.RGB565_SWAPPED
    ),
)
splash.append(face)
display.refresh()#board.DISPLAY.refresh()

# Display repeatedly.
while True:
    # Sleep for the frame delay specified by the GIF,
    # minus the overhead measured to advance between frames.
    time.sleep(max(0, next_delay - overhead))
    next_delay = odg.next_frame()