import board
import gifio
import displayio
import time
from adafruit_st7789 import ST7789
import busio
import os

# Configuration for the ST7735 display
tft_cs = board.GP9 
tft_dc = board.GP12 
tft_res = board.GP13
spi_mosi = board.GP11 
spi_clk = board.GP10 

displayio.release_displays()
spi = busio.SPI(spi_clk, MOSI=spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_res, baudrate=31250000)
display = ST7789(display_bus, rotation=90, width=320, height=240)

splash = displayio.Group()
display.root_group = splash

# Function to load and display a GIF
def display_gif(filename):
    print(filename)
    odg = gifio.OnDiskGif(filename)
    face = displayio.TileGrid(
        odg.bitmap,
        pixel_shader=displayio.ColorConverter(
            input_colorspace=displayio.Colorspace.RGB565_SWAPPED
        ),
    )
    splash.append(face)
    display.refresh()  # Refresh display

    for _ in range(odg.frame_count):
        start = time.monotonic()
        next_delay = odg.next_frame()  # Load the next frame
        end = time.monotonic()
        overhead = end - start

        time.sleep(max(0, next_delay - overhead))

    splash.remove(face)  # Remove the GIF when done

# List all GIF files in the specified directory
gif_directory = "/"
gif_files = [f for f in os.listdir(gif_directory) if f.endswith('.gif')]

while True:
    for gif_file in gif_files:
        display_gif(gif_directory + "/" + gif_file)  # Display the next GIF
